import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Attr
from app.config.conexion_aws import conexion_aws_boto3

dynamodb = conexion_aws_boto3()

def obtener_hoja_vida(cod_hoj_vida, documento):
    """
    Obtiene un registro de la tabla HojasVida por su clave primaria
    
    Args:
        cod_hoj_vida: Código de la hoja de vida (HASH key)
        documento: Número de documento (RANGE key)
        
    Returns:
        dict: {"success": True/False, "message": str, "data": item}
    """
    try:
        table = dynamodb.Table('HojasVida')
        
        response = table.get_item(
            Key={
                'cod_hoj_vida': cod_hoj_vida,
                'documento': documento
            }
        )
        
        if 'Item' in response:
            print(f"✅ Hoja de vida encontrada")
            return {
                "success": True,
                "message": "Hoja de vida encontrada",
                "data": response['Item']
            }
        else:
            print(f"⚠️ Hoja de vida no encontrada")
            return {
                "success": False,
                "message": "Hoja de vida no encontrada"
            }
            
    except Exception as e:
        print(f"❌ Error al obtener hoja de vida: {str(e)}")
        return {
            "success": False,
            "message": f"Error al obtener hoja de vida: {str(e)}"
        }


def obtener_todas_hojas_vida(limite=10, offset=0):
    """
    ⚠️ NOTA: Esta función no está disponible sin parámetros de búsqueda
    para evitar operaciones SCAN costosas en DynamoDB.
    
    Usa los siguientes endpoints en lugar:
    - GET /hoja-vida/{cod_hoj_vida}/{documento} - Por claves primarias
    - GET /hoja-vida/documento/{documento} - Por documento
    
    Args:
        limite: Número máximo de registros a retornar
        offset: Número de registros a saltar
        
    Returns:
        dict: {"success": False, "message": str}
    """
    return {
        "success": False,
        "message": "SCAN no permitido por ser costoso en DynamoDB. Usa endpoints específicos: /hoja-vida/{cod_hoj_vida}/{documento} o /hoja-vida/documento/{documento}"
    }


def obtener_hojas_vida_por_documento(documento):
    """
    Obtiene registros de hoja de vida por número de documento usando el índice secundario
    
    Args:
        documento: Número de documento a buscar
        
    Returns:
        dict: {"success": True/False, "message": str, "data": items, "count": int}
    """
    try:
        table = dynamodb.Table('HojasVida')
        
        response = table.query(
            IndexName='documento-index',
            KeyConditionExpression='documento = :doc',
            ExpressionAttributeValues={
                ':doc': documento
            }
        )
        
        items = response.get('Items', [])
        
        if items:
            print(f"✅ Se encontraron {len(items)} registros para el documento {documento}")
            return {
                "success": True,
                "message": f"Se encontraron {len(items)} registros",
                "data": items,
                "count": len(items)
            }
        else:
            print(f"⚠️ No se encontraron registros para el documento {documento}")
            return {
                "success": False,
                "message": f"No se encontraron registros para el documento {documento}"
            }
            
    except Exception as e:
        print(f"❌ Error al obtener hojas de vida por documento: {str(e)}")
        return {
            "success": False,
            "message": f"Error al obtener hojas de vida por documento: {str(e)}"
        }


def obtener_hojas_vida_por_rango_fecha(fecha_inicio, fecha_fin):
    """
    Obtiene registros de hoja de vida dentro de un rango de fechas.

    Args:
        fecha_inicio: Fecha inicial (inclusive) en formato ISO 8601, por ejemplo '2026-04-01'
        fecha_fin: Fecha final (inclusive) en formato ISO 8601, por ejemplo '2026-04-30'

    Returns:
        dict: {"success": True/False, "message": str, "data": items, "count": int}
    """
    try:
        try:
            fecha_inicio_dt = datetime.fromisoformat(fecha_inicio)
            fecha_fin_dt = datetime.fromisoformat(fecha_fin)
        except ValueError:
            return {
                "success": False,
                "message": "Formato de fecha inválido. Use ISO 8601, por ejemplo '2026-04-01' o '2026-04-01T00:00:00'"
            }

        if fecha_inicio_dt > fecha_fin_dt:
            return {
                "success": False,
                "message": "La fecha de inicio no puede ser mayor que la fecha de fin"
            }

        table = dynamodb.Table('HojasVida')
        scan_kwargs = {
            'FilterExpression': Attr('fecha').between(fecha_inicio, fecha_fin)
        }

        items = []
        response = table.scan(**scan_kwargs)
        items.extend(response.get('Items', []))

        while 'LastEvaluatedKey' in response:
            response = table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey'],
                **scan_kwargs
            )
            items.extend(response.get('Items', []))

        print(f"✅ Se encontraron {len(items)} registros entre {fecha_inicio} y {fecha_fin}")
        return {
            "success": True,
            "message": f"Se encontraron {len(items)} registros entre {fecha_inicio} y {fecha_fin}",
            "data": items,
            "count": len(items)
        }
    except Exception as e:
        print(f"❌ Error al obtener hojas de vida por rango de fecha: {str(e)}")
        return {
            "success": False,
            "message": f"Error al obtener hojas de vida por rango de fecha: {str(e)}"
        }


