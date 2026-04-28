import boto3
from app.config.conexion_aws import conexion_aws_boto3

dynamodb = conexion_aws_boto3()

def generar_datos_ejemplo():
    """
    Genera 40 registros de ejemplo en la tabla HojasVida
    con el mismo cod_hoja_vida pero diferente documento (RANGE key)
    
    Returns:
        dict: {"success": True/False, "message": str, "items_creados": int}
    """
    try:
        table = dynamodb.Table('HojasVida')
        
        # Generar 40 registros de ejemplo con el mismo cod_hoja_vida
        datos_ejemplo = []
        cod_hoj_vida_fijo = 'HV-001'
        
        for i in range(1, 41):
            item = {
                'cod_hoj_vida': cod_hoj_vida_fijo,
                'documento': f'{str(i).zfill(10)}',
                'fecha': f'2026-04-{str((i % 30) + 1).zfill(2)}',
                'nombre_apellido': f'Usuario Nombre {i} Apellido {i}',
                'key_s3': f's3://bucket/hoja-vida/documento-{str(i).zfill(3)}.pdf'
            }
            datos_ejemplo.append(item)
        
        # Insertar en batch
        with table.batch_writer() as batch:
            for item in datos_ejemplo:
                batch.put_item(Item=item)
        
        print(f"✅ Se crearon exitosamente 40 registros de ejemplo con cod_hoja_vida: {cod_hoj_vida_fijo}")
        return {
            "success": True,
            "message": f"Se crearon exitosamente 40 registros de ejemplo con cod_hoja_vida: {cod_hoj_vida_fijo}",
            "items_creados": 40,
            "cod_hoja_vida": cod_hoj_vida_fijo
        }
        
    except Exception as e:
        print(f"❌ Error al generar datos de ejemplo: {str(e)}")
        return {
            "success": False,
            "message": f"Error al generar datos de ejemplo: {str(e)}"
        }
