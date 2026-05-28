import torch
from torch import nn
from torch.nn import functional as F
from timm.layers.helpers import to_2tuple
from timm.models.swin_transformer_v2 import SwinTransformerV2Stage
from typing import Sequence, Optional, Dict, Any


def get_pad3d(input_resolution, window_size):
    """
    Args:
        input_resolution (tuple[int]): (Depth, Height, Width)
        window_size (tuple[int]): (Depth, Height, Width)

    Returns:
        padding (tuple[int]): (left, right, top, bottom, front, back)
    """
    D, H, W = input_resolution
    win_d, win_h, win_w = window_size

    padding_left = padding_right = padding_top = padding_bottom = padding_front = padding_back = 0
    d_remainder = D % win_d
    h_remainder = H % win_h
    w_remainder = W % win_w

    if d_remainder:
        d_pad = win_d - d_remainder
        padding_front = d_pad // 2
        padding_back = d_pad - padding_front
    if h_remainder:
        h_pad = win_h - h_remainder
        padding_top = h_pad // 2
        padding_bottom = h_pad - padding_top
    if w_remainder:
        w_pad = win_w - w_remainder
        padding_left = w_pad // 2
        padding_right = w_pad - padding_left

    return padding_left, padding_right, padding_top, padding_bottom, padding_front, padding_back


def get_pad2d(input_resolution, window_size):
    """
    Args:
        input_resolution (tuple[int]): (Height, Width)
        window_size (tuple[int]): (Height, Width)

    Returns:
        padding (tuple[int]): (left, right, top, bottom)
    """
    input_resolution = [2] + list(input_resolution)
    window_size = [2] + list(window_size)
    padding = get_pad3d(input_resolution, window_size)
    return padding[:4]


class CubeEmbedding3D(nn.Module):
    """3D Cube Embedding for processing pseudo-3D ocean data

    Args:
        img_size: (T, H, W) - temporal, height, width
        patch_size: (T, H, W) - patch dimensions
    """
    def __init__(self, img_size, patch_size, in_chans, embed_dim, norm_layer=nn.LayerNorm):
        super().__init__()
        patches_resolution = [
            img_size[0] // patch_size[0],
            img_size[1] // patch_size[1],
            img_size[2] // patch_size[2]
        ]

        self.img_size = img_size
        self.patches_resolution = patches_resolution
        self.embed_dim = embed_dim
        self.proj = nn.Conv3d(in_chans, embed_dim, kernel_size=patch_size, stride=patch_size)

        if norm_layer is not None:
            self.norm = norm_layer(embed_dim)
        else:
            self.norm = None

    def forward(self, x: torch.Tensor):
        B, C, T, H, W = x.shape
        assert T == self.img_size[0] and H == self.img_size[1] and W == self.img_size[2], \
            f"Input size ({T}*{H}*{W}) doesn't match model ({self.img_size[0]}*{self.img_size[1]}*{self.img_size[2]})."

        x = self.proj(x).reshape(B, self.embed_dim, -1).transpose(1, 2)  # B (T*H*W) C
        if self.norm is not None:
            x = self.norm(x)
        x = x.transpose(1, 2).reshape(B, self.embed_dim, *self.patches_resolution)
        return x


class PatchEmbed2D(nn.Module):
    """2D Patch Embedding for processing 2D ocean data

    Args:
        img_size: (H, W) - height, width
        patch_size: (H, W) - patch dimensions
    """
    def __init__(self, img_size, patch_size, in_chans, embed_dim, norm_layer=nn.LayerNorm):
        super().__init__()
        patches_resolution = [
            img_size[0] // patch_size[0],
            img_size[1] // patch_size[1]
        ]

        self.img_size = img_size
        self.patches_resolution = patches_resolution
        self.embed_dim = embed_dim
        self.proj = nn.Conv2d(in_chans, embed_dim, kernel_size=patch_size, stride=patch_size)

        if norm_layer is not None:
            self.norm = norm_layer(embed_dim)
        else:
            self.norm = None

    def forward(self, x: torch.Tensor):
        B, C, H, W = x.shape
        assert H == self.img_size[0] and W == self.img_size[1], \
            f"Input size ({H}*{W}) doesn't match model ({self.img_size[0]}*{self.img_size[1]})."

        x = self.proj(x)  # B C H' W'
        if self.norm is not None:
            x = x.flatten(2).transpose(1, 2)  # B (H'*W') C
            x = self.norm(x)
            x = x.transpose(1, 2).reshape(B, self.embed_dim, *self.patches_resolution)
        return x


