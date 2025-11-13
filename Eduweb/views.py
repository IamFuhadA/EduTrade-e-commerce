from django.shortcuts import render,redirect, get_object_or_404
from EduApp.models import Category,Book,Accessory
from .models import RegistrationDB, ContactMessage
# Create your views here.

def home_page(request):
    category = Category.objects.all()
    featured_books = Book.objects.order_by('-created_at')[:6]
    featured_accessories = Accessory.objects.order_by('-created_at')[:6]
    return render(request,"home.html",{
        'category':category,
        'featured_books': featured_books,
        'featured_accessories': featured_accessories,
    })

def about_page(request):
    category = Category.objects.all()
    return render(request, "about.html", {"category": category})

def popular_page(request):
    category = Category.objects.all()
    books = Book.objects.order_by('-created_at')[:8]
    accessories = Accessory.objects.order_by('-created_at')[:8]
    return render(request, "popular.html", {"category": category, "books": books, "accessories": accessories})

def contact_page(request):
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')
        if name and email and message_text:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject or "",
                message=message_text
            )
            return redirect('contact')
    return render(request,"contact.html", {"category": category})

def category_page(request, category):
    category_list = Category.objects.all()
    books = Book.objects.filter(category=category)
    accessories = Accessory.objects.filter(category=category)
    context = {
        'category': category_list,
        'selected_category': category,
        'books': books,
        'accessories': accessories,
    }
    return render(request, "category.html", context)


def book_details(request,book_id):
    category_list = Category.objects.all()
    book = get_object_or_404(Book, pk=book_id)
    context = {
        'category': category_list,
        'book': book,
        'selected_category': book.category,
    }
    return render(request, "details.html", context)


def accessory_details(request,acc_id):
    category_list = Category.objects.all()
    accessory = get_object_or_404(Accessory, pk=acc_id)
    context = {
        'category': category_list,
        'accessory': accessory,
        'selected_category': accessory.category,
    }
    return render(request, "details.html", context)



#auth---------------------------------------------------------------------------------------------------------------
def signup_page(request):
    # if request.user.is_authenticated:
    #     return redirect(home_page)
    return render(request, "signup.html")

def save_signup(request):
    if request.method == "POST":
        username=request.POST.get('username')
        name=request.POST.get('name')
        mail=request.POST.get('email')
        contact=request.POST.get('number')
        password=request.POST.get('password')
        cnf_password=request.POST.get('confirm')

        obj = RegistrationDB(
            username=username,name=name,
            mail=mail,contact=contact,password=password,
            confirm_password=cnf_password
        )
        if RegistrationDB.objects.filter(name=name).exists():
            return redirect(signup_page)
        elif RegistrationDB.objects.filter(mail=mail).exists():
            return redirect(signup_page)
        elif RegistrationDB.objects.filter(username=username).exists():
            return redirect(signup_page)
        else :
            obj.save()
            return redirect(signin_page)

#auth---------------------------------------------------------------------------------------------------------------
def signin_page(request):
    return render(request, "signin.html")

def signin(request):
    if request.method == "POST":
        name = request.POST.get('username')
        password= request.POST.get('password')
        if RegistrationDB.objects.filter(username=name,password=password).exists():
            request.session["username"]=name
            request.session["password"]=password
            return redirect(home_page)
        else:
            return redirect(signin_page)
    else:
        return redirect(signin_page)

def sign_out(request):
    request.session.pop("username", None)
    request.session.pop("password", None)
    return redirect(home_page)