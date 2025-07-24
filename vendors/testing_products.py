from vendors.models import Product

products = Product.objects.all()
print(products)