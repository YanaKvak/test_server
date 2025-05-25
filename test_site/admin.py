from django.contrib import admin
from .models import Chat, Author, Book

admin.site.register(Chat)
admin.site.register(Author)
admin.site.register(Book)