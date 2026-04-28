import boto3
from app.config.conexion_aws import conexion_aws_boto3

dynamodb = conexion_aws_boto3()

def insertar_hoja_vida(hoja_vida_data):
    """
    Inserta un registro en la tabla HojasVida
    
    Args:
        hoja_vida_data: Diccionario con los datos de la hoja de vida
        
    Returns:
        dict: {"success": True/False, "message": str, "data": item}
    """
    try:
        table = dynamodb.Table('HojasVida')
        
        # Insertar el item en la tabla
        response = table.put_item(
            Item={
                'cod_hoj_vida': hoja_vida_data['cod_hoj_vida'],
                'documento': hoja_vida_data['documento'],
                'fecha': hoja_vida_data['fecha'],
                'nombre_apellido': hoja_vida_data['nombre_apellido'],
                'key_s3': hoja_vida_data['key_s3']
            }
        )
        
        print("✅ Hoja de vida insertada correctamente")
        return {
            "success": True,
            "message": "Hoja de vida insertada correctamente",
            "data": hoja_vida_data
        }
        
    except Exception as e:
        print(f"❌ Error al insertar hoja de vida: {str(e)}")
        return {
            "success": False,
            "message": f"Error al insertar hoja de vida: {str(e)}"
        }
