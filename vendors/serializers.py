from rest_framework import serializers
from .models import Store, Product
from reviews.models import Review_product


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['vendor',
                  'name',
                  'description']
        
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['store',
                  'name',
                  'description',
                  'price']
        
        read_only_fields = ['store']
        
    def create(self, validated_data):
        store = self.context['store']
        return Product.objects.create(store=store, **validated_data)
    
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review_product
        fields = ['user', 
                  'text', 
                  'rating']