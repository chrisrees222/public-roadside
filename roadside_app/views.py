from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm
from django.contrib import messages
from .models import Profile
from django.core.files.base import ContentFile
from .models import Profile
from . import models
from django.views import generic
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import logout as auth_logout, get_user_model
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse, HttpResponse
import stripe
from datetime import datetime, timedelta, date
from .forms import CaptchaAuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from json import dumps

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.http import HttpRequest
from importlib import import_module
from  django.contrib.auth.middleware import get_user
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy
import djstripe
from json import dumps
import json
import requests
from django.contrib.auth.forms import AuthenticationForm 
import os


# for the user profile, loads current with option to save new details.
class UserProfile(View):
    template_name = 'profile.html'
    #gets the user logged in details.
    def get(self, request):
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user_profile = None
        form_data = {
            'company': user_profile.company_name if user_profile else '',
            'name': user_profile.full_name if user_profile else '',
            'email': request.user.email if user_profile else '', 
            'mobile_no': user_profile.mobile_number if user_profile else '',
            'profile_image': user_profile.profile_image if user_profile else '',
            'profile_summary': user_profile.profile_summary if user_profile else '',
            'city': user_profile.city if user_profile else '',
            'postcode': user_profile.postcode if user_profile else '',
            'latitude': user_profile.latitude if user_profile else '', 
            'longitude': user_profile.longitude if user_profile else '',
            
        }

        today = date.today()
        stripe_date_user = user_profile.stripePaidDate
        left_over_days = stripe_date_user.date() - today
        total_days = left_over_days.days

        #print("this is the date only hopefully " + str(stripe_date_user.date()) + " " + str(today) + " " + str(total_days) )

        context = {
        'profile': user_profile,
        'form_data': form_data,
        'days_left': total_days
        }
        return render(request, self.template_name, context)

    # For saving new details in profile.
    def post(self, request):
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user_profile = None
        uploaded_image = request.FILES.get('profile_image', None)
        if uploaded_image:
            user_profile.profile_image.save(uploaded_image.name, ContentFile(uploaded_image.read()))
        company_name = request.POST.get('company')
        full_name = request.POST.get('name')
        email = request.POST.get('email') 
        mobile_number = request.POST.get('mobile_no')
        profile_summary = request.POST.get('profile_summary')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if user_profile:
            user_profile.company_name = company_name
            user_profile.full_name = full_name
            user_profile.mobile_number = mobile_number
            user_profile.profile_summary = profile_summary
            user_profile.city = city
            user_profile.postcode = postcode
            user_profile.latitude = latitude
            user_profile.longitude = longitude
            user_profile.save()       
            user_profile.user.email = email
            user_profile.user.save()

        return redirect('user-profile') 

# For loading the home page on start up.
def homeView(request):
    # gets all the users registered by filtering dates of stripe paid date and checking its greater than today's date.
    #locations = Profile.objects.filter(stripePaidDate__gt=datetime.now())

    #get all profiles , for ad based app initially
    locations = Profile.objects.all()
    #serialise function called from models file to create geoJson object.
    location_list = [l.serialize() for l in locations]
    location_dict = {
        "type": "FeatureCollection",
        "features": location_list
    }
    location_json = dumps(location_dict)

    context = {
        'locations': location_json
    }
    return render(request, 'home.html', context)
            
# for rendering the about page   
def about(request):
    return render(request, 'about.html')  

# for rendering the compdetails page 
def compdetails(request):
    return render(request, 'company_details.html')

# for rendering the models to show users details in company page.
class ProfileDetailView(generic.DetailView):
    template_name = 'company_details.html'
    model = models.Profile
    context_object_name = 'companydetail'

# for showing the companies page.
def recoverycompanies(request):
    my_data = Profile.objects.all() #for all the records      
    return render(request, 'recovery_companies.html', {'companies': my_data}) 

#rendering the contact page from home page.
def contactus(request):
    return render(request, 'contact.html')

# For registering a new user.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            #Send email to user welcoming.
            subject = 'Welcome to TMH'
            message = 'Hello ' + str(user) + ' Thank you for registering an account. Please log in and complete profile to complete account set up.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)   
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# renders the login form for users.
def user_login(request):
    if request.method == "POST":
        form = CaptchaAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home-page')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = CaptchaAuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

# logs out user, directs to login page.
def user_logout(request):
    logout(request)
    return redirect('login')

# allows user to edit profile from the user tab.
def profile_settings(request):
    return render(request, 'profile_settings.html')

