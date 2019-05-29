import os
from pydicom.filereader import dcmread
from pprint import pprint
import numpy as np
from PIL import Image
import pandas as pd
from tqdm import tqdm

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
    for folder in folders:
        nested = sorted(os.listdir(f"{path}/{folder}"))
        for key in nested:
            for imgs in os.listdir(f"{path}/{folder}/{key}/{key.split('_')[-1]}/CT/"):
                data = {
                    "patient_id": [],
                    "slice_id": [],
                    "x": [],
                    "y": [],
                    "intensity": [],
                    "label": [],
                }

                for idx, img in enumerate(
                    os.listdir(f"{path}/{folder}/{key}/{key.split('_')[-1]}/CT/{imgs}")[
                        40:80
                    ]
                ):
                    if img[::-1][:4] == "mcd.":
                        dcm = dcmread(
                            f"{path}/{folder}/{key}/{key.split('_')[-1]}/CT/{imgs}/{img}"
                        )
                        dcm = dcm.pixel_array.astype(np.uint16)
                        rgb = to_rgb(dcm).astype(np.uint8)
                        im = Image.fromarray(rgb)
                        rgb = np.array(im.resize((256, 256)))

                        for x in range(256):
                            for y in range(256):
                                data = create_row(
                                    data=data,
                                    patient_id=key.split("_")[-1],
                                    slice_id=f"{imgs}-{img}",
                                    x=x,
                                    y=y,
                                    intesity=rgb[x][y],
                                )
                        print(f"Image {idx} was processed.")
                create_csv(data=data, patient_id=key.split("_")[-1], folder=folder)


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


def create_csv(data: dict, patient_id: str, folder: str):
    df = pd.DataFrame(data)
    df.to_csv(f"patientId-{patient_id}-{folder}.csv")
    print(f"File 'patientId-{patient_id}-{folder}.csv' was processed.")


if __name__ == "__main__":
    data = process_dataset()
