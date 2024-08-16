from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth import logout  
from .forms import *
from .models import *
from django.contrib import messages
import random
from DoctorClinic import settings
from django.core.mail import send_mail
# from django.core.exceptions import ObjectDoesNotExist
import requests


# Create your views here.
def index(request):
    user = request.session.get('user')
    return render(request,'index.html',{'user':user})

def  about(request):
    user = request.session.get('user')
    return render(request,'about.html',{'user':user})

def appointment(request):
    user = request.session.get('user')
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        if form.is_valid():
            form.save()
            # Email Send
            Name = [request.POST['Name']]
            Date = [request.POST['Date']]
            Doctor = [request.POST['Doctor']]
            sub = "Book Our Appointment"
            msg = f"Dear {Name}\nThis Mail is For Doctor Clinic Team,\nYour Appointment {Doctor} has to {Date} is SuccessFull Booked\nYou Make Sour to Comming on time To Appointment.\nany query to contact on\nkavathiyaparth852@Email.com\nparth: 6354287550"
            from_email = settings.EMAIL_HOST_USER
            # to_Email = ["pp7810559@Email.com"]
            to_Email = [request.POST['Email']]
            
            # send_mail(subject=sub,message=msg,from_Email=from_email,recipient_list=to_Email)
            send_mail(sub, msg, settings.EMAIL_HOST_USER, to_Email)
            # SMS Sending
            # mobile = request.POST['Mobile']
            # url = "https://www.fast2sms.com/dev/bulkV2"

            # querystring = {"authorization":"gWMAeKq0ExoPnDvUiHGbj1OJsF9aC8yB7dR6L254hVcXrfNmQTc1NKT34eJrdkRYMFqlHwSsLAfmCZ70","message":f"Dear User,\nThe HealthiFy Hospital your Appointment {Date} Booked SuccessFuly!\nMake Sour Your are Coming on time.","language":"english","route":"q","numbers":f"{mobile}"}

            # headers = {
            #     'cache-control': "no-cache"
            # }

            # response = requests.request("GET", url, headers=headers, params=querystring)

            # print(response.text)
            return redirect('/') # redirect to a success page
    else:
        form = AppointmentBookingForm()
    # return render(request, 'book_appointment.html', {'form': form})
    return render(request,'appointment.html',{'user':user, 'form': form})

def contact(request):
    user = request.session.get('user')
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # Send Email notification
            # Email Send
            Name = [request.POST['Name']]
            sub = "24/7 Help Contact"
            msg = f"Dear {Name}\nThis Mail is For Doctor Clinic Team,\nMy Team is shortly contact for You. \nThank You.\nany query to contact on\nkavathiyaparth852@Email.com\nparth: 6354287550"
            from_email = settings.EMAIL_HOST_USER
            # to_email = ["pp7810559@gmail.com"]
            to_email = [request.POST['Email']]
            # send_mail(subject=sub,message=msg,from_Email=from_email,recipient_list=to_email)
            send_mail(
                sub,
                msg,
                from_email,  # from_email, not from_Email
                to_email,
                fail_silently=False,
            )
            return redirect('/')
    else:
        form = ContactForm()
    return render(request,'contact.html',{'user':user})

