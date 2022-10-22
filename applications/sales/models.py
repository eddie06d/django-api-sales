from django.db import models
from applications.warehouse.models import Product
import json

# Create your models here.

class Currency(models.Model):
    """
    Clase Moneda.
    Ejemplo 1: Moneda Sol
    Código: PEN
    Simbolo: S/.
    Nombre: Sol Peruano
    
    Ejemplo 2: Moneda Dólares Americanos.
    Código: USD
    Simbolo: $.
    Nombre: Dólares Americanos
    """
    id = models.AutoField(primary_key=True)

    code = models.CharField(max_length=3,unique=True, verbose_name="Código")

    symbol = models.CharField(max_length=4, verbose_name="Simbolo")

    name = models.CharField(max_length=20, verbose_name="Nombre")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    def __str__(self):
        return f"{self.symbol} {self.code}"

    class Meta:
        db_table = "currency"
        verbose_name = "Moneda"

class Client(models.Model):
    id = models.AutoField(primary_key=True)

    ruc = models.CharField(max_length=12, unique=True, verbose_name="RUC")

    name = models.CharField(max_length=50, verbose_name="Razón Social")
    
    district = models.CharField(max_length=50, verbose_name="Distrito")
    
    type_client = models.CharField(max_length=20, verbose_name="Tipo de Cliente")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "client"
        verbose_name = "Cliente"

class Order(models.Model):
    id = models.AutoField(primary_key=True)

    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Cliente")

    number = models.CharField(max_length=20, verbose_name="Número")

    date = models.DateField(verbose_name="Fecha")
    
    list_products = models.CharField(max_length=500,  verbose_name="Lista de Productos")
    
    delivery_date = models.DateField(verbose_name="Fecha de Entrega")
    
    delivery_address = models.CharField(max_length=100, verbose_name="Dirección de Entrega")
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal", default=0)
    
    igv = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="IGV", default=0)
    
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total", default=0)
    
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Descuento", default=0)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    def __str__(self):
        return self.number
    
    def save(self, *args, **kwargs):
        products = json.loads(self.list_products)
        total_base = 0
        for product in products:
            quantity = product['quantity']
            p = Product.objects.get(code=product['code'])
            self.subtotal += p.sale_price * quantity
            total_base += p.base_sale_price * quantity
        self.total_discount = total_base - self.subtotal
        self.igv = round(float(self.subtotal) * 0.18, 2)
        self.total = float(self.subtotal) + self.igv
        super(Order, self).save(*args, **kwargs)

    class Meta:
        db_table = "order"
        verbose_name = "Pedido"