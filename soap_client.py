# soap_client.py
from suds.client import Client
from suds.cache import NoCache

client = Client('http://127.0.0.1:8000/soap_service/?WSDL', cache=NoCache())

print('Categories:')
categories = client.service.get_categories()
for category in categories:
    print(f"ID: {category.id}, Name: {category.name}")

print('\nProducts in Category 1:')
products = client.service.get_products_by_category(1)
for product in products:
    print(f"ID: {product.id}, Name: {product.name}, Price: {product.price}, Quantity: {product.quantity}")
