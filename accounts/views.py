from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import SetPasswordForm
from django.urls import reverse
from .forms import UserSignUpForm
from django.core.mail import EmailMessage
from vendors.models import Product
from datetime import timedelta
from django.utils import timezone
from .models import ResetToken, User_Profile
import secrets
from hashlib import sha1

User = get_user_model()


def register_user(request):
    
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
        
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            user_type = form.cleaned_data['user_type']
            User_Profile.objects.get_or_create(
                user=user,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                user_type=user_type
            )

            login(request, user)

            if user_type == 'buyer':
                return redirect('home_dash')
            elif user_type == 'vendor':
                return redirect('vendors:home_vendor')

        else:
            messages.error(request, "The registration was unsuccessful. Please try again.")
            return render(request, 'accounts/register_user.html', {'form': form})
    else:
        form = UserSignUpForm()
    return render(request, 'accounts/register_user.html', {'form': form})
    

def home_view(request):
    dash_list = {
        'products': Product.objects.all()}
    return render(request, 'vendors/home.html', {'dash_list': dash_list})
    

def login_user(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            try:
                profile = User_Profile.objects.get(user=user)
                user_type = profile.user_type

                messages.success(request, f'Welcome back, {username}!')

                if user_type == 'buyer':
                    return redirect('home_dash')
                elif user_type == 'vendor':
                    return redirect('vendors:home_vendor')
                else:
                    return redirect('home_view')  
            except User_Profile.DoesNotExist:
                messages.error(request, "User profile not found. Please register first.")
                return redirect('register_user')
        else:
            messages.error(request, 'Login was unsuccessful. Please try again.')
            return HttpResponseRedirect(reverse('login_user'))
    
    return render(request, 'accounts/login_user.html')
        

def logout_user(request):
    logout(request)
    messages.success(request, ('You have been successfully logged out '))
    return redirect('home_view')


def build_email(user, reset_url):
    subject = "Password Reset"
    user_email = user.email
    domain_email = "example@domain.com"
    body = f"Hi {user.username},\nHere is your link to reset your password: {reset_url}"
    email = EmailMessage(subject, body, domain_email, [user_email])
    return email


def generate_reset_url(request):
    
    if request.method == "POST":
        email = request.POST.get('email')
        users = User.objects.filter(email=email)

        if not users.exists():
            messages.error(request, "No user with that email was found.")
        else:
            for user in users:
                domain = "http://127.0.0.1:8000/"
                token = secrets.token_urlsafe(16)
                expiry_date = timezone.now() + timedelta(minutes=5)
                hashed_token = sha1(token.encode()).hexdigest()

                
                ResetToken.objects.create(user=user, token=hashed_token, expiry_date=expiry_date)

                reset_link = f"{domain}takealot/password_reset_user/{user.id}/{token}/"


            messages.success(request, "A password reset link has been sent to your email.")

        return redirect('login_user')

    return render(request, 'accounts/password_reset.html')


def reset_user_password(request):

    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.filter(email=email)
            url = generate_reset_url(request)
            email = EmailMessage("Reset Your Password", f"Click the link to reset your password: {url}")
            email.send()

            messages.success(request, "A password reset link has been sent to your email.")
        except User.DoesNotExist:
            messages.error(request, "No user with that email was found.")
        return redirect('login_user')
    return render(request, 'accounts/password_reset.html')


def password_confirmation(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        reset_token = ResetToken.objects.get(user=user)

        if not reset_token.is_valid(token):
            messages.error(request, "Reset link is invalid or has expired.")
            return redirect('login_buyer')

        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                reset_token.delete()
                messages.success(request, "Password reset successful.")
                return redirect('login_buyer')
        else:
            form = SetPasswordForm(user)
    except (User.DoesNotExist, ResetToken.DoesNotExist):
        messages.error(request, "Invalid reset request.")
        return redirect('login_buyer')

    return render(request, 'accounts/password_reset_confirm.html', {'form': form})

