import platform
import subprocess
import threading
from threading import Thread, Lock
from queue import Queue
import time

kaikkiServerit = range(1, 277, 1)
serverit = []
sanakirja = {}
threadMaara = 20
jonotus = Queue()
lukko = Lock()

def lahetetaanPing(serveri: int) -> str:
    host = (f"oldschool{serveri}.runescape.com")
    parametri = '-n' if platform.system().lower() == 'windows' else '-c'
    komento = ['ping', parametri, '1', host]
    vastaus = subprocess.run(komento, stdout=subprocess.PIPE, text=True)

    return vastaus.stdout

def kirjoitetaanTiedostoon(server: int, answer: str):
    f = open("venv/tallennetut.txt", "w")
    f.write(answer)
    f.close()

    f = open("venv/tallennetut.txt", "r")
    file = f.readlines()
    for line in file:
        if "Average" in line:
            serv = server + 300
            pingSanakirjaan(serv, line)

def pingSanakirjaan(servu: int, ping: str):
    pingLinja = ping.split(" ")
    pelkkaPing = (pingLinja[-1])
    pelkkaPing = pelkkaPing.replace("m", "")
    pelkkaPing = pelkkaPing.replace("s", "")
    pelkkaPing = pelkkaPing.replace("/", "")
    pelkkaPing = pelkkaPing.replace("n", "")
    pelkkaPing = pelkkaPing.replace("=", "")
    average = int(pelkkaPing)
    sanakirja[servu] = average
    sorted_items = sorted(sanakirja.items())
    sanakirja.clear()
    sanakirja.update(sorted_items)

def toiminta(world: int):
    tallennus = lahetetaanPing(world)
    with lukko:
        kirjoitetaanTiedostoon(world, tallennus)

def thread():
    global jonotus
    while True:
        worker = jonotus.get()
        toiminta(worker)
        jonotus.task_done()

def threadAloitus(serverit):
    global jonotus
    for x in range(threadMaara):
        x = Thread(target=thread)
        x.daemon = True
        x.start()
    for x in serverit:
        jonotus.put(x)
    jonotus.join()

def alku():
    while True:
        threadAloitus(kaikkiServerit)
        time.sleep(10)

t1 = threading.Thread(target=alku)
t1.start()