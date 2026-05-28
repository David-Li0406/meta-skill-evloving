import torch
import torch.nn as nn
import torch.nn.functional as F
from einops import rearrange, repeat
from math import ceil, sqrt
from .base import BaseModel


# ==================== Attention Modules ====================
class FullAttention(nn.Module):
    """Full attention mechanism with scaled dot-product"""
    def __init__(self, scale=None, attention_dropout=0.1):
        super().__init__()
        self.scale = scale
        self.dropout = nn.Dropout(attention_dropout)
        
    def forward(self, queries, keys, values):
        """
        Args:
            queries: (B, L, H, E)
            keys: (B, S, H, E)
            values: (B, S, H, D)
        Returns:
            (B, L, H, D)
        """
        B, L, H, E = queries.shape
        _, S, _, D = values.shape
        scale = self.scale or 1.0 / sqrt(E)

        # Efficient einsum attention
        scores = torch.einsum("blhe,bshe->bhls", queries, keys)
        A = self.dropout(torch.softmax(scale * scores, dim=-1))
        V = torch.einsum("bhls,bshd->blhd", A, values)
        
        return V.contiguous()


class AttentionLayer(nn.Module):
    """Multi-head Self-Attention Layer"""
    def __init__(self, d_model, n_heads, d_keys=None, d_values=None, dropout=0.1):
        super().__init__()

        d_keys = d_keys or (d_model // n_heads)
        d_values = d_values or (d_model // n_heads)

        self.inner_attention = FullAttention(scale=None, attention_dropout=dropout)
        self.query_projection = nn.Linear(d_model, d_keys * n_heads)
        self.key_projection = nn.Linear(d_model, d_keys * n_heads)
        self.value_projection = nn.Linear(d_model, d_values * n_heads)
        self.out_projection = nn.Linear(d_values * n_heads, d_model)
        self.n_heads = n_heads

    def forward(self, queries, keys, values):
        """
        Args:
            queries: (B, L, d_model)
            keys: (B, S, d_model)
            values: (B, S, d_model)
        Returns:
            (B, L, d_model)
        """
        B, L, _ = queries.shape
        _, S, _ = keys.shape
        H = self.n_heads

        queries = self.query_projection(queries).view(B, L, H, -1)
        keys = self.key_projection(keys).view(B, S, H, -1)
        values = self.value_projection(values).view(B, S, H, -1)

        out = self.inner_attention(queries, keys, values)
        out = rearrange(out, 'b l h d -> b l (h d)')

        return self.out_projection(out)


class TwoStageAttentionLayer(nn.Module):
    """
    Two Stage Attention (TSA) Layer - adapted for spatiotemporal data
    
    Original shape: [B, data_dim, seg_num, d_model]
    In our case: 
        - data_dim = num_patches (spatial patches)
        - seg_num = temporal segments
    
    Stage 1 (Cross-Time): Apply attention across temporal segments for each patch
    Stage 2 (Cross-Patch): Apply attention across patches using router mechanism
    """
    def __init__(self, seg_num, factor, d_model, n_heads, d_ff=None, dropout=0.1):
        super().__init__()
        d_ff = d_ff or 4 * d_model

        # Stage 1: Temporal attention
        self.time_attention = AttentionLayer(d_model, n_heads, dropout=dropout)
        
        # Stage 2: Spatial (patch) attention with router
        self.patch_sender = AttentionLayer(d_model, n_heads, dropout=dropout)
        self.patch_receiver = AttentionLayer(d_model, n_heads, dropout=dropout)
        self.router = nn.Parameter(torch.randn(seg_num, factor, d_model))
        
        self.dropout = nn.Dropout(dropout)

        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.norm3 = nn.LayerNorm(d_model)
        self.norm4 = nn.LayerNorm(d_model)

        self.MLP1 = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Linear(d_ff, d_model)
        )
        self.MLP2 = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Linear(d_ff, d_model)
        )

    def forward(self, x):
        """
        Args:
            x: (B, num_patches, seg_num, d_model)
        Returns:
            (B, num_patches, seg_num, d_model)
        """
        batch = x.shape[0]
        
        # Stage 1: Cross-Time Attention
        # For each patch, apply attention across temporal segments
        time_in = rearrange(x, 'b p s d -> (b p) s d')
        time_enc = self.time_attention(time_in, time_in, time_in)
        patch_in = time_in + self.dropout(time_enc)
        patch_in = self.norm1(patch_in)
        patch_in = patch_in + self.dropout(self.MLP1(patch_in))
        patch_in = self.norm2(patch_in)

        # Stage 2: Cross-Patch Attention with router
        # For each temporal segment, apply attention across patches
        patch_send = rearrange(patch_in, '(b p) s d -> (b s) p d', b=batch)
        batch_router = repeat(self.router, 's f d -> (b s) f d', b=batch)
        
        # Router aggregates information from all patches
        patch_buffer = self.patch_sender(batch_router, patch_send, patch_send)
        # Distribute information back to patches
        patch_receive = self.patch_receiver(patch_send, patch_buffer, patch_buffer)
        
        patch_enc = patch_send + self.dropout(patch_receive)
        patch_enc = self.norm3(patch_enc)
        patch_enc = patch_enc + self.dropout(self.MLP2(patch_enc))
        patch_enc = self.norm4(patch_enc)

        final_out = rearrange(patch_enc, '(b s) p d -> b p s d', b=batch)

        return final_out


