from rest_framework import serializers
from main.models import Book, Order

class BookSerializer(serializers.ModelSerializer):
    class Meta:
      model = Book
      fields = ['id', 'author', 'title', 'year']

    def to_representation(self, instance):
      representation = super().to_representation(instance)
      # Подсчет количества заказов, в которых присутствует текущая книга
      orders_count = instance.order_set.count()
      representation['orders_count'] = orders_count
      return representation


# Сериализатор извлекает из модели `Book` нужные поля `author`, `title` и `year` 
class SimpleBookSerializer(serializers.ModelSerializer):
    class Meta:
      model = Book
      fields = ['author', 'title', 'year']


class OrderSerializer(serializers.ModelSerializer):
    books = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), many=True, required=False)

    class Meta:
      model = Order
      fields = ['id', 'user_name', 'days_count', 'date', 'books']

    def to_representation(self, instance):
      response = super().to_representation(instance)
      response['books'] = SimpleBookSerializer(instance.books.all(), many=True).data
      return response