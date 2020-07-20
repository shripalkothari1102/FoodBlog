from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .utils import *
from django.urls import reverse
import random

# Create your views here.

def index (request):
    return render(request, "Recipes4Foodies/index.html")

def recipes (request):
    return render(request, "Recipes4Foodies/recipes.html")

def recipe_single (request):
    return render(request, "Recipes4Foodies/recipe-single.html")

def about (request):
    return render(request, "Recipes4Foodies/about.html")

def contact (request):
    return render(request, "Recipes4Foodies/contact.html")

def login (request):
    # CHECK IF SESSION IS AVAILABLE
    if "email" in request.session:
        return HttpResponseRedirect('/')

    elif request.COOKIES.get('email'):
        cookie_data = {
            'email': request.COOKIES.get('email'),
            'password': request.COOKIES.get('password'),
        }
        return render(request, "Recipes4Foodies/login.html", {"cookie_data": cookie_data})
    else:
        return render(request, "Recipes4Foodies/login.html")

def register (request):
    # CHECK IF SESSION IS AVAILABLE
    if "email" in request.session:
        return HttpResponseRedirect('/')
    return render(request, "Recipes4Foodies/register.html")

def forget_password(request):
    # CHECK IF SESSION IS AVAILABLE
    if "email" in request.session:
        return HttpResponseRedirect('/')
    return render(request, "Recipes4Foodies/forget_password.html")

def register_user (request):
    if request.method =="GET":
        return HttpResponseRedirect('/register/')
    
    try:
        # RETRIVE FORM DATA
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        # CREATE A USER IN DATABASE AND THROW AN EXCEPTION IF THE EMAIL ALREADY EXIST
        user = User.objects.create(username = username, email = email, password = password)

        # CHECK IF USER OBJECT IS CREATED 
        if user:
            mail_subject = "Confirmation Mail"
            mail_template = "mail_welcome"
            mail_message = "Thank you for the registration in FOODBLOG."
            sendmail(mail_subject, mail_template, email, {"username": username, "email": email})
            success_message = "Registration successful."
            return render(request, "Recipes4Foodies/login.html", {'success_message' : success_message})
        else:
            error_message = "Registration error. Try again."
            return render(request, "Recipes4Foodies/register.html", {'error_message' : error_message})
        
    except:
        error_message = "User already have an account."
        return render(request, "Recipes4Foodies/register.html", {'error_message' : error_message})

def login_user (request):
    if request.method =="GET":
        return HttpResponseRedirect('/login/')
    
    # RETRIVE FORM DATA
    email = request.POST["email"]
    password = request.POST["password"]
        
    # ACCESS USER FROM THE DATABASE
    user = User.objects.filter(email = email)
                
    # CHECK IF USER EXIST AND MATCH THE PASSWORD
    if user and user[0].password == password:
        # CREATE SESSION
        request.session['username'] = user[0].username
        request.session['email'] = user[0].email
            
        response = HttpResponseRedirect('/')
            
        if request.POST.get("checked"):
            max_age = 365*24*60*60
            response.set_cookie('email', email, max_age)
            response.set_cookie('password', password, max_age)
        else:
            response.delete_cookie('email')
            response.delete_cookie('password')
            
        return response
                
    else:
        error_message = "Incorrect email or password."
        return render(request, "Recipes4Foodies/login.html", {'error_message' : error_message})

def forget_password_user(request):
    if request.method =="GET":
        return HttpResponseRedirect('/forget_password/')
    
    try:
        # RETRIVE FORM DATA
        email = request.POST["email"]

        # ACCESS USER FROM THE DATABASE
        user = User.objects.get(email = email)
                    
        # CHECK IF USER AVAILABLE
        if user:
            otp = random.randint(1000,9999)
            user.otp = otp
            user.save()
            mail_subject = "OTP"
            mail_message = str(otp) + " is your OTP to change you password in your FoodBlog."
            send_otp_mail(mail_subject, mail_message, user.email)
            success_message = "OTP has been sent to this email address."
            return render( 
                request, 
                "Recipes4Foodies/forget_password_otp.html", 
                {'success_message' : success_message, "email" : user.email}
            )
    except :
        error_message = "Email does not exist."
        return render(
            request,
            "Recipes4Foodies/forget_password.html",
            {'error_message':error_message}
        )    

