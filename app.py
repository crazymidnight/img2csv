import os
from pydicom.filereader import dcmread
from pprint import pprint
import numpy as np
from PIL import Image
import pandas as pd

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
    data = {
        "patient_id": [],
        "slice_id": [],
        "x": [],
        "y": [],
        "intensity": [],
        "label": [],
    }

    for folder in folders:
        if not os.path.exists(f"../data/{folder}"):
            os.makedirs(f"../data/{folder}/")
        nested = sorted(os.listdir(f"{path}/{folder}"))
        for key in nested:
            if not os.path.exists(f"../data/{folder}/{key}/{key.split('_')[-1]}"):
                os.makedirs(f"../data/{folder}/{key}/{key.split('_')[-1]}")
            for imgs in os.listdir(f"{path}/{folder}/{key}/{key.split('_')[-1]}/CT/"):
                if not os.path.exists(
                    f"../data/{folder}/{key}/{key.split('_')[-1]}/CT/"
                ):
                    os.makedirs(f"../data/{folder}/{key}/{key.split('_')[-1]}/CT/")
                for img in os.listdir(
                    f"{path}/{folder}/{key}/{key.split('_')[-1]}/CT/{imgs}"
                ):
                    if img[::-1][:4] == "mcd.":
                        dcm = dcmread(
                            f"{path}/{folder}/{key}/{key.split('_')[-1]}/CT/{imgs}/{img}"
                        )
                        dcm = dcm.pixel_array.astype(np.uint16)
                        rgb = to_rgb(dcm)

                        for x in range(512):
                            for y in range(512):
                                data = create_row(
                                    data=data,
                                    patient_id=key.split("_")[-1],
                                    slice_id=f"{imgs}-{img}",
                                    x=x,
                                    y=y,
                                    intesity=rgb[x][y],
                                )
    return data


# Convert dicom to rgb
def to_rgb(img: np.array) -> np.array:

    img[img < LUNG_MODE["left"]] = LUNG_MODE["left"]
    img[img > LUNG_MODE["right"]] = LUNG_MODE["right"]

    rgb = (img - LUNG_MODE["left"]) / (LUNG_MODE["right"] - LUNG_MODE["left"]) * 255
    return rgb.astype(np.uint8)


def create_row(data, patient_id, slice_id, x, y, intesity):
    data["patient_id"].append(patient_id)
    data["slice_id"].append(slice_id)
    data["x"].append(x)
    data["y"].append(y)
    data["intensity"].append(intesity)
    data["label"].append(0)
    return data


def create_csv():
    pass


if __name__ == "__main__":
    data = process_dataset()
    df = pd.DataFrame(data)
    df.to_cvs("data.csv")
