import os
import time
from pyjoystick.sdl2 import Key, Joystick, run_event_loop
from tinydb import TinyDB, Query

import pymsteams


def msg(name: str):
    myTeamsMessage = pymsteams.connectorcard("https://hypoportsystems.webhook.office.com/webhookb2/aade4e90-7a75-45df-9c84-66bbb7fbbd01@8899db84-419b-4a2f-a612-4b819ec57add/IncomingWebhook/2f39b69d9bcc486dbc0a3a94ac114910/641a193c-43e2-445b-9b6b-f1e26a9bec6f")
    myTeamsMessage.text(name + " auffüllen")
    myTeamsMessage.send()


db = TinyDB("db.json")
Bier = Query()


def print_add(joy):
    print("Added", joy)


def print_remove(joy):
    print("Removed", joy)


def countup(name: str):
    data = db.get(Bier.name == name)
    value = data["quantity"]
    db.update({"quantity": value + 1}, Bier.name == name)


def reset(name: str):
    db.update({"quantity": 0}, Bier.name == name)


def key_received(key):

    if key == "Button 0" and key.value == 1:  # Grün Urplis
        name = "Karlsberg"
        countup(name)
        countup("Insgesamt")  # hier drin da es sonst 2x zählt zu faul für fix
        if db.get(Bier.name == name)["quantity"] == 10:
            msg(name)

    if key == "Button 1" and key.value == 1:  # Bitburger Gelb mit Zettel
        name = "Bitburger"
        countup(name)
        countup("Insgesamt")
        if db.get(Bier.name == name)["quantity"] == 10:
            msg(name)

    if key == "Button 2" and key.value == 1:  # Radler Gelb ohne Zettel
        name = "Radler"
        countup(name)
        countup("Insgesamt")
        if db.get(Bier.name == name)["quantity"] == 10:
            msg(name)

    if key == "Button 3" and key.value == 1:  # AlkFrei Blau
        name = "Alkfrei"
        countup(name)
        countup("Insgesamt")
        if db.get(Bier.name == name)["quantity"] == 10:
            msg(name)

    if key == "Button 4" and key.value == 1:  # Rot Emergency
        print(key)

    if key == "Button 4" and key == "Button 3" and key.value == 1:  # Reset Alkfrei
        reset("AlkFrei")

    if key == "Button 4" and key == "Button 2" and key.value == 1:  # Reset Radler
        reset("Radler")

    if key == "Button 4" and key == "Button 1" and key.value == 1:  # Reset Bitburger
        reset("Bitburger")

    if key == "Button 4" and key == "Button 0" and key.value == 1:  # Reset Karlsberg
        reset("Karlsberg")

    time.sleep(0.5)


run_event_loop(print_add, print_remove, key_received)