def forget_password_otp(request):
    if request.method == "GET":
        return HttpResponseRedirect('/forget_password/')
    
    # RETRIVE FORM DATA
    email = request.POST["email"]
    otp = request.POST["otp"]
    new_password = request.POST["new_password"]
    confirm_password = request.POST["confirm_password"]
    
    if int(otp) == 0:
        error_message = "Incorrect OTP."
        return render(
            request, 
            "Recipes4Foodies/forget_password_otp.html", 
            {'error_message' : error_message, "email" : email}
        )

    if new_password != confirm_password:
        error_message = "Password don't match."
        return render(
            request, "Recipes4Foodies/forget_password_otp.html", 
            {'error_message' : error_message, "email" : email}
        )

    user = User.objects.filter(email = email)
    if user:
        if user[0].otp == int(otp):
            user[0].password = new_password
            user[0].otp = None
            user[0].save()
            success_message = "Password has been changed successfully."         
            return render(
                request, "Recipes4Foodies/login.html", {'success_message' : success_message}
            )
            
    error_message = "Incorrect OTP."
    return render(
        request, 
        "Recipes4Foodies/forget_password_otp.html", 
        {'error_message' : error_message, "email" : email}
    )

def resend_otp(request):
    if request.method =="GET":
        return HttpResponseRedirect('/forget_password/')
    
    try:
        # RETRIVE FORM DATA
        email = request.POST["email"]

        # ACCESS USER FROM THE DATABASE
        user = User.objects.get(email = email)
                    
        # CHECK IF USER AVAILABLE
        if user:
            otp = random.randint(1000,9999)
            user.otp = otp
            user.save()
            mail_subject = "OTP"
            mail_message = str(otp) + " is your OTP to change you password in your FoodBlog."
            send_otp_mail(mail_subject, mail_message, user.email)
            success_message = "New OTP has been sent to this email address."
            return render( 
                request, 
                "Recipes4Foodies/forget_password_otp.html", 
                {'success_message' : success_message, "email" : user.email}
            )
    except:
        error_message = "Email does not exist."
        return render(
            request,
            "Recipes4Foodies/forget_password.html",
            {'error_message':error_message}
        )    

def profile (request):
    # CHECK IF SESSION IS AVAILABLE
    if "email" in request.session:
        user = User.objects.get(email = request.session["email"])
        return render(request, "Recipes4Foodies/profile.html", {"user" : user})
    
    elif request.COOKIES.get('email'):
        cookie_data = {
            'email': request.COOKIES.get('email'),
            'password': request.COOKIES.get('password'),
        }
        return render(request, "Recipes4Foodies/login.html", {"cookie_data": cookie_data})
    else:
        return HttpResponseRedirect('/login/')

def change_password(request):
    # CHECK IF SESSION IS AVAILABLE
    if "email" in request.session:
        return render(request, "Recipes4Foodies/change_password.html")
    return HttpResponseRedirect('/login/')

def update_profile_user(request):
    if request.method == "GET":
        if "email" in request.session:
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/login/')
    else:
        # RETRIVE FORM DATA
        username = request.POST["username"]
        user = User.objects.get(email = request.session["email"])

        user.username = username
        user.save()
        request.session["username"] = username
        return HttpResponseRedirect('/')    

def change_password_user(request):
    if request.method == "GET":
        if "email" in request.session:
            return HttpResponseRedirect('/change_password/')
        return HttpResponseRedirect('/login/')
    
    else:
        # RETRIVE FORM DATA
        current_password = request.POST["current_password"]
        new_password = request.POST["new_password"]
        retype_new_password = request.POST["retype_new_password"]
        
        if new_password != retype_new_password:
            error_message = "Password don't match."
            return render(
                request, 
                "Recipes4Foodies/change_password.html", 
                {'error_message' : error_message}
            )
        
        else:
            user = User.objects.get(email = request.session["email"])
            if user.password != current_password:
                error_message = "Incorrect Password."
                return render(
                    request, 
                    "Recipes4Foodies/change_password.html", 
                    {'error_message' : error_message}
                )
            else:
                user.password = new_password
                user.save()
                success_message = "Password has been changed successfully."         
                return render(
                    request, 
                    "Recipes4Foodies/profile.html", 
                    {'success_message' : success_message, "user" : user}
                )

def logout(request):
    # CHECK IF SESSION IS AVAILABLE
    if "email" in request.session:
        # CLEAR SESSION
        request.session.flush()
    return HttpResponseRedirect('/')
