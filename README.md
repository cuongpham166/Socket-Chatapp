# VSYChatNew

## Server1 starten (Port 5050)
python server.py 

## Server 2 starten (Port 5060)
python server.py 5060

## Client starten
python client.py
Name input
Bei Frage nach Default ja, dann werden die Ports oben verwendet.

## Ausfallsicherheit testen
Server 1 per Konsole ausschalten (cltr+break) dann werden die Nachrichten über den
anderen Server geleitet. Die Nachrichten werden in der Konsole des Server
angezeigt.
