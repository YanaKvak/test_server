from django.contrib import admin
from django.urls import path, include
from test_site import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page),
    path("accounts/", include("django.contrib.auth.urls")),
    path('chat/', views.chat_page),
    path("registration/", views.registration_page),
    path('books/', views.book_list, name='book_list'),
    path('authors/', views.author_list, name='author_list'),
    path('books/add/', views.add_book, name='add_book'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)