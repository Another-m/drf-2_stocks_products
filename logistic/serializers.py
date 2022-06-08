from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = '__all__'



class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = '__all__'
        read_only_fields = ("stock", )


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'products', 'address', 'positions', ]

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)
        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions


        for element in range(len(positions)):
            StockProduct.objects.create(stock=stock, **positions[element])

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        # for element in range(len(positions)):
            # stocks_positions = stock.positions.get(product=positions[element].get('product'))
            # stocks_positions.price = positions[element].get('price', stocks_positions.price)
            # stocks_positions.quantity = positions[element].get('quantity', stocks_positions.quantity)
            # stocks_positions.save()
        for value in positions:
            StockProduct.objects.update_or_create(
                stock=stock,
                product=value.get('product'),
                defaults={
                    'quantity': value.get('quantity'),
                    'price': value.get('price')
                }
            )

        return stock
