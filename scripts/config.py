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
LANG_SPECIAL_TOKEN = "na"


def custom_function(subject_uri, doc) -> dict:
    """
    Custom function to be called during the mapping process.
    Add your custom function here.
    Expected return is a dict were the key is the predicate and the value is the object.
    """
    object_uri = dict()
    xpath = "//tei:pb"
    pb = doc.any_xpath(xpath)
    if isinstance(pb, list) and len(pb) > 0:
        for p in pb:
            try:
                conditional = p.xpath("@facs")[0].split("/")[-1]
            except IndexError:
                conditional = None
            try:
                pb_type = p.xpath("@type")[0]
            except IndexError:
                pb_type = None
            try:
                pb_ed = p.xpath("@ed")[0]
            except IndexError:
                pb_ed = None
            if conditional is not None and conditional in subject_uri:
                if pb_type is not None and pb_ed is not None:
                    object_uri["hasTitle"] = f"{pb_type.capitalize()} {pb_ed}"
                elif pb_type is not None and pb_ed is None:
                    object_uri["hasTitle"] = f"{pb_type.capitalize()}"
                elif pb_type is None and pb_ed is not None:
                    object_uri["hasTitle"] = f"{pb_ed}"
    xpath = "//tei:availability"
    availability = doc.any_xpath(xpath)
    if isinstance(availability, list) and len(availability) > 0:
        vocabs_ns = "https://vocabs.acdh.oeaw.ac.at"
        for a in availability:
            try:
                status = a.xpath("@status")[0]
            except IndexError:
                status = None
            if status is not None:
                if status == "restricted":
                    try:
                        facs = a.xpath("./tei:licence/@facs", namespaces={"tei": "http://www.tei-c.org/ns/1.0"})[0]
                        facs = facs.split("/")[-2]
                    except IndexError:
                        facs = False
                    if facs and facs in subject_uri:
                        object_uri["hasAccessRestrictions"] = f"{vocabs_ns}/archeaccessrestrictions/public"
                        object_uri["hasLicense"] = f"{vocabs_ns}/archelicenses/inc"
                    else:
                        object_uri["hasAccessRestrictions"] = f"{vocabs_ns}/archeaccessrestrictions/public"
                        object_uri["hasLicense"] = f"{vocabs_ns}/archelicenses/cc-by-4-0"
                elif status == "free":
                    object_uri["hasAccessRestrictions"] = f"{vocabs_ns}/archeaccessrestrictions/public"
                    object_uri["hasLicense"] = f"{vocabs_ns}/archelicenses/cc-by-4-0"
            else:
                object_uri["hasAccessRestrictions"] = f"{vocabs_ns}/archeaccessrestrictions/public"
                object_uri["hasLicense"] = f"{vocabs_ns}/archelicenses/cc-by-4-0"
    return object_uri


