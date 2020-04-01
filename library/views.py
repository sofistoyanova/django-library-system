from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Book, Author, BookInstance


def books(request):
    library_books = Book.objects.filter(status='a')
    context = {
        'books': library_books
    }
    return render(request, 'library/books.html', context)


def authors(request):
    book_authors = Author.objects.all()
    context = {
        'authors': book_authors
    }
    return render(request, 'library/authors.html', context)


def book_details(request, pk):
    book = Book.objects.get(pk=pk)
    context = {
        'book': book
    }
    return render(request, 'library/book_details.html', context)


def loan_book(request, pk):
    number_of_loaned_books = BookInstance.objects.filter(current_owner=request.user)
    if len(number_of_loaned_books) >= 10:
        message = 'You have loaned more than 10 books already'
        library_books = Book.objects.filter(status='a')
        context = {
            'message': message,
            'books': library_books
        }
        return render(request, 'library/books.html', context)

    loaned_original_book = Book.objects.get(pk=pk)
    loaned_original_book.status = 'l'
    loaned_original_book.save()

    loaned_copy_book = BookInstance()
    loaned_copy_book.current_owner = request.user
    loaned_copy_book.book = loaned_original_book
    loaned_copy_book.save()

    return HttpResponseRedirect(reverse('users:profile'))


def return_book(request, pk):
    returned_copy_book = BookInstance.objects.get(pk=pk)
    returned_copy_book.delete()

    returned_original_book = Book.objects.get(pk=returned_copy_book.book.id)
    returned_original_book.status = 'a'
    returned_original_book.save()
    return HttpResponseRedirect(reverse('users:profile'))

