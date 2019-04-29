import os
from pydicom.filereader import dcmread
from pprint import pprint

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
def load_dataset(path: str = ROOT_PATH, folders: tuple = DATA_PATH) -> dict:
    data = {folder: None for folder in folders}
    for folder in folders:
        nested = sorted(os.listdir(f"{path}/{folder}"))
        data[folder] = {
            key: {
                img: {
                    [
                        dcmread(
                            f"{path}/{folder}/{key}/{key.split('_')[-1]}/CT/{img}/{x}"
                        )
                        for x in os.listdir(
                            f"{path}/{folder}/{key}/{key.split('_')[-1]}/CT/{img}"
                        )
                    ]
                }
                for img in os.listdir(f"{path}/{folder}/{key}/{key.split('_')[-1]}/CT/")
            }
            for key in nested
        }
    pprint(data)
    return data


def load_data(path=ROOT_PATH):
    files = sorted(os.listdir(path))
    print(f"files: {files}")
    for i in files:
        file = os.listdir(f"{path}{i}")
        print(file)


def create_csv():
    pass


if __name__ == "__main__":
    load_dataset()
