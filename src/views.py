from django.views.decorators.csrf import csrf_exempt
from spyne import Application, rpc, ServiceBase, Unicode, Integer, Array
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from spyne.model.complex import ComplexModel
import MySQLdb

db = MySQLdb.connect("localhost", "user", "password", "store")

class Category(ComplexModel):
    id = Integer
    name = Unicode

class Product(ComplexModel):
    id = Integer
    category_id = Integer
    name = Unicode
    price = Integer
    quantity = Integer

class SoapService(ServiceBase):
    @rpc(_returns=Array(Category))
    def get_categories(ctx):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM categories")
        rows = cursor.fetchall()
        categories = [Category(id=row[0], name=row[1]) for row in rows]
        return categories

    @rpc(Integer(nillable=False), _returns=Array(Product))
    def get_products_by_category(ctx, category_id):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM products WHERE category_id = %s", (category_id,))
        rows = cursor.fetchall()
        products = [Product(id=row[0], category_id=row[1], name=row[2], price=row[3], quantity=row[4]) for row in rows]
        return products

soap_app = Application([SoapService],
                       tns='django.soap.example',
                       in_protocol=Soap11(validator='lxml'),
                       out_protocol=Soap11())

django_soap_application = DjangoApplication(soap_app)
my_soap_application = csrf_exempt(django_soap_application)
