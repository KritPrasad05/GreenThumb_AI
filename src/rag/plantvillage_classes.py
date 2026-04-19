import os
from typing import List, Tuple


def extract_plantvillage_classes(dataset_root: str) -> List[Tuple[str, str]]:
    """
    Extract (crop, disease) pairs from PlantVillage directory structure.

    Args:
        dataset_root (str): Path to PlantVillage 'color' directory

    Returns:
        List of (crop, disease) tuples
    """
    classes = []

    if not os.path.isdir(dataset_root):
        raise FileNotFoundError(f"Dataset root not found: {dataset_root}")

    for class_name in os.listdir(dataset_root):
        class_path = os.path.join(dataset_root, class_name)

        if not os.path.isdir(class_path):
            continue

        # Expected format: Crop___Disease
        if "___" not in class_name:
            continue

        crop, disease = class_name.split("___", maxsplit=1)

        crop = (
            crop.replace("_", " ")
                .replace("(including sour)", "")
                .strip()
        )

        disease = disease.replace("_", " ").strip()

        classes.append((crop, disease))

    return classes
