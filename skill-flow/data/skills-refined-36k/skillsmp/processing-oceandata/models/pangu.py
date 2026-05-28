"""
Pangu2 Model - 2D+3D混合版本
将2D数据同时输入到2D和3D处理路径，融合两种特征
"""

import torch
import torch.nn as nn
from einops import rearrange
import math
import numpy as np
from .base import BaseModel


# ==================== 辅助函数 ====================
def get_pad3d(input_resolution, window_size):
    """计算3D padding"""
    Pl, Lat, Lon = input_resolution
    win_pl, win_lat, win_lon = window_size

    padding_left = padding_right = padding_top = padding_bottom = padding_front = padding_back = 0

    pl_remainder = Pl % win_pl
    lat_remainder = Lat % win_lat
    lon_remainder = Lon % win_lon

    if pl_remainder:
        pl_pad = win_pl - pl_remainder
        padding_front = pl_pad // 2
        padding_back = pl_pad - padding_front
    if lat_remainder:
        lat_pad = win_lat - lat_remainder
        padding_top = lat_pad // 2
        padding_bottom = lat_pad - padding_top
    if lon_remainder:
        lon_pad = win_lon - lon_remainder
        padding_left = lon_pad // 2
        padding_right = lon_pad - padding_left

    return (padding_left, padding_right, padding_top, padding_bottom, padding_front, padding_back)


def get_pad2d(input_resolution, window_size):
    """计算2D padding"""
    input_resolution = [2] + list(input_resolution)
    window_size = [2] + list(window_size)
    padding = get_pad3d(input_resolution, window_size)
    return padding[:4]


def crop3d(x, resolution):
    """裁剪3D tensor"""
    _, _, Pl, Lat, Lon = x.shape
    pl_pad = Pl - resolution[0]
    lat_pad = Lat - resolution[1]
    lon_pad = Lon - resolution[2]

    padding_front = pl_pad // 2
    padding_back = pl_pad - padding_front
    padding_top = lat_pad // 2
    padding_bottom = lat_pad - padding_top
    padding_left = lon_pad // 2
    padding_right = lon_pad - padding_left

    return x[:, :,
             padding_front:Pl-padding_back,
             padding_top:Lat-padding_bottom,
             padding_left:Lon-padding_right]


def crop2d(x, resolution):
    """裁剪2D tensor"""
    _, _, Lat, Lon = x.shape
    lat_pad = Lat - resolution[0]
    lon_pad = Lon - resolution[1]

    padding_top = lat_pad // 2
    padding_bottom = lat_pad - padding_top
    padding_left = lon_pad // 2
    padding_right = lon_pad - padding_left

    return x[:, :, padding_top:Lat-padding_bottom, padding_left:Lon-padding_right]


