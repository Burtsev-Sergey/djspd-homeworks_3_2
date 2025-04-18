from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from main.models import Book, Order
from main.serializers import BookSerializer, OrderSerializer


# Реализация получения списка всех книг.
@api_view(['GET'])
def books_list(request):
    books = Book.objects.all()
    ser = BookSerializer(books, many=True)
    return Response(ser.data)


# Реализация добавления новой книги.
class CreateBookView(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
          serializer.save()
          return Response({'message': 'Книга успешно создана'}, status=status.HTTP_201_CREATED)


# Реализация получения одной книги. 
class BookDetailsView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# Реализация редактирования данных о книге.
class BookUpdateView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# Реализация удаления книги.
class BookDeleteView(DestroyAPIView):
    queryset = Book.objects.all()
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        book = self.get_object()
        book.delete()
        return Response({'message': 'Книга успешно удалена.'}, status=status.HTTP_204_NO_CONTENT)


# Реализация CRUD для заказов
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
      data = request.data.copy()
      book_ids = data.pop('books', [])

      # Создаем заказ без книг
      serializer = self.get_serializer(data=data)
      if serializer.is_valid():
        order = serializer.save()

        # Добавляем книги к заказу после его создания
        if book_ids:
          books = Book.objects.filter(id__in=book_ids)
          if len(books) != len(book_ids):
            return Response({'error': 'Одна или несколько указанных книг не существует.'}, status=status.HTTP_400_BAD_REQUEST)
          order.books.set(books)

        # Подготовка ответа
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
      else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)