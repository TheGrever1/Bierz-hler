import os
import time
from pyjoystick.sdl2 import Key, Joystick, run_event_loop
from tinydb import TinyDB, Query

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def mail(name: str):
    # Serverdaten
    #smtpServer = "smtp.gmail.com"#"pim.hypoport.de"
    #smtpPort = 587
    mailserver = smtplib.SMTP('pim.hypoport.de', '25')

    # Zugangsdaten
    username = ""
    password = ""

    # Sender & Empfänger
    sender = ""
    reciever = ""

    # Betreff & Inhalt
    subject = "BierKühlschrank"
    body = name + " Auffüllen"

    # Message Objekt für die E-Mail
    # später kann an dieses Objekt eine
    # oder mehrere Dateien angehängt
    # werden.
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = reciever

    part = MIMEText(body, 'plain')
    msg.attach(part)

    # Erzeugen einer Mail Session
    smtpObj = smtplib.SMTP(mailserver)
    # Debuginformationen auf der Konsole ausgeben
    smtpObj.set_debuglevel(1)
    # Wenn der Server eine Authentifizierung benötigt dann...
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(username, password)

    # absenden der E-Mail
    smtpObj.sendmail(sender, reciever, msg.as_string())


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
            mail(name)

    if key == "Button 1" and key.value == 1:  # Bitburger Gelb mit Zettel
        name = "Bitburger"
        countup(name)
        countup("Insgesamt")
        if db.get(Bier.name == name)["quantity"] == 10:
            mail(name)

    if key == "Button 2" and key.value == 1:  # Radler Gelb ohne Zettel
        name = "Radler"
        countup(name)
        countup("Insgesamt")
        if db.get(Bier.name == name)["quantity"] == 10:
            mail(name)

    if key == "Button 3" and key.value == 1:  # AlkFrei Blau
        name = "Alkfrei"
        countup(name)
        countup("Insgesamt")
        if db.get(Bier.name == name)["quantity"] == 10:
            mail(name)

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
