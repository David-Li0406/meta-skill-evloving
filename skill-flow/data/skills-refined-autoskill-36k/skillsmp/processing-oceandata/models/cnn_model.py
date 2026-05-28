import torch
import torch.nn as nn
from einops import rearrange
from .base import BaseModel


class PatchEmbed(nn.Module):
    """Patch embedding layer: b t c h w -> b t (c*p*p) (h/p) (w/p)"""
    def __init__(self, patch_size=1):
        super().__init__()
        self.patch_size = patch_size

    def forward(self, x):
        """
        x: (B, T, C, H, W)
        return: (B, T, C*P*P, H/P, W/P)
        """
        if self.patch_size == 1:
            return x

        return rearrange(
            x,
            'b t c (h p1) (w p2) -> b t (c p1 p2) h w',
            p1=self.patch_size,
            p2=self.patch_size
        )

    def reverse(self, x, out_channels):
        """
        Reverse patch embedding
        x: (B, T, C*P*P, H, W)
        return: (B, T, out_channels, H*P, W*P)
        """
        if self.patch_size == 1:
            return x

        return rearrange(
            x,
            'b t (c p1 p2) h w -> b t c (h p1) (w p2)',
            c=out_channels,
            p1=self.patch_size,
            p2=self.patch_size
        )


class OceanCNN(BaseModel):
    """
    Basic CNN model for ocean velocity prediction (baseline)
    Pure encoder-decoder architecture without temporal modeling

    Process: Concatenate input frames -> Encoder -> Decoder -> Output frame
    Input: (B, T_in, C, H, W) -> (B, T_in*C, H, W)
    Output: (B, T_out, C, H, W)
    """
    def __init__(self, args):
        super(BaseModel, self).__init__()

        self.input_len = args.get('input_len', 7)
        self.output_len = args.get('output_len', 1)
        self.in_channels = args.get('in_channels', 2)  # u and v components

        # Calculate input channels after concatenating temporal frames
        input_channels = self.input_len * self.in_channels

        # Encoder: Basic convolutional layers with pooling
        self.encoder = nn.Sequential(
            # Block 1: input_channels -> 64
            nn.Conv2d(input_channels, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # H/2, W/2

            # Block 2: 64 -> 128
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # H/4, W/4

            # Block 3: 128 -> 256
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # H/8, W/8
        )

        # Decoder: Upsampling with transposed convolutions
        self.decoder = nn.Sequential(
            # Block 1: 256 -> 128
            nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2),  # H/4, W/4
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),

            # Block 2: 128 -> 64
            nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2),  # H/2, W/2
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),

            # Block 3: 64 -> output_channels
            nn.ConvTranspose2d(64, 32, kernel_size=2, stride=2),  # H, W
            nn.Conv2d(32, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, self.output_len * self.in_channels, kernel_size=3, padding=1),
        )

    def forward(self, x):
        """
        x: (B, T_in, C, H, W)
        return: (B, T_out, C, H, W)
        """
        B, T_in, C, H, W = x.shape

        # Concatenate temporal frames along channel dimension
        # (B, T_in, C, H, W) -> (B, T_in*C, H, W)
        x = x.reshape(B, T_in * C, H, W)

        # Encoder
        encoded = self.encoder(x)  # (B, 256, H/8, W/8)

        # Decoder
        decoded = self.decoder(encoded)  # (B, T_out*C, H, W)

        # Reshape to output format
        # (B, T_out*C, H, W) -> (B, T_out, C, H, W)
        output = decoded.reshape(B, self.output_len, C, H, W)

        return output
