from django.contrib.auth.models import User
from rest_framework import serializers
from .models import MenuItem
from .models import Cart, Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity', 'unit_price', 'price']


class OrderSerializer(serializers.ModelSerializer):
    # items = OrderItemSerializer(many=True, read_only=True, source='orderitem_set')
    delivery_crew = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total', 'date', 'delivery_crew']#'items'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'menu_item', 'quantity', 'unit_price', 'price', 'user']

    def create(self, validated_data):
        """
        Calculate the price based on quantity * unit price before saving.
        """
        menu_item = validated_data['menu_item']
        quantity = validated_data['quantity']
        unit_price = menu_item.price
        validated_data['unit_price'] = unit_price
        validated_data['price'] = quantity * unit_price
        return super().create(validated_data)

class MenuItemSerializer(serializers.ModelSerializer):
    category=serializers.StringRelatedField()
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']