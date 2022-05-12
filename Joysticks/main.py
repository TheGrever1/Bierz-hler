import os
import time
from pyjoystick.sdl2 import Key, Joystick, run_event_loop
from tinydb import TinyDB, Query

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
        countup("Karlsberg")
        countup("Insgesamt")  # hier drin da es sonst 2x zählt zu faul für fix

    if key == "Button 1" and key.value == 1:  # Bitburger Gelb mit Zettel
        countup("Bitburger")
        countup("Insgesamt")

    if key == "Button 2" and key.value == 1:  # Radler Gelb ohne Zettel
        countup("Radler")
        countup("Insgesamt")

    if key == "Button 3" and key.value == 1:  # AlkFrei Blau
        countup("AlkFrei")
        countup("Insgesamt")

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