def window_partition(x, window_size, ndim=3):
    """将输入分割为窗口"""
    if ndim == 3:
        B, Pl, Lat, Lon, C = x.shape
        win_pl, win_lat, win_lon = window_size
        x = x.view(B, Pl // win_pl, win_pl, Lat // win_lat, win_lat, Lon // win_lon, win_lon, C)
        windows = x.permute(0, 5, 1, 3, 2, 4, 6, 7).contiguous()
        windows = windows.view(-1, (Pl // win_pl) * (Lat // win_lat), win_pl * win_lat * win_lon, C)
        return windows
    else:
        B, Lat, Lon, C = x.shape
        win_lat, win_lon = window_size
        x = x.view(B, Lat // win_lat, win_lat, Lon // win_lon, win_lon, C)
        windows = x.permute(0, 3, 1, 2, 4, 5).contiguous()
        windows = windows.view(-1, Lat // win_lat, win_lat * win_lon, C)
        return windows


def window_reverse(windows, window_size, Pl=None, Lat=None, Lon=None, ndim=3):
    """将窗口恢复为原始形状"""
    if ndim == 3:
        win_pl, win_lat, win_lon = window_size
        B = int(windows.shape[0] / (Lon / win_lon))
        x = windows.view(B, Lon // win_lon, Pl // win_pl, Lat // win_lat,
                        win_pl, win_lat, win_lon, -1)
        x = x.permute(0, 2, 4, 3, 5, 1, 6, 7).contiguous().view(B, Pl, Lat, Lon, -1)
        return x
    else:
        win_lat, win_lon = window_size
        B = int(windows.shape[0] / (Lon / win_lon))
        x = windows.view(B, Lon // win_lon, Lat // win_lat, win_lat, win_lon, -1)
        x = x.permute(0, 2, 3, 1, 4, 5).contiguous().view(B, Lat, Lon, -1)
        return x


def get_earth_position_index(window_size, ndim=3):
    """生成Earth Position Index"""
    if ndim == 3:
        win_pl, win_lat, win_lon = window_size
        coords_zi = torch.arange(win_pl)
        coords_zj = -torch.arange(win_pl) * win_pl
        coords_hi = torch.arange(win_lat)
        coords_hj = -torch.arange(win_lat) * win_lat
        coords_w = torch.arange(win_lon)

        coords_1 = torch.stack(torch.meshgrid([coords_zi, coords_hi, coords_w]))
        coords_2 = torch.stack(torch.meshgrid([coords_zj, coords_hj, coords_w]))
    else:
        win_lat, win_lon = window_size
        coords_hi = torch.arange(win_lat)
        coords_hj = -torch.arange(win_lat) * win_lat
        coords_w = torch.arange(win_lon)

        coords_1 = torch.stack(torch.meshgrid([coords_hi, coords_w]))
        coords_2 = torch.stack(torch.meshgrid([coords_hj, coords_w]))

    coords_flatten_1 = torch.flatten(coords_1, 1)
    coords_flatten_2 = torch.flatten(coords_2, 1)
    coords = coords_flatten_1[:, :, None] - coords_flatten_2[:, None, :]
    coords = coords.permute(1, 2, 0).contiguous()

    if ndim == 3:
        coords[:, :, 2] += win_lon - 1
        coords[:, :, 1] *= 2 * win_lon - 1
        coords[:, :, 0] *= (2 * win_lon - 1) * win_lat * win_lat
    else:
        coords[:, :, 1] += win_lon - 1
        coords[:, :, 0] *= 2 * win_lon - 1

    position_index = coords.sum(-1)
    return position_index


# ==================== 模块定义 ====================
class PatchEmbed2D(nn.Module):
    """2D Patch Embedding"""
    def __init__(self, img_size, patch_size, in_chans, embed_dim):
        super().__init__()
        self.img_size = img_size
        height, width = img_size
        h_patch, w_patch = patch_size

        padding_left = padding_right = padding_top = padding_bottom = 0

        h_remainder = height % h_patch
        w_remainder = width % w_patch

        if h_remainder:
            h_pad = h_patch - h_remainder
            padding_top = h_pad // 2
            padding_bottom = h_pad - padding_top

        if w_remainder:
            w_pad = w_patch - w_remainder
            padding_left = w_pad // 2
            padding_right = w_pad - padding_left

        self.pad = nn.ZeroPad2d((padding_left, padding_right, padding_top, padding_bottom))
        self.proj = nn.Conv2d(in_chans, embed_dim, kernel_size=patch_size, stride=patch_size)
        self.norm = nn.LayerNorm(embed_dim)

    def forward(self, x):
        x = self.pad(x)
        x = self.proj(x)
        x = rearrange(x, 'b c h w -> b h w c')
        x = self.norm(x)
        x = rearrange(x, 'b h w c -> b c h w')
        return x


class PatchEmbed3D(nn.Module):
    """3D Patch Embedding"""
    def __init__(self, img_size, patch_size, in_chans, embed_dim):
        super().__init__()
        self.img_size = img_size
        level, height, width = img_size
        l_patch, h_patch, w_patch = patch_size

        padding_left = padding_right = padding_top = padding_bottom = padding_front = padding_back = 0

        l_remainder = level % l_patch
        h_remainder = height % h_patch
        w_remainder = width % w_patch

        if l_remainder:
            l_pad = l_patch - l_remainder
            padding_front = l_pad // 2
            padding_back = l_pad - padding_front
        if h_remainder:
            h_pad = h_patch - h_remainder
            padding_top = h_pad // 2
            padding_bottom = h_pad - padding_top
        if w_remainder:
            w_pad = w_patch - w_remainder
            padding_left = w_pad // 2
            padding_right = w_pad - padding_left

        self.pad = nn.ConstantPad3d((padding_left, padding_right, padding_top, padding_bottom,
                                 padding_front, padding_back), 0)
        self.proj = nn.Conv3d(in_chans, embed_dim, kernel_size=patch_size, stride=patch_size)
        self.norm = nn.LayerNorm(embed_dim)

    def forward(self, x):
        x = self.pad(x)
        x = self.proj(x)
        x = rearrange(x, 'b c l h w -> b l h w c')
        x = self.norm(x)
        x = rearrange(x, 'b l h w c -> b c l h w')
        return x


class PatchRecovery2D(nn.Module):
    """2D Patch Recovery"""
    def __init__(self, img_size, patch_size, in_chans, out_chans):
        super().__init__()
        self.img_size = img_size
        self.conv = nn.ConvTranspose2d(in_chans, out_chans, patch_size, patch_size)

    def forward(self, x):
        output = self.conv(x)
        _, _, H, W = output.shape
        h_pad = H - self.img_size[0]
        w_pad = W - self.img_size[1]

        padding_top = h_pad // 2
        padding_bottom = h_pad - padding_top
        padding_left = w_pad // 2
        padding_right = w_pad - padding_left

        return output[:, :, padding_top:H-padding_bottom, padding_left:W-padding_right]


class PatchRecovery3D(nn.Module):
    """3D Patch Recovery"""
    def __init__(self, img_size, patch_size, in_chans, out_chans):
        super().__init__()
        self.img_size = img_size
        self.conv = nn.ConvTranspose3d(in_chans, out_chans, patch_size, patch_size)

    def forward(self, x):
        output = self.conv(x)
        _, _, Pl, Lat, Lon = output.shape

        pl_pad = Pl - self.img_size[0]
        lat_pad = Lat - self.img_size[1]
        lon_pad = Lon - self.img_size[2]

        padding_front = pl_pad // 2
        padding_back = pl_pad - padding_front
        padding_top = lat_pad // 2
        padding_bottom = lat_pad - padding_top
        padding_left = lon_pad // 2
        padding_right = lon_pad - padding_left

        return output[:, :,
                     padding_front:Pl-padding_back,
                     padding_top:Lat-padding_bottom,
                     padding_left:Lon-padding_right]


class EarthAttention3D(nn.Module):
    """Earth-aware 3D Attention"""
    def __init__(self, dim, input_resolution, window_size, num_heads, qkv_bias=True,
                 attn_drop=0., proj_drop=0.):
        super().__init__()
        self.dim = dim
        self.window_size = window_size
        self.num_heads = num_heads
        head_dim = dim // num_heads
        self.scale = head_dim ** -0.5

        self.type_of_windows = (input_resolution[0] // window_size[0]) * \
                              (input_resolution[1] // window_size[1])

        self.earth_position_bias_table = nn.Parameter(
            torch.zeros((window_size[0]**2) * (window_size[1]**2) * (window_size[2]*2-1),
                       self.type_of_windows, num_heads)
        )
        nn.init.trunc_normal_(self.earth_position_bias_table, std=0.02)

        earth_position_index = get_earth_position_index(window_size)
        self.register_buffer("earth_position_index", earth_position_index)

        self.qkv = nn.Linear(dim, dim * 3, bias=qkv_bias)
        self.attn_drop = nn.Dropout(attn_drop)
        self.proj = nn.Linear(dim, dim)
        self.proj_drop = nn.Dropout(proj_drop)

    def forward(self, x):
        B_, nW_, N, C = x.shape

        qkv = self.qkv(x).reshape(B_, nW_, N, 3, self.num_heads, C // self.num_heads).permute(3, 0, 4, 1, 2, 5)
        q, k, v = qkv[0], qkv[1], qkv[2]

        q = q * self.scale
        attn = q @ k.transpose(-2, -1)

        # Earth position bias
        earth_position_bias = self.earth_position_bias_table[self.earth_position_index.view(-1)].view(
            self.window_size[0] * self.window_size[1] * self.window_size[2],
            self.window_size[0] * self.window_size[1] * self.window_size[2],
            self.type_of_windows, -1
        )
        earth_position_bias = earth_position_bias.permute(3, 2, 0, 1).unsqueeze(0)
        attn = attn + earth_position_bias

        attn = attn.softmax(dim=-1)
        attn = self.attn_drop(attn)

        x = (attn @ v).transpose(1, 2).reshape(B_, nW_, N, C)
        x = self.proj(x)
        x = self.proj_drop(x)
        return x


class EarthAttention2D(nn.Module):
    """Earth-aware 2D Attention"""
    def __init__(self, dim, input_resolution, window_size, num_heads, qkv_bias=True,
                 attn_drop=0., proj_drop=0.):
        super().__init__()
        self.dim = dim
        self.window_size = window_size
        self.num_heads = num_heads
        head_dim = dim // num_heads
        self.scale = head_dim ** -0.5

        self.type_of_windows = input_resolution[0] // window_size[0]

        self.earth_position_bias_table = nn.Parameter(
            torch.zeros((window_size[0]**2) * (window_size[1]*2-1),
                       self.type_of_windows, num_heads)
        )
        nn.init.trunc_normal_(self.earth_position_bias_table, std=0.02)

        earth_position_index = get_earth_position_index(window_size, ndim=2)
        self.register_buffer("earth_position_index", earth_position_index)

        self.qkv = nn.Linear(dim, dim * 3, bias=qkv_bias)
        self.attn_drop = nn.Dropout(attn_drop)
        self.proj = nn.Linear(dim, dim)
        self.proj_drop = nn.Dropout(proj_drop)

    def forward(self, x):
        B_, nW_, N, C = x.shape

        qkv = self.qkv(x).reshape(B_, nW_, N, 3, self.num_heads, C // self.num_heads).permute(3, 0, 4, 1, 2, 5)
        q, k, v = qkv[0], qkv[1], qkv[2]

        q = q * self.scale
        attn = q @ k.transpose(-2, -1)

        # Earth position bias
        earth_position_bias = self.earth_position_bias_table[self.earth_position_index.view(-1)].view(
            self.window_size[0] * self.window_size[1],
            self.window_size[0] * self.window_size[1],
            self.type_of_windows, -1
        )
        earth_position_bias = earth_position_bias.permute(3, 2, 0, 1).unsqueeze(0)
        attn = attn + earth_position_bias

        attn = attn.softmax(dim=-1)
        attn = self.attn_drop(attn)

        x = (attn @ v).transpose(1, 2).reshape(B_, nW_, N, C)
        x = self.proj(x)
        x = self.proj_drop(x)
        return x


class Transformer3DBlock(nn.Module):
    """3D Transformer Block"""
    def __init__(self, dim, input_resolution, num_heads, window_size=None,
                 shift_size=None, mlp_ratio=4., qkv_bias=True, drop=0.,
                 attn_drop=0., drop_path=0.):
        super().__init__()
        window_size = (2, 6, 12) if window_size is None else window_size
        shift_size = (1, 3, 6) if shift_size is None else shift_size
        self.dim = dim
        self.input_resolution = input_resolution
        self.window_size = window_size
        self.shift_size = shift_size

        self.norm1 = nn.LayerNorm(dim)
        padding = get_pad3d(input_resolution, window_size)
        self.pad = nn.ConstantPad3d(padding, 0)

        pad_resolution = list(input_resolution)
        pad_resolution[0] += padding[-1] + padding[-2]
        pad_resolution[1] += padding[2] + padding[3]
        pad_resolution[2] += padding[0] + padding[1]

        self.attn = EarthAttention3D(
            dim=dim,
            input_resolution=pad_resolution,
            window_size=window_size,
            num_heads=num_heads,
            qkv_bias=qkv_bias,
            attn_drop=attn_drop,
            proj_drop=drop
        )

        self.drop_path = DropPath(drop_path) if drop_path > 0. else nn.Identity()
        self.norm2 = nn.LayerNorm(dim)
        mlp_hidden_dim = int(dim * mlp_ratio)
        self.mlp = Mlp(in_features=dim, hidden_features=mlp_hidden_dim, drop=drop)

    def forward(self, x):
        Pl, Lat, Lon = self.input_resolution
        B, L, C = x.shape

        shortcut = x
        x = self.norm1(x)
        x = rearrange(x, 'b (pl lat lon) c -> b pl lat lon c', pl=Pl, lat=Lat, lon=Lon)

        # Pad
        x = rearrange(x, 'b pl lat lon c -> b c pl lat lon')
        x = self.pad(x)
        _, _, Pl_pad, Lat_pad, Lon_pad = x.shape
        x = rearrange(x, 'b c pl lat lon -> b pl lat lon c')

        # Cyclic shift
        if self.shift_size[0] > 0:
            shifted_x = torch.roll(x, shifts=tuple(-s for s in self.shift_size), dims=(1, 2, 3))
        else:
            shifted_x = x

        # Partition windows
        x_windows = window_partition(shifted_x, self.window_size, ndim=3)

        # W-MSA
        attn_windows = self.attn(x_windows)

        # Merge windows
        shifted_x = window_reverse(attn_windows, self.window_size, Pl_pad, Lat_pad, Lon_pad, ndim=3)

        # Reverse cyclic shift
        if self.shift_size[0] > 0:
            x = torch.roll(shifted_x, shifts=self.shift_size, dims=(1, 2, 3))
        else:
            x = shifted_x

        # Crop
        x = rearrange(x, 'b pl lat lon c -> b c pl lat lon')
        x = crop3d(x, self.input_resolution)
        x = rearrange(x, 'b c pl lat lon -> b (pl lat lon) c')

        # FFN
        x = shortcut + self.drop_path(x)
        x = x + self.drop_path(self.mlp(self.norm2(x)))

        return x


class Transformer2DBlock(nn.Module):
    """2D Transformer Block"""
    def __init__(self, dim, input_resolution, num_heads, window_size=None,
                 shift_size=None, mlp_ratio=4., qkv_bias=True, drop=0.,
                 attn_drop=0., drop_path=0.):
        super().__init__()
        window_size = (6, 12) if window_size is None else window_size
        shift_size = (3, 6) if shift_size is None else shift_size
        self.dim = dim
        self.input_resolution = input_resolution
        self.window_size = window_size
        self.shift_size = shift_size

        self.norm1 = nn.LayerNorm(dim)
        padding = get_pad2d(input_resolution, window_size)
        self.pad = nn.ZeroPad2d(padding)

        pad_resolution = list(input_resolution)
        pad_resolution[0] += padding[2] + padding[3]
        pad_resolution[1] += padding[0] + padding[1]

        self.attn = EarthAttention2D(
            dim=dim,
            input_resolution=pad_resolution,
            window_size=window_size,
            num_heads=num_heads,
            qkv_bias=qkv_bias,
            attn_drop=attn_drop,
            proj_drop=drop
        )

        self.drop_path = DropPath(drop_path) if drop_path > 0. else nn.Identity()
        self.norm2 = nn.LayerNorm(dim)
        mlp_hidden_dim = int(dim * mlp_ratio)
        self.mlp = Mlp(in_features=dim, hidden_features=mlp_hidden_dim, drop=drop)

    def forward(self, x):
        Lat, Lon = self.input_resolution
        B, L, C = x.shape

        shortcut = x
        x = self.norm1(x)
        x = rearrange(x, 'b (lat lon) c -> b lat lon c', lat=Lat, lon=Lon)

        # Pad
        x = rearrange(x, 'b lat lon c -> b c lat lon')
        x = self.pad(x)
        _, _, Lat_pad, Lon_pad = x.shape
        x = rearrange(x, 'b c lat lon -> b lat lon c')

        # Cyclic shift
        if self.shift_size[0] > 0:
            shifted_x = torch.roll(x, shifts=tuple(-s for s in self.shift_size), dims=(1, 2))
        else:
            shifted_x = x

        # Partition windows
        x_windows = window_partition(shifted_x, self.window_size, ndim=2)

        # W-MSA
        attn_windows = self.attn(x_windows)

        # Merge windows
        shifted_x = window_reverse(attn_windows, self.window_size, Lat=Lat_pad, Lon=Lon_pad, ndim=2)

        # Reverse cyclic shift
        if self.shift_size[0] > 0:
            x = torch.roll(shifted_x, shifts=self.shift_size, dims=(1, 2))
        else:
            x = shifted_x

        # Crop
        x = rearrange(x, 'b lat lon c -> b c lat lon')
        x = crop2d(x, self.input_resolution)
        x = rearrange(x, 'b c lat lon -> b (lat lon) c')

        # FFN
        x = shortcut + self.drop_path(x)
        x = x + self.drop_path(self.mlp(self.norm2(x)))

        return x


class DropPath(nn.Module):
    """Drop paths (Stochastic Depth)"""
    def __init__(self, drop_prob=0.):
        super(DropPath, self).__init__()
        self.drop_prob = drop_prob

    def forward(self, x):
        if self.drop_prob == 0. or not self.training:
            return x
        keep_prob = 1 - self.drop_prob
        shape = (x.shape[0],) + (1,) * (x.ndim - 1)
        random_tensor = keep_prob + torch.rand(shape, dtype=x.dtype, device=x.device)
        random_tensor.floor_()
        output = x.div(keep_prob) * random_tensor
        return output


class Mlp(nn.Module):
    """MLP层"""
    def __init__(self, in_features, hidden_features=None, out_features=None, drop=0.):
        super().__init__()
        out_features = out_features or in_features
        hidden_features = hidden_features or in_features
        self.fc1 = nn.Linear(in_features, hidden_features)
        self.act = nn.GELU()
        self.fc2 = nn.Linear(hidden_features, out_features)
        self.drop = nn.Dropout(drop)

    def forward(self, x):
        x = self.fc1(x)
        x = self.act(x)
        x = self.drop(x)
        x = self.fc2(x)
        x = self.drop(x)
        return x


class DownSample3D(nn.Module):
    """3D下采样模块"""
    def __init__(self, in_dim, input_resolution, output_resolution):
        super().__init__()
        self.linear = nn.Linear(in_dim * 4, in_dim * 2, bias=False)
        self.norm = nn.LayerNorm(4 * in_dim)
        self.input_resolution = input_resolution
        self.output_resolution = output_resolution

        in_pl, in_lat, in_lon = input_resolution
        out_pl, out_lat, out_lon = output_resolution

        h_pad = out_lat * 2 - in_lat
        w_pad = out_lon * 2 - in_lon

        pad_top = h_pad // 2
        pad_bottom = h_pad - pad_top
        pad_left = w_pad // 2
        pad_right = w_pad - pad_left

        self.pad = nn.ConstantPad3d((pad_left, pad_right, pad_top, pad_bottom, 0, 0), 0)

    def forward(self, x):
        B, L, C = x.shape
        in_pl, in_lat, in_lon = self.input_resolution
        out_pl, out_lat, out_lon = self.output_resolution

        x = rearrange(x, 'b (pl lat lon) c -> b pl lat lon c', pl=in_pl, lat=in_lat, lon=in_lon)

        # Pad and downsample
        x = rearrange(x, 'b pl lat lon c -> b c pl lat lon')
        x = self.pad(x)
        x = rearrange(x, 'b c pl lat lon -> b pl lat lon c')

        x = rearrange(x, 'b pl (h p1) (w p2) c -> b pl h w (p1 p2 c)',
                     p1=2, p2=2, h=out_lat, w=out_lon)
        x = x.reshape(B, out_pl * out_lat * out_lon, 4 * C)

        x = self.norm(x)
        x = self.linear(x)

        return x


class UpSample3D(nn.Module):
    """3D上采样模块"""
    def __init__(self, in_dim, out_dim, input_resolution, output_resolution):
        super().__init__()
        self.linear1 = nn.Linear(in_dim, out_dim * 4, bias=False)
        self.linear2 = nn.Linear(out_dim, out_dim, bias=False)
        self.norm = nn.LayerNorm(out_dim)
        self.input_resolution = input_resolution
        self.output_resolution = output_resolution

    def forward(self, x):
        B, L, C = x.shape
        in_pl, in_lat, in_lon = self.input_resolution
        out_pl, out_lat, out_lon = self.output_resolution

        x = self.linear1(x)
        x = x.reshape(B, in_pl, in_lat, in_lon, -1)

        # PixelShuffle-like upsampling
        x = rearrange(x, 'b pl h w (p1 p2 c) -> b pl (h p1) (w p2) c', p1=2, p2=2)

        # Crop to target resolution
        pad_h = in_lat * 2 - out_lat
        pad_w = in_lon * 2 - out_lon
        pad_top = pad_h // 2
        pad_bottom = pad_h - pad_top
        pad_left = pad_w // 2
        pad_right = pad_w - pad_left

        x = x[:, :out_pl, pad_top:2*in_lat-pad_bottom, pad_left:2*in_lon-pad_right, :]
        x = x.reshape(B, out_pl * out_lat * out_lon, -1)

        x = self.norm(x)
        x = self.linear2(x)

        return x


class FuserLayer(nn.Module):
    """融合层 - 处理3D特征"""
    def __init__(self, dim, input_resolution, depth, num_heads, window_size,
                 mlp_ratio=4., qkv_bias=True, drop=0., attn_drop=0., drop_path=0.):
        super().__init__()
        self.dim = dim
        self.input_resolution = input_resolution
        self.depth = depth

        self.blocks = nn.ModuleList([
            Transformer3DBlock(
                dim=dim,
                input_resolution=input_resolution,
                num_heads=num_heads,
                window_size=window_size,
                shift_size=(0, 0, 0) if i % 2 == 0 else None,
                mlp_ratio=mlp_ratio,
                qkv_bias=qkv_bias,
                drop=drop,
                attn_drop=attn_drop,
                drop_path=drop_path[i] if isinstance(drop_path, list) else drop_path
            ) for i in range(depth)
        ])

    def forward(self, x):
        for blk in self.blocks:
            x = blk(x)
        return x


# ==================== 主模型 ====================
class OceanPangu2(BaseModel):
    """
    Pangu2 - 2D+3D混合版本
    将2D数据同时输入到2D和3D处理路径，融合两种特征
    """
    def __init__(self, args):
        super(BaseModel, self).__init__()

        # 任务参数
        self.input_len = args.get('input_len', 7)
        self.output_len = args.get('output_len', 1)
        self.in_channels = args.get('in_channels', 2)

        # 模型参数
        img_size = args.get('img_size', (240, 240))
        patch_size = args.get('patch_size', (2, 4, 4))  # 3D patch size
        patch_size_2d = patch_size[1:]  # 2D patch size
        embed_dim = args.get('embed_dim', 192)
        num_heads = args.get('num_heads', (6, 12, 12, 6))
        window_size = args.get('window_size', (2, 6, 12))  # 3D window
        window_size_2d = window_size[1:]  # 2D window
        drop_path_rate = args.get('drop_path_rate', 0.2)

        # 时序维度作为伪3D的深度维度
        # 确保能被 patch_size[0] 整除
        self.pseudo_3d_depth = 8 if self.input_len > 4 else 4  # 使用能被2整除的值

        # 时序嵌入
        self.temporal_embed = nn.Conv2d(
            self.input_len * self.in_channels,
            embed_dim // 2,
            kernel_size=1
        )

        # 2D和3D Patch Embedding
        self.patch_embed_2d = PatchEmbed2D(
            img_size=img_size,
            patch_size=patch_size_2d,
            in_chans=embed_dim // 2,
            embed_dim=embed_dim
        )

        self.patch_embed_3d = PatchEmbed3D(
            img_size=(self.pseudo_3d_depth, img_size[0], img_size[1]),
            patch_size=patch_size,
            in_chans=embed_dim // 2,
            embed_dim=embed_dim
        )

        # 计算patch后的分辨率
        patched_shape = (
            self.pseudo_3d_depth // patch_size[0],
            img_size[0] // patch_size[1],
            img_size[1] // patch_size[2]
        )
        patched_shape_2d = patched_shape[1:]

        # Drop path
        drop_path = np.linspace(0, drop_path_rate, 8).tolist()

        # ========== 3D处理路径 ==========
        # Layer 1 - 3D Fuser
        self.layer3d_1 = FuserLayer(
            dim=embed_dim,
            input_resolution=patched_shape,
            depth=2,
            num_heads=num_heads[0],
            window_size=window_size,
            drop_path=drop_path[:2]
        )

        # Downsample
        patched_shape_down = (
            patched_shape[0],
            patched_shape[1] // 2,
            patched_shape[2] // 2
        )
        self.downsample_3d = DownSample3D(
            embed_dim, patched_shape, patched_shape_down
        )

        # Layer 2 & 3 - 3D Fuser (低分辨率)
        self.layer3d_2 = FuserLayer(
            dim=embed_dim * 2,
            input_resolution=patched_shape_down,
            depth=6,
            num_heads=num_heads[1],
            window_size=window_size,
            drop_path=drop_path[2:]
        )

        self.layer3d_3 = FuserLayer(
            dim=embed_dim * 2,
            input_resolution=patched_shape_down,
            depth=6,
            num_heads=num_heads[2],
            window_size=window_size,
            drop_path=drop_path[2:]
        )

        # Upsample
        self.upsample_3d = UpSample3D(
            embed_dim * 2, embed_dim, patched_shape_down, patched_shape
        )

        # Layer 4 - 3D Fuser
        self.layer3d_4 = FuserLayer(
            dim=embed_dim,
            input_resolution=patched_shape,
            depth=2,
            num_heads=num_heads[3],
            window_size=window_size,
            drop_path=drop_path[:2]
        )

        # ========== 2D处理路径 ==========
        # 2D Transformer blocks
        self.layers_2d = nn.ModuleList()
        for i in range(4):
            self.layers_2d.append(
                Transformer2DBlock(
                    dim=embed_dim,
                    input_resolution=patched_shape_2d,
                    num_heads=num_heads[0] if i < 2 else num_heads[3],
                    window_size=window_size_2d,
                    shift_size=(0, 0) if i % 2 == 0 else tuple(w//2 for w in window_size_2d),
                    mlp_ratio=4.,
                    qkv_bias=True,
                    drop=0.,
                    attn_drop=0.,
                    drop_path=drop_path[i % len(drop_path)]
                )
            )

        # ========== 特征融合和输出 ==========
        # 特征融合
        self.fusion = nn.Linear(embed_dim * 3, embed_dim * 2)  # 3D skip + 3D output + 2D output

        # Patch Recovery
        self.patch_recovery_2d = PatchRecovery2D(
            img_size, patch_size_2d, embed_dim * 2, self.output_len * self.in_channels
        )

        self.norm = nn.LayerNorm(embed_dim)

    def forward(self, x):
        """
        输入: (B, T_in, C, H, W)
        输出: (B, T_out, C, H, W)
        """
        B, T_in, C, H, W = x.shape

        # 时序融合: (B, T_in, C, H, W) -> (B, T_in*C, H, W)
        x_flat = rearrange(x, 'b t c h w -> b (t c) h w')
        x_embed = self.temporal_embed(x_flat)

        # ========== 3D路径 ==========
        # 为3D路径创建伪3D数据: (B, C', H, W) -> (B, C', D, H, W)
        # 通过在深度维度上复制来创建伪3D
        x_3d = x_embed.unsqueeze(2).repeat(1, 1, self.pseudo_3d_depth, 1, 1)

        # 3D Patch Embedding
        x_3d = self.patch_embed_3d(x_3d)  # (B, C, D', H', W')
        _, C3d, D, Hp, Wp = x_3d.shape
        x_3d = rearrange(x_3d, 'b c d h w -> b (d h w) c')

        # 3D Processing
        x_3d = self.layer3d_1(x_3d)
        x_3d_skip = x_3d  # Skip connection

        x_3d = self.downsample_3d(x_3d)
        x_3d = self.layer3d_2(x_3d)
        x_3d = self.layer3d_3(x_3d)
        x_3d = self.upsample_3d(x_3d)
        x_3d = self.layer3d_4(x_3d)

        # ========== 2D路径 ==========
        # 2D Patch Embedding
        x_2d = self.patch_embed_2d(x_embed)  # (B, C, H', W')
        x_2d = rearrange(x_2d, 'b c h w -> b (h w) c')

        # 2D Processing
        for blk in self.layers_2d:
            x_2d = blk(x_2d)

        # ========== 特征融合 ==========
        # 将3D特征投影回2D空间
        x_3d_proj = x_3d.reshape(B, D, Hp * Wp, -1).mean(dim=1)  # 在深度维度上平均
        x_3d_skip_proj = x_3d_skip.reshape(B, D, Hp * Wp, -1).mean(dim=1)

        # 规范化
        x_2d = self.norm(x_2d)
        x_3d_proj = self.norm(x_3d_proj)
        x_3d_skip_proj = self.norm(x_3d_skip_proj)

        # 拼接所有特征
        x_combined = torch.cat([x_2d, x_3d_proj, x_3d_skip_proj], dim=-1)

        # 融合
        x_fused = self.fusion(x_combined)

        # Reshape for patch recovery
        x_fused = x_fused.transpose(1, 2).reshape(B, -1, Hp, Wp)

        # Patch Recovery
        output = self.patch_recovery_2d(x_fused)

        # Reshape: (B, T_out*C, H, W) -> (B, T_out, C, H, W)
        output = rearrange(output, 'b (t c) h w -> b t c h w', t=self.output_len, c=C)

        return output



class OceanPangu2Autoregressive(OceanPangu2):
    """Autoregressive version of OceanPangu2 for long-term prediction.
    Uses single-frame prediction and rolls out for multiple steps.
    """

    def __init__(self, args):
        # Force single frame output for autoregressive mode
        args_auto = dict(args)
        args_auto["output_len"] = 1
        super().__init__(args_auto)

        self.rollout_steps = args.get("rollout_steps", 1)

    def forward(self, x, rollout_steps=None):
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

        # Stack predictions
        output = torch.cat(predictions, dim=1)  # [B, rollout_steps, C, H, W]
        return output

