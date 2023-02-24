from django.shortcuts import render
from ServeritSanakirja import sanakirja

def index(request):
    freeServers = []
    with open('freeworlds') as f:
        for line in f:
            freeServers.append(int(line.strip()))
    serverit = sanakirja
    return render(request, 'app.html', {'sanakirja': serverit, "freeworlds": freeServers})
