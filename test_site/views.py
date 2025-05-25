from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Chat, Book, Author
from .forms import BookForm
from datetime import datetime

def index_page(request):
    context = {
        "page_name": "Главная", 
        "menu_items": get_base_menu(request),
        "year": datetime.now().year
    }
    
def get_base_menu(request):  # Добавлен параметр request
    menu_items = [
        {"link": "/", "text": "Главная страница"},
        {"link": "/admin/", "text": "Админ. панель"},
        {"link": "/chat/", "text": "Чат"},
        {"link": "/books/", "text": "Книги"},
        {"link": "/authors/", "text": "Авторы"},
    ]
    
    if not request.user.is_authenticated:
        menu_items.extend([
            {"link": "/accounts/login/", "text": "Войти в систему"},
            {"link": "/registration/", "text": "Регистрация"}
        ])
    
    return menu_items

def login_view(request):
    context = {"page_name": "Страница авторизации", "menu_items": get_base_menu(request)}  # Передаем request
    return render(request, "registration/login.html", context)

def index_page(request):
    context = {"page_name": "Главная", "menu_items": get_base_menu(request)}  # Передаем request
    
    if request.user.is_authenticated:
        pass  # Делаем что-то, если пользователь вошёл в систему
    else:
        pass  # Делаем что-то, если пользователь не вошёл в систему
    
    if request.user.username == "ons33":
        context["is_ONS"] = True 
    
    return render(request, "index_page.html", context)

def registration_page(request):
    context = {"page_name": "Страница регистрации", "menu_items": get_base_menu(request)}  # Передаем request

    if request.method == "POST":
        reg_form = UserCreationForm(request.POST)
        
        if reg_form.is_valid():
            reg_form.save()
            
            username = reg_form.cleaned_data.get("username")
            password = reg_form.cleaned_data.get("password1")
        
            user = authenticate(username=username, password=password)
            
            login(request, user)  
            
            return redirect('/')
    else:
        reg_form = UserCreationForm() 
            
    context["reg_form"] = reg_form    

    return render(request, "registration/registration_page.html", context)

@login_required
def chat_page(request):
    context = {"page_name": "Чат", "menu_items": get_base_menu(request)}  # Передаем request

    if request.method == "POST":
        message = request.POST.get("message")
        Chat(author=request.user, message=message).save()

    if request.user.username == "ons33":
        return redirect("/")

    context["chat_items"] = Chat.objects.all()

    return render(request, "chat/chat_page.html", context)

@login_required
def book_list(request):
    books = Book.objects.all().select_related('author')
    context = {
        "page_name": "Список книг",
        "menu_items": get_base_menu(request),  # Передаем request
        "books": books
    }
    return render(request, "books/book_list.html", context)

@login_required
def author_list(request):
    authors = Author.objects.prefetch_related('books').all()
    context = {
        "page_name": "Список авторов",
        "menu_items": get_base_menu(request),  # Передаем request
        "authors": authors
    }
    return render(request, "books/author_list.html", context)

@login_required
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    
    context = {
        "page_name": "Добавить книгу",
        "menu_items": get_base_menu(request),  # Передаем request
        "form": form
    }
    return render(request, "books/add_book.html", context)