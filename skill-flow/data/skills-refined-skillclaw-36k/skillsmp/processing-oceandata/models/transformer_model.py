import torch
import torch.nn as nn
import math
from einops import rearrange
from .base import BaseModel
from .cnn_model import PatchEmbed


class PositionalEncoding(nn.Module):
    """Positional encoding for spatiotemporal tokens"""
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)

    def forward(self, x):
        """
        x: (B, T, d_model)
        """
        return x + self.pe[:, :x.size(1)]


class SpatialPositionalEncoding(nn.Module):
    """2D positional encoding for spatial dimensions"""
    def __init__(self, channels, height, width):
        super().__init__()
        self.channels = channels
        self.height = height
        self.width = width

        # Create 2D positional encoding
        pe = torch.zeros(channels, height, width)

        # Compute position encodings
        y_pos = torch.arange(0, height, dtype=torch.float).unsqueeze(1).repeat(1, width)
        x_pos = torch.arange(0, width, dtype=torch.float).unsqueeze(0).repeat(height, 1)

        div_term = torch.exp(torch.arange(0, channels, 2).float() * (-math.log(10000.0) / channels))

        pe[0::2] = torch.sin(y_pos.unsqueeze(0) * div_term.unsqueeze(1).unsqueeze(2))
        pe[1::2] = torch.cos(x_pos.unsqueeze(0) * div_term.unsqueeze(1).unsqueeze(2))

        self.register_buffer('pe', pe.unsqueeze(0))

    def forward(self, x):
        """
        x: (B, C, H, W)
        """
        return x + self.pe


class TransformerEncoderLayer(nn.Module):
    """Custom Transformer Encoder Layer for spatiotemporal data"""
    def __init__(self, d_model, nhead, dim_feedforward=2048, dropout=0.1):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(d_model, nhead, dropout=dropout, batch_first=True)
        self.linear1 = nn.Linear(d_model, dim_feedforward)
        self.dropout = nn.Dropout(dropout)
        self.linear2 = nn.Linear(dim_feedforward, d_model)

        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)

    def forward(self, src):
        """
        src: (B, N, d_model)
        """
        # Self-attention
        src2, _ = self.self_attn(src, src, src)
        src = src + self.dropout1(src2)
        src = self.norm1(src)

        # FFN
        src2 = self.linear2(self.dropout(torch.relu(self.linear1(src))))
        src = src + self.dropout2(src2)
        src = self.norm2(src)

        return src


class OceanTransformer(BaseModel):
    """
    Vision Transformer (ViT) model for ocean velocity prediction (baseline)
    Standard ViT architecture with encoder-decoder structure

    Process: Concatenate input frames -> Patch embedding -> Transformer Encoder -> Decoder -> Output frame
    Input: (B, T_in, C, H, W) -> (B, T_in*C, H, W)
    Output: (B, T_out, C, H, W)
    """
    def __init__(self, args):
        super(BaseModel, self).__init__()

        self.input_len = args.get('input_len', 7)
        self.output_len = args.get('output_len', 1)
        self.in_channels = args.get('in_channels', 2)
        self.patch_size = args.get('patch_size', 8)  # Standard ViT patch size
        self.d_model = args.get('d_model', 256)
        self.nhead = args.get('nhead', 8)
        self.num_layers = args.get('num_layers', 6)
        self.dim_feedforward = args.get('dim_feedforward', 1024)
        self.dropout = args.get('dropout', 0.1)

        # Calculate input channels after concatenating temporal frames
        input_channels = self.input_len * self.in_channels
        patch_dim = input_channels * (self.patch_size ** 2)

        # Patch embedding: flatten patches and project to d_model
        self.patch_embedding = nn.Linear(patch_dim, self.d_model)

        # Class token for global representation
        self.cls_token = nn.Parameter(torch.randn(1, 1, self.d_model))

        # Positional encoding (will be created dynamically based on input size)
        self.pos_embedding = None

        # Transformer encoder layers (standard ViT)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=self.d_model,
            nhead=self.nhead,
            dim_feedforward=self.dim_feedforward,
            dropout=self.dropout,
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=self.num_layers)

        # Decoder: MLP to predict output patches
        output_patch_dim = (self.output_len * self.in_channels) * (self.patch_size ** 2)
        self.decoder = nn.Sequential(
            nn.Linear(self.d_model, self.dim_feedforward),
            nn.GELU(),
            nn.Dropout(self.dropout),
            nn.Linear(self.dim_feedforward, output_patch_dim)
        )

    def patchify(self, x):
        """
        Convert image to patches
        x: (B, C, H, W)
        return: (B, num_patches, patch_dim)
        """
        B, C, H, W = x.shape
        p = self.patch_size

        # Ensure image dimensions are divisible by patch size
        assert H % p == 0 and W % p == 0, f"Image dimensions ({H}, {W}) must be divisible by patch size ({p})"

        # Reshape to patches
        x = x.reshape(B, C, H // p, p, W // p, p)
        x = x.permute(0, 2, 4, 1, 3, 5).contiguous()
        x = x.reshape(B, (H // p) * (W // p), C * p * p)
        return x

    def unpatchify(self, x, out_channels, H, W):
        """
        Convert patches back to image
        x: (B, num_patches, patch_dim)
        return: (B, out_channels, H, W)
        """
        B = x.shape[0]
        p = self.patch_size
        h = H // p
        w = W // p

        x = x.reshape(B, h, w, out_channels, p, p)
        x = x.permute(0, 3, 1, 4, 2, 5).contiguous()
        x = x.reshape(B, out_channels, H, W)
        return x

    def forward(self, x):
        """
        x: (B, T_in, C, H, W)
        return: (B, T_out, C, H, W)
        """
        B, T_in, C, H, W = x.shape

        # Concatenate temporal frames along channel dimension
        # (B, T_in, C, H, W) -> (B, T_in*C, H, W)
        x = x.reshape(B, T_in * C, H, W)

        # Convert to patches
        patches = self.patchify(x)  # (B, num_patches, patch_dim)
        num_patches = patches.shape[1]

        # Patch embedding
        x = self.patch_embedding(patches)  # (B, num_patches, d_model)

        # Add cls token
        cls_tokens = self.cls_token.expand(B, -1, -1)  # (B, 1, d_model)
        x = torch.cat([cls_tokens, x], dim=1)  # (B, num_patches+1, d_model)

        # Add positional encoding
        if self.pos_embedding is None or self.pos_embedding.shape[1] != x.shape[1]:
            self.pos_embedding = nn.Parameter(torch.randn(1, num_patches + 1, self.d_model)).to(x.device)
        x = x + self.pos_embedding

        # Transformer encoder
        x = self.transformer_encoder(x)  # (B, num_patches+1, d_model)

        # Remove cls token
        x = x[:, 1:, :]  # (B, num_patches, d_model)

        # Decode to output patches
        output_patches = self.decoder(x)  # (B, num_patches, output_patch_dim)

        # Unpatchify to image
        output = self.unpatchify(output_patches, self.output_len * self.in_channels, H, W)  # (B, T_out*C, H, W)

        # Reshape to output format
        # (B, T_out*C, H, W) -> (B, T_out, C, H, W)
        output = output.reshape(B, self.output_len, self.in_channels, H, W)

        return output
