from django.contrib import admin
from django.urls import path,include
from MyApp import views

urlpatterns = [
    path('',views.index, name='index'),
    path('about/',views.about, name='about'),
    path('appointment/',views.appointment, name='appointment'),
    path('contact/',views.contact, name='contact'),
    path('login/',views.login, name='login'),
    path('appointment/',views.logout_view, name='appointment'),
    path('profile/',views.profile,name='profile'),
    path('signup/',views.signup, name='signup'),
    path('forgot/',views.forgot,name='forgot'),
    path('otp/',views.otp, name='otp'),
    path('change/',views.change, name='change'),
    # Admin URLs....
    # path('admin/',views.admin),
    path('base/',views.base, name='base'),
    path('deletedata/<int:id>',views.deletedata, name='deletedata'),
    path('update_date/<int:id>',views.update_date, name='update_date'),
    path('appoint/',views.D_Appointment, name='D_Appointment'),
    path('account/',views.D_Account, name='D_Account'),
    path('contac/',views.D_Contact, name='D_Contact'),
    path('myadmin/',views.adminLogin, name='adminLogin'),
    path('adminSignUp/',views.adminSignUp, name='adminSignUp'),
]