# ==================== Embedding Modules ====================

class PatchEmbedding(nn.Module):
    """
    Spatial Patch Embedding
    Convert (B, T, C, H, W) to (B, T, num_patches, patch_dim)
    """
    def __init__(self, img_size, patch_size, in_channels):
        super().__init__()
        self.img_size = img_size
        self.patch_size = patch_size
        self.grid_size = (img_size[0] // patch_size[0], img_size[1] // patch_size[1])
        self.num_patches = self.grid_size[0] * self.grid_size[1]
        self.patch_dim = in_channels * patch_size[0] * patch_size[1]
        
    def forward(self, x):
        """
        Args:
            x: (B, T, C, H, W)
        Returns:
            (B, T, num_patches, patch_dim)
        """
        B, T, C, H, W = x.shape
        p_h, p_w = self.patch_size
        
        # Rearrange to patches
        x = rearrange(
            x,
            'b t c (h p_h) (w p_w) -> b t (h w) (c p_h p_w)',
            p_h=p_h, p_w=p_w
        )
        return x


class DSW_embedding(nn.Module):
    """
    Dimension-Segment-Wise (DSW) Embedding
    Segments temporal dimension and embeds each segment
    
    Input: (B, T, num_patches, patch_dim)
    Output: (B, num_patches, seg_num, d_model)
    """
    def __init__(self, seg_len, patch_dim, d_model):
        super().__init__()
        self.seg_len = seg_len
        self.linear = nn.Linear(seg_len * patch_dim, d_model)

    def forward(self, x):
        """
        Args:
            x: (B, T, num_patches, patch_dim)
        Returns:
            (B, num_patches, seg_num, d_model)
        """
        B, T, num_patches, patch_dim = x.shape
        seg_num = T // self.seg_len
        
        # Reshape to segments
        x = rearrange(
            x,
            'b (s seg_len) p d -> b p s (seg_len d)',
            seg_len=self.seg_len, s=seg_num
        )
        
        # Embed each segment
        x = self.linear(x)  # (B, num_patches, seg_num, d_model)
        
        return x


# ==================== Encoder Modules ====================

class SegmentMerging(nn.Module):
    """
    Segment Merging Layer for multi-scale encoding
    Merges adjacent temporal segments to create coarser scale
    """
    def __init__(self, d_model, win_size, norm_layer=nn.LayerNorm):
        super().__init__()
        self.d_model = d_model
        self.win_size = win_size
        self.linear_trans = nn.Linear(win_size * d_model, d_model)
        self.norm = norm_layer(win_size * d_model)

    def forward(self, x):
        """
        Args:
            x: (B, num_patches, seg_num, d_model)
        Returns:
            (B, num_patches, seg_num//win_size, d_model)
        """
        B, num_patches, seg_num, d_model = x.shape
        
        # Pad if needed
        pad_num = seg_num % self.win_size
        if pad_num != 0:
            pad_num = self.win_size - pad_num
            x = torch.cat([x, x[:, :, -pad_num:, :]], dim=2)
        
        # Merge segments
        seg_to_merge = []
        for i in range(self.win_size):
            seg_to_merge.append(x[:, :, i::self.win_size, :])
        
        x = torch.cat(seg_to_merge, -1)  # (B, num_patches, seg_num//win_size, win_size*d_model)
        x = self.norm(x)
        x = self.linear_trans(x)
        
        return x


class ScaleBlock(nn.Module):
    """
    Scale block with segment merging and TSA layers
    """
    def __init__(self, win_size, d_model, n_heads, d_ff, depth, dropout, seg_num, factor):
        super().__init__()

        if win_size > 1:
            self.merge_layer = SegmentMerging(d_model, win_size, nn.LayerNorm)
        else:
            self.merge_layer = None
        
        self.encode_layers = nn.ModuleList()
        for _ in range(depth):
            self.encode_layers.append(
                TwoStageAttentionLayer(seg_num, factor, d_model, n_heads, d_ff, dropout)
            )
    
    def forward(self, x):
        """
        Args:
            x: (B, num_patches, seg_num, d_model)
        Returns:
            (B, num_patches, seg_num', d_model)
        """
        if self.merge_layer is not None:
            x = self.merge_layer(x)
        
        for layer in self.encode_layers:
            x = layer(x)
        
        return x


class Encoder(nn.Module):
    """Multi-scale Crossformer Encoder"""
    def __init__(self, e_blocks, win_size, d_model, n_heads, d_ff, block_depth, 
                 dropout, in_seg_num, factor):
        super().__init__()
        self.encode_blocks = nn.ModuleList()

        # First block: no merging
        self.encode_blocks.append(
            ScaleBlock(1, d_model, n_heads, d_ff, block_depth, dropout, in_seg_num, factor)
        )
        
        # Subsequent blocks: with merging
        for i in range(1, e_blocks):
            seg_num_at_scale = ceil(in_seg_num / (win_size ** i))
            self.encode_blocks.append(
                ScaleBlock(win_size, d_model, n_heads, d_ff, block_depth, dropout, 
                          seg_num_at_scale, factor)
            )

    def forward(self, x):
        """
        Args:
            x: (B, num_patches, seg_num, d_model)
        Returns:
            List of encoder outputs at each scale
        """
        encode_x = [x]
        
        for block in self.encode_blocks:
            x = block(x)
            encode_x.append(x)

        return encode_x


# ==================== Decoder Modules ====================

class DecoderLayer(nn.Module):
    """Decoder layer with self-attention, cross-attention, and prediction"""
    def __init__(self, seg_len, d_model, n_heads, d_ff, dropout, out_seg_num, factor, patch_dim):
        super().__init__()
        self.seg_len = seg_len
        self.patch_dim = patch_dim
        
        self.self_attention = TwoStageAttentionLayer(out_seg_num, factor, d_model, n_heads, d_ff, dropout)
        self.cross_attention = AttentionLayer(d_model, n_heads, dropout=dropout)
        
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
        
        self.MLP = nn.Sequential(
            nn.Linear(d_model, d_model),
            nn.GELU(),
            nn.Linear(d_model, d_model)
        )
        
        # Predict segment values
        self.linear_pred = nn.Linear(d_model, seg_len * patch_dim)

    def forward(self, x, cross):
        """
        Args:
            x: (B, num_patches, out_seg_num, d_model) - decoder input
            cross: (B, num_patches, in_seg_num, d_model) - encoder output
        Returns:
            dec_output: (B, num_patches, out_seg_num, d_model)
            layer_predict: (B, T_out, num_patches, patch_dim)
        """
        B = x.shape[0]
        
        # Self-attention
        x = self.self_attention(x)
        
        # Cross-attention
        x_flat = rearrange(x, 'b p s d -> (b p) s d')
        cross_flat = rearrange(cross, 'b p s d -> (b p) s d')
        
        tmp = self.cross_attention(x_flat, cross_flat, cross_flat)
        x_flat = x_flat + self.dropout(tmp)
        y = x_flat = self.norm1(x_flat)
        y = self.MLP(y)
        dec_output = self.norm2(x_flat + y)
        
        dec_output = rearrange(dec_output, '(b p) s d -> b p s d', b=B)
        
        # Predict segment values
        layer_predict = self.linear_pred(dec_output)  # (B, num_patches, out_seg_num, seg_len*patch_dim)
        layer_predict = rearrange(
            layer_predict, 
            'b p s (seg_len d) -> b (s seg_len) p d',
            seg_len=self.seg_len, d=self.patch_dim
        )
        
        return dec_output, layer_predict


class Decoder(nn.Module):
    """Multi-scale Crossformer Decoder"""
    def __init__(self, seg_len, d_layers, d_model, n_heads, d_ff, dropout, 
                 out_seg_num, factor, patch_dim):
        super().__init__()
        
        self.decode_layers = nn.ModuleList()
        for _ in range(d_layers):
            self.decode_layers.append(
                DecoderLayer(seg_len, d_model, n_heads, d_ff, dropout, out_seg_num, factor, patch_dim)
            )

    def forward(self, x, cross):
        """
        Args:
            x: (B, num_patches, out_seg_num, d_model) - decoder input
            cross: List of encoder outputs at each scale
        Returns:
            (B, T_out, num_patches, patch_dim)
        """
        final_predict = None
        
        for i, layer in enumerate(self.decode_layers):
            cross_enc = cross[i]
            x, layer_predict = layer(x, cross_enc)
            
            if final_predict is None:
                final_predict = layer_predict
            else:
                final_predict = final_predict + layer_predict
        
        return final_predict


# ==================== Main Model ====================

class OceanCrossformer(BaseModel):
    """
    Crossformer adapted for ocean velocity prediction
    
    Input: (B, T_in, C, H, W)
    Output: (B, T_out, C, H, W)
    
    Process:
    1. Spatial patchification
    2. Temporal segmentation
    3. Multi-scale encoding with Two-Stage Attention
    4. Multi-scale decoding
    5. Spatial reconstruction
    """
    def __init__(self, args):
        super(BaseModel, self).__init__()
        
        # Task parameters
        self.input_len = args.get('input_len', 7)
        self.output_len = args.get('output_len', 1)
        self.in_channels = args.get('in_channels', 2)
        
        # Model parameters
        self.img_size = args.get('img_size', [240, 240])
        self.patch_size = args.get('patch_size', [8, 8])
        self.seg_len = args.get('seg_len', 1)  # Temporal segment length
        self.win_size = args.get('win_size', 2)  # Window size for segment merging
        self.factor = args.get('factor', 10)  # Router factor
        
        self.d_model = args.get('d_model', 256)
        self.d_ff = args.get('d_ff', 512)
        self.n_heads = args.get('n_heads', 8)
        self.e_layers = args.get('e_layers', 3)  # Number of encoder scales
        self.dropout = args.get('dropout', 0.1)
        self.baseline = args.get('baseline', False)  # Use baseline prediction
        
        # Calculate dimensions
        self.patch_embedding = PatchEmbedding(self.img_size, self.patch_size, self.in_channels)
        self.num_patches = self.patch_embedding.num_patches
        self.patch_dim = self.patch_embedding.patch_dim
        
        # Padding for segment alignment
        self.pad_in_len = ceil(self.input_len / self.seg_len) * self.seg_len
        self.pad_out_len = ceil(self.output_len / self.seg_len) * self.seg_len
        self.in_len_add = self.pad_in_len - self.input_len
        
        self.in_seg_num = self.pad_in_len // self.seg_len
        self.out_seg_num = self.pad_out_len // self.seg_len
        
        # Embedding layers
        self.enc_value_embedding = DSW_embedding(self.seg_len, self.patch_dim, self.d_model)
        self.enc_pos_embedding = nn.Parameter(
            torch.randn(1, self.num_patches, self.in_seg_num, self.d_model)
        )
        self.pre_norm = nn.LayerNorm(self.d_model)
        
        # Encoder
        self.encoder = Encoder(
            e_blocks=self.e_layers,
            win_size=self.win_size,
            d_model=self.d_model,
            n_heads=self.n_heads,
            d_ff=self.d_ff,
            block_depth=1,
            dropout=self.dropout,
            in_seg_num=self.in_seg_num,
            factor=self.factor
        )
        
        # Decoder
        self.dec_pos_embedding = nn.Parameter(
            torch.randn(1, self.num_patches, self.out_seg_num, self.d_model)
        )
        self.decoder = Decoder(
            seg_len=self.seg_len,
            d_layers=self.e_layers + 1,
            d_model=self.d_model,
            n_heads=self.n_heads,
            d_ff=self.d_ff,
            dropout=self.dropout,
            out_seg_num=self.out_seg_num,
            factor=self.factor,
            patch_dim=self.patch_dim
        )

    def forward(self, x):
        """
        Args:
            x: (B, T_in, C, H, W)
        Returns:
            (B, T_out, C, H, W)
        """
        B, T_in, C, H, W = x.shape
        
        # Baseline prediction (optional)
        if self.baseline:
            base = x.mean(dim=1, keepdim=True)  # (B, 1, C, H, W)
        else:
            base = 0
        
        # Pad temporal dimension if needed
        if self.in_len_add != 0:
            x = torch.cat([x[:, :1].expand(-1, self.in_len_add, -1, -1, -1), x], dim=1)
        
        # Spatial patchification: (B, T, C, H, W) -> (B, T, num_patches, patch_dim)
        x_patches = self.patch_embedding(x)
        
        # Temporal segmentation and embedding: (B, T, P, D) -> (B, P, S, d_model)
        x_embed = self.enc_value_embedding(x_patches)
        x_embed = x_embed + self.enc_pos_embedding
        x_embed = self.pre_norm(x_embed)
        
        # Encode
        enc_out = self.encoder(x_embed)
        
        # Decode
        dec_in = repeat(
            self.dec_pos_embedding, 
            '1 p s d -> b p s d', 
            b=B
        )
        predict_patches = self.decoder(dec_in, enc_out)  # (B, T_out_pad, num_patches, patch_dim)
        
        # Trim to actual output length
        predict_patches = predict_patches[:, :self.output_len]  # (B, T_out, num_patches, patch_dim)
        
        # Reconstruct spatial dimensions
        p_h, p_w = self.patch_size
        g_h, g_w = self.patch_embedding.grid_size
        
        output = rearrange(
            predict_patches,
            'b t (h w) (c p_h p_w) -> b t c (h p_h) (w p_w)',
            h=g_h, w=g_w, c=C, p_h=p_h, p_w=p_w
        )
        
        return base + output


class OceanCrossformerAutoregressive(OceanCrossformer):
    """
    Autoregressive version of OceanCrossformer for long-term prediction
    Uses single-frame prediction and rolls out for multiple steps
    """
    def __init__(self, args):
        # Force single frame output for autoregressive mode
        args_auto = dict(args)
        args_auto["output_len"] = 1
        super().__init__(args_auto)
        
        self.rollout_steps = args.get("rollout_steps", 1)

    def forward(self, x, rollout_steps=None):
        """
        Autoregressive forward pass
        
        Args:
            x: (B, T_in, C, H, W) input features
            rollout_steps: Number of autoregressive steps (default: self.rollout_steps)
        Returns:
            (B, rollout_steps, C, H, W) output predictions
        """
        if rollout_steps is None:
            rollout_steps = self.rollout_steps
        
        B, T_in, C, H, W = x.shape
        predictions = []
        
        current_input = x
        
        for step in range(rollout_steps):
            # Predict next frame
            next_frame = super().forward(current_input)  # (B, 1, C, H, W)
            predictions.append(next_frame)
            
            # Update input: slide window and add prediction
            if T_in > 1:
                current_input = torch.cat([
                    current_input[:, 1:],  # Remove oldest frame
                    next_frame  # Add new prediction
                ], dim=1)
            else:
                current_input = next_frame
        
        # Stack predictions
        output = torch.cat(predictions, dim=1)  # (B, rollout_steps, C, H, W)
        return output