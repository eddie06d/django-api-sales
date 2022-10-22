from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import OrderSerializer, ClientSerializer, ProductSerializer
from applications.sales.models import Order, Client
from applications.warehouse.models import Product
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
import json

class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filter_set_fields = ['number', 'date', 'delivery_date']
    
    def post(self, request, format=None, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            products = json.loads(request.data['list_products'])
            for product in products:
                product_code = product['code']
                quantity = int(product['quantity'])
                product = Product.objects.get(code=product_code)
                if product.active and product.stock >= quantity:
                    product.stock = product.stock - quantity
                    product.save()
                else:
                    return Response({'message': 'No hay stock suficiente'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None, *args, **kwargs):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        
        return Response(serializer.data)
   
class OrderDetailView(APIView): 
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None, id=0, *args, **kwargs):
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            pass
        serializer = OrderSerializer(order)
        client = Client.objects.get(id=serializer.data['client_id'])
        payload = {
            'number': serializer.data['number'],
            'date': serializer.data['date'],
            'delivery_address': serializer.data['delivery_address'],
            'delivery_date': serializer.data['delivery_date'],
            'subtotal': serializer.data['subtotal'],
            'igv': serializer.data['igv'],
            'total': serializer.data['total'],
            'list_products': json.loads(serializer.data['list_products']),
            'client': {
                'ruc': client.ruc,
                'business_name': client.name,
                'distrcit': client.district,
                'type_client': client.type_client,
            }
        }
        
        return JsonResponse(payload)

class OrderGainView(APIView):
    #permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None, id=0, *args, **kwargs):
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            pass
        serializer = OrderSerializer(order)
        total_base = 0
        
        for p in json.loads(serializer.data['list_products']):
            product = Product.objects.get(code=p['code'])
            total_base += p['quantity'] * product.base_sale_price
        
        payload = {
            "numero_pedido": serializer.data['number'],
            "venta_neta": float(serializer.data['subtotal']),
            "costo_compra": float(total_base),
            "ganancia": float(serializer.data['subtotal']) - float(total_base)
        }
        
        return JsonResponse(payload)

class ClientViewSet(ModelViewSet):
    #permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    
    filter_backends = [DjangoFilterBackend]
    filter_set_fields = ['ruc', 'type_client']

class ProductViewSet(ModelViewSet):
    #permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class OrdersOfClientView(APIView):
    #permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None, id=0, *args, **kwargs):
        try:
            client = Client.objects.get(id=id)
        except Client.DoesNotExist:
            pass
        orders = Order.objects.filter(client_id=client.id)
        payload_orders = []
        
        for order in orders:
            payload_orders.append({
                "numero_pedido": order.number,
                "fecha_pedido": order.date,
                "importe_total": order.total,
                "importe_total_descuento": order.total_discount,
            })
        
        return JsonResponse(payload_orders, safe=False)