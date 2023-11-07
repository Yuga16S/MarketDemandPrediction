from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Max, Q
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View


import ml_scripts.linear_removing_outliers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from marketdemandpredictionapp.models import Crops, UserProfile, UserPreferences

import smtplib
from email.mime.text import MIMEText
from django.conf import settings

import json

class BannerView(View):
    def get(self, request):
        return render(request, 'banner.html')

class GuestView(View):

    def get(self, request):
        crop_names = Crops.objects.values_list('crop_name', flat=True)

        context = {
            'crop_names': crop_names,
        }
        return render(request, 'guest_home.html', context)


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not (username and email and password):
            context = {
                "error": "Please enter all the fields."
            }
            return render(request, 'register.html', context=context)

        existing_user = User.objects.filter(Q(username=username) | Q(email=email)).first()
        if existing_user:
            context = {
                "error": "Username or email already exists!"
            }
            return render(request, 'register.html', context=context)

        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user)
        return redirect('login')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    error = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not (email and password):
            error = 'Please enter both email and password.'
        else:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                error = 'Invalid email or password.'

    return render(request, 'login.html', {'error': error})


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            current_site = get_current_site(request)
            reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            reset_url = f"{request.scheme}://{current_site}{reset_url}"

            email_subject = 'Password reset for Market Demand Prediction Online site'
            email_message = render_to_string('password_reset_email.html', {
                'user': user,
                'password_reset_url': reset_url,
            })

            sender = settings.EMAIL_HOST_USER
            recipients = [user.email]
            password = settings.EMAIL_HOST_PASSWORD

            msg = MIMEText(email_message)
            msg['Subject'] = email_subject
            msg['From'] = sender
            msg['To'] = ', '.join(recipients)
            with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT) as smtp_server:
                smtp_server.login(sender, password)
                smtp_server.sendmail(sender, recipients, msg.as_string())
            print("Message sent!")

            return redirect('password_reset_done')
        else:
            messages.error(request, 'No user with that email address exists.')
            return redirect('forgot_password')
    else:
        return render(request, 'forgot_password.html')


@login_required
def home(request):
    crop_names = Crops.objects.values_list('crop_name', flat=True)
    selected_crop_name = request.GET.get('cropName', '')
    selected_start_year = request.GET.get('startYear', '')
    selected_end_year = request.GET.get('endYear', '')

    context = {
        'crop_names': crop_names,
        'selected_crop_name': selected_crop_name,
        'selected_start_year': selected_start_year,
        'selected_end_year': selected_end_year
    }
    return render(request, 'home.html', context)


@method_decorator(login_required, name='get')
class ProfileView(View):
    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)

        user_preferences = UserPreferences.objects.filter(user_profile=user_profile)

        context = {
            'user_profile': user_profile,
            'user_preferences': user_preferences,
        }
        return render(request, 'profile.html', context)


def about_us(request):
    return render(request, 'about_us.html')


def predict(request):
    user_profile = None;
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)

    selected_crop = request.GET.get('selected_crop', None)

    selected_end_year = request.GET.get('selected_end_year', None)
    end_year = int(selected_end_year)

    selected_start_year = request.GET.get('selected_start_year', None)
    start_year = int(selected_start_year) if selected_start_year else end_year

    crop = Crops.objects.get(crop_name=selected_crop)

    predictions = ml_scripts.linear_removing_outliers.predict(crop, start_year, end_year)

    chart_data = ml_scripts.linear_removing_outliers.getChartData(predictions, crop, start_year, end_year)
    chart_json_data = json.dumps(chart_data)

    save_preference = request.GET.get('save', None) == 'true'

    if user_profile and save_preference:
        UserPreferences.objects.create(
            user_profile=user_profile,
            selected_crop=crop,
            selected_start_year=start_year,
            selected_end_year=end_year
        )

    return HttpResponse(chart_json_data)

"""
#old register view without validation
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        existing_user = User.objects.filter(Q(username=username) | Q(email=email)).first()
        context = {"error": None}
        if existing_user:
            context = {
                "error": "username or email already exists!"
            }
            return render(request, 'register.html', context=context)
        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user)
        return redirect('login')

        return render(request, 'register.html', context=context)"""


"""
#Code where validation is done but won't login the user
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    error = None  # Initialize error as None.

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not (username and password):
            error = 'Please enter both username and password.'
        else:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                error = 'Invalid username or password.'

    return render(request, 'login.html', {'error': error})"""


"""
#old login code that had no validation
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid username or password.'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')"""