def login(request):
    if request.method=='POST':
        Email=request.POST['Email']
        password=request.POST['Password']
        user = Register_Form.objects.filter(Email=Email,Password=password)
        uid = Register_Form.objects.get(Email=Email)
        if user: #true
            print('Login Successfuly!')
            request.session["user"]=Email #session create
            request.session["uid"]=uid.id
            request.session['Name']=uid.Name
            return redirect('/')
        else:
            print('Error!')
    return render(request,'Login.html')

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')  # assuming you have a login view
    else:
        form = RegisterForm()
    return render(request,'signup.html',{'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

def profile(request):
    user = request.session.get('user')
    uid = request.session.get('uid')
    cid=Register_Form.objects.get(id=uid)
    if request.method=='POST':
        update = UpdateProfile(request.POST)
        if update.is_valid():
            update=UpdateProfile(request.POST,instance=cid)
            update.save()
            print('Your Profile has been Updated')
            return redirect('/')
        else:
            print(update.errors)
    return render(request,'profile.html',{'user':user,'uid':Register_Form.objects.get(id=uid)})

def forgot(request):
    if request.method == 'POST':
        Email = request.POST.get('Email')
        try:
            user = Register_Form.objects.get(Email=Email)
        except Register_Form.DoesNotExist:
            return render(request, 'forgot_password.html', {'error': 'Email not found'})
        # global otp
        global otp
        otp=random.randint(111111,999999)
        # sub="Welcome"
        # msg=f"Dear user your otp is{otp} \n your one time passoword \n Your Account has been Created With Us\n Enjoy our Services\n If any qaury, contact on\n Mo= +91 8780240806"
        # from_mail=settings.Email_HOST_USER
        # to_Email=[Email]
        # send_mail(subject=sub,message=msg,from_Email=from_mail,recipient_list=to_Email)
        # print('your otp is',otp)
        
        sub = "Change Our Password"
        msg = f"Dear user\nThis Mail is For Doctor Clinic Team,\nYour one time password is {otp}.\nany query to contact on\nkavathiyaparth852@Email.com\nparth: 6354287550"
        # from_Email = settings.Email_HOST_USER
        # to_Email = ["pp7810559@Email.com"]
        to_Email = [request.POST['Email']]
        
        # send_mail(subject=sub,message=msg,from_Email=from_Email,recipient_list=to_Email)
        send_mail(sub, msg, settings.EMAIL_HOST_USER, to_Email)
        
        
        
        return redirect('/otp')
        # You might want to redirect the user to another page, such as a profile page, instead of printing to console

    else:
        pass
    return render(request,'forgot.html')

def otp(request):
    if request.method == 'POST':
        global otp
        eotp = ''
        for i in range(1, 7):
            eotp += request.POST.get(f'otp_{i}', '')
        
        stored_otp = request.session.get('otp')
        if eotp == str(otp):
            print('OTP verified successfully')
            # You might want to redirect the user to another page instead of printing to console
            return redirect('/change')
        else:
            print("Please try again")
            # Provide feedback to the user on the webpage
    return render(request,'otp.html')

def change(request):
    email = request.session.get('Email')
    user_email = Register_Form.objects.get(Email=email)

    if request.method == 'POST':
        form = forpass(request.POST, instance=user_email)
        if form.is_valid():
            form.save()
            print("pin is updeted")
            return redirect('/login')
        else:
            return render(request, 'changePassword.html', {'form': form, 'error': 'Form is not valid'})
    else:
        form = forpass(instance=user_email)

    return render(request,'changePassword.html',{'form': form})

def adminLogin(request):
    if request.method=='POST':
        username=request.POST['UserName']
        password=request.POST['Password']
        
        Doctor = AdminSignUp.objects.filter(UserName=username,Password=password)
        Did = AdminSignUp.objects.get(UserName=username)
        if Doctor: #true
            print('Login Successfuly!')
            request.session["Doctor"]= username #session create
            request.session["Did"]=Did.id
            return redirect('/base')
        else:
            print('Error!')
    return render(request,'Doctor/admin_login.html')

def base(request):
    data = Appointment_Booking.objects.all()
    return render(request,'Doctor/base.html',{'data':data})

def deletedata(request,id):
    cid = Appointment_Booking.objects.get(id=id)
    Appointment_Booking.delete(cid)
    return redirect('/base')

def update_date(request,id):
    # Doctor = request.session.get('Doctor')
    data = Appointment_Booking.objects.all()
    cid = Appointment_Booking.objects.get(id=id)
    if request.method=='POST':
        UpdateAppointment=AppointmentForm(request.POST)
        if UpdateAppointment.is_valid():
            UpdateAppointment=AppointmentForm(request.POST,instance=cid)
            UpdateAppointment.save()
            # Email Send
            Date = [request.POST['Date']]
            Name = [request.POST['Name']]
            sub = "Book Our Appointment"
            msg = f"Dear User!\nHello Dear'{Name}\nThe HealthiFy Hospetal Your Appointment {Date} is Changed\n Decose HealthiFy Hospital Dector is Not A avalible for this Data \nYou Make Sour to Comming on time To Appointment.\nany query to contact on\nhealthify0989@gmail.com\nparth: 6354287550"
            from_email = settings.EMAIL_HOST_USER
            # to_email = ["pp7810559@gmail.com"]
            to_email = [request.POST['Email']]
            
            send_mail(subject=sub,message=msg,from_email=from_email,recipient_list=to_email)
            
            # SMS Sending
            mobile = request.POST['Mobile']
            url = "https://www.fast2sms.com/dev/bulkV2"

            querystring = {"authorization":"gWMAeKq0ExoPnDvUiHGbj1OJsF9aC8yB7dR6L254hVcXrfNmQTc1NKT34eJrdkRYMFqlHwSsLAfmCZ70","message":f"Dear User, {Name}\nThe HealthiFy Hospital your Appointment {Date} is Chagend\n \n Decose HealthiFy Hospital Dector is Not A avalible for this Data \nMake Sour Your are Coming on time.","language":"english","route":"q","numbers":f"{mobile}"}

            headers = {
                'cache-control': "no-cache"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)

            print(response.text)
            
            return redirect('/base')
        else:
            print(UpdateAppointment.errors)
    return render(request,'Doctor/Update_appointment.html',{'data':data,'client':Appointment_Booking.objects.get(id=id)})

def D_Appointment(request):
    Doctor = request.session.get('Doctor')
    data = Appointment_Booking.objects.all()
    return render(request,'Doctor/Appointment.html',{'data':data,'Doctor':Doctor})

def D_Account(request):
    data = Register_Form.objects.all()   
    Doctor = request.session.get('Doctor') 
    return render(request,'Doctor/account.html',{'data':data,'Doctor':Doctor})

def D_Contact(request):
    data = Contact_Form.objects.all()    
    Doctor = request.session.get('Doctor')
    return render(request,'Doctor/Contact.html',{'data':data,'Doctor':Doctor})

def adminSignUp(request):
    Doctor = request.session.get('Doctor')
    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/base')  # redirect to admin list page
    else:
        form = AdminSignUpForm()
    return render(request,'Doctor/add_admin.html',{'Doctor':Doctor})