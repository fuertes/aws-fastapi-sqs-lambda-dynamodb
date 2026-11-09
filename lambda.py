import json
import logging
import os
from decimal import Decimal
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

NOMBRE_TABLA_DYNAMODB = "ExampleOrdes"

def lambda_handler(event, context):
    """
    Worker que lee de SQS e inserta cada elemento en DynamoDB.
    """
    logger.info(f"Se han recibido {len(event['Records'])} mensaje(s) de SQS.")
    
    for record in event['Records']:
        try:
            raw_body = record['body']
            data = json.loads(raw_body)
            
            order_id = data.get('order_id')
            customer_email = data.get('customer_email')
            product = data.get('product')
            
            amount = Decimal(str(data.get('amount')))
            
            logger.info(f"[PROCESANDO] Insertando pedido '{order_id}' en la tabla '{NOMBRE_TABLA_DYNAMODB}'...")
            
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table(NOMBRE_TABLA_DYNAMODB)

            table.put_item(
                Item={
                    'order_id': order_id,          
                    'customer_email': customer_email,
                    'product': product,
                    'amount': amount,
                    'status': 'PROCESADO'           
                }
            )
            
            logger.info(f"[ÉXITO] Pedido '{order_id}' guardado correctamente en DynamoDB.")
            
        except Exception as e:
            logger.error(f"[ERROR] No se pudo guardar el pedido en DynamoDB: {str(e)}")
            raise e

    return {
        'statusCode': 200,
        'body': json.dumps('Procesamiento e inserción en DynamoDB completados con éxito.')
    }