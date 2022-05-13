import random
import time
from pygame import key
from pygame import mixer
from pyjoystick.sdl2 import Key, Joystick, run_event_loop
from tinydb import TinyDB, Query

import pymsteams

import playsound


def msg(name: str):
    myTeamsMessage = pymsteams.connectorcard("https://hypoportsystems.webhook.office.com/webhookb2/aade4e90-7a75-45df-9c84-66bbb7fbbd01@8899db84-419b-4a2f-a612-4b819ec57add/IncomingWebhook/2f39b69d9bcc486dbc0a3a94ac114910/641a193c-43e2-445b-9b6b-f1e26a9bec6f")
    myTeamsMessage.text(name + " auffüllen")
    #myTeamsMessage.send()


db = TinyDB("db.json")
Bier = Query()
keyAlt = 0

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

def switch_urpils(argument):
    switcher = {
        1: "139-item-catch.mp3",
        2: "anime-wow-sound-effect-mp3cut.mp3",
        3: "auf-alkohol.mp3",
        4: "ballern-dropin.mp3",
        5: "boomheadshot.swf.mp3",
        6: "ha-bier.mp3",
        7: "hello-its-john-cena.mp3",
        8: "i-will-send-you-to-jesus-steven-he.mp3",
        9: "ich-bin-der-uwe-ich-bin-auch-dabei.mp3",
        10: "klarersieger.mp3",
        11: "lets-go-meme.mp3",
        12: "pink-fluffy-unicorns.mp3",
        13: "pokemon-german.mp3",
        14: "tmpdbnm_5a3.mp3",
        15: "tralala_1.mp3",
        16: "was-geht-aaaaaaaab.mp3"
    }
    return str(switcher.get(argument))

def switch_noturpils(argument):
    switcher = {
        1: "an-diesem-tisch-wird-nicht-gelogen.mp3",
        2: "arbeitslos.mp3",
        3: "boar-ich-krieg-gansehaut-vor-cringe.mp3",
        4: "classic_hurt.mp3",
        5: "drohoefter-polier-dir-die-fresse.mp3",
        6: "du-dreckiger-hurensohn.mp3",
        7: "durchfall_01.mp3",
        8: "elotrix-oh-nein.mp3",
        9: "facebook-video-1419170238098335.mp3",
        10: "fbi-open-up-sfx.mp3",
        11: "green-screen-windwos-xp-error-virus-error-footage-sound.mp3",
        12: "hurensohne.mp3",
        13: "ich-bin-der-uwe-ich-bin-auch-dabei.mp3",
        14: "in-die-fresse.mp3",
        15: "inglourious-basterds-hitler-funny.mp3",
        16: "jetzt-bekommt-ihr-arger.mp3",
        17: "kuckuck-du-klein-schlampe.mp3",
        18: "lesbische-nazinutten.mp3",
        19: "little-britain-usa-computer-sagt-nein-mp3cut.mp3",
        20: "na-na-du-hurensohn.mp3",
        21: "nicht-so-tief-rudiger.mp3",
        22: "no-god-please-no-noooooooooo.mp3",
        23: "ob-du-behindert-bist.mp3",
        24: "raus_mit_die_viecher.mp3",
        25: "sieht-nicht-gut-aus.mp3",
        26: "spongebob-fail.mp3",
        27: "werner-bist-du-blod.mp3",
        28: "you_were_banned_2.mp3"
    }
    return str(switcher.get(argument))

def play_sound(name: str):
    mixer.init()
    if name == "Karlsberg":
        sound = mixer.Sound(switch_urpils(random.randint(1, 16)))
        sound.play()
        time.sleep(sound.get_length())
        sound.stop()
    elif name == "Bitburger" or name == "Radler" or name == "AlkFrei":
        sound = mixer.Sound(switch_noturpils(random.randint(1, 28)))
        sound.play()
        time.sleep(sound.get_length())
        sound.stop()


def key_received(key):

    if key == "Button 0" and key.value == 1:  # Grün Urplis
        name = "Karlsberg"
        countup(name)
        play_sound(name)
        countup("Insgesamt")  # hier drin da es sonst 2x zählt zu faul für fix
        if db.get(Bier.name == name)["quantity"] == 10:
            msg(name)


    if key == "Button 1" and key.value == 1:  # Bitburger Gelb mit Zettel
        name = "Bitburger"
        countup(name)
        countup("Insgesamt")
        play_sound(name)
        if db.get(Bier.name == name)["quantity"] == 10:
            msg(name)

    if key == "Button 2" and key.value == 1:  # Radler Gelb ohne Zettel
        name = "Radler"
        countup(name)
        countup("Insgesamt")
        play_sound(name)
        if db.get(Bier.name == name)["quantity"] == 10:
            msg(name)

    if key == "Button 3" and key.value == 1:  # AlkFrei Blau
        name = "AlkFrei"
        countup(name)
        countup("Insgesamt")
        play_sound(name)
        if db.get(Bier.name == name)["quantity"] == 10:
            msg(name)

    if keyAlt == "Button 4":
        keyAlt = ""
        if key == "Button 4" and key.value == 1:
            reset("insgesamt")
            reset("Karlsberg")
            reset("Bitburger")
            reset("Radler")
            reset("AlkFrei")

    if key == "Button 4" and key.value == 1:
        if keyAlt == "":
            keyAlt = "Button 4"

    if key == "Button 4" and key == "Button 3" and key.value == 1:  # Reset Alkfrei
        reset("AlkFrei")

    if key == "Button 4" and key == "Button 2" and key.value == 1:  # Reset Radler
        reset("Radler")

    if key == "Button 4" and key == "Button 1" and key.value == 1:  # Reset Bitburger
        reset("Bitburger")

    if key == "Button 4" and key == "Button 0" and key.value == 1:  # Reset Karlsberg
        reset("Karlsberg")

    time.sleep(0.5)

    keyAlt=key
run_event_loop(print_add, print_remove, key_received)