class DownBlock(nn.Module):
    """Downsampling block with residual connections"""
    def __init__(self, in_chans: int, out_chans: int, num_groups: int, num_residuals: int = 2):
        super().__init__()
        self.conv = nn.Conv2d(in_chans, out_chans, kernel_size=3, stride=2, padding=1)

        blk = []
        for i in range(num_residuals):
            blk.append(nn.Conv2d(out_chans, out_chans, kernel_size=3, stride=1, padding=1))
            blk.append(nn.GroupNorm(num_groups, out_chans))
            blk.append(nn.SiLU())

        self.blocks = nn.Sequential(*blk)

    def forward(self, x):
        _, _, h, w = x.shape
        x = self.conv(x)

        shortcut = x
        x = self.blocks(x)

        res = x + shortcut
        # Handle odd dimensions
        if h % 2 != 0:
            res = res[:, :, :-1, :]
        if w % 2 != 0:
            res = res[:, :, :, :-1]
        return res


class UpBlock(nn.Module):
    """Upsampling block with residual connections"""
    def __init__(self, in_chans, out_chans, num_groups, num_residuals=2):
        super().__init__()
        self.conv = nn.ConvTranspose2d(in_chans, out_chans, kernel_size=2, stride=2)

        blk = []
        for i in range(num_residuals):
            blk.append(nn.Conv2d(out_chans, out_chans, kernel_size=3, stride=1, padding=1))
            blk.append(nn.GroupNorm(num_groups, out_chans))
            blk.append(nn.SiLU())

        self.blocks = nn.Sequential(*blk)

    def forward(self, x):
        x = self.conv(x)
        shortcut = x
        x = self.blocks(x)
        return x + shortcut


class UTransformer(nn.Module):
    """U-shaped Transformer with downsampling and upsampling

    Args:
        embed_dim (int): Embedding dimension
        num_groups (int | tuple[int]): Number of groups for GroupNorm
        input_resolution (tuple[int]): (H, W) input resolution
        num_heads (int): Number of attention heads
        window_size (int | tuple[int]): Window size for attention
        depth (int): Number of transformer blocks
    """
    def __init__(self, embed_dim, num_groups, input_resolution, num_heads, window_size, depth):
        super().__init__()
        num_groups = to_2tuple(num_groups)
        window_size = to_2tuple(window_size)

        # Calculate padding for window partitioning
        padding = get_pad2d(input_resolution, window_size)
        padding_left, padding_right, padding_top, padding_bottom = padding
        self.padding = padding
        self.pad = nn.ZeroPad2d(padding)

        # Adjust input resolution for padding
        input_resolution = list(input_resolution)
        input_resolution[0] = input_resolution[0] + padding_top + padding_bottom
        input_resolution[1] = input_resolution[1] + padding_left + padding_right

        self.down = DownBlock(embed_dim, embed_dim, num_groups[0])
        self.layer = SwinTransformerV2Stage(
            embed_dim, embed_dim, input_resolution, depth, num_heads, window_size
        )
        self.up = UpBlock(embed_dim * 2, embed_dim, num_groups[1])

    def forward(self, x):
        B, C, H, W = x.shape
        padding_left, padding_right, padding_top, padding_bottom = self.padding

        # Downsample
        x = self.down(x)
        shortcut = x

        # Pad for window partitioning
        x = self.pad(x)
        _, _, pad_h, pad_w = x.shape

        # Apply transformer
        x = x.permute(0, 2, 3, 1)  # B H W C
        x = self.layer(x)
        x = x.permute(0, 3, 1, 2)  # B C H W

        # Crop padding
        x = x[:, :, padding_top: pad_h - padding_bottom, padding_left: pad_w - padding_right]

        # Concatenate with shortcut
        x = torch.cat([shortcut, x], dim=1)  # B 2*C H W

        # Upsample
        x = self.up(x)
        return x


