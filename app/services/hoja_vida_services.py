from app.persistencia.crear_tabla_hoja_de_vida import crear_tabla_hojas_vida
from app.persistencia.insertar_hoja_vida import insertar_hoja_vida as insertar_en_tabla
from app.persistencia.obtener_hoja_vida import (
    obtener_hoja_vida as obtener_por_clave,
    obtener_todas_hojas_vida as obtener_todos,
    obtener_hojas_vida_por_documento as obtener_por_doc,
    obtener_hojas_vida_por_rango_fecha as obtener_por_fecha,
    obtener_hojas_vida_por_cod_hoja as obtener_por_cod
)
from app.persistencia.generar_datos_ejemplo import generar_datos_ejemplo as generar_datos


def crear_tabla_hoja_de_vida():
    return crear_tabla_hojas_vida()


def insertar_hoja_vida_service(hoja_vida_data):
    """
    Servicio para insertar una hoja de vida
    """
    return insertar_en_tabla(hoja_vida_data)


def obtener_hoja_vida_service(cod_hoj_vida, documento):
    """
    Servicio para obtener una hoja de vida por sus claves
    """
    return obtener_por_clave(cod_hoj_vida, documento)


def obtener_todas_hojas_vida_service(limite=10, offset=0):
    """
    Servicio para obtener todas las hojas de vida con paginación por offset
    """
    return obtener_todos(limite, offset)


def obtener_hojas_vida_por_documento_service(documento):
    """
    Servicio para obtener hojas de vida por número de documento
    """
    return obtener_por_doc(documento)


def obtener_hojas_vida_por_rango_fecha_service(fecha_inicio, fecha_fin):
    """
    Servicio para obtener hojas de vida dentro de un rango de fechas
    """
    return obtener_por_fecha(fecha_inicio, fecha_fin)


def obtener_hojas_vida_por_cod_hoja_service(cod_hoj_vida, limite=10, page=1):
    """
    Servicio para obtener todos los documentos de un cod_hoja_vida con paginación por página
    """
    return obtener_por_cod(cod_hoj_vida, limite, page)


def generar_datos_ejemplo_service():
    """
    Servicio para generar 40 registros de ejemplo
    """
    return generar_datos()