# SketchMe API Dokumentation

## Quick Start

Um den Demonstrator zu starten, werden [Docker](https://www.docker.com/get-docker)
und [Docker Compose](https://docs.docker.com/compose/install/) benötigt.
Zum Starten des Projektes muss das Repository lokal geklont und in der Shell
der folgende Command ausgeführt werden:

```
$ docker-compose up
```

Daraufhin ist der Demonstrator unter `http://localhost:8081/#localhost:9000`
verfügbar.

## Backend

Die Dokumentation ist hier verfügbar: [Backend Dokumentation](https://github.com/leolabs/ip-ml-api/blob/master/ip-ml-tensorflow/README.md)

## Frontend

Die Dokumentation ist hier verfügbar: [Frontend](https://github.com/leolabs/ip-ml-frontend/blob/master/README.md)

## Abhängigkeiten

Damit das API lauffähig ist werden folgende Abhängigkeiten benötigt:

* Python3
* numpy

  Library zur Berechnung von mehrdimensionalen Vektoren und Matrizen. Wird von
  SketchMe benötigt zur Verarbeitung der Bilddaten.

* Autobahn

  Library, die das WebSocket Protocol in Python implementiert. Wird von SketchMe
  zur Kommunikation zwischen API und Frontend benötigt.

* PIL

  Library zum Einlesen und Bearbeiten von Bilddaten. Wird von SketchMe benötigt,
  um Bilddaten anzupassen und sie numpy bereitzustellen.

## Erläuterung

Das API implementiert einen WebSocket zum Datenaustausch mit dem Frontend. Es
importiert das Backend und kann auf dessen Funktionalität zugreifen. Konkret
kann das API Zeichnungen vom Frontend als 28x28 bitmap entgegen nehmen
und sie zur Erkennung an das Backend weiterreichen. Die Ergebnisse werden im
JSON-Format ans Frontend geschickt. Im Anschluss kann das Frontend dem Benutzer
anzeigen, als was das Backend die Zeichnung des Benutzers erkannt hat. Das API
übernimmt somit eine Vermittlerrolle zwischen den beiden Instanzen.

## Benutzung

Zum Starten des WebSockets muss die Datei "api_py_websocket.py" mit python3
ausgeführt werden. Von da an wird der WebSocket Anfragen des Frontend-Parts
entgegen nehmen und verarbeiten.
