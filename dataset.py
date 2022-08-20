import torch
from PIL import Image
import os
import numpy as np

from torch.utils.data import Dataset

class MapDataset(Dataset):
    def __init__(self, root_dir) -> None:
        super().__init__()
        self.root_dir = root_dir
        self.list_files = os.listdir(self.root_dir)

    def __getitem__(self, i):
        img_file = self.list_files[i]
        img_path = os.path.join(self.root_dir, img_file)

        image = np.array(Image.open(img_path))
        

        return 


    def __len__(self):
        return len(self.list_files)
