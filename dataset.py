from PIL import Image
import os
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torchvision.utils import save_image
import albumentations as A
from albumentations.pytorch import ToTensorV2




both_transform = A.Compose(
    [A.Resize(width=256, height=256),], additional_targets={"image0": "image"},
)

transform_only_input = A.Compose(
    [
        A.HorizontalFlip(p=0.5),
        A.ColorJitter(p=0.2),
        A.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5], max_pixel_value=255.0,),
        ToTensorV2(),
    ]
)

transform_only_mask = A.Compose(
    [
        A.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5], max_pixel_value=255.0,),
        ToTensorV2(),
    ]
)

class MapDataset(Dataset):
    def __init__(self, root_dir) -> None:
        super().__init__()
        self.root_dir = root_dir
        self.list_files = os.listdir(self.root_dir)

    def __getitem__(self, i):
        img_file = self.list_files[i]
        img_path = os.path.join(self.root_dir, img_file)

        image = np.array(Image.open(img_path))

        input_image = image[:, :600, :] # For MapDataset image is 1200pxs in width
        target_image = image[:, 600:, :]

        augmentations = both_transform(image=input_image, image0=target_image)
        input_image, target_image = augmentations['image'], augmentations['image0']


        input_image = transform_only_input(image=input_image)["image"]
        target_image = transform_only_mask(image=target_image)["image"]

        return input_image, target_image 


    def __len__(self):
        return len(self.list_files)


if __name__ == "__main__":
    dataset = MapDataset("data/maps/maps/train")
    loader = DataLoader(dataset, batch_size=1, shuffle=True)

    for x, y in loader:
        print(x.shape)
        save_image(x, "x.png")
        save_image(y, "y.png")

        import sys
        sys.exit()

