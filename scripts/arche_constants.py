import json
import re
import glob
import os
import requests
import shutil
import zipfile
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
    subject_uri = URIRef(data["hasIdentifier"])
    if entity_type == "person":
        object_uri = URIRef(ARCHE["Person"])
    elif entity_type == "place":
        object_uri = URIRef(ARCHE["Place"])
    elif entity_type == "organization":
        object_uri = URIRef(ARCHE["Organisation"])
    create_type_triple(g, subject_uri, object_uri)
    if isinstance(data["Name"], str) and len(data["Name"]) > 0:
        if isinstance(data["Language"], str) and len(data["Language"]) > 0:
            create_custom_triple(g, subject_uri, ARCHE["hasTitle"], Literal(data["Name"], lang=data["Language"]))
        else:
            raise ValueError(f'No language for {data["Name"]} given!')


def create_full_entity_triple(predicate, object, lang) -> None:
    if isinstance(object, str) and len(object) > 0:
        if "__nolang" in predicate:
            predicate = predicate.replace("__nolang", "")
            object_uri = Literal(object)
            create_custom_triple(g, subject_uri, ARCHE[predicate], object_uri)
        else:
            object_uri = Literal(object, lang=lang)
            create_custom_triple(g, subject_uri, ARCHE[predicate], object_uri)
    elif isinstance(object, list) and len(object) > 0:
        get_entity_uri(object)


def get_entity_uri(entity, entity_type=None) -> None:
    """
    Create an URIRef from a string.
    """
    if isinstance(entity, list) and len(entity) > 0:
        for ent in entity:
            if len(ent["data"]["hasIdentifier"]) > 0:
                object_uri = URIRef(ent["data"]["hasIdentifier"])
            else:
                continue
            create_custom_triple(g, subject_uri, predicate_uri, object_uri)
            if entity_type is not None:
                create_minimal_entity_triple(ent, entity_type)


def get_resource_uri(resource) -> None:
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


def get_literal(literal, literal_lang) -> None:
    """
    Create a Literal with or without language from a string.
    """
    if isinstance(literal, str) and len(literal) > 0:
        if isinstance(literal_lang, str) and len(literal_lang) > 0:
            if literal_lang != "na":
                create_custom_triple(g, subject_uri, predicate_uri, Literal(literal, lang=literal_lang))
            else:
                create_custom_triple(g, subject_uri, predicate_uri, Literal(literal))


def get_date(date) -> None:
    """
    Create a Literal with datatype date from a string.
    """
    if isinstance(date, str) and len(date) > 0:
        create_custom_triple(g, subject_uri, predicate_uri, Literal(date, datatype=f'{NAMESPACES["xsd"]}date'))


def get_number(number) -> None:
    """
    Create a Literal with datatype integer from a string.
    """
    if isinstance(number, int) and len(number) > 0:
        create_custom_triple(g, subject_uri, predicate_uri, Literal(number, datatype=f'{NAMESPACES["xsd"]}integer'))


# create empty graph
g = create_empty_graph(
    namespaces=NAMESPACES,
    identifier=arche_id,
    store=create_memory_store()
)

for meta in tqdm(metadata.values(), total=len(metadata)):
    subject_uri = URIRef(f'{arche_id}{meta["Subject_uri"]}')
    if isinstance(meta["Class"], list) and len(meta["Class"]) == 1:
        type_class = meta["Class"][0]
        type_uri = URIRef(f'{type_class["data"]["Namespace"]}{type_class["value"]}')
        create_type_triple(g, subject_uri, type_uri)
    if isinstance(meta["Predicate_uri"], list) and len(meta["Predicate_uri"]) == 1:
        predicate_class = meta["Predicate_uri"][0]
        predicate_uri = URIRef(f'{predicate_class["data"]["Namespace"]}{predicate_class["value"]}')
        get_entity_uri(meta["Object_uri_persons"], "person")
        get_entity_uri(meta["Object_uri_places"], "place")
        get_entity_uri(meta["Object_uri_organizations"], "organization")
        get_resource_uri(meta["Object_uri_resource"])
        get_resource_uri(meta["Object_uri_vocabs"])
        get_literal(meta["Literal"], meta["Language"])
        get_date(meta["Date"])
        get_number(meta["Number"])

# create graph for ARCHE entities
# open json file
files = ["Persons_denormalized", "Places", "Organizations"]
file_glob = glob.glob("json_dumps/*.json")

for file in file_glob:
    fn = file.split("/")[-1].split(".")[0]
    if fn in files:
        with open(file, "r") as f:
            data = json.load(f)
        for meta in tqdm(data.values(), total=len(data)):
            subject_uri = URIRef(meta["hasIdentifier"])
            entity_type = fn.replace("_denormalized", "").lower()
            special_handling = ["Name", "Uri", "hasIdentifier", "Language", "filename", "id", "order"]
            for key, value in meta.items():
                if key not in special_handling:
                    predicate_uri = ARCHE[key]
                    create_full_entity_triple(key, value, meta["Language"])

# create graph for resources
# open xml files
# LATEST_RELEASE = os.environ.get("LATEST_RELEASE")
# r = requests.get(LATEST_RELEASE)

# with open("resources.zip", "wb") as f:
#     f.write(r.content)

# shutil.rmtree("amp-data", ignore_errors=True)
# os.makedirs("amp-data", exist_ok=True)
# with zipfile.ZipFile("resources.zip", "r") as zip_ref:
#     zip_ref.extractall("amp-data")

# files = glob.glob("amp-data/*/data")
# shutil.move(files[0], ".")
# shutil.rmtree("amp-data", ignore_errors=True)
# os.remove("resources.zip")

edition_files = glob.glob("data/editions/*.xml")
for file in tqdm(edition_files, total=len(edition_files)):
    doc = TeiReader(file)
    xml_id = (
        doc.tree.getroot()
        .attrib["{http://www.w3.org/XML/1998/namespace}id"]
    )
    item_id = f'{arche_id}auden-musulin-papers/{xml_id}'
    subject_uri = URIRef(item_id)
    create_type_triple(g, subject_uri, ARCHE["Resource"])

# serialize graph
serialize_graph(g, "turtle", "arche_constants.ttl")
print("Done with ARCHE constants. file: arche_constants.ttl")
