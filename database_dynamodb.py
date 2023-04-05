"Database layer - the dynamo version"
import uuid
import time
import boto3

def list_products():
    "Select all the products from the database"
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('products')
        return table.scan()["Items"]
    except:
        return 0

def load_product(product_id):
    "Select one the product from the database"
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('products')
        response = table.get_item(
            Key={
                'id': product_id
            }
        )
        return response['Item']
    except:
        pass

def add_product(designation, price, quantity, category):
    "Add an product to the database"
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('products')
        item = {
            'id': str(uuid.uuid4()),
            'designation': designation,
            'price': price,
            'quantity': quantity,
            'category': category,
            'created': int(time.time()),
            'updated': int(time.time())
        }

        table.put_item(
            Item=item
        )
    except:
        pass


def update_product(product_id, designation, price, quantity, category):
    "Update an product to the database"
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('products')
        item = {
            
            
            'designation':{'Value': designation, 'Action': 'PUT'},
            'price': {'Value': price, 'Action': 'PUT'},
            'quantity': {'Value': quantity, 'Action': 'PUT'},
            'category': {'Value': category, 'Action': 'PUT'},
            'updated': {'Value': int(time.time()), 'Action': 'PUT'},
        }
        

        table.update_item(
            Key={
                'id': product_id
            },
            AttributeUpdates=item
        )
    except:
        pass

def delete_product(product_id):
    "Delete an product."
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('products')
        table.delete_item(
            Key={
                'id': product_id
            }
        )
    except:
        pass