# user configuration of provided data
USER_CONFIG = {
    "auden-musulin-papers/edition__resource": {
        "resource_file_path": "data/editions",
        "file_format": "xml",
        "id": "//tei:TEI[@xml:id]/@xml:id",
        "custom_lang": "en",
        "xpaths": {
            "hasTitle": "//tei:titleStmt/tei:title[@level='a']",
            "hasPid": "//tei:publicationStmt/tei:idno[@type='handle']",
            "hasAuthor": "//tei:titleStmt/tei:author[@ref]/@ref"
        },
        "static_values": {
            "hasAccessRestrictions": "https://vocabs.acdh.oeaw.ac.at/archeaccessrestrictions/public",
            "hasCategory": "https://vocabs.acdh.oeaw.ac.at/archecategory/text/tei",
            "isPartOf": "https://id.acdh.oeaw.ac.at/auden-musulin-papers/edition",
        },
        "vocabs_lookup": {
            "hasTitle": {
                "lang": "en",
                "prefix": False,
                "custom_suffix": False
            },
            "hasPid": {
                "lang": LANG_SPECIAL_TOKEN,
                "prefix": False,
                "custom_suffix": False
            },
            "hasAuthor": {
                "lang": LANG_SPECIAL_TOKEN,
                "prefix": False,
                "custom_suffix": False
            },
        },
    },
    "auden-musulin-papers/facsimiles__collection": {
        "resource_file_path": "data/editions",
        "file_format": "xml",
        "id": "//tei:TEI[@xml:id][child::tei:text[not(@type='photograph')]]/@xml:id",
        "id_suffix": "-facsimiles",
        "custom_lang": "en",
        "xpaths": {
            "hasTitle": "//tei:titleStmt/tei:title[@level='a']"
        },
        "static_values": {
            "isPartOf": "https://id.acdh.oeaw.ac.at/auden-musulin-papers/facsimiles",
            "hasPid": "create"
        },
        "vocabs_lookup": {
            "hasTitle": {
                "lang": "en",
                "prefix": False,
                "custom_suffix": False
            }
        }
    },
    "auden-musulin-papers/facsimiles__resource": {
        "resource_file_path": "data/editions",
        "file_format": "xml",
        "id": "//tei:pb/@facs[ancestor::tei:text[not(@type='photograph')]]",
        "custom_lang": "en",
        "id_suffix": ".tif",
        "id_as_filename": True,
        "xpaths": {
            "isSourceOf": "//tei:TEI[@xml:id]/@xml:id",
            "hasAuthor": "//tei:titleStmt/tei:author[@ref]/@ref",
            "isPartOf": "//tei:TEI[@xml:id][child::tei:text[not(@type='photograph')]]/@xml:id",
        },
        "static_values": {
            "hasAccessRestrictions": "https://vocabs.acdh.oeaw.ac.at/archeaccessrestrictions/public",
            "hasCategory": "https://vocabs.acdh.oeaw.ac.at/archecategory/image",
            "hasPid": "create",
            "hasLincense": "https://vocabs.acdh.oeaw.ac.at/archelicenses/cc-by-4-0"
        },
        "vocabs_lookup": {
            "hasLicense": {
                "lang": LANG_SPECIAL_TOKEN,
                "prefix": False,
                "custom_suffix": False
            },
            "hasAccessRestrictions": {
                "lang": LANG_SPECIAL_TOKEN,
                "prefix": False,
                "custom_suffix": False
            },
            "isSourceOf": {
                "lang": LANG_SPECIAL_TOKEN,
                "prefix": True,
                "custom_suffix": False
            },
            "hasCreator": {
                "lang": LANG_SPECIAL_TOKEN,
                "prefix": False,
                "custom_suffix": False
            },
            "isPartOf": {
                "lang": LANG_SPECIAL_TOKEN,
                "prefix": True,
                "custom_suffix": "/facsimiles"
            },
            "hasTitle": {
                "lang": "en",
                "prefix": False,
                "custom_suffix": False
            },
        },
        "custom_def": True
    },
    "auden-musulin-papers/photos__collection": {
        "resource_file_path": "data/editions",
        "file_format": "xml",
        "id": "//tei:TEI[@xml:id][child::tei:text[@type='photograph']]/@xml:id",
        "id_suffix": "-photos",
        "custom_lang": "en",
        "xpaths": {
            "hasTitle": "//tei:titleStmt/tei:title[@level='a']"
        },
        "static_values": {
            "isPartOf": "https://id.acdh.oeaw.ac.at/auden-musulin-papers/photos",
            "hasPid": "create"
        },
        "vocabs_lookup": {
            "hasTitle": {
                "lang": "en",
                "prefix": False,
                "custom_suffix": False
            }
        }
    },
    "auden-musulin-papers/photos__resource": {
        "resource_file_path": "data/editions",
        "file_format": "xml",
        "id": "//tei:pb/@facs[ancestor::tei:text[@type='photograph']]",
        "id_suffix": ".tif",
        "id_as_filename": True,
        "custom_lang": "en",
        "xpaths": {
            "isSourceOf": "//tei:TEI[@xml:id]/@xml:id",
            "hasCreator": "//tei:titleStmt/tei:author[@ref]/@ref",
            "isPartOf": "//tei:TEI[@xml:id][child::tei:text[@type='photograph']]/@xml:id"
        },
        "static_values": {
            "hasCategory": "https://vocabs.acdh.oeaw.ac.at/archecategory/image",
            "hasPid": "create"
        },
        "vocabs_lookup": {
            "hasLicense": {
                "lang": LANG_SPECIAL_TOKEN,
                "prefix": False,
                "custom_suffix": False
            },
            "hasAccessRestrictions": {
                "lang": LANG_SPECIAL_TOKEN,
                "prefix": False,
                "custom_suffix": False
            },
            "isSourceOf": {
                "lang": LANG_SPECIAL_TOKEN,
                "prefix": True,
                "custom_suffix": False
            },
            "hasCreator": {
                "lang": LANG_SPECIAL_TOKEN,
                "prefix": False,
                "custom_suffix": False
            },
            "isPartOf": {
                "lang": LANG_SPECIAL_TOKEN,
                "prefix": True,
                "custom_suffix": "/photos"
            },
            "hasTitle": {
                "lang": "en",
                "prefix": False,
                "custom_suffix": False
            },
        },
        "custom_def": True
    },
    "auden-musulin-papers/indexes__resource": {
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
        "vocabs_lookup": {
            "hasTitle": {
                "lang": "en",
                "prefix": False,
                "custom_suffix": False
            }
        }
    }
}

# Baserow client and jwt_token
br_client = BaseRowClient(BASEROW_USER, BASEROW_PW, BASEROW_TOKEN, br_base_url=BASEROW_URL)
jwt_token = br_client.get_jwt_token()
