# server-starter-lite

REST-API für eine Ressource: User. Eine Datei, `main.py`. Kein Frontend. Keine Datenbank. Der Speicher ist ein Dict.

Beim Start liegen zehn User im Dict, von `{"id": 1, "name": "Ada"}` bis `{"id": 10, "name": "Jens"}`. Ein Neustart wirft jeden User weg, der danach angelegt wurde, und lädt die zehn wieder.

In dieser Fassung steht der Vertrag im Vordergrund: Pfad, Methode, Status, Form. Und wo dieser Vertrag in `/docs` steht.

## REST

Der Pfad nennt die Ressource, nicht die Tätigkeit: `/users`.

`/api` hält die Schnittstelle von einer späteren Seite getrennt. `/v1` ist die erste Version. Pfade, Felder und Statuscodes gehören zu dieser Version.

| Absicht | Methode | Pfad | Status |
|---|---|---|---|
| Anlegen | POST | `/api/v1/users` | **201** |
| Alle lesen | GET | `/api/v1/users` | **200** |
| Einen lesen | GET | `/api/v1/users/{user_id}` | **200** |
| Ersetzen | PUT | `/api/v1/users/{user_id}` | **200** |
| Entfernen | DELETE | `/api/v1/users/{user_id}` | **204** |

Die Id steht im Pfad, sobald es um einen User geht. Der Body von POST und PUT trägt nur den Namen. Die Id vergibt der Server.

```json
{"name": "Ben"}
```

GET legt nichts an. PUT ersetzt den ganzen Eintrag, die Id bleibt. DELETE antwortet ohne Body.

Die Formen `User` und `UserBody` sind Pydantic-Modelle in `main.py`. FastAPI macht daraus JSON. Am Feld steht `Field(description=...)`. Das ist der Text unter dem Feld in `/docs`.

## Dokumentation

FastAPI schreibt die Beschreibung beim Start. Keine zweite Datei. Sichtbar unter [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Die Datei dazu ist [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json).

Fünf Ebenen, alle in `main.py`:

1. **App** — `FastAPI(...)`: `title`, `description`, `version`. Steht oben in `/docs`.
2. **Router** — `APIRouter(prefix="/api/v1", tags=["users"])`. Jede Route hängt unter dem Präfix. Der Tag gruppiert die Ressource.
3. **Operation** — am Decorator: `summary`. Das ist die kurze Zeile in der Liste.
4. **Methode** — der Docstring unter der Funktion. Hier steht Markdown: was die Operation tut, der Status, ein JSON-Beispiel.
5. **Feld** — `Field(description=...)` an `UserBody` und `User`. Steht am Schema in `/docs`, unter dem Feld.

Die Ebenen 1 bis 3 und das Feld sind Klartext. Markdown nur im Docstring.

## FastAPI und uvicorn

**FastAPI** baut die Schnittstelle. In `main.py` steht `app`. Was eine Funktion zurückgibt, geht als JSON an den Client. FastAPI öffnet keinen Port.

**uvicorn** ist der Server. Er lädt `app` und nimmt HTTP an.

## Setup

Die Pakete liegen in einer `.venv` in diesem Ordner.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Die Zeile zeigt `(.venv)`. Erst dann ist `uvicorn` da.

## Start

Im Ordner `server-starter-lite/`:

```powershell
uvicorn main:app --reload
```

`main` ist die Datei. `app` ist das Objekt. `--reload` startet neu, wenn `main.py` sich ändert.

- Liste: [http://127.0.0.1:8000/api/v1/users](http://127.0.0.1:8000/api/v1/users)
- Beschreibung: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Im Terminal **Strg+C**. Der Prozess hört auf.
