from django.urls import path
from  Eduweb import views

urlpatterns=[
    path('home/',views.home_page,name='home'),
    path('about/',views.about_page,name='about'),
    path('popular/',views.popular_page,name='popular'),
    path('contact/',views.contact_page,name='contact'),
    path('category/<category>/',views.category_page,name='category'),
    path('details/book/<int:book_id>/', views.book_details, name='book_details'),
    path('details/accessory/<int:acc_id>/', views.accessory_details, name='accessory_details'),
    #auth------------------------------------------------------------------------------------
    path('signup/', views.signup_page, name='signup'),
    path('save_signup/', views.save_signup, name='save_signup'),
    path('signin/', views.signin_page, name='signin'),
    path('signin_in/', views.signin, name='signin_in'),
    path('signin_out/', views.sign_out, name='signin_out'),
]