class Fuxi(nn.Module):
    """Ocean-adapted Fuxi model with 2D/3D dual path processing

    Key adaptations:
    1. Handles 2D ocean data (u, v velocity components)
    2. Creates pseudo-3D by adding depth dimension
    3. Processes through both 2D and 3D paths
    4. Supports multi-frame input/output for video prediction
    5. Adaptive to 240x240 spatial resolution

    Args:
        args (dict): Configuration dictionary containing:
            - input_len (int): Number of input frames
            - output_len (int): Number of output frames
            - in_channels (int): Number of input channels (2 for u,v)
            - img_size (tuple): Spatial dimensions (H, W)
            - patch_size (tuple): Patch size for embedding
            - embed_dim (int): Embedding dimension
            - num_groups (int): Number of groups for GroupNorm
            - num_heads (int): Number of attention heads
            - window_size (int): Window size for attention
            - depth (int): Number of transformer blocks
            - use_3d_path (bool): Whether to use 3D processing path
            - pseudo_depth (int): Depth dimension for pseudo-3D
    """
    def __init__(self, args: Dict[str, Any]):
        super().__init__()

        # Extract configuration
        self.input_len = args.get('input_len', 7)
        self.output_len = args.get('output_len', 1)
        self.in_channels = args.get('in_channels', 2)

        # Spatial configuration
        img_size = args.get('img_size', [240, 240])
        if isinstance(img_size, int):
            img_size = [img_size, img_size]
        self.img_size = img_size

        # Patch configuration
        patch_size = args.get('patch_size', [4, 4])
        if isinstance(patch_size, int):
            patch_size = [patch_size, patch_size]
        self.patch_size_2d = patch_size

        # Model dimensions
        self.embed_dim = args.get('embed_dim', 512)
        self.num_groups = args.get('num_groups', 32)
        self.num_heads = args.get('num_heads', 8)
        self.window_size = args.get('window_size', 7)
        self.depth = args.get('depth', 48)

        # Dual path configuration
        self.use_3d_path = args.get('use_3d_path', True)
        self.pseudo_depth = args.get('pseudo_depth', 4)  # Pseudo depth dimension

        # Calculate total input channels (concatenated temporal frames)
        total_in_channels = self.input_len * self.in_channels

        # 2D Path components
        self.patch_embed_2d = PatchEmbed2D(
            img_size=img_size,
            patch_size=patch_size,
            in_chans=total_in_channels,
            embed_dim=self.embed_dim,
            norm_layer=nn.LayerNorm
        )

        # Calculate input resolution after patching and downsampling
        input_resolution_2d = (
            img_size[0] // patch_size[0] // 2,
            img_size[1] // patch_size[1] // 2
        )

        self.u_transformer_2d = UTransformer(
            embed_dim=self.embed_dim,
            num_groups=self.num_groups,
            input_resolution=input_resolution_2d,
            num_heads=self.num_heads,
            window_size=self.window_size,
            depth=self.depth
        )

        # 3D Path components (optional)
        if self.use_3d_path:
            # 3D patch size includes pseudo depth
            patch_size_3d = [1, patch_size[0], patch_size[1]]  # Keep depth dimension at 1
            img_size_3d = [self.pseudo_depth, img_size[0], img_size[1]]

            self.patch_embed_3d = CubeEmbedding3D(
                img_size=img_size_3d,
                patch_size=patch_size_3d,
                in_chans=total_in_channels,
                embed_dim=self.embed_dim,
                norm_layer=nn.LayerNorm
            )

            # 3D path also uses 2D transformer after squeezing depth
            self.u_transformer_3d = UTransformer(
                embed_dim=self.embed_dim,
                num_groups=self.num_groups,
                input_resolution=input_resolution_2d,
                num_heads=self.num_heads,
                window_size=self.window_size,
                depth=self.depth // 2  # Fewer layers for 3D path
            )

            # Fusion layer for combining 2D and 3D features
            self.fusion = nn.Sequential(
                nn.Conv2d(self.embed_dim * 2, self.embed_dim, kernel_size=1),
                nn.GroupNorm(self.num_groups, self.embed_dim),
                nn.SiLU()
            )

        # Output projection
        out_dim = self.output_len * self.in_channels * patch_size[0] * patch_size[1]
        self.fc = nn.Linear(self.embed_dim, out_dim)

        # Initialize weights
        self.apply(self._init_weights)

    def _init_weights(self, m):
        """Initialize model weights"""
        if isinstance(m, nn.Linear):
            nn.init.trunc_normal_(m.weight, std=0.02)
            if m.bias is not None:
                nn.init.constant_(m.bias, 0)
        elif isinstance(m, (nn.Conv2d, nn.Conv3d)):
            nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
            if m.bias is not None:
                nn.init.constant_(m.bias, 0)
        elif isinstance(m, (nn.LayerNorm, nn.GroupNorm)):
            nn.init.constant_(m.bias, 0)
            nn.init.constant_(m.weight, 1.0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass

        Args:
            x: Input tensor of shape (B, T_in, C, H, W)

        Returns:
            Output tensor of shape (B, T_out, C, H, W)
        """
        B, T_in, C, H, W = x.shape
        assert T_in == self.input_len, f"Input frames {T_in} != expected {self.input_len}"
        assert C == self.in_channels, f"Input channels {C} != expected {self.in_channels}"

        # Reshape temporal dimension into channel dimension
        x_2d = x.reshape(B, T_in * C, H, W)  # (B, T_in*C, H, W)

        # 2D Path
        x_embed_2d = self.patch_embed_2d(x_2d)  # (B, embed_dim, H', W')
        x_trans_2d = self.u_transformer_2d(x_embed_2d)  # (B, embed_dim, H', W')

        # 3D Path (if enabled)
        if self.use_3d_path:
            # Create pseudo-3D by repeating along depth dimension
            x_3d = x_2d.unsqueeze(2)  # (B, T_in*C, 1, H, W)
            x_3d = x_3d.repeat(1, 1, self.pseudo_depth, 1, 1)  # (B, T_in*C, D, H, W)

            # Process through 3D embedding
            x_embed_3d = self.patch_embed_3d(x_3d)  # (B, embed_dim, D', H', W')

            # Squeeze depth dimension for 2D transformer
            # Average pool along depth dimension
            x_embed_3d = x_embed_3d.mean(dim=2)  # (B, embed_dim, H', W')

            # Process through 3D transformer
            x_trans_3d = self.u_transformer_3d(x_embed_3d)  # (B, embed_dim, H', W')

            # Fuse 2D and 3D features
            x_fused = torch.cat([x_trans_2d, x_trans_3d], dim=1)  # (B, 2*embed_dim, H', W')
            x_features = self.fusion(x_fused)  # (B, embed_dim, H', W')
        else:
            x_features = x_trans_2d

        # Get patch dimensions
        _, _, H_patch, W_patch = x_features.shape
        patch_h, patch_w = self.patch_size_2d

        # Project to output dimension
        x_features = x_features.permute(0, 2, 3, 1)  # (B, H', W', embed_dim)
        x_out = self.fc(x_features)  # (B, H', W', T_out*C*patch_h*patch_w)

        # Reshape and rearrange patches
        x_out = x_out.reshape(B, H_patch, W_patch, self.output_len, self.in_channels, patch_h, patch_w)
        x_out = x_out.permute(0, 3, 4, 1, 5, 2, 6)  # (B, T_out, C, H', patch_h, W', patch_w)
        x_out = x_out.reshape(B, self.output_len, self.in_channels, H_patch * patch_h, W_patch * patch_w)

        # Interpolate to original resolution if needed
        if H_patch * patch_h != H or W_patch * patch_w != W:
            # Reshape for interpolation
            B_out, T_out, C_out, H_out, W_out = x_out.shape
            x_out = x_out.reshape(B_out * T_out, C_out, H_out, W_out)
            x_out = F.interpolate(x_out, size=(H, W), mode='bilinear', align_corners=False)
            x_out = x_out.reshape(B_out, T_out, C_out, H, W)

        return x_out

    def count_parameters(self) -> int:
        """Count total number of trainable parameters"""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


class FuxiAutoregressive(Fuxi):
    """Autoregressive version of Fuxi for long-term prediction.
    Uses single-frame prediction and rolls out for multiple steps.
    """

    def __init__(self, args):
        # Force single frame output for autoregressive mode
        args_auto = dict(args)
        args_auto['output_len'] = 1
        super().__init__(args_auto)

        self.rollout_steps = args.get('rollout_steps', 1)

    def forward(self, x: torch.Tensor, rollout_steps: Optional[int] = None) -> torch.Tensor:
        """
        Autoregressive forward pass.

        Args:
            x: [B, T_in, C, H, W] input features
            rollout_steps: Number of autoregressive steps (default: self.rollout_steps)
        Returns:
            [B, rollout_steps, C, H, W] output predictions
        """
        if rollout_steps is None:
            rollout_steps = self.rollout_steps

        B, T_in, C, H, W = x.shape
        predictions = []

        current_input = x

        for step in range(rollout_steps):
            # Predict next frame
            next_frame = super().forward(current_input)  # [B, 1, C, H, W]
            predictions.append(next_frame)

            # Update input: slide window and add prediction
            if T_in > 1:
                current_input = torch.cat([
                    current_input[:, 1:],  # Remove oldest frame
                    next_frame  # Add new prediction
                ], dim=1)
            else:
                current_input = next_frame

        # Concatenate all predictions
        return torch.cat(predictions, dim=1)


if __name__ == '__main__':
    # Test the model
    args = {
        'input_len': 7,
        'output_len': 1,
        'in_channels': 2,
        'img_size': [240, 240],
        'patch_size': [4, 4],
        'embed_dim': 512,
        'num_groups': 32,
        'num_heads': 8,
        'window_size': 7,
        'depth': 48,
        'use_3d_path': True,
        'pseudo_depth': 4
    }

    model = Fuxi(args)

    # Test input
    batch_size = 2
    inputs = torch.randn(batch_size, args['input_len'], args['in_channels'],
                         args['img_size'][0], args['img_size'][1])

    print(f"Input shape: {inputs.shape}")
    print(f"Model parameters: {model.count_parameters():,}")

    # Forward pass
    with torch.no_grad():
        outputs = model(inputs)

    print(f"Output shape: {outputs.shape}")
    print(f"Expected shape: ({batch_size}, {args['output_len']}, {args['in_channels']}, {args['img_size'][0]}, {args['img_size'][1]})")