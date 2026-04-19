# src/data/datamodule.py

import os
from glob import glob
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader

from .dataset import PlantVillageDataset
from .transforms import get_train_transforms, get_val_transforms

class PlantVillageDataModule:
    def __init__(
        self,
        data_dir,
        img_size=224,
        batch_size=32,
        num_workers=4,
        val_split=0.15,
        test_split=0.15,
        seed=42
    ):
        self.data_dir = data_dir
        self.img_size = img_size
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.val_split = val_split
        self.test_split = test_split
        self.seed = seed

        self.class_to_idx = {}
        self.idx_to_class = {}

    def setup(self):
        image_paths = []
        labels = []

        class_names = sorted(os.listdir(self.data_dir))
        self.class_to_idx = {cls: i for i, cls in enumerate(class_names)}
        self.idx_to_class = {i: cls for cls, i in self.class_to_idx.items()}

        for cls in class_names:
            cls_dir = os.path.join(self.data_dir, cls)
            imgs = glob(os.path.join(cls_dir, "*.jpg"))

            image_paths.extend(imgs)
            labels.extend([self.class_to_idx[cls]] * len(imgs))

        # Stratified split
        X_temp, X_test, y_temp, y_test = train_test_split(
            image_paths,
            labels,
            test_size=self.test_split,
            stratify=labels,
            random_state=self.seed
        )

        val_ratio_adjusted = self.val_split / (1 - self.test_split)

        X_train, X_val, y_train, y_val = train_test_split(
            X_temp,
            y_temp,
            test_size=val_ratio_adjusted,
            stratify=y_temp,
            random_state=self.seed
        )

        self.train_dataset = PlantVillageDataset(
            X_train, y_train, get_train_transforms(self.img_size)
        )
        self.val_dataset = PlantVillageDataset(
            X_val, y_val, get_val_transforms(self.img_size)
        )
        self.test_dataset = PlantVillageDataset(
            X_test, y_test, get_val_transforms(self.img_size)
        )

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=self.num_workers,
            pin_memory=True
        )

    def val_dataloader(self):
        return DataLoader(
            self.val_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            pin_memory=True
        )

    def test_dataloader(self):
        return DataLoader(
            self.test_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            pin_memory=True
        )
