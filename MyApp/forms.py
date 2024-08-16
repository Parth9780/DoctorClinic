from django import forms
from .models import *

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register_Form
        fields = '__all__'
    
class LoginForm(forms.Form):
    Email = forms.EmailField()
    Password = forms.CharField(widget=forms.PasswordInput)
        
class UpdateProfile(forms.ModelForm):
    class Meta:
        model = Register_Form
        fields = ['Name','Mobile','Email']
        
class forpass(forms.ModelForm):
    class Meta:
        model=Register_Form
        fields=['Password']

class AppointmentBookingForm(forms.ModelForm):
    class Meta:
        model = Appointment_Booking
        fields = '__all__'
        
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact_Form
        fields = '__all__'

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment_Booking
        fields = ['Date', 'Time']

class AdminSignUpForm(forms.ModelForm):
    class Meta:
        model = AdminSignUp
        fields = '__all__'