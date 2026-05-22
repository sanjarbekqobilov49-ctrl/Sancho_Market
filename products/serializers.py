from rest_framework import serializers
from .models import Product, Category, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    extra_images = ProductImageSerializer(source='images', many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image', 'description', 'category', 'category_name', 'extra_images', 'created_at']
