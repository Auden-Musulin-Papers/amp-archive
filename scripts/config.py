import os
from acdh_baserow_pyutils import BaseRowClient

# Baserow config
BASEROW_DB_ID = os.environ.get("BASEROW_DB_ID")
BASEROW_URL = "https://baserow.acdh-dev.oeaw.ac.at/api/"
BASEROW_USER = os.environ.get("BASEROW_USER")
BASEROW_PW = os.environ.get("BASEROW_PW")
BASEROW_TOKEN = os.environ.get("BASEROW_TOKEN")
LATEST_RELEASE = os.environ.get("LATEST_RELEASE")
PRIMARY_DATA_DIRECTORY = os.environ.get("PRIMARY_DATA_DIRECTORY")
PRMARY_FILE_FORMAT = os.environ.get("PRIMARY_FILE_FORMAT")
PROJECT_NAME = os.environ.get("PROJECT_NAME")

# denormalize mapping
MAPPING_PROJECT = {
    "Class": "Classes.json",
    "Predicate_uri": "Properties.json",
    "Object_uri_persons": "Persons.json",
    "Object_uri_places": "Places.json",
    "Object_uri_organizations": "Organizations.json",
    "Object_uri_vocabs": "Vocabs.json"
}
MAPPING_PERSONS = {
    "Predicate_uri": "Properties.json",
    "Object_uri_organizations": "Organizations.json"
}
MAPPING_ORGS = {
    "Predicate_uri": "Properties.json"
}
MAPPING_PLACES = {
    "Predicate_uri": "Properties.json"
}

# user configuration of provided data
USER_CONFIG = {
    "auden-musulin-papers/edition": {
        "resource_file_path": "data",
        "file_format": "xml",
        "id": "//tei:TEI[@xml:id]/@xml:id",
        "xpaths": {
            "hasTitle": "//tei:titleStmt/tei:title[@level='a']",
            "hasPid__nolang": "//tei:publicationStmt/tei:idno[@type='handle']",
        },
        "static_values": {
            "hasAccessRestrictions": "https://vocabs.acdh.oeaw.ac.at/archeaccessrestrictions/public",
            "hasCategory": "https://vocabs.acdh.oeaw.ac.at/archecategory/text/tei",
            "isPartOf": "https://id.acdh.oeaw.ac.at/auden-musulin-papers/edition",
        },
        "vocabs_lookup": {}
    },
    "auden-musulin-papers/facs": {
        "resource_file_path": "data",
        "file_format": "xml",
        "id": "//tei:pb/@facs",
        "id_suffix": ".tif",
        "id_as_title": True,
        "id_as_title_prefix": "Facsimile:",
        "xpaths": {
            "isSourceOf__prefix__nolang": "//tei:TEI/@xml:id"
        },
        "static_values": {
            "hasAccessRestrictions": "https://vocabs.acdh.oeaw.ac.at/archeaccessrestrictions/public",
            "hasCategory": "https://vocabs.acdh.oeaw.ac.at/archecategory/image",
            "isPartOf": "https://id.acdh.oeaw.ac.at/auden-musulin-papers/facs",
            "hasPid": "create"
        },
        "vocabs_lookup": {}
    },
    "auden-musulin-papers/web-img": {
        "resource_file_path": "data",
        "file_format": "xml",
        "id": "//tei:pb/@facs",
        "id_suffix": ".tif",
        "id_as_title": True,
        "id_as_title_prefix": "Facsimile:",
        "xpaths": {
            "isSourceOf__prefix__nolang": "//tei:TEI/@xml:id"
        },
        "static_values": {
            "hasAccessRestrictions": "https://vocabs.acdh.oeaw.ac.at/archeaccessrestrictions/public",
            "hasCategory": "https://vocabs.acdh.oeaw.ac.at/archecategory/image",
            "isPartOf": "https://id.acdh.oeaw.ac.at/auden-musulin-papers/facs",
            "hasPid": "create"
        },
        "vocabs_lookup": {}
    }
}

# Baserow client and jwt_token
br_client = BaseRowClient(BASEROW_USER, BASEROW_PW, BASEROW_TOKEN, br_base_url=BASEROW_URL)
jwt_token = br_client.get_jwt_token()
