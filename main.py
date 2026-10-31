from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field
from fastapi import APIRouter, FastAPI, HTTPException

Role = Literal["dev", "crm", "project", "sales"]
Hobby = Literal[
    "outdoors",
    "gaming",
    "movies",
    "books",
    "sports",
    "music",
    "cooking",
    "travel",
]

app = FastAPI(
    title="Users",
    version="0.1.0",
    description="REST-API für die Ressource User. Eine Version: `/api/v1`. Speicher ist ein Dictionary.",
)

router = APIRouter(prefix="/api/v1", tags=["User"])


class UserBody(BaseModel):
    name: str = Field(description="Name. Pflicht.")
    role: Role | None = Field(
        default=None,
        description="Optional. Eine von dev, crm, project, sales.",
    )
    hobbies: list[Hobby] | None = Field(
        default=None,
        description="Optional. Mehrere möglich: outdoors, gaming, movies, books, sports, music, cooking, travel.",
    )
    email: str | None = Field(
        default=None,
        description="Optional. Adresse des Users.",
    )


class User(BaseModel):
    id: int = Field(description="Vergibt der Server. Steht im Pfad, sobald es um einen User geht.")
    name: str = Field(description="Name des Users.")
    role: Role | None = Field(
        default=None,
        description="Optional. dev, crm, project oder sales.",
    )
    created_at: str | None = Field(
        default=None,
        description="Vergibt der Server. Optional. Eine Schreibweise: created_at.",
    )
    hobbies: list[Hobby] | None = Field(
        default=None,
        description="Optional. Mindestens eines bei den zehn. Mehrere möglich.",
    )
    email: str | None = Field(
        default=None,
        description="Optional. Bei den zehn gesetzt.",
    )


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


users: dict[int, User] = {
    1: User(id=1, name="Ada", role="dev", created_at="2026-10-02T08:14:00Z", hobbies=["cooking", "books", "movies"], email="ada.klein@example.com"),
    2: User(id=2, name="Berta", role="crm", created_at="2026-10-03T09:41:00Z", hobbies=["sports"], email="berta.huber@example.com"),
    3: User(id=3, name="Chris", role="project", created_at="2026-10-06T11:05:00Z", hobbies=["outdoors", "travel", "books"], email="chris.wagner@example.com"),
    4: User(id=4, name="Dora", role="sales", created_at="2026-10-08T14:22:00Z", hobbies=["gaming"], email="dora.bauer@example.com"),
    5: User(id=5, name="Emil", role="dev", created_at="2026-10-11T16:03:00Z", hobbies=["gaming", "movies", "music"], email="emil.gruber@example.com"),
    6: User(id=6, name="Fritz", role="crm", created_at="2026-10-14T08:55:00Z", hobbies=["gaming"], email="fritz.steiner@example.com"),
    7: User(id=7, name="Greta", role="project", created_at="2026-10-17T10:18:00Z", hobbies=["sports", "cooking"], email="greta.mayer@example.com"),
    8: User(id=8, name="Hans", role="sales", created_at="2026-10-20T13:47:00Z", hobbies=["books", "cooking"], email="hans.fischer@example.com"),
    9: User(id=9, name="Ida", role="dev", created_at="2026-10-23T15:09:00Z", hobbies=["gaming", "sports", "books", "travel"], email="ida.berger@example.com"),
    10: User(id=10, name="Jens", role="crm", created_at="2026-10-28T09:33:00Z", hobbies=["outdoors"], email="jens.hofer@example.com"),
}
next_id = 11


@router.post("/users", status_code=201, summary="User anlegen")
def create_user(body: UserBody) -> User:
    """Legt einen User an.

    Die Id und `created_at` vergibt der Server. `role`, `hobbies` und `email` sind optional.

    ```json
    {"name": "Ben", "role": "sales", "hobbies": ["books", "gaming"]}
    ```

    Antwort **201**:

    ```json
    {"id": 11, "name": "Ben", "role": "sales", "created_at": "2026-10-31T13:00:00Z", "hobbies": ["books", "gaming"]}
    ```
    """
    global next_id
    user = User(
        id=next_id,
        name=body.name,
        role=body.role,
        created_at=now_iso(),
        hobbies=body.hobbies,
        email=body.email,
    )
    users[user.id] = user
    next_id += 1
    return user


@router.get("/users", summary="Alle User lesen")
def list_users() -> list[User]:
    """Liest die Ressource. Legt nichts an.

    Antwort **200**, eine Liste:

    ```json
    [{"id": 1, "name": "Ada", "role": "dev", "created_at": "2026-10-02T08:14:00Z", "hobbies": ["cooking", "books", "movies"], "email": "ada.klein@example.com"}]
    ```
    """
    return list(users.values())


@router.get("/users/{user_id}", summary="Einen User lesen")
def read_user(user_id: int) -> User:
    """Liest einen User. Die Id steht im Pfad.

    Antwort **200**:

    ```json
    {"id": 1, "name": "Ada", "role": "dev", "created_at": "2026-10-02T08:14:00Z", "hobbies": ["cooking", "books", "movies"], "email": "ada.klein@example.com"}
    ```
    """
    if user_id in users:
        return users[user_id]
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/users/{user_id}", summary="User ersetzen")
def replace_user(user_id: int, body: UserBody) -> User:
    """    Ersetzt den Eintrag. Die Id und `created_at` bleiben. `role`, `hobbies` und `email` nur, wenn der Body sie trägt.

    Body:

    ```json
    {"name": "Cleo", "role": "project", "hobbies": ["sports"]}
    ```

    Antwort **200**:

    ```json
    {"id": 1, "name": "Cleo", "role": "project", "created_at": "2026-10-02T08:14:00Z", "hobbies": ["sports"]}
    ```
    """
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    current = users[user_id]
    user = User(
        id=current.id,
        name=body.name,
        role=body.role if body.role is not None else current.role,
        created_at=current.created_at,
        hobbies=body.hobbies if body.hobbies is not None else current.hobbies,
        email=body.email if body.email is not None else current.email,
    )
    users[user_id] = user
    return user


@router.delete("/users/{user_id}", status_code=204, summary="User löschen")
def delete_user(user_id: int) -> None:
    """Entfernt den User. Die Id steht im Pfad.

    Antwort **204**. Kein Body.
    """
    del users[user_id]


app.include_router(router)
