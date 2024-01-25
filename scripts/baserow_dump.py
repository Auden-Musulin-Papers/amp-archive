import requests
import shutil
import os
import zipfile
import glob
from config import (
    br_client,
    BASEROW_DB_ID,
    MAPPING_PROJECT,
    MAPPING_PERSONS,
    MAPPING_ORGS,
    MAPPING_PLACES,
    LATEST_RELEASE,
    PRIMARY_DATA_DIRECTORY,
    PRMARY_FILE_FORMAT,
    ADDITIONAL_RESOURCES,
    ADDITIONAL_DATA_DIRECTORY,
    ADDITIONAL_FILE_FORMAT
)
from utils.denormalize import denormalize_json

if isinstance(BASEROW_DB_ID, str) or isinstance(BASEROW_DB_ID, int) and BASEROW_DB_ID != 0:
    print("Downloading data from Baserow...")
    files = br_client.dump_tables_as_json(BASEROW_DB_ID, folder_name="json_dumps", indent=2)
    print("Data downloaded.")

    print("Denormalizing data...")
    denormalize_json("Project", "json_dumps", MAPPING_PROJECT)
    denormalize_json("Persons", "json_dumps", MAPPING_PERSONS)
    denormalize_json("Organizations", "json_dumps", MAPPING_ORGS)
    denormalize_json("Places", "json_dumps", MAPPING_PLACES)
    print("Data denormalized.")


def download_resources(
    url: str = LATEST_RELEASE,
    dir: str = PRIMARY_DATA_DIRECTORY,
    file_format: str = PRMARY_FILE_FORMAT,
    to_dir: str = "editions"
) -> None:
    if isinstance(url, str) and len(url) != 0:
        print("Downloading data from resources...")
        # create graph for resources
        # open xml files
        if isinstance(dir, str) and len(dir) > 0:
            dir = dir
        else:
            dir = "*"
        if isinstance(file_format, str) and len(file_format) > 0:
            file_format = file_format.lower()
        else:
            file_format = "xml"
        r = requests.get(url)
        with open("resources.zip", "wb") as f:
            f.write(r.content)

        shutil.rmtree("tmp", ignore_errors=True)
        os.makedirs("tmp", exist_ok=True)
        with zipfile.ZipFile("resources.zip", "r") as zip_ref:
            zip_ref.extractall("tmp")

        data_path = glob.glob(f"tmp/*/{dir}/*.{file_format}")
        shutil.rmtree(f"data/{dir.split('/')[-1]}", ignore_errors=True)
        os.makedirs("data", exist_ok=True)
        os.makedirs(f"data/{to_dir}", exist_ok=True)
        for x in data_path:
            if os.path.isdir(x):
                shutil.copytree(x, f"data/{to_dir}")
            elif os.path.isfile(x) and x.endswith(file_format):
                shutil.copy(x, f"data/{to_dir}")
        shutil.rmtree("tmp", ignore_errors=True)
        os.remove("resources.zip")
        print("Data from Resources downloaded.")


download_resources(LATEST_RELEASE, PRIMARY_DATA_DIRECTORY, PRMARY_FILE_FORMAT, "editions")
download_resources(ADDITIONAL_RESOURCES, ADDITIONAL_DATA_DIRECTORY, ADDITIONAL_FILE_FORMAT, "indexes")