# allows the user to delete their profile completely.
@login_required
def delete_profile(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('register')
    else:
        return render(request, 'delete_profile.html')

# allows user to change password.
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # To keep the user logged in
            return redirect('password_reset_complete')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


########## Aditional for payment stripe set up ######################################################################

#preset configuration for stripe payment set up.
@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=True)

# stripe payment £15 for 30 days. creates checkout session when the button in select payment is pressed.
@csrf_exempt
def create_checkout_session_thirty(request):
    if request.method == "GET":
        domain_url = "https://django-road-side-project.azurewebsites.net/"
        stripe.api_key = settings.STRIPE_SECRET_KEY # From settings which is in another file env.
        try:
            #create a checkout session
            checkout_session = stripe.checkout.Session.create(                
                client_reference_id = int(request.user.id) if request.user.is_authenticated else None,
                success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "cancel/",
                payment_method_types= ["card"],
                mode = "payment",
                line_items=[ 
                    {
                        "price": settings.STRIPE_PRICE_ID_15, #key for £15 purchase. from settings env.
                        "quantity": 1,
                    }
                ]
            )            
            user_profile = Profile.objects.get(user=request.user)
            user_profile.stripeCustomerId = checkout_session.client_reference_id
            user_profile.stripeSubscriptionId = checkout_session.id
            user_profile.save()
            
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})

# stripe payment £15 for 30 days. creates checkout session when the button in select payment is pressed.
@csrf_exempt
def create_checkout_session_sixty(request):
    if request.method == "GET":
        domain_url = "https://django-road-side-project.azurewebsites.net/"
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            #create a checkout session
            checkout_session = stripe.checkout.Session.create(                
                client_reference_id = int(request.user.id) if request.user.is_authenticated else None,
                success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "cancel/",
                payment_method_types= ["card"],
                mode = "payment",
                line_items=[ 
                    {
                        "price": settings.STRIPE_PRICE_ID_25, #key for £25 purchase.
                        "quantity": 1,
                    }
                ]
            )            
            user_profile = Profile.objects.get(user=request.user)
            user_profile.stripeCustomerId = checkout_session.client_reference_id
            user_profile.stripeSubscriptionId = checkout_session.id
            user_profile.save()
            
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})

# stripe payment £30 for 90 days. creates checkout session when the button in select payment is pressed.
@csrf_exempt
def create_checkout_session_ninety(request):
    if request.method == "GET":
        domain_url = "https://django-road-side-project.azurewebsites.net/"
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            #create a checkout session
            checkout_session = stripe.checkout.Session.create(                
                client_reference_id = int(request.user.id) if request.user.is_authenticated else None,
                success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "cancel/",
                payment_method_types= ["card"],
                mode = "payment",
                line_items=[ 
                    {
                        "price": settings.STRIPE_PRICE_ID_30, #key for £30 purchase.
                        "quantity": 1,
                    }
                ]
            )            
            user_profile = Profile.objects.get(user=request.user)
            user_profile.stripeCustomerId = checkout_session.client_reference_id
            user_profile.stripeSubscriptionId = checkout_session.id
            user_profile.save()
            
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})
        
# In production mode, the web hook will be linked via stripe account, so when payment is made.
# the webhook listens to confirm which payment (15,25,30) was created, then adds the date to user model.       
@csrf_exempt
def my_webhook_view(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
                
        user = Profile.objects.get(id=client_reference_id) 
        if session.get('payment_status') == 'paid':               #To check that the pyment is paid.
            if session.get('id') == user.stripeSubscriptionId:    #To check the id that was made, matches the webhook that came through. then checks how much payment was made.
                if session.get('amount_total') == 1500:
                    expiry = datetime.now() + timedelta(31)
                    user.stripePaidDate = expiry
                    user.stripeWebHookStatus = 'paid'
                    user.save()
                elif session.get('amount_total') == 2500:
                    expiry = datetime.now() + timedelta(62)
                    user.stripePaidDate = expiry
                    user.stripeWebHookStatus = 'paid'
                    user.save()
                elif session.get('amount_total') == 3000:
                    expiry = datetime.now() + timedelta(93)
                    user.stripePaidDate = expiry
                    user.stripeWebHookStatus = 'paid'
                    user.save()                   
        else:
            user.stripePaidDate = datetime.now()
            user.stripeWebHookStatus = 'failed'
            user.save()

    return HttpResponse(status=200)

# If payment was succesful, then loads the succes html page.       
@csrf_exempt
def success(request):
    return render(request, "success.html")

#If payment failed or cancelled, loads the cancelled html page.
@csrf_exempt
def cancel(request):
    return render(request, "cancel.html")

#when user enters the subscribe checkout button on profile, loads the select payment option.
def select_payment(request):
    return render(request, "select_payment.html")
