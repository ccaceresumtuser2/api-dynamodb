import boto3
from app.config.conexion_aws import conexion_aws_boto3

dynamodb = conexion_aws_boto3()

def crear_tabla_hojas_vida():
    print("Creando tabla HojasVida...")

    try:
        table = dynamodb.create_table(
            TableName='HojasVida',

            # 🔑 PK + SK
            KeySchema=[
                {'AttributeName': 'cod_hoj_vida', 'KeyType': 'HASH'},
                {'AttributeName': 'documento', 'KeyType': 'RANGE'}
            ],

            AttributeDefinitions=[
                {'AttributeName': 'cod_hoj_vida', 'AttributeType': 'S'},
                {'AttributeName': 'documento', 'AttributeType': 'S'},
                {'AttributeName': 'fecha', 'AttributeType': 'S'},
                {'AttributeName': 'nombre_apellido', 'AttributeType': 'S'},
                {'AttributeName': 'key_s3', 'AttributeType': 'S'}
            ],

            GlobalSecondaryIndexes=[

                # 🔍 documento
                {
                    'IndexName': 'documento-index',
                    'KeySchema': [
                        {'AttributeName': 'documento', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                },

                # 🔍 fecha
                {
                    'IndexName': 'fecha-index',
                    'KeySchema': [
                        {'AttributeName': 'fecha', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                },

                # 🔍 nombre
                {
                    'IndexName': 'nombre-index',
                    'KeySchema': [
                        {'AttributeName': 'nombre_apellido', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                },

                # 🔍 key_s3
                {
                    'IndexName': 'key-s3-index',
                    'KeySchema': [
                        {'AttributeName': 'key_s3', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],

            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        table.wait_until_exists()
        print("✅ Tabla HojasVida creada correctamente")
        return {"success": True, "message": "Tabla HojasVida creada correctamente"}

    except Exception as e:
        print("❌ Error al crear la tabla HojasVida")
        print(e)
        #return {"success": False, "message": str(e)}
        return {"success": False, "message": "Error al crear la tabla HojasVida"}