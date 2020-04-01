from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import date, timedelta
from django.db.models.signals import post_delete


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000)
    genre = models.ManyToManyField(Genre)

    LOAN_STATUS = (
        ('l', 'loaned'),
        ('a', 'available')
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, default='a')

    def __str__(self):
        return self.title


def get_due_date():
    return date.today() + timedelta(days=30)


class BookInstance(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    due_date = models.DateField(default=get_due_date)
    current_owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def is_past_due(self):
        return date.today() >= self.due_date

    def __str__(self):
        return self.book.title


def on_bookinstance_delete(sender, instance, **kwargs):
    book = Book.objects.get(pk=instance.book.pk)
    book.status = 'a'
    book.save()
    print('book id:', instance.book.pk)
    print(book)
    print('on delete')


post_delete.connect(on_bookinstance_delete, sender=BookInstance)
