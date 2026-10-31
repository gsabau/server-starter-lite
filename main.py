from pydantic import BaseModel, Field
from fastapi import APIRouter, FastAPI, HTTPException

app = FastAPI(
    title="Users",
    version="0.1.0",
    description="REST-API für die Ressource User. Eine Version: `/api/v1`. Speicher ist ein Dictionary.",
)

router = APIRouter(prefix="/api/v1", tags=["User"])


class UserBody(BaseModel):
    name: str = Field(description="Name. Der Body von POST und PUT trägt nur dieses Feld.")


class User(BaseModel):
    id: int = Field(description="Vergibt der Server. Steht im Pfad, sobald es um einen User geht.")
    name: str = Field(description="Name des Users.")

users: dict[int, User] = {
    1: User(id=1, name="Ada"),
    2: User(id=2, name="Berta"),
    3: User(id=3, name="Chris"),
    4: User(id=4, name="Dora"),
    5: User(id=5, name="Emil"),
    6: User(id=6, name="Fritz"),
    7: User(id=7, name="Greta"),
    8: User(id=8, name="Hans"),
    9: User(id=9, name="Ida"),
    10: User(id=10, name="Jens"),
}
next_id = 11


@router.post("/users", status_code=201, summary="User anlegen")
def create_user(body: UserBody) -> User:
    """Legt einen User an.

    Die Id vergibt der Server. Der Body trägt nur `name`.

    ```json
    {"name": "Ben"}
    ```

    Antwort **201**:

    ```json
    {"id": 11, "name": "Ben"}
    ```
    """
    global next_id
    user = User(id=next_id, name=body.name)
    users[user.id] = user
    next_id += 1
    return user


@router.get("/users", summary="Alle User lesen")
def list_users() -> list[User]:
    """Liest die Ressource. Legt nichts an.

    Antwort **200**, eine Liste:

    ```json
    [{"id": 1, "name": "Ada"}]
    ```
    """
    return list(users.values())


@router.get("/users/{user_id}", summary="Einen User lesen")
def read_user(user_id: int) -> User:
    """Liest einen User. Die Id steht im Pfad.

    Antwort **200**:

    ```json
    {"id": 1, "name": "Ada"}
    ```
    """
    if user_id in users:
        return users[user_id]
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/users/{user_id}", summary="User ersetzen")
def replace_user(user_id: int, body: UserBody) -> User:
    """Ersetzt den Eintrag. Die Id bleibt die aus dem Pfad.

    Body:

    ```json
    {"name": "Cleo"}
    ```

    Antwort **200**:

    ```json
    {"id": 1, "name": "Cleo"}
    ```
    """
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    current = users[user_id]
    user = User(id=current.id, name=body.name)
    users[user_id] = user
    return user


@router.delete("/users/{user_id}", status_code=204, summary="User löschen")
def delete_user(user_id: int) -> None:
    """Entfernt den User. Die Id steht im Pfad.

    Antwort **204**. Kein Body.
    """
    del users[user_id]


app.include_router(router)
