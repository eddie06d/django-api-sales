from django.contrib import admin

from applications.warehouse.models import Product, ProductCategory, UnitMeasure, UnitMeasureCategory

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ('code', 'name', 'product_category_id', 'unit_measure_id', 'currency_id', 'purchase_price', 'base_sale_price', 'percent_discount', 'stock', 'active')
    list_display = ('code', 'name', 'product_category_id', 'display_purchase_price', 'display_sale_price')
    
    def display_sale_price(self, obj) -> (str):
        """
        Método que devuelve el precio de venta del producto con el simbolo
        de la moneda.
        """
        return f"{obj.currency_id.symbol} {obj.sale_price}"
    
    def display_purchase_price(self, obj) -> (str):
        """
        Método que devuelve el precio de compra del producto con el simbolo
        de la moneda.
        """
        return f"{obj.currency_id.symbol} {obj.purchase_price}"

    # Defimos el nombre de la columna
    display_sale_price.short_description = "Precio de Venta"
    display_purchase_price.short_description = "Precio de Compra"

admin.site.register(UnitMeasureCategory)
admin.site.register(UnitMeasure)
admin.site.register(ProductCategory)