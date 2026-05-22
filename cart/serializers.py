from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'total']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_sum = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'is_active', 'fio', 'phone', 'address', 'telegram', 'created_at', 'items', 'total_sum']

    def get_total_sum(self, obj):
        return sum(item.total for item in obj.items.all())


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)
