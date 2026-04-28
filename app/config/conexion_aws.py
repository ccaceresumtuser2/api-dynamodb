"""
===========================================================
MÓDULO: Gestión de Usuarios en DynamoDB
===========================================================

🧾 DESCRIPCIÓN:
Este archivo contiene la conexión con AWS DynamoDb con boto3

🛠 TECNOLOGÍA:
- AWS DynamoDB
- boto3 (Python SDK)

AUTOR: Carlos Jose Caceres Ochoa
FECHA: 13-04-2026
VERSIÓN: 1.0

===========================================================
"""
import boto3

#importar Propiedades del Modulo
from app.config.enviroment.enviroment import (
    REGION_AWS, 
    SERVICIO_AWS_DYNAMODB
    )

#conexión con AWS Servicio DYNAMODB

def conexion_aws_boto3():
    return boto3.resource(SERVICIO_AWS_DYNAMODB,
                           region_name=REGION_AWS)

