from django.shortcuts import render, redirect
from .models import Category, Book, Accessory
from Eduweb.models import ContactMessage
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login

def index(request):
    date = datetime.now().strftime("%b %d, %Y")
    data = {
        'date': date,
        'categories_count': Category.objects.count(),
        'books_count': Book.objects.count(),
        'accessories_count': Accessory.objects.count(),
        'messages_count': ContactMessage.objects.count(),
    }
    return render(request, "index.html", data)


def login_page(request):
    return render(request,"login.html")


def admin_login(request):
    if request.method == "POST":
        name = request.POST.get('username')
        pasd = request.POST.get('password')
        if User.objects.filter(username__contains=name).exists():
            data = authenticate(username=name,password=pasd)
            if data is not None:
                login(request,data)
                request.session["username"]=name
                request.session["password"]=pasd
                return redirect(index)
            else:
                return redirect(login_page)
    else:
        return redirect(login_page)


def logout_page(request):
    del request.session['username']
    del request.session['password']
    return redirect(login_page)

# -------------------------------- Category --------------------------------

def add_category(request):
    number = Category.objects.count()
    return render(request, "add_category.html", {'number': number})


def save_category(request):
    if request.method == "POST":
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        icon = request.FILES.get('icon')
        obj = Category(name=name, slug=slug, description=description, icon=icon)
        obj.save()
        return redirect(add_category)


def display_category(request):
    data = Category.objects.all()
    return render(request, "display_category.html", {'data': data})


def edit_category(request, u_id):
    cat = Category.objects.get(id=u_id)
    return render(request, "edit_category.html", {'cat': cat})


def update_category(request, u_id):
    if request.method == "POST":
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        try:
            icon_set = request.FILES['icon']
            fs = FileSystemStorage()
            filename = fs.save(icon_set.name, icon_set)
        except MultiValueDictKeyError:
            filename = Category.objects.get(id=u_id).icon
        Category.objects.filter(id=u_id).update(name=name, slug=slug, description=description, icon=filename)
        return redirect(display_category)


def delete_category(request, d_id):
    Category.objects.filter(id=d_id).delete()
    return redirect(display_category)

# -------------------------------- Book --------------------------------

def add_book(request):
    categories = Category.objects.all()
    return render(request, "add_book.html", {'categories': categories})


def save_book(request):
    if request.method == "POST":
        category_name = request.POST.get('category')
        title = request.POST.get('title')
        author = request.POST.get('author')
        publisher = request.POST.get('publisher')
        price = request.POST.get('price') or None
        description = request.POST.get('description')
        cover_image = request.FILES.get('cover_image')
        obj = Book(
            category=category_name,
            title=title,
            author=author,
            publisher=publisher,
            price=price,
            description=description,
            cover_image=cover_image,
        )
        obj.save()
        return redirect(add_book)


def display_book(request):
    data = Book.objects.all()
    return render(request, "display_book.html", {'data': data})


def edit_book(request, b_id):
    book = Book.objects.get(id=b_id)
    categories = Category.objects.all()
    return render(request, "edit_book.html", {'book': book, 'categories': categories})


def update_book(request, b_id):
    if request.method == "POST":
        category_name = request.POST.get('category')
        title = request.POST.get('title')
        author = request.POST.get('author')
        publisher = request.POST.get('publisher')
        price = request.POST.get('price') or None
        description = request.POST.get('description')
        try:
            img = request.FILES['cover_image']
            fs = FileSystemStorage()
            filename = fs.save(img.name, img)
        except MultiValueDictKeyError:
            filename = Book.objects.get(id=b_id).cover_image
        Book.objects.filter(id=b_id).update(
            category=category_name,
            title=title,
            author=author,
            publisher=publisher,
            price=price,
            description=description,
            cover_image=filename,
        )
        return redirect('display_book')


def delete_book(request, b_id):
    Book.objects.filter(id=b_id).delete()
    return redirect('display_book')

# -------------------------------- Accessory --------------------------------

def add_accessory(request):
    categories = Category.objects.all()
    return render(request, "add_accessory.html", {'categories': categories})


def save_accessory(request):
    if request.method == "POST":
        category_name = request.POST.get('category')
        name = request.POST.get('name')
        brand = request.POST.get('brand')
        price = request.POST.get('price') or None
        specs = request.POST.get('specs')
        image = request.FILES.get('image')
        obj = Accessory(
            category=category_name,
            name=name,
            brand=brand,
            price=price,
            specs=specs,
            image=image,
        )
        obj.save()
        return redirect(add_accessory)


def display_accessory(request):
    data = Accessory.objects.all()
    return render(request, "display_accessory.html", {'data': data})


def edit_accessory(request, a_id):
    accessory = Accessory.objects.get(id=a_id)
    categories = Category.objects.all()
    return render(request, "edit_accessory.html", {'accessory': accessory, 'categories': categories})


def update_accessory(request, a_id):
    if request.method == "POST":
        category_name = request.POST.get('category')
        name = request.POST.get('name')
        brand = request.POST.get('brand')
        price = request.POST.get('price') or None
        specs = request.POST.get('specs')
        try:
            img = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(img.name, img)
        except MultiValueDictKeyError:
            filename = Accessory.objects.get(id=a_id).image
        Accessory.objects.filter(id=a_id).update(
            category=category_name,
            name=name,
            brand=brand,
            price=price,
            specs=specs,
            image=filename,
        )
        return redirect('display_accessory')


def delete_accessory(request, a_id):
    Accessory.objects.filter(id=a_id).delete()
    return redirect('display_accessory')

# -------------------------------- Messages (from Eduweb) --------------------------------

def display_messages(request):
    msgs = ContactMessage.objects.order_by('-created_at')
    return render(request, "display_messages.html", {'messages': msgs})

def delete_message(request, m_id):
    ContactMessage.objects.filter(id=m_id).delete()
    return redirect('display_messages')
