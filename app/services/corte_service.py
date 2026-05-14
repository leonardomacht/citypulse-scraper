from app.schemas.corte import Corte
from app.core.database import db_manager

class CorteService():
    @staticmethod
    async def process_corte(corte : Corte):
        inicio_key = corte.fecha_inicio.strftime("%Y%m%d%H%M")
        fin_key = corte.fecha_fin.strftime("%Y%m%d%H%M")
        special_key = f"acuacar_{inicio_key}_{fin_key}"
        success = await db_manager.save_if_new(corte.model_dump(), special_key)
    
        return special_key
    
