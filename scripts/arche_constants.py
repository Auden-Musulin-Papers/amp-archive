import json
import re
import glob
import os
from config import USER_CONFIG, PROJECT_NAME, LATEST_RELEASE
from acdh_tei_pyutils.tei import TeiReader
from tqdm import tqdm
from acdh_graph_pyutils.graph import (
    create_empty_graph,
    create_custom_triple,
    create_type_triple,
    create_memory_store,
    serialize_graph
)
from acdh_graph_pyutils.namespaces import NAMESPACES
from rdflib import URIRef, Literal, Namespace

# load metadata json files
with open("json_dumps/Project_denormalized.json", "r") as f:
    metadata = json.load(f)

# define namespaces
NAMESPACES["rdf"] = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
NAMESPACES["rdfs"] = "http://www.w3.org/2000/01/rdf-schema#"
NAMESPACES["xsd"] = "http://www.w3.org/2001/XMLSchema#"
NAMESPACES["arche"] = "https://vocabs.acdh.oeaw.ac.at/schema#"
arche_id = URIRef("https://id.acdh.oeaw.ac.at/")
ARCHE = Namespace(NAMESPACES["arche"])
COLLECTION_NAME = PROJECT_NAME


def create_entity_uri_from_string(string) -> URIRef:
    """
    Create an URIRef from a string.
    """
    if isinstance(string, str) and len(string) > 0:
        if ", " in string:
            string = string.split(", ")
            last_name = [re.sub(r"[^a-zA-Z0-9]+", "", string[0])]
            if len(string[1].split(" ")) == 1:
                first_name = re.sub(r"[^a-zA-Z0-9]+", "", string[1].split(" ")[0])
                first_name_letter = first_name[1]
                last_name.insert(0, first_name_letter)
            elif len(string[1].split(" ")) > 1:
                for x in string[1].split(" "):
                    name = re.sub(r"[^a-zA-Z0-9]+", "", x)
                    last_name.insert(0, name[0])
            return URIRef(f'{arche_id}{"".join(last_name).lower()}')
        else:
            return URIRef(f'{arche_id}{string}')
    else:
        return ""


def create_minimal_entity_triple(entity, entity_type) -> None:
    """
    Create URIRef from string and entity type triple.
    """
    try:
        data = entity["data"]
    except KeyError:
        return
    subject_uri = URIRef(data["Subject_uri"])
    if entity_type == "persons":
        object_uri = URIRef(ARCHE["Person"])
    elif entity_type == "places":
        object_uri = URIRef(ARCHE["Place"])
    elif entity_type == "organizations":
        object_uri = URIRef(ARCHE["Organisation"])
    else:
        raise UnboundLocalError(f"Entity type not defined. {entity_type}")
    create_type_triple(g, subject_uri, object_uri)


def get_entity_uri(
    subject_uri: URIRef,
    predicate_uri: URIRef,
    entity: list,
    entity_type: str = None
) -> None:
    """
    Create an URIRef from a string.
    """
    if isinstance(entity, list) and len(entity) > 0:
        for ent in entity:
            if len(ent["data"]["Subject_uri"]) > 0:
                object_uri = URIRef(ent["data"]["Subject_uri"])
            else:
                continue
            create_custom_triple(g, subject_uri, predicate_uri, object_uri)
            if entity_type is not None:
                create_minimal_entity_triple(ent, entity_type)


def get_resource_uri(
    subject_uri: URIRef,
    predicate_uri: URIRef,
    resource: list,
) -> None:
    """
    Create an URIRef from a string.
    """
    if isinstance(resource, list) and len(resource) > 0:
        for res in resource:
            try:
                object_uri = URIRef(f'{res["data"]["Namespace"]}{res["value"]}')
            except KeyError:
                object_uri = URIRef(f'{arche_id}{res["value"]}')
            create_custom_triple(g, subject_uri, predicate_uri, object_uri)


