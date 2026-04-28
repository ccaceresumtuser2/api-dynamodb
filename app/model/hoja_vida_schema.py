from pydantic import BaseModel

class HojaVidaRequest(BaseModel):
    cod_hoj_vida: str
    documento: str
    fecha: str
    nombre_apellido: str
    key_s3: str