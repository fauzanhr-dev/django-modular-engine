from django.apps import AppConfig

__version__ = '1.0.0'

class ProductModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product_module'
    verbose_name = 'Product Module'