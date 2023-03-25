import io
import os

import qrcode
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.files import File
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.views import View

from Scanner.models import Person

from PIL import Image, ImageDraw


class LoginView(View):
    # Add template name
    template_name = 'Scanner/login.html'

    # Create get function
    def get(self, request):
        # Check if user is logged in
        if request.user.is_authenticated:
            # Redirect back to dashboard if true
            return HttpResponseRedirect(reverse('Scanner:home'))
        # Otherwise
        else:
            # Go to login page
            return render(request, self.template_name)

    # Create post function
    def post(self, request):
        if request.method == 'POST':
            # Process the input
            username = request.POST.get('username').strip()
            password = request.POST.get('password').strip()
            # Authenticate the user login details
            user = authenticate(request, username=username, password=password)
            # Check if user exists
            if user is not None:
                # Log in the user
                login(request, user)
                # Redirect to dashboard page
                return HttpResponseRedirect(reverse('Scanner:home'))
            # If user does not exist
            else:
                # Create an error message
                messages.error(request, "Invalid login details")
                # Redirect back to the login page
                return HttpResponseRedirect(reverse('Scanner:login'))


# Create a view for the register page
class RegisterView(View):
    # Add template name
    template_name = 'Scanner/register.html'

    # Create get function
    def get(self, request):
        # Check if user is logged in
        if request.user.is_authenticated:
            # Redirect back to dashboard if true
            return HttpResponseRedirect(reverse('Scanner:home'))
        # Otherwise
        else:
            # Go to login page
            return render(request, self.template_name)

    # Create post function to process the form on submission
    def post(self, request):
        if request.method == 'POST':
            full_name = request.POST.get('full_name').upper().strip()
            email = request.POST.get('email').strip()
            phone_no = request.POST.get('phone_no')
            username = request.POST.get('username').strip()
            password = request.POST.get('password').strip()
            password2 = request.POST.get('password2').strip()

            if password != password2:
                messages.error(request, "Password does not match")
                return HttpResponseRedirect(reverse('Scanner:register'))
            else:
                # Create user and person object
                user = User.objects.create_user(username=username, password=password)
                person = Person.objects.create(user=user, full_name=full_name, email=email, phone_no=phone_no)


                # Create the qr code
                qrcode_img = qrcode.make(f"{username}-{password}")
                canvas = Image.new("RGB", (300, 300), "white")
                ImageDraw.Draw(canvas)
                canvas.paste(qrcode_img)
                buffer = io.BytesIO()
                canvas.save(buffer, "PNG")
                person.qr_image.save(f"{username}", File(buffer), save=False)
                canvas.close()

                person.save()

                messages.success(request, "Registration successful. Kindly login to your account.")
                return render(request, 'Scanner/code.html', {'person': person})


# Create a view for the home page
class HomeView(View):
    # Add template name
    template_name = 'Scanner/home.html'

    # Create get function
    def get(self, request):
        # Check if user is logged in
        if request.user.is_authenticated:
            # Go to page
            return render(request, self.template_name)
        # Otherwise
        else:
            # Redirect back to login
            return HttpResponseRedirect(reverse('Scanner:login'))


# Create a view for the about page
class AboutView(View):
    # Add template name
    template_name = 'Scanner/about.html'

    # Create get function
    def get(self, request):
        # Check if user is logged in
        if request.user.is_authenticated:
            # Go to page
            return render(request, self.template_name)
        # Otherwise
        else:
            # Redirect back to login
            return HttpResponseRedirect(reverse('Scanner:login'))


# Create a view for the about page
class ContactView(View):
    # Add template name
    template_name = 'Scanner/contact.html'

    # Create get function
    def get(self, request):
        # Check if user is logged in
        if request.user.is_authenticated:
            # Go to page
            return render(request, self.template_name)
        # Otherwise
        else:
            # Redirect back to login
            return HttpResponseRedirect(reverse('Scanner:login'))