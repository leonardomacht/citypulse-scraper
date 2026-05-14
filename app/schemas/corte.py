from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from app.schemas.programacion import Programacion

class Corte(BaseModel):
    tipo_servicio: str 
    programaciones : list[Programacion]
    fecha_inicio: datetime
    fecha_fin: Optional[datetime]
    descripcion: str
    fuente: str        