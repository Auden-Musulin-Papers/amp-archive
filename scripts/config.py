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
ADDITIONAL_RESOURCES = os.environ.get("ADDITIONAL_RESOURCES")
ADDITIONAL_DATA_DIRECTORY = os.environ.get("ADDITIONAL_DATA_DIRECTORY")
ADDITIONAL_FILE_FORMAT = os.environ.get("ADDITIONAL_FILE_FORMAT")

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
        "resource_file_path": "data/editions",
        "file_format": "xml",
        "id": "//tei:TEI[@xml:id]/@xml:id",
        "custom_lang": "en",
        "xpaths": {
            "hasTitle": "//tei:titleStmt/tei:title[@level='a']",
            "hasPid__nolang": "//tei:publicationStmt/tei:idno[@type='handle']",
            "hasAuthor__nolang": "//tei:titleStmt/tei:author[@ref]/@ref"
        },
        "static_values": {
            "hasAccessRestrictions": "https://vocabs.acdh.oeaw.ac.at/archeaccessrestrictions/public",
            "hasCategory": "https://vocabs.acdh.oeaw.ac.at/archecategory/text/tei",
            "isPartOf": "https://id.acdh.oeaw.ac.at/auden-musulin-papers/edition",
        },
        "vocabs_lookup": {}
    },
    "auden-musulin-papers/facsimiles": {
        "resource_file_path": "data/editions",
        "file_format": "xml",
        "id": "//tei:pb/@facs[ancestor::tei:text[not(@type='photograph')]]",
        "custom_lang": "en",
        "id_suffix": ".tif",
        "id_as_title": False,
        "id_as_title_prefix": "Facsimile:",
        "id_as_filename": True,
        "createTitle_xpaths": """//tei:pb[ancestor::tei:text[not(@type='photograph')]]__@type|
                                //tei:pb[ancestor::tei:text[not(@type='photograph')]]__@ed""",
        "xpaths": {
            "isSourceOf__prefix__nolang": "//tei:TEI[@xml:id]/@xml:id",
            "hasAuthor__nolang": "//tei:titleStmt/tei:author[@ref]/@ref"
        },
        "static_values": {
            "hasAccessRestrictions": "https://vocabs.acdh.oeaw.ac.at/archeaccessrestrictions/public",
            "hasCategory": "https://vocabs.acdh.oeaw.ac.at/archecategory/image",
            "isPartOf": "https://id.acdh.oeaw.ac.at/auden-musulin-papers/facsimiles",
            "hasPid": "create"
        },
        "vocabs_lookup": {}
    },
    "auden-musulin-papers/photos": {
        "resource_file_path": "data/editions",
        "file_format": "xml",
        "id": "//tei:pb/@facs[ancestor::tei:text[@type='photograph']]",
        "id_suffix": ".tif",
        "id_as_title": True,
        "id_as_title_prefix": "Photo:",
        "id_as_filename": True,
        "custom_lang": "en",
        "createTitle_xpaths": """//tei:pb[ancestor::tei:text[@type='photograph']]__@type|
                                //tei:pb[ancestor::tei:text[@type='photograph']]__@ed""",
        "xpaths": {
            "isSourceOf__prefix__nolang": "//tei:TEI[@xml:id]/@xml:id",
            "hasCreator__nolang": "//tei:titleStmt/tei:author[@ref]/@ref"
        },
        "static_values": {
            "hasAccessRestrictions": "https://vocabs.acdh.oeaw.ac.at/archeaccessrestrictions/public",
            "hasCategory": "https://vocabs.acdh.oeaw.ac.at/archecategory/image",
            "isPartOf": "https://id.acdh.oeaw.ac.at/auden-musulin-papers/photos",
            "hasPid": "create"
        },
        "vocabs_lookup": {}
    },
    "auden-musulin-papers/indexes": {
        "resource_file_path": "data/indexes",
        "file_format": "xml",
        "id": "//tei:TEI[@xml:id]/@xml:id",
        "custom_lang": "en",
        "xpaths": {
            "hasTitle": "//tei:titleStmt/tei:title[1]"
        },
        "static_values": {
            "hasAccessRestrictions": "https://vocabs.acdh.oeaw.ac.at/archeaccessrestrictions/public",
            "hasCategory": "https://vocabs.acdh.oeaw.ac.at/archecategory/text/tei",
            "isPartOf": "https://id.acdh.oeaw.ac.at/auden-musulin-papers/indexes",
            "hasPid": "create"
        },
        "vocabs_lookup": {}
    }
}

# Baserow client and jwt_token
br_client = BaseRowClient(BASEROW_USER, BASEROW_PW, BASEROW_TOKEN, br_base_url=BASEROW_URL)
jwt_token = br_client.get_jwt_token()
