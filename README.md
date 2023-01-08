# gateway

## Entwicklungsumgebung

```
git clone https://github.com/Projekt-DataScience/gateway.git
cd gateway
```

Optional können die Umgebungsvariablen in der Datei "env" angepasst werden.

Für eine einfache Entwicklung werden die anderen Services benötigt, dafür existiert die docker-compose.yml Datei. Die Umgebung kann mit dem folgenden Kommando gestartet werden:

```
docker-compose up
```

# Ausführen der Tests
Damit die Tests funktioniert muss zuvor die Testumgebung mittels docker-compose deployed sein:
```
docker-compose up
```


Zum Ausführen der Tests wird pytest verwendet:

```
pytest tests
```

Anforderungen installlieren:

```
python -m virtualenv venv
venv\Scripts\activate
pip install -r requirements.txt
```
