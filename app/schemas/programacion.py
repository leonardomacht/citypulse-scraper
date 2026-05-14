from datetime import datetime

from pydantic import BaseModel


class Programacion(BaseModel):
    fecha : datetime
    horario: str
    barrios: list[str]