from PIL import Image
import os
import numpy as np
import config
from torch.utils.data import Dataset, DataLoader
from torchvision.utils import save_image

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

        augmentations = config.both_transform(image=input_image, image0=target_image)
        input_image, target_image = augmentations['image'], augmentations['image0']


        input_image = config.transform_only_input(image=input_image)["image"]
        target_image = config.transform_only_mask(image=target_image)["image"]

        return input_image, target_image 


    def __len__(self):
        return len(self.list_files)


if __name__ == "__main__":
    dataset = MapDataset("data/maps/train")
    loader = DataLoader(dataset, batch_size=1)

    for x, y in loader:
        print(x.shape)
        save_image(x, "x.png")
        save_image(y, "y.png")



