from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.books, name='books'),
    path('authors/', views.authors, name='authors'),
    path('book_details/<int:pk>', views.book_details, name='book_details'),
    path('loan_book/<int:pk>', views.loan_book, name='loan_book'),
    path('return_book/<int:pk>', views.return_book, name='return_book'),
]