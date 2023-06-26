from app.models.message import Message, save_message, find_by_user_id
from wit import Wit
import os
from unidecode import unidecode


def save_message(json_data, user_id):
    content = json_data["content"]

    client = Wit(os.getenv("SERVER_ACCESS_TOKEN"))
    data = client.get_message(content)

    if "intent" in data["outcomes"][0]["entities"]:
        intents = data["outcomes"][0]["entities"]["intent"]

    intent = ""
    if len(intents) > 0:
        intent = intents[0]

    entities = []
    keys = data["outcomes"][0]["entities"].keys()
    for key in keys:
        if key != "intent":
            for obj in data["outcomes"][0]["entities"][key]:
                split_key = key.split(":")
                entity = {
                    "value": obj["value"],
                    "entity": split_key[0] if len(split_key) > 0 else key
                }

                entities.append(entity)

    new_message = Message(id="",content=content, intent=intent, entities=entities, user_id=user_id)

    _id = save_message(new_message)
    dict_message = new_message.__dict__
    dict_message["id"] = _id
    
    return {
        "data": dict_message,
        "status": 201
    }


def get_messages(user_id):
    messages = find_by_user_id(user_id)
    print("messages::", messages)

    res_messages = []
    
    for message in messages:
        print("content::", message["content"])
        message["id"] = str(message["_id"])
        message["_id"] = str(message["_id"])
        res_messages.append(message)

    return {
        "data": res_messages,
        "status": 200
    }


def predict_keyword(keyword):
    client = Wit(os.getenv("SERVER_ACCESS_TOKEN"))
    data = client.get_message(keyword)
    keywords = []

    intents = []
    if "intent" in data["outcomes"][0]["entities"]:
        intents = data["outcomes"][0]["entities"]["intent"]
    entities = []
    keys = data["outcomes"][0]["entities"].keys()
    for key in keys:
        if key != "intent":
            for obj in data["outcomes"][0]["entities"][key]:
                split_key = key.split(":")
                split_value = unidecode(obj["value"]).lower().split(" ")
                for value in split_value:
                    keywords.append(value)
                entity = {
                    "value": obj["value"],
                    "entity": split_key[0] if len(split_key) > 0 else key
                }

                entities.append(entity)

    return {
        "intents": intents,
        "entities": entities,
        "keywords": keywords,
        "intent": intents[0]["value"] if len(intents) > 0 else ""
    }


def get_keywords(entities):
    keywords = []
    for entity in entities:
        split_value = unidecode(entity["value"]).lower().split(" ")
        for value in split_value:
            print("value",value)
            keywords.append(value)
    print("keywords",keywords)

    return keywords