import torch
import torch.nn as nn
from .base import BaseModel


class BasicBlock(nn.Module):
    """Basic ResNet block from original paper"""

    def __init__(self, in_channels, out_channels, stride=1, downsample=None):
        super().__init__()
        self.conv1 = nn.Conv2d(
            in_channels,
            out_channels,
            kernel_size=3,
            stride=stride,
            padding=1,
            bias=False,
        )
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(
            out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False
        )
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample

    def forward(self, x):
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)

        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)

        return out


class OceanResNet(BaseModel):
    """
    ResNet-based model for ocean velocity prediction (baseline)
    Standard ResNet-18 architecture with encoder-decoder structure

    Process: Concatenate input frames -> ResNet Encoder -> Decoder -> Output frame
    Input: (B, T_in, C, H, W) -> (B, T_in*C, H, W)
    Output: (B, T_out, C, H, W)
    """

    def __init__(self, args):
        super(BaseModel, self).__init__()

        self.input_len = args.get("input_len", 7)
        self.output_len = args.get("output_len", 1)
        self.in_channels = args.get("in_channels", 2)  # u and v components

        # Calculate input channels after concatenating temporal frames
        input_channels = self.input_len * self.in_channels

        # Encoder: Standard ResNet-18 architecture
        self.conv1 = nn.Conv2d(
            input_channels, 64, kernel_size=7, stride=2, padding=3, bias=False
        )
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        # ResNet layers (ResNet-18: [2, 2, 2, 2])
        self.layer1 = self._make_layer(64, 64, 2, stride=1)
        self.layer2 = self._make_layer(64, 128, 2, stride=2)
        self.layer3 = self._make_layer(128, 256, 2, stride=2)
        self.layer4 = self._make_layer(256, 512, 2, stride=2)

        # Decoder: Transpose convolutions to restore spatial dimensions
        self.decoder = nn.Sequential(
            # 512 -> 256
            nn.ConvTranspose2d(
                512, 256, kernel_size=3, stride=2, padding=1, output_padding=1
            ),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            # 256 -> 128
            nn.ConvTranspose2d(
                256, 128, kernel_size=3, stride=2, padding=1, output_padding=1
            ),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            # 128 -> 64
            nn.ConvTranspose2d(
                128, 64, kernel_size=3, stride=2, padding=1, output_padding=1
            ),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            # 64 -> 32
            nn.ConvTranspose2d(
                64, 32, kernel_size=3, stride=2, padding=1, output_padding=1
            ),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            # 32 -> output_channels
            nn.ConvTranspose2d(
                32,
                self.output_len * self.in_channels,
                kernel_size=7,
                stride=2,
                padding=3,
                output_padding=1,
            ),
        )

    def _make_layer(self, in_channels, out_channels, blocks, stride=1):
        """Create a layer with multiple BasicBlocks"""
        downsample = None
        if stride != 1 or in_channels != out_channels:
            downsample = nn.Sequential(
                nn.Conv2d(
                    in_channels, out_channels, kernel_size=1, stride=stride, bias=False
                ),
                nn.BatchNorm2d(out_channels),
            )

        layers = []
        layers.append(BasicBlock(in_channels, out_channels, stride, downsample))
        for _ in range(1, blocks):
            layers.append(BasicBlock(out_channels, out_channels))

        return nn.Sequential(*layers)

    def forward(self, x):
        """
        x: (B, T_in, C, H, W)
        return: (B, T_out, C, H, W)

        Shape transformations:
            Input: (B, T_in, C, H, W) e.g., (16, 7, 2, 240, 240)
            -> Concat: (B, T_in*C, H, W) e.g., (16, 14, 240, 240)
            -> Encoder: (B, 512, H/32, W/32) e.g., (16, 512, 8, 8)
            -> Decoder: (B, T_out*C, H', W') e.g., (16, 2, 256, 256)
            -> Resize: (B, T_out*C, H, W) e.g., (16, 2, 240, 240)
            -> Reshape: (B, T_out, C, H, W) e.g., (16, 1, 2, 240, 240)
        """
        B, T_in, C, H, W = x.shape

        # Concatenate temporal frames along channel dimension
        # (B, T_in, C, H, W) -> (B, T_in*C, H, W)
        x = x.reshape(B, T_in * C, H, W)

        # Encoder: Standard ResNet forward pass
        x = self.conv1(x)  # (B, 64, H/2, W/2)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)  # (B, 64, H/4, W/4)

        x = self.layer1(x)  # (B, 64, H/4, W/4)
        x = self.layer2(x)  # (B, 128, H/8, W/8)
        x = self.layer3(x)  # (B, 256, H/16, W/16)
        x = self.layer4(x)  # (B, 512, H/32, W/32)

        # Decoder
        decoded = self.decoder(x)  # (B, T_out*C, H', W') where H' may not equal H

        # Resize to match input spatial dimensions if needed
        # This handles cases where H, W are not multiples of 32
        if decoded.shape[2] != H or decoded.shape[3] != W:
            import torch.nn.functional as F

            decoded = F.interpolate(
                decoded, size=(H, W), mode="bilinear", align_corners=False
            )

        # Reshape to output format
        # (B, T_out*C, H, W) -> (B, T_out, C, H, W)
        # Use self.in_channels instead of C (which is from input shape)
        output = decoded.reshape(B, self.output_len, self.in_channels, H, W)

        return output

