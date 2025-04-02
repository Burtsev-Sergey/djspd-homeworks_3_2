from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from main.models import Book, Order
from main.serializers import BookSerializer


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


class OrderViewSet(viewsets.ModelViewSet):
    # реализуйте CRUD для заказов
    ...