def get_literal(
    subject_uri: URIRef,
    predicate_uri: URIRef,
    literal: str,
    literal_lang: str
) -> None:
    """
    Create a Literal with or without language from a string.
    """
    if isinstance(literal, str) and len(literal) > 0:
        if isinstance(literal_lang, str) and len(literal_lang) > 0:
            if literal_lang != "na":
                create_custom_triple(g, subject_uri, predicate_uri, Literal(literal, lang=literal_lang))
            else:
                create_custom_triple(g, subject_uri, predicate_uri, Literal(literal))


def get_date(
    subject_uri: URIRef,
    predicate_uri: URIRef,
    date: str
) -> None:
    """
    Create a Literal with datatype date from a string.
    """
    if isinstance(date, str) and len(date) > 0:
        create_custom_triple(g, subject_uri, predicate_uri, Literal(date, datatype=f'{NAMESPACES["xsd"]}date'))


def get_number(
    subject_uri: URIRef,
    predicate_uri: URIRef,
    number: int
) -> None:
    """
    Create a Literal with datatype integer from a string.
    """
    if isinstance(number, int) and len(number) > 0:
        create_custom_triple(g, subject_uri, predicate_uri, Literal(number, datatype=f'{NAMESPACES["xsd"]}integer'))


def get_resource_triple_from_xpath(
    doc: TeiReader,
    subject_uri: URIRef,
    xpaths: dict
) -> None:
    print("Getting triples from xpath.")
    if isinstance(xpaths, dict) and len(xpaths) > 0:
        for key, value in xpaths.items():
            lang = "en"
            prefix = ""
            if "__nolang" in key:
                key = key.replace("__nolang", "")
                lang = "na"
            if "__prefix" in key:
                key = key.replace("__prefix", "")
                prefix = f"https://id.acdh.oeaw.ac.at/{COLLECTION_NAME}/"
            predicate_uri = URIRef(f'{NAMESPACES["arche"]}{key}')
            object_uri = doc.any_xpath(value)
            if isinstance(object_uri, list) and len(object_uri) > 0:
                for obj in object_uri:
                    try:
                        obj_text = obj.text
                    except AttributeError:
                        obj_text = obj
                    get_literal(
                        subject_uri=subject_uri,
                        predicate_uri=predicate_uri,
                        literal=f"{prefix}{obj_text}",
                        literal_lang=lang
                    )
    return print("Triples from xpaths created.")


def create_resource_triples(
    file_path: str,
    file_format: str,
    subject_id: str,
    id_suffix: str = "",
    id_as_title: bool = False,
    id_as_title_prefix: str = "",
    init: bool = False,
    xpaths: dict = None,
    static_values: dict = None,
    vocabs_lookup: dict = None
) -> None:
    """
    Create an URIRef from a string.
    """
    edition_files = glob.glob(f"{file_path}/*.{file_format}")
    for file in tqdm(edition_files, total=len(edition_files)):
        doc = TeiReader(file)
        xml_id = doc.any_xpath(subject_id)
        if isinstance(xml_id, list) and len(xml_id) > 0:
            for x in xml_id:
                resource_id = x
                if resource_id.startswith("#"):
                    resource_id = resource_id.replace("#", "")
                elif resource_id.startswith("http"):
                    resource_id = resource_id.split("/")[-2]
                if len(resource_id) != 0:
                    item_id = f'{arche_id}{COLLECTION_NAME}/{resource_id}{id_suffix}'
                    subject_uri = URIRef(item_id)
                    if init:
                        create_type_triple(g, subject_uri, ARCHE["Resource"])
                        if id_as_title:
                            create_custom_triple(
                                g,
                                subject=subject_uri,
                                predicate=ARCHE["hasTitle"],
                                object=Literal(f'{id_as_title_prefix} {resource_id}', lang="en")
                            )
                        get_resource_triple_from_xpath(doc, subject_uri, xpaths)
                        if isinstance(static_values, dict) and len(static_values) > 0:
                            for key, value in static_values.items():
                                predicate = URIRef(f'{NAMESPACES["arche"]}{key}')
                                object_uri = URIRef(value)
                                create_custom_triple(
                                    g,
                                    subject=subject_uri,
                                    predicate=predicate,
                                    object=object_uri
                                )
                        # if isinstance(vocabs_lookup, dict) and len(vocabs_lookup) > 0:
                        #     for key, value in vocabs_lookup.items():
                        #         predicate = URIRef(f'{NAMESPACES["arche"]}{key}')
                        #         object_uri = URIRef(f'{NAMESPACES["arche"]}{doc.any_xpath(value)}')
                        #         create_custom_triple(
                        #             g,
                        #             subject=subject_uri,
                        #             predicate=predicate,
                        #             object=object_uri
                        #         )
                    else:
                        get_entity_uri(
                            subject_uri=subject_uri,
                            predicate_uri=predicate_uri,
                            entity=persons_list
                        )
                        get_entity_uri(
                            subject_uri=subject_uri,
                            predicate_uri=predicate_uri,
                            entity=places_list
                        )
                        get_entity_uri(
                            subject_uri=subject_uri,
                            predicate_uri=predicate_uri,
                            entity=organizations_list
                        )
                        get_resource_uri(
                            subject_uri=subject_uri,
                            predicate_uri=predicate_uri,
                            resource=resource_list
                        )
                        get_resource_uri(
                            subject_uri=subject_uri,
                            predicate_uri=predicate_uri,
                            resource=vocabs_list
                        )
                        get_literal(
                            subject_uri=subject_uri,
                            predicate_uri=predicate_uri,
                            literal=literal,
                            literal_lang=language
                        )
                        get_date(
                            subject_uri=subject_uri,
                            predicate_uri=predicate_uri,
                            date=date
                        )
                        get_number(
                            subject_uri=subject_uri,
                            predicate_uri=predicate_uri,
                            number=number
                        )


def verify_config_keys(key, result):
    try:
        return CONFIG[key]
    except KeyError:
        if result == "raise":
            raise UnboundLocalError(f"User Config: id {key} is required")
        else:
            return result


# create empty graph
g = create_empty_graph(
    namespaces=NAMESPACES,
    identifier=arche_id,
    store=create_memory_store()
)

# initialize resource URIs (lookup USER_CONFIG)
if isinstance(LATEST_RELEASE, str) and len(LATEST_RELEASE) > 0:
    for CONFIG in USER_CONFIG.values():
        create_resource_triples(
            file_path=verify_config_keys("resource_file_path", "raise"),
            file_format=verify_config_keys("file_format", "raise"),
            subject_id=verify_config_keys("id", "raise"),
            id_suffix=verify_config_keys("id_suffix", ""),
            id_as_title=verify_config_keys("id_as_title", ""),
            id_as_title_prefix=verify_config_keys("id_as_title_prefix", ""),
            init=True,
            xpaths=verify_config_keys("xpaths", None),
            static_values=verify_config_keys("static_values", None),
            vocabs_lookup=verify_config_keys("vocabs_lookup", None)
        )

for meta in tqdm(metadata.values(), total=len(metadata)):
    subject_string = meta["Subject_uri"]
    subject_uri = URIRef(f'{arche_id}{subject_string}')
    if isinstance(meta["Class"], list) and len(meta["Class"]) == 1:
        type_class = meta["Class"][0]
        type_uri = URIRef(f'{type_class["data"]["Namespace"]}{type_class["value"]}')
        create_type_triple(g, subject_uri, type_uri)
    if isinstance(meta["Predicate_uri"], list) and len(meta["Predicate_uri"]) == 1:
        predicate_class = meta["Predicate_uri"][0]
        predicate_uri = URIRef(f'{predicate_class["data"]["Namespace"]}{predicate_class["value"]}')
        # create triples from persons
        persons_list = meta["Object_uri_persons"]
        get_entity_uri(
            subject_uri=subject_uri,
            predicate_uri=predicate_uri,
            entity=persons_list,
            entity_type="persons"
        )
        # create triples from places
        places_list = meta["Object_uri_places"]
        get_entity_uri(
            subject_uri=subject_uri,
            predicate_uri=predicate_uri,
            entity=places_list,
            entity_type="places"
        )
        # create triples from organizations
        organizations_list = meta["Object_uri_organizations"]
        get_entity_uri(
            subject_uri=subject_uri,
            predicate_uri=predicate_uri,
            entity=organizations_list,
            entity_type="organizations"
        )
        # create triples from resources
        resource_list = meta["Object_uri_resource"]
        get_resource_uri(
            subject_uri=subject_uri,
            predicate_uri=predicate_uri,
            resource=resource_list
        )
        # create triples from vocabs
        vocabs_list = meta["Object_uri_vocabs"]
        get_resource_uri(
            subject_uri=subject_uri,
            predicate_uri=predicate_uri,
            resource=vocabs_list
        )
        # create triples from literal
        literal = meta["Literal"]
        language = meta["Language"]
        get_literal(
            subject_uri=subject_uri,
            predicate_uri=predicate_uri,
            literal=literal,
            literal_lang=language
        )
        # create triples from date
        date = meta["Date"]
        get_date(
            subject_uri=subject_uri,
            predicate_uri=predicate_uri,
            date=date
        )
        # create triples from number
        number = meta["Number"]
        get_number(
            subject_uri=subject_uri,
            predicate_uri=predicate_uri,
            number=number
        )
        if isinstance(LATEST_RELEASE, str) and len(LATEST_RELEASE) > 0:
            if isinstance(meta["Inherit"], list) and len(meta["Inherit"]) > 0:
                for inherit in meta["Inherit"]:
                    try:
                        CONFIG = USER_CONFIG[subject_string]
                        create_resource_triples(
                            file_path=verify_config_keys("resource_file_path", "raise"),
                            file_format=verify_config_keys("file_format", "raise"),
                            subject_id=verify_config_keys("id", "raise"),
                            id_suffix=verify_config_keys("id_suffix", ""),
                            id_as_title=verify_config_keys("id_as_title", ""),
                            id_as_title_prefix=verify_config_keys("id_as_title_prefix", ""),
                        )
                    except KeyError:
                        print("No config for this resource.")

# create graph for ARCHE entities
# open json file
files = ["Persons_denormalized", "Places_denormalized", "Organizations_denormalized"]
file_glob = glob.glob("json_dumps/*.json")

for file in file_glob:
    fn = file.split("/")[-1].split(".")[0]
    if fn in files:
        with open(file, "r") as f:
            data = json.load(f)
        for meta in tqdm(data.values(), total=len(data)):
            subject_uri = URIRef(meta["Subject_uri"])
            if isinstance(meta["Predicate_uri"], list) and len(meta["Predicate_uri"]) == 1:
                predicate_class = meta["Predicate_uri"][0]
                predicate_uri = URIRef(f'{predicate_class["data"]["Namespace"]}{predicate_class["value"]}')
                entity_type = fn.replace("_denormalized", "").lower()
                try:
                    get_entity_uri(
                        subject_uri=subject_uri,
                        predicate_uri=predicate_uri,
                        entity=meta["Object_uri_organizations"],
                        entity_type="organizations"
                    )
                except KeyError:
                    # placeholder
                    print("No organizations.")
                get_literal(
                    subject_uri=subject_uri,
                    predicate_uri=predicate_uri,
                    literal=meta["Literal"],
                    literal_lang=meta["Language"]
                )

# serialize graph
os.makedirs("rdf", exist_ok=True)
serialize_graph(g, "turtle", "rdf/arche.ttl")
print("Done with ARCHE constants. file: rdf/arche.ttl")
