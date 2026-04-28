from fastapi import APIRouter, HTTPException
from app.model.hoja_vida_schema import HojaVidaRequest
from app.services.hoja_vida_services import (
    insertar_hoja_vida_service,
    obtener_hoja_vida_service,
    obtener_hojas_vida_por_documento_service,
    obtener_hojas_vida_por_rango_fecha_service,
    obtener_hojas_vida_por_cod_hoja_service,
    generar_datos_ejemplo_service
)
from app.persistencia.crear_tabla_hoja_de_vida import crear_tabla_hojas_vida

router = APIRouter()


@router.post("/create-table/hoja-vida")
async def create_hoja_vida_table():
    try:
        return crear_tabla_hojas_vida()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generar/datos-ejemplo")
async def generar_datos_ejemplo():
    """
    Genera 40 registros de ejemplo en la tabla HojasVida
    para pruebas de paginación y consultas
    """
    try:
        resultado = generar_datos_ejemplo_service()

        if resultado["success"]:
            return resultado
        else:
            raise HTTPException(status_code=400, detail=resultado["message"])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.post("/new/hoja-vida")
async def insertar_hoja_vida(hoja_vida: HojaVidaRequest):
    """
    Inserta un nuevo registro de hoja de vida
    """
    try:
        resultado = insertar_hoja_vida_service(hoja_vida.dict())

        if resultado["success"]:
            return resultado
        else:
            raise HTTPException(status_code=400, detail=resultado["message"])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/hoja-vida/documento/{documento}")
async def obtener_hojas_vida_por_documento(documento: str):
    """
    Obtiene hojas de vida por número de documento
    """
    try:
        resultado = obtener_hojas_vida_por_documento_service(documento)

        if resultado["success"]:
            return resultado
        else:
            raise HTTPException(status_code=404, detail=resultado["message"])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/hoja-vida/fecha")
async def obtener_hojas_vida_por_fecha(fecha_inicio: str, fecha_fin: str):
    """
    Obtiene hojas de vida dentro de un rango de fechas.
    """
    try:
        resultado = obtener_hojas_vida_por_rango_fecha_service(fecha_inicio, fecha_fin)

        if resultado["success"]:
            return resultado
        else:
            raise HTTPException(status_code=400, detail=resultado["message"])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/hoja-vida/cod/{cod_hoj_vida}")
async def obtener_hojas_vida_por_cod_hoja(cod_hoj_vida: str, limite: int = 10, page: int = 1):
    """
    Obtiene todos los documentos asociados a un cod_hoja_vida con paginación por página
    """
    try:
        resultado = obtener_hojas_vida_por_cod_hoja_service(cod_hoj_vida, limite, page)

        if resultado["success"]:
            return resultado
        else:
            raise HTTPException(status_code=404, detail=resultado["message"])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/hoja-vida/{cod_hoj_vida}/{documento}")
async def obtener_hoja_vida(cod_hoj_vida: str, documento: str):
    """
    Obtiene una hoja de vida por su código y documento
    """
    try:
        resultado = obtener_hoja_vida_service(cod_hoj_vida, documento)

        if resultado["success"]:
            return resultado
        else:
            raise HTTPException(status_code=404, detail=resultado["message"])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
