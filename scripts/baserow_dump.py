from config import br_client, BASEROW_DB_ID, MAPPING_PROJECT, MAPPING_PERSONS
from utils.denormalize import denormalize_json

files = br_client.dump_tables_as_json(BASEROW_DB_ID, folder_name="json_dumps", indent=2)

denormalize_json("Project", "json_dumps", MAPPING_PROJECT)
denormalize_json("Persons", "json_dumps", MAPPING_PERSONS)
