# server-starter-lite

REST-API für eine Ressource: User. Eine Datei, `main.py`. Kein Frontend. Keine Datenbank. Der Speicher ist ein Dict.

Beim Start liegen zehn User im Dict, von Ada bis Jens. Jeder hat eine `role` (`dev`, `crm`, `project`, `sales`), ein `created_at` und `hobbies`. Dazu optional `email`. Bei den zehn ist sie gesetzt. Die Hobbys sind `outdoors`, `gaming`, `movies`, `books`, `sports`, `music`, `cooking`, `travel`. Jeder der zehn hat mindestens eines, manche mehrere. Ein Neustart wirft jeden User weg, der danach angelegt wurde, und lädt die zehn wieder.

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

Die Id steht im Pfad, sobald es um einen User geht. Der Body von POST und PUT trägt den Namen und optional `role`, `hobbies` und `email`. Die Id und `created_at` vergibt der Server.

```json
{"name": "Ben", "role": "sales"}
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

## Chat

`app.py` ist der Chat, kein zweiter Server. Er öffnet im Browser. Modell, Schlüssel und die User-API stehen in `.env`. Die Vorlage ist `.env.example`.

```powershell
copy .env.example .env
```

| Name | Bedeutung |
|---|---|
| `USERS_API` | Basis der User-API, Standard `http://127.0.0.1:8000/api/v1` |
| `MODEL_NAME` | Modell bei Ollama, Standard `llama3.2` |
| `MODEL_BASE_URL` | Ollama, Standard `http://127.0.0.1:11434/v1` |
| `MODEL_API_KEY` | Schlüssel, bei Ollama lokal `ollama` |

Fehlt ein Name, gilt derselbe Standard. `python app.py` startet also auch ohne Datei.

Die Aufrufe stehen in `tools.py`. Welche davon das Modell bekommt, steht in `agent.py` in `make_agent`, in der Liste `tools=[...]`. Ein Name, der dort fehlt, ist nicht dabei. Jetzt sind es drei. User nur lesen, gegen diese API. Wetter über Open-Meteo, ohne Schlüssel, bis zu 10 Tage:

- `list_users` — `GET /api/v1/users`
- `get_user` — `GET /api/v1/users/{user_id}`
- `get_weather` — Stadt und Anzahl Tage, zum Beispiel Vienna, 7

Anlegen, Ersetzen und Löschen gibt es hier nicht. Der Verlauf bleibt im Fenster. Oben links steht die Summe aus Prompt- und Antwort-Tokens für dieses Fenster.

`main.py` läuft auf Port 8000. Ollama muss laufen, mit dem Modell aus `MODEL_NAME`.

```powershell
pip install -r requirements.txt
python app.py
```
