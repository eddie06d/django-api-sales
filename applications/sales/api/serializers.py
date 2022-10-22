from rest_framework.serializers import ModelSerializer
from applications.sales.models import Order, Client
from applications.warehouse.models import Product

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'