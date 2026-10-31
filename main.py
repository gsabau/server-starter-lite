from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field
from fastapi import APIRouter, FastAPI, HTTPException

Role = Literal["dev", "crm", "project", "sales"]

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


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


users: dict[int, User] = {
    1: User(id=1, name="Ada", role="dev", created_at="2026-10-02T08:14:00Z"),
    2: User(id=2, name="Berta", role="crm", created_at="2026-10-03T09:41:00Z"),
    3: User(id=3, name="Chris", role="project", created_at="2026-10-06T11:05:00Z"),
    4: User(id=4, name="Dora", role="sales", created_at="2026-10-08T14:22:00Z"),
    5: User(id=5, name="Emil", role="dev", created_at="2026-10-11T16:03:00Z"),
    6: User(id=6, name="Fritz", role="crm", created_at="2026-10-14T08:55:00Z"),
    7: User(id=7, name="Greta", role="project", created_at="2026-10-17T10:18:00Z"),
    8: User(id=8, name="Hans", role="sales", created_at="2026-10-20T13:47:00Z"),
    9: User(id=9, name="Ida", role="dev", created_at="2026-10-23T15:09:00Z"),
    10: User(id=10, name="Jens", role="crm", created_at="2026-10-28T09:33:00Z"),
}
next_id = 11


@router.post("/users", status_code=201, summary="User anlegen")
def create_user(body: UserBody) -> User:
    """Legt einen User an.

    Die Id und `created_at` vergibt der Server. `role` ist optional.

    ```json
    {"name": "Ben", "role": "sales"}
    ```

    Antwort **201**:

    ```json
    {"id": 11, "name": "Ben", "role": "sales", "created_at": "2026-10-31T13:00:00Z"}
    ```
    """
    global next_id
    user = User(id=next_id, name=body.name, role=body.role, created_at=now_iso())
    users[user.id] = user
    next_id += 1
    return user


@router.get("/users", summary="Alle User lesen")
def list_users() -> list[User]:
    """Liest die Ressource. Legt nichts an.

    Antwort **200**, eine Liste:

    ```json
    [{"id": 1, "name": "Ada", "role": "dev", "created_at": "2026-10-02T08:14:00Z"}]
    ```
    """
    return list(users.values())


@router.get("/users/{user_id}", summary="Einen User lesen")
def read_user(user_id: int) -> User:
    """Liest einen User. Die Id steht im Pfad.

    Antwort **200**:

    ```json
    {"id": 1, "name": "Ada", "role": "dev", "created_at": "2026-10-02T08:14:00Z"}
    ```
    """
    if user_id in users:
        return users[user_id]
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/users/{user_id}", summary="User ersetzen")
def replace_user(user_id: int, body: UserBody) -> User:
    """    Ersetzt den Eintrag. Die Id und `created_at` bleiben. `role` nur, wenn der Body sie trägt.

    Body:

    ```json
    {"name": "Cleo", "role": "project"}
    ```

    Antwort **200**:

    ```json
    {"id": 1, "name": "Cleo", "role": "project", "created_at": "2026-10-02T08:14:00Z"}
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
