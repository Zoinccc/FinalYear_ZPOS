from rest_framework import serializers
from .models import Product, Category, Sale, SaleItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = '__all__'

class SaleItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product')

    class Meta:
        model = SaleItem
        fields = ['product_id', 'quantity']


class SaleItemDetailSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product')
    name = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = SaleItem
        fields = ['product_id', 'quantity', 'name', 'price']

    def get_name(self, obj):
        return obj.product.name

    def get_price(self, obj):
        return obj.product.price

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemDetailSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['id', 'created_at', 'total', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        sale = Sale.objects.create(**validated_data)

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            if product.stock < quantity:
                raise serializers.ValidationError(  
                    f"Not enough stock for '{product.name}'. Only {product.stock} left."
                )

            product.stock -= quantity
            product.save()

            SaleItem.objects.create(sale=sale, product=product, quantity=quantity)

        return sale
