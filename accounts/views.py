from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            # 1. Create the user (Ensure your model default is is_active=False)
            user = Account.objects.create_user(
                first_name=first_name, 
                last_name=last_name, 
                email=email, 
                username=username, 
                password=password
            )
            user.phone_number = phone_number
            user.save()

            # 2. Email Verification Logic
            current_site = get_current_site(request)
            mail_subject = 'NEMA Ecommerce Portal Account Confirmation'
            
            # Pass the data clearly to the template
            context = {
                'user': user,
                'domain': current_site.domain, # CRITICAL: use .domain
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }
            
            message = render_to_string('accounts/account_verification_email.html', context)
            
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.content_subtype = "html" # Ensures HTML rendering
            send_email.send()
            
            messages.success(request, 'Registration successful! Check your email for confirmation.', extra_tags='success_registration')
            return redirect('register') # Better to redirect than render after POST
    else:
        form = RegistrationForm()
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        # Handle login logic here
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user=auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.', extra_tags='success_login')
            return redirect('home')
        else:
            messages.error(request, "Invalid login credentials", extra_tags='error_login')
            return redirect('login')
        pass
    return render(request, 'accounts/login.html')

@login_required(login_url='login')

def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out.', extra_tags='success_logout')
    return redirect('home')

def activate(request,uidb64, token):
    # Activation logic to be implemented
    return HttpResponse('Account activated successfully!')