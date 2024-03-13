import os
from acdh_baserow_pyutils import BaseRowClient
from acdh_tei_pyutils.tei import TeiReader

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
    Expected return is a dict were the key is the ARCHE vocabs predicate and the value is the object as string.
    """
    object_uri = dict()
    xpath = "//tei:pb"
    pb = doc.any_xpath(xpath)
    if isinstance(pb, list) and len(pb) > 0:
        count = 1
        for p in pb:
            try:
                doc_name = p.xpath("//tei:TEI/@xml:id",
                                   namespaces={"tei": "http://www.tei-c.org/ns/1.0"})[0]\
                            .split("__")[-1]\
                            .replace(".xml", "")
            except IndexError:
                doc_name = None
            try:
                conditional = p.xpath("@facs")[0].split("/")[-2]
            except IndexError:
                conditional = None
            try:
                pb_type = p.xpath("@type")[0]
            except IndexError:
                pb_type = None
            try:
                pb_ed = f'{p.xpath("@ed")[0]}'
            except IndexError:
                pb_ed = f"{count}"
                count += 1
            if conditional is not None and conditional in subject_uri:
                if pb_type is not None and pb_ed is not None:
                    object_uri["hasTitle"] = f"""{doc_name} {pb_type.capitalize()} {pb_ed
                        .replace("r", ' [recto]')
                        .replace('v', ' [verso]')}"""
                elif pb_type is not None and pb_ed is None:
                    object_uri["hasTitle"] = f"{doc_name} {pb_type.capitalize()}"
                elif pb_type is None and pb_ed is not None:
                    object_uri["hasTitle"] = f"{doc_name} {pb_ed}"
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
                        object_uri["hasAccessRestriction"] = f"{vocabs_ns}/archeaccessrestrictions/public"
                        object_uri["hasLicense"] = f"{vocabs_ns}/archelicenses/inc"
                    else:
                        object_uri["hasAccessRestriction"] = f"{vocabs_ns}/archeaccessrestrictions/public"
                        object_uri["hasLicense"] = f"{vocabs_ns}/archelicenses/cc-by-4-0"
                elif status == "free":
                    object_uri["hasAccessRestriction"] = f"{vocabs_ns}/archeaccessrestrictions/public"
                    object_uri["hasLicense"] = f"{vocabs_ns}/archelicenses/cc-by-4-0"
            else:
                object_uri["hasAccessRestriction"] = f"{vocabs_ns}/archeaccessrestrictions/public"
                object_uri["hasLicense"] = f"{vocabs_ns}/archelicenses/cc-by-4-0"
    rights = {
        "default_rights": {
            "hasRightsHolder": ["https://id.acdh.oeaw.ac.at/org-whaudenestate"],
            "hasLicensor": ["https://id.acdh.oeaw.ac.at/org-whaudenestate"],
            "hasOwner": ["https://d-nb.info/gnd/1108283586"],
            "hasDigitisingAgent": [
                "https://orcid.org/0000-0002-0914-9245",
                "https://orcid.org/0000-0002-3997-5193",
                "https://d-nb.info/gnd/1024881253"
            ],
            "documents": [
                "amp_0001",
                "amp_0002",
                "amp_0003",
                "amp_0004",
                "amp_0005",
                "amp_0006",
                "amp_0007",
                "amp_0008",
                "amp_0009",
                "amp_0010",
                "amp_0011",
                "amp_0012",
                "amp_0013",
                "amp_0014",
                "amp_0015",
                "amp_0016",
                "amp_0017",
                "amp_0018",
                "amp_0019",
                "amp_0020",
                "amp_0021",
                "amp_0022",
                "amp_0023",
                "amp_0024",
                "amp_0025",
                "amp_0026",
                "amp_0035",
                "amp_0038",
                "amp_0041",
                "amp_0042",
                "amp_0043",
                "amp_0044",
                "amp_0045",
                "amp_0057",
                "amp_0058",
                "amp_0059",
                "amp_0070"
            ]
        },
        "default_rights1": {
            "hasRightsHolder": ["https://d-nb.info/gnd/137925816"],
            "hasLicensor": ["https://d-nb.info/gnd/137925816"],
            "hasOwner": ["https://d-nb.info/gnd/1108283586"],
            "hasDigitisingAgent": [
                "https://orcid.org/0000-0002-0914-9245",
                "https://orcid.org/0000-0002-3997-5193",
                "https://d-nb.info/gnd/1024881253"
            ],
            "documents": [
                "amp_0028",
                "amp_0029",
                "amp_0030",
                "amp_0031",
                "amp_0046",
                "amp_0047",
                "amp_0048",
                "amp_0051",
                "amp_0053",
                "amp_0054",
                "amp_0055",
                "amp_0062",
                "amp_0071"
            ]
        },
        "default_rights2": {
            "hasRightsHolder": ["https://d-nb.info/gnd/14000761X"],
            "hasLicensor": ["https://d-nb.info/gnd/14000761X"],
            "hasOwner": ["https://d-nb.info/gnd/1108283586"],
            "hasDigitisingAgent": [
                "https://orcid.org/0000-0002-0914-9245",
                "https://orcid.org/0000-0002-3997-5193",
                "https://d-nb.info/gnd/1024881253"
            ],
            "documents": [
                "amp_0032",
                "amp_0033"
            ]
        },
        "default_rights3": {
            "hasRightsHolder": ["https://d-nb.info/gnd/1173017283"],
            "hasLicensor": ["https://d-nb.info/gnd/1173017283"],
            "hasOwner": ["https://d-nb.info/gnd/1108283586"],
            "hasDigitisingAgent": [
                "https://orcid.org/0000-0002-0914-9245",
                "https://orcid.org/0000-0002-3997-5193",
                "https://d-nb.info/gnd/1024881253"
            ],
            "documents": [
                "amp_0034"
            ]
        },
        "default_rights4": {
            "hasRightsHolder": ["https://d-nb.info/gnd/2175892-X"],
            "hasLicensor": ["https://d-nb.info/gnd/2175892-X"],
            "hasOwner": ["https://d-nb.info/gnd/1108283586"],
            "hasDigitisingAgent": [
                "https://orcid.org/0000-0002-0914-9245",
                "https://orcid.org/0000-0002-3997-5193",
                "https://d-nb.info/gnd/1024881253"
            ],
            "documents": [
                "amp_0049"
            ]
        },
        "default_rights5": {
            "hasRightsHolder": ["https://www.wikidata.org/wiki/Q680662"],
            "hasLicensor": ["https://www.wikidata.org/wiki/Q680662"],
            "hasOwner": ["https://d-nb.info/gnd/1108283586"],
            "hasDigitisingAgent": [
                "https://orcid.org/0000-0002-0914-9245",
                "https://orcid.org/0000-0002-3997-5193",
                "https://d-nb.info/gnd/1024881253"
            ],
            "documents": [
                "amp_0050"
            ]
        },
        "default_rights6": {
            "hasRightsHolder": ["https://id.acdh.oeaw.ac.at/amendelssohn"],
            "hasLicensor": ["https://id.acdh.oeaw.ac.at/amendelssohn"],
            "hasOwner": ["https://d-nb.info/gnd/1108283586"],
            "hasDigitisingAgent": [
                "https://orcid.org/0000-0002-0914-9245",
                "https://orcid.org/0000-0002-3997-5193",
                "https://d-nb.info/gnd/1024881253"
            ],
            "documents": [
                "amp_0052"
            ]
        },
        "default_rights7": {
            "hasRightsHolder": ["https://d-nb.info/gnd/121076261"],
            "hasLicensor": ["https://d-nb.info/gnd/121076261"],
            "hasOwner": ["https://d-nb.info/gnd/2175892-X"],
            "hasDigitisingAgent": [
                "https://orcid.org/0000-0002-0914-9245",
                "https://orcid.org/0000-0002-3997-5193",
                "https://d-nb.info/gnd/1024881253"
            ],
            "documents": [
                "amp_0060"
            ]
        },
        "default_rights8": {
            "hasRightsHolder": ["https://d-nb.info/gnd/121076261"],
            "hasLicensor": ["https://d-nb.info/gnd/137925816"],
            "hasOwner": ["https://d-nb.info/gnd/2175892-X"],
            "hasDigitisingAgent": [
                "https://orcid.org/0000-0002-0914-9245",
                "https://orcid.org/0000-0002-3997-5193",
                "https://d-nb.info/gnd/1024881253"
            ],
            "documents": [
                "amp_0061"
            ]
        },
        "default_rights9": {
            "hasRightsHolder": ["https://id.acdh.oeaw.ac.at/kkubaczek", "https://id.acdh.oeaw.ac.at/wrohringer"],
            "hasLicensor": ["https://id.acdh.oeaw.ac.at/kkubaczek", "https://id.acdh.oeaw.ac.at/wrohringer"],
            "hasOwner": ["https://d-nb.info/gnd/2020893-5"],
            "hasDigitisingAgent": ["https://d-nb.info/gnd/2020893-5"],
            "documents": [
                "amp_0063"
            ]
        },
        "default_rights10": {
            "hasRightsHolder": ["https://d-nb.info/gnd/137925816"],
            "hasLicensor": ["https://d-nb.info/gnd/137925816"],
            "hasOwner": ["https://d-nb.info/gnd/137925816"],
            "hasDigitisingAgent": [
                "https://orcid.org/0000-0002-0914-9245",
                "https://orcid.org/0000-0002-3997-5193",
                "https://d-nb.info/gnd/1024881253"
            ],
            "documents": [
                "amp_0064",
                "amp_0065",
                "amp_0066",
                "amp_0067",
                "amp_0068",
                "amp_0069",
                "amp_0072",
                "amp_0073",
                "amp_0074",
                "amp_0075"
            ]
        },
        "default_rights11": {
            "hasRightsHolder": ["https://id.acdh.oeaw.ac.at/org-whaudenestate"],
            "hasLicensor": ["https://id.acdh.oeaw.ac.at/org-whaudenestate"],
            "hasOwner": ["https://d-nb.info/gnd/1108283586"],
            "hasDigitisingAgent": [
                "https://orcid.org/0000-0002-0914-9245",
                "https://orcid.org/0000-0002-3997-5193",
                "https://d-nb.info/gnd/1024881253"
            ],
            "documents": [
                "amp_0039",
                "amp_0040"
            ]
        },
    }
    subject_uri_split = subject_uri.split("/")[-1].split(".")[0]
    for key, value in rights.items():
        docs = value["documents"]
        for x in docs:
            file = x.replace("amp_", "")
            doc = TeiReader(f"data/editions/amp-transcript__{file}.xml")
            facs = doc.any_xpath("//tei:pb/@facs")
            if f"https://iiif.acdh.oeaw.ac.at/amp/{subject_uri_split}/" in facs:
                print(subject_uri_split, "in", file)
                object_uri["hasRightsHolder"] = value["hasRightsHolder"]
                object_uri["hasLicensor"] = value["hasLicensor"]
                object_uri["hasOwner"] = value["hasOwner"]
                object_uri["hasDigitisingAgent"] = value["hasDigitisingAgent"]
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
            "hasAccessRestriction": "https://vocabs.acdh.oeaw.ac.at/archeaccessrestrictions/public",
            "hasCategory": "https://vocabs.acdh.oeaw.ac.at/archecategory/text/tei",
            "isPartOf": "https://id.acdh.oeaw.ac.at/auden-musulin-papers/edition",
            "hasLicense": "https://vocabs.acdh.oeaw.ac.at/archelicenses/cc-by-4-0",
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
    # "auden-musulin-papers/facsimiles__collection": {
    #     "resource_file_path": "data/editions",
    #     "file_format": "xml",
    #     "id": "//tei:TEI[@xml:id][child::tei:text[not(@type='photograph')]]/@xml:id",
    #     "id_suffix": "-facsimiles",
    #     "custom_lang": "en",
    #     "xpaths": {
    #         "hasTitle": "//tei:titleStmt/tei:title[@level='a']"
    #     },
    #     "static_values": {
    #         "isPartOf": "https://id.acdh.oeaw.ac.at/auden-musulin-papers/facsimiles",
    #         "hasPid": "create"
    #     },
    #     "vocabs_lookup": {
    #         "hasTitle": {
    #             "lang": "en",
    #             "prefix": False,
    #             "custom_suffix": False
    #         }
    #     }
    # },
    "auden-musulin-papers/facsimiles__resource": {
        "resource_file_path": "data/editions",
        "file_format": "xml",
        "id": "//tei:pb/@facs[ancestor::tei:text[not(@type='photograph')]]",
        "custom_lang": "en",
        "id_suffix": ".tif",
        "id_as_filename": True,
        "xpaths": {
            "isSourceOf": "//tei:TEI[@xml:id]/@xml:id",
            "hasCreator": "//tei:titleStmt/tei:author[@ref]/@ref"
        },
        "static_values": {
            "hasAccessRestriction": "https://vocabs.acdh.oeaw.ac.at/archeaccessrestrictions/public",
            "hasCategory": "https://vocabs.acdh.oeaw.ac.at/archecategory/image",
            "hasPid": "create",
            "isPartOf": "https://id.acdh.oeaw.ac.at/auden-musulin-papers/facsimiles"
        },
        "vocabs_lookup": {
            "hasLicense": {
                "lang": LANG_SPECIAL_TOKEN,
                "prefix": False,
                "custom_suffix": False
            },
            "hasAccessRestriction": {
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
            "hasTitle": {
                "lang": "en",
                "prefix": False,
                "custom_suffix": False
            },
        },
        "custom_def": True
    },
    # "auden-musulin-papers/photos__collection": {
    #     "resource_file_path": "data/editions",
    #     "file_format": "xml",
    #     "id": "//tei:TEI[@xml:id][child::tei:text[@type='photograph']]/@xml:id",
    #     "id_suffix": "-photos",
    #     "custom_lang": "en",
    #     "xpaths": {
    #         "hasTitle": "//tei:titleStmt/tei:title[@level='a']"
    #     },
    #     "static_values": {
    #         "isPartOf": "https://id.acdh.oeaw.ac.at/auden-musulin-papers/photos",
    #         "hasPid": "create"
    #     },
    #     "vocabs_lookup": {
    #         "hasTitle": {
    #             "lang": "en",
    #             "prefix": False,
    #             "custom_suffix": False
    #         }
    #     }
    # },
    "auden-musulin-papers/photos__resource": {
        "resource_file_path": "data/editions",
        "file_format": "xml",
        "id": "//tei:pb/@facs[ancestor::tei:text[@type='photograph']]",
        "id_suffix": ".tif",
        "id_as_filename": True,
        "custom_lang": "en",
        "xpaths": {
            "isSourceOf": "//tei:TEI[@xml:id]/@xml:id",
            "hasCreator": "//tei:titleStmt/tei:author[@ref]/@ref"
        },
        "static_values": {
            "hasCategory": "https://vocabs.acdh.oeaw.ac.at/archecategory/image",
            "hasPid": "create",
            "isPartOf": "https://id.acdh.oeaw.ac.at/auden-musulin-papers/photos",
        },
        "vocabs_lookup": {
            "hasLicense": {
                "lang": LANG_SPECIAL_TOKEN,
                "prefix": False,
                "custom_suffix": False
            },
            "hasAccessRestriction": {
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
                "custom_suffix": False
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
            "hasAccessRestriction": "https://vocabs.acdh.oeaw.ac.at/archeaccessrestrictions/public",
            "hasCategory": "https://vocabs.acdh.oeaw.ac.at/archecategory/text/tei",
            "isPartOf": "https://id.acdh.oeaw.ac.at/auden-musulin-papers/indexes",
            "hasPid": "create",
            "hasLicense": "https://vocabs.acdh.oeaw.ac.at/archelicenses/cc-by-4-0",
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