def obtener_hojas_vida_por_cod_hoja(cod_hoj_vida, limite=10, page=1):
    """
    Obtiene registros asociados a un cod_hoj_vida usando query paginada por página
    
    Args:
        cod_hoj_vida: Código de hoja de vida (HASH key)
        limite: Número máximo de registros a retornar (default: 10, máximo: 100)
        page: Número de página (1-indexed)
        
    Returns:
        dict: {
            "success": True/False, 
            "message": str, 
            "data": items, 
            "count": int,
            "cod_hoja_vida": str,
            "page": int,
            "limite": int,
            "tiene_mas": bool
        }
    """
    try:
        table = dynamodb.Table('HojasVida')
        limite = min(int(limite), 100)
        page = max(int(page), 1)

        # Obtener el total de registros para este cod_hoj_vida
        total_response = table.query(
            KeyConditionExpression='cod_hoj_vida = :cod',
            ExpressionAttributeValues={
                ':cod': cod_hoj_vida
            },
            Select='COUNT'
        )
        total_count = total_response.get('Count', 0)
        total_pages = (total_count + limite - 1) // limite if total_count > 0 else 0

        if total_count == 0:
            return {
                "success": False,
                "message": f"No se encontraron registros para cod_hoja_vida {cod_hoj_vida}",
                "data": [],
                "count": 0,
                "cod_hoja_vida": cod_hoj_vida,
                "page": page,
                "limite": limite,
                "total_count": 0,
                "total_pages": 0,
                "tiene_mas": False
            }

        if page > total_pages:
            return {
                "success": True,
                "message": f"Página {page} fuera de rango. Total de páginas: {total_pages}",
                "data": [],
                "count": 0,
                "cod_hoja_vida": cod_hoj_vida,
                "page": page,
                "limite": limite,
                "total_count": total_count,
                "total_pages": total_pages,
                "tiene_mas": False
            }

        query_params = {
            'KeyConditionExpression': 'cod_hoj_vida = :cod',
            'ExpressionAttributeValues': {
                ':cod': cod_hoj_vida
            },
            'Limit': limite
        }

        start_key = None
        # Avanzar a la página solicitada sin exponer token al cliente
        for _ in range(page - 1):
            if start_key:
                query_params['ExclusiveStartKey'] = start_key
            response_page = table.query(**query_params)
            start_key = response_page.get('LastEvaluatedKey')
            if not start_key:
                return {
                    "success": True,
                    "message": f"No hay registros en la página {page} para cod_hoja_vida {cod_hoj_vida}",
                    "data": [],
                    "count": 0,
                    "cod_hoja_vida": cod_hoj_vida,
                    "page": page,
                    "limite": limite,
                    "total_count": total_count,
                    "total_pages": total_pages,
                    "tiene_mas": False
                }
            query_params.pop('ExclusiveStartKey', None)

        if start_key:
            query_params['ExclusiveStartKey'] = start_key

        response = table.query(**query_params)
        items = response.get('Items', [])
        last_evaluated_key = response.get('LastEvaluatedKey')

        print(f"✅ Se obtuvieron {len(items)} registros para cod_hoja_vida {cod_hoj_vida} página {page}")
        return {
            "success": True,
            "message": f"Se obtuvieron {len(items)} registros para cod_hoja_vida {cod_hoj_vida} en la página {page}",
            "data": items,
            "count": len(items),
            "cod_hoja_vida": cod_hoj_vida,
            "page": page,
            "limite": limite,
            "total_count": total_count,
            "total_pages": total_pages,
            "tiene_mas": last_evaluated_key is not None
        }
    except Exception as e:
        print(f"❌ Error al obtener hojas de vida por cod_hoja_vida: {str(e)}")
        return {
            "success": False,
            "message": f"Error al obtener hojas de vida por cod_hoja_vida: {str(e)}"
        }
