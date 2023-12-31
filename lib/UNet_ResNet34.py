import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
import timm
from timm.models import ConvNeXt


class DecoderBlock(nn.Module):
    def __init__(self,
                 in_channels=512,
                 n_filters=256,
                 kernel_size=3,
                 is_deconv=False,
                 ):
        super().__init__()
        if kernel_size == 3:
            conv_padding = 1
        elif kernel_size == 1:
            conv_padding = 0
        # B, C, H, W -> B, C/4, H, W
        self.conv1 = nn.Conv2d(in_channels,
                               in_channels // 4,
                               kernel_size,
                               padding=1,bias=False)
        self.norm1 = nn.BatchNorm2d(in_channels // 4)
        self.relu1 = nn.ReLU(inplace=True)
        # B, C/4, H, W -> B, C, H, W
        self.conv2 = nn.Conv2d(in_channels // 4,
                               n_filters,
                               kernel_size,
                               padding=conv_padding,bias=False)
        self.norm2 = nn.BatchNorm2d(n_filters)
        self.relu2 = nn.ReLU(inplace=True)
        if is_deconv == True:
            self.deconv = nn.ConvTranspose2d(in_channels // 4,
                                              in_channels // 4,
                                              3,
                                              stride=2,
                                              padding=1,
                                              output_padding=conv_padding,bias=False)
        else:
            self.deconv = nn.Upsample(scale_factor=2)
    def forward(self, x):

        x = self.conv1(x)
        x = self.norm1(x)
        x = self.relu1(x)

        x = self.conv2(x)
        x = self.norm2(x)
        x = self.relu2(x)

        x = self.deconv(x)

        return x
    
class BasicConv2d(nn.Module):
    def __init__(self, in_planes, out_planes, kernel_size, stride, padding=0):
        super(BasicConv2d, self).__init__()
        self.conv = nn.Conv2d(in_planes, out_planes,
                              kernel_size=kernel_size, stride=stride,
                              padding=padding, bias=False)  # verify bias false
        self.bn = nn.BatchNorm2d(out_planes)
        self.relu = nn.ReLU(inplace=False)
    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        return x


class ResNet34Unet(nn.Module):
    def __init__(self,
                 num_classes=1,
                 num_channels=3,
                 is_deconv=False,
                 decoder_kernel_size=3,
                 pretrained=True
                 ):
        super().__init__()

        filters = [96, 192, 384, 768]
        self.filters = filters
        
        self.convnext = timm.create_model('convnext_tiny', features_only=True, out_indices=(0,1,2,3), pretrained=True)

 
        # Decoder
        self.center = DecoderBlock(in_channels=filters[3],
                                   n_filters=filters[3],
                                   kernel_size=decoder_kernel_size,
                                   is_deconv=is_deconv)
        self.decoder4 = DecoderBlock(in_channels=filters[2],
                                     n_filters=filters[2],
                                     kernel_size=decoder_kernel_size,
                                     is_deconv=is_deconv)
        self.decoder3 = DecoderBlock(in_channels=filters[1],
                                     n_filters=filters[1],
                                     kernel_size=decoder_kernel_size,
                                     is_deconv=is_deconv)
        self.decoder2 = DecoderBlock(in_channels=filters[0],
                                     n_filters=filters[0],
                                     kernel_size=decoder_kernel_size,
                                     is_deconv=is_deconv)
        self.decoder1 = DecoderBlock(in_channels=filters[0] + 96,
                                     n_filters=filters[0],
                                     kernel_size=decoder_kernel_size,
                                     is_deconv=is_deconv)
 
 
        self.finalconv1 = nn.Sequential(nn.Conv2d(filters[0], 48, 3, padding=1, bias=False),
                                       nn.BatchNorm2d(48),
                                       nn.ReLU(),
                                       nn.Dropout2d(0.1, False),
                                       nn.Conv2d(48, num_classes, 1))
        self.finalconv2 = nn.Sequential(nn.Conv2d(filters[0], 48, 3, padding=1, bias=False),
                                       nn.BatchNorm2d(48),
                                       nn.ReLU(),
                                       nn.Dropout2d(0.1, False),
                                       nn.Conv2d(48, num_classes, 1))
        self.finalconv3 = nn.Sequential(nn.Conv2d(filters[1], 48, 3, padding=1, bias=False),
                                       nn.BatchNorm2d(48),
                                       nn.ReLU(),
                                       nn.Dropout2d(0.1, False),
                                       nn.Conv2d(48, num_classes, 1))
        self.finalconv4 = nn.Sequential(nn.Conv2d(filters[2], 48, 3, padding=1, bias=False),
                                       nn.BatchNorm2d(48),
                                       nn.ReLU(),
                                       nn.Dropout2d(0.1, False),
                                       nn.Conv2d(48, num_classes, 1))
 
    def forward(self, x):


        e = self.convnext(x)

        e1 = e[0]
        e2 = e[1]
        e3 = e[2]
        e4 = e[3]
 
        center = self.center(e4)
 
        d4 = self.decoder4(torch.cat([center, e3], 1))
        d3 = self.decoder3(torch.cat([d4, e2], 1))
        d2 = self.decoder2(torch.cat([d3, e1], 1))
        d1 = self.decoder1(torch.cat([d2, x], 1))
 
        f1 = self.finalconv1(d1)
        f2 = self.finalconv2(d2)
        f3 = self.finalconv3(d3)
        f4 = self.finalconv4(d4)
        f4 = F.interpolate(f4, scale_factor=8, mode='bilinear', align_corners=True)
        f3 = F.interpolate(f3, scale_factor=4, mode='bilinear', align_corners=True)
        f2 = F.interpolate(f2, scale_factor=2, mode='bilinear', align_corners=True)
        return f4, f3, f2, f1
if __name__ == "__main__":
    model = ResNet34Unet()