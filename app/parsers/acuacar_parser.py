from datetime import datetime

from bs4 import BeautifulSoup
from lxml import etree
import re

from app.schemas.corte import Corte
from app.schemas.programacion import Programacion

class AcuacarParser:
    @staticmethod
    def parse_html(html_content: str) -> Corte:
        soup = BeautifulSoup(html_content, 'lxml')
        dom = etree.HTML(html_content)
        fechas = dom.xpath("//button[@role='tab']//span[text()]")
        cortes = dom.xpath("//div[@class='mt-5']")
        informacion = dom.xpath("//div[div[text()='Atención']]")
        programaciones : list[Programacion] = []
        descripcion = soup.select("p")[0].text

        fechaInicio = "" 
        fechaFin = ""
       
        for i in range(0, len(cortes)):
            if i == 0:
                fechaInicio = AcuacarParser.get_date_formatted(fechas[i].text)
            elif i == (len(cortes) - 1 ):
                fechaFin = AcuacarParser.get_date_formatted(fechas[i].text)

            barrios = []
            raw_horario = informacion[i].xpath("./p/text()")
            raw_barrios = cortes[i].xpath(".//span/div[normalize-space()]")
            for raw_barrio in raw_barrios:
                barrios.append(raw_barrio.text)

            raw_data ={
                "fecha": AcuacarParser.get_date_formatted(fechas[i].text),
                "horario" : AcuacarParser.get_hours(raw_horario),
                "barrios" : barrios
            }
            programacion = Programacion(**raw_data)
            programaciones.append(programacion)
        
        print()

        raw_data = {
            "tipo_servicio" : "agua",
            "programaciones": programaciones,
            "fecha_inicio" : fechaInicio,
            "fecha_fin" : fechaFin,
            "descripcion" : descripcion,
            "fuente" : "acuacar"   
        }

        corte = Corte(**raw_data)
        
        return corte

    @staticmethod
    def get_hours(hours : list[str]) -> str:
        texto = hours[0]
        match = re.search(r'Horario:\s*(.+)', texto)

        if match:
            horario = match.group(1).strip()
            return horario
        else:
            return "" 

    @staticmethod
    def get_date_formatted(text : str) -> datetime:
        meses = {
            "ENERO": 1, "FEBRERO": 2, "MARZO": 3, "ABRIL": 4,
            "MAYO": 5, "JUNIO": 6, "JULIO": 7, "AGOSTO": 8,
            "SEPTIEMBRE": 9, "OCTUBRE": 10, "NOVIEMBRE": 11, "DICIEMBRE": 12
        }

        limpio = text.split("(")[0].strip()  
        partes = limpio.split(" DE ")         

        dia, mes, año = int(partes[0]), meses[partes[1]], int(partes[2])
        resultado = f"{año}-{mes:02d}-{dia:02d}"
        return datetime.strptime(resultado, "%Y-%m-%d") 


   