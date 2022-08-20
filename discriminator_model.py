import torch
import torch.nn as nn


class CNNBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride) -> None:
        super(CNNBlock, self).__init__()
        
        self.conv = nn.Sequential(
            nn.Conv2d(
                in_channels, out_channels, 4, stride, bias=False, padding_mode='reflect'
            ),
            nn.BatchNorm2d(out_channels),
            nn.LeakyReLU(0.2)
        )

    def forward(self, x):
        return self.conv(x)

class Discriminator(nn.Module):
    def __init__(self, in_channels=3, features=[64, 128, 256, 512]) -> None:
        super().__init__()

        self.initial = nn.Sequential(
            nn.Conv2d(
                in_channels * 2, # Input is both x and y
                features[0],
                kernel_size=4,
                stride=2,
                padding=1,
                padding_mode='reflect'
            ),
            nn.LeakyReLU(0.2)
        )

        layers = []
        in_channels = features[0]

        for feature in features[1:]:
            layers.append(
                CNNBlock(in_channels, feature, stride=1 if feature == features[-1] else 2) # different stride for last feature size
            )
            in_channels = feature

        layers.append(
            nn.Conv2d(
                in_channels, 1, kernel_size=4, stride=1, padding=1, padding_mode='reflect'
            )
        )

        self.model = nn.Sequential(*layers) # unpack all layers

    def forward(self, x, y):
        x = torch.cat([x,y], dim=1)
        x = self.initial(x)
        x = self.model(x)
        return x

def test():
    x = torch.randn((1, 3, 256, 256))
    y = torch.randn((1, 3, 256, 256))
    model = Discriminator(in_channels=3)
    preds = model(x, y)
    print(model)
    print(preds.shape)


if __name__ == "__main__":
    test()