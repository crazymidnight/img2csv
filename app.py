import os
from pydicom.filereader import dcmread
from pprint import pprint
import numpy as np
from PIL import Image

LUNG_MODE = {"left": -164, "right": 712}
ROOT_PATH = "../../../diploma/medical_data"
DATA_PATH = (
    "Disseminated_TB",
    "Fibroso_Cavernous_TB",
    "Focal_TB",
    "Infiltrative_TB",
    "Tuberculoma",
)

# TODO: разобрать эту жесть и сделать исключение не dcm-файлов
def process_dataset(path: str = ROOT_PATH, folders: tuple = DATA_PATH) -> dict:
    data = {folder: None for folder in folders}
    
    for folder in folders:
        if not os.path.exists(f"../data/{folder}"):
            os.mkdir(f"../data/{folder}/")
        nested = sorted(os.listdir(f"{path}/{folder}"))
        for key in nested:
            if not os.path.exists(f"../data/{folder}/{key}/{key.split('_')[-1]}"):
                os.mkdir(f"../data/{folder}/{key}/{key.split('_')[-1]}")
            for img in os.listdir(f"{path}/{folder}/{key}/{key.split('_')[-1]}/CT/"):
                if not os.path.exists(f"../data/{folder}/{key}/{key.split('_')[-1]}/CT/"):
                    os.mkdir(f"../data/{folder}/{key}/{key.split('_')[-1]}/CT/")
                for x in os.listdir(
                    f"{path}/{folder}/{key}/{key.split('_')[-1]}/CT/{img}"
                ):
                    if x[::-1][:4] == "mcd.":
                        dcm = dcmread(
                            f"{path}/{folder}/{key}/{key.split('_')[-1]}/CT/{img}/{x}"
                        )
                        dcm = dcm.pixel_array.astype(np.uint16)
                        rgb = to_rgb(dcm)
                        im = Image.fromarray(rgb)
                        im.save(
                            f"../data/{folder}/{key}/{key.split('_')[-1]}/CT/{img}.png",
                            format="png",
                        )


# Convert dicom to rgb
def to_rgb(img: np.array) -> np.array:

    img[img < LUNG_MODE["left"]] = LUNG_MODE["left"]
    img[img > LUNG_MODE["right"]] = LUNG_MODE["right"]

    rgb = (img - LUNG_MODE["left"]) / (LUNG_MODE["right"] - LUNG_MODE["left"]) * 255
    return rgb.astype(np.uint8)


def create_csv():
    pass


if __name__ == "__main__":
    process_dataset()
