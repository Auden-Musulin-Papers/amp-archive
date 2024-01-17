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
    PRMARY_FILE_FORMAT
)
from utils.denormalize import denormalize_json

print("Downloading data from Baserow...")
files = br_client.dump_tables_as_json(BASEROW_DB_ID, folder_name="json_dumps", indent=2)
print("Data downloaded.")

print("Denormalizing data...")
denormalize_json("Project", "json_dumps", MAPPING_PROJECT)
denormalize_json("Persons", "json_dumps", MAPPING_PERSONS)
denormalize_json("Organizations", "json_dumps", MAPPING_ORGS)
denormalize_json("Places", "json_dumps", MAPPING_PLACES)
print("Data denormalized.")

print("Downloading data from resources...")
# create graph for resources
# open xml files
if isinstance(PRIMARY_DATA_DIRECTORY, str) and len(PRIMARY_DATA_DIRECTORY) > 0:
    dir = PRIMARY_DATA_DIRECTORY
else:
    dir = ""
if isinstance(PRMARY_FILE_FORMAT, str) and len(PRMARY_FILE_FORMAT) > 0:
    file_format = PRMARY_FILE_FORMAT
else:
    file_format = "xml"
r = requests.get(LATEST_RELEASE)
with open("resources.zip", "wb") as f:
    f.write(r.content)

shutil.rmtree("tmp", ignore_errors=True)
os.makedirs("tmp", exist_ok=True)
with zipfile.ZipFile("resources.zip", "r") as zip_ref:
    zip_ref.extractall("tmp")

data_path = glob.glob(f"tmp/*/{dir}/*.{file_format}")
shutil.rmtree("data", ignore_errors=True)
os.makedirs("data", exist_ok=True)
for file in data_path:
    shutil.copy(file, "data")
shutil.rmtree("tmp", ignore_errors=True)
os.remove("resources.zip")
print("Data from Resources downloaded.")
