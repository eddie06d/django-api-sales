from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
#from applications.sales.models import Currency

# Create your models here.

class UnitMeasureCategory(models.Model):
    """ 
    Clase de Categoría de Unidades de Medida
    Ejemplo: Peso, Volumen, Longitud
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=3, unique=True, verbose_name='Código')
    name = models.CharField(max_length=50,verbose_name='Nombre')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'unit_measure_category'
        verbose_name = 'Categoría de Unidades de Medida'

class UnitMeasure(models.Model):
    """ 
    Clase Unidad de Medida
    Ejemplo: Kilogramo(Kg) -> Categoria Peso, Litro(Lt) -> Categoria Volumen, Gramo(g), Miligramo(mg)
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=3, unique=True, verbose_name='Código')
    name = models.CharField(max_length=50,verbose_name='Nombre')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    # Relación con la tabla UnitMeasureCategory
    unit_measure_category_id = models.ForeignKey(UnitMeasureCategory, on_delete=models.CASCADE, default=None, db_column='unit_measure_category_id', verbose_name='Categoría de Unidad de Medida')
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'unit_measure'
        verbose_name = 'Unidades de Medida'

class ProductCategory(models.Model):
    """ 
    Clase Categoría de Producto
    Ejemplo: Abarrotes
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=3, unique=True, verbose_name='Código')
    name = models.CharField(max_length=50,verbose_name='Nombre')
    percent_discount = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(50)], verbose_name='Descuento (%)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'product_category'
        verbose_name = 'Categoría de Producto'

class Product(models.Model):
    id = models.AutoField(primary_key=True)

    code = models.CharField(max_length=5, unique=True, verbose_name="Código")

    name = models.CharField(max_length=60, verbose_name="Nombre")
    
    # foreign_key: categoría de producto
    product_category_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, default=None, db_column="product_category_id", verbose_name="Categoría Producto")

    # foreign_key: unidad de medida
    unit_measure_id = models.ForeignKey(UnitMeasure, on_delete=models.CASCADE, default=None, db_column="unit_measure_id", verbose_name="Unidad de Medida")
    
    # foreign_key: Moneda
    currency_id = models.ForeignKey("sales.Currency", on_delete=models.CASCADE, default=None, db_column="currency_id", verbose_name="Moneda")

    # precio de compra.
    purchase_price = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name="Precio de Compra")

    # precio de venta base
    base_sale_price = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name="Precio de Venta Base")

    # require: from django.core.validators
    percent_discount = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(60)], verbose_name="Descuento (%)")

    discount_amount = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name="Monto Descuento")

    # precio de venta
    sale_price = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name="Precio de Venta")

    # stock: PositiveIntegerField
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")

    # Activo: BooleanField
    active = models.BooleanField(default=True, verbose_name="Activo")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Creación")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha Actualización")
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Sobre escribimos el método save de la clase Model.
        """
        # Calculamos el monto de descuento
        self.discount_amount = round(
            (int(self.percent_discount)/100)*float(self.base_sale_price), 2)
        
        # Calculamos el precio de venta
        self.sale_price = float(self.base_sale_price) - \
            float(abs(self.discount_amount))
        
        # Guardamos información del modelo
        super(Product, self).save(*args, **kwargs)

    class Meta:
        db_table = "product"
        verbose_name = "Producto"