from typing import Literal

from pydantic import BaseModel, Field

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
