from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from dashboard.models import UserData
from django.http import JsonResponse
from validate_email import validate_email
import json
from django.core.mail import EmailMessage
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import token_generator
from django.urls import reverse
from django.contrib import auth
import threading
from django.contrib.auth.tokens import PasswordResetTokenGenerator
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    def run(self):
        self.email.send(fail_silently=False)
def EmailValidationView(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid!'})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry this email is in use, choose another one!'})
        return JsonResponse({'email_valid': True})
def UsernameValidationView(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters!'})
        exists = User.objects.filter(username=username).exists()
        if exists:
            return JsonResponse({'username_error': 'Sorry! This username is in use, choose another one! '})
        return JsonResponse({'username_valid': True})
def RegistrationView(request):
    if request.method == 'GET':
        return render(request, 'auth/registration.html')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'fieldValues': request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Please set a password greater than 6 characters!')
                    return render(request, 'auth/registration.html', context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token_generator.make_token(user),
                }
                link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})
                email_subject = 'Activate your account'
                activate_url = 'http://'+current_site.domain+link
                email = EmailMessage(
                    email_subject,
                    'Hi '+user.username + ', we\'re glad that you registered your account with us! Please click the below link to activate your account. Hope you have a wonderful experence with us! \n'+activate_url,
                    'noreply@semycolon.com',
                    [email],
                )
                EmailThread(email).start()
                messages.success(
                    request, 'Your account was created successfully. Please check your mail to activate your account.')
                return redirect('login')
            messages.error(request, 'This email is already registered with us! Please user another one!')
            return render(request, 'auth/registration.html')
        messages.error(request, 'This username is already registered with us! Please user another one!')
        return render(request, 'auth/registration.html')
def VerificationView(request,uidb64, token):
    try:
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)
        if not token_generator.check_token(user, token):
            messages.error(request, 'Wrong activation link!')
            return redirect('login')

        if user.is_active:
            messages.error(request, 'This user is already activated! You may proceed to login now!')
            return redirect('login')
        user.is_active = True
        user.save()
        messages.success(request, 'Your account was activated successfully! You can securely login now!')
        return redirect('login')
    except Exception as ex:
        messages.error(request, 'There was some error in the link that you clicked! Please register yourself again!')
        return redirect('login')
def LoginView(request):
    if request.method == "GET":
        return render(request, 'auth/login.html')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        if email and password:
            try:
                username = User.objects.get(email=email).username
            except Exception as a:
                messages.error(request, 'Invalid credentials!')
                return redirect('login')
            user = auth.authenticate(username = username,password=password)
            if user:
                if user.is_active:
                    if user.is_staff:
                        auth.login(request, user)
                        messages.success(request, 'Welcome ' +
                                 user.username+'! You are now logged in!')
                        return redirect('udashboard')
                    else:
                        auth.login(request, user)
                        messages.success(request, 'Welcome ' +
                                 user.username+'! You are now logged in!')
                        return redirect('dashboard')
                else:
                    messages.error(request, 'Account is not activated yet! Please check your email to activate your account!')
                    return redirect('login')
            else:
                messages.error(
                    request, 'Either your credentials are wrong or you haven\'t activated your account!')
                return redirect('login')
        else:
            messages.error(request, 'Please fill all fields!')
            return redirect('login')
def LogoutView(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')
def RequestPasswordResetEmail(request):
    if request.method == "GET":
        return render(request, 'auth/resetpassword.html')
    if request.method == "POST":
        email = request.POST['email']
        context={'values':request.POST}
        if not User.objects.filter(email=email).exists() or not validate_email(email): 
            messages.error(request, 'This email is not registered with us. Please register yourself first.')
            return render(request, 'auth/resetpassword.html', context)
        current_site = get_current_site(request)
        user = User.objects.filter(email=email)
        if user.exists():
            email_contents = {
                    'user': user[0],
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user[0])),
                    'token': PasswordResetTokenGenerator().make_token(user[0]),}
            link = reverse('reset-user-password', kwargs={
                               'uidb64': email_contents['uid'], 'token': email_contents['token']})
            email_subject = 'Reset your password'
            reset_url = 'http://'+current_site.domain+link
            email = EmailMessage(
                    email_subject,
                    'Hi there!, Please click the link below to set a new password for your account \n'+ reset_url,
                    'noreply@semycolon.com',
                    [email],)
            EmailThread(email).start()
            messages.success(request, 'We have sent you an email with the link to reset your password')
            return render(request, 'auth/resetpassword.html')
def CompletePasswordReset(request,uidb64, token):
    if request.method=="GET":
        context = {'uidb64':uidb64,'token':token}
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(username=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, 'Password link is invalid or has been used earlier, please request a new one.')
                return render(request, 'auth/resetpassword.html')
        except Exception as a: 
            messages.info(request, 'Something went wrong, try again.')   
        return render( request, 'auth/setnewpass.html', context)
    if request.method=="POST":
        context = {'uidb64':uidb64,'token':token}
        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            messages.error(request, 'Passwords do not match. Re-enter both again.')
            return render( request, 'auth/setnewpass.html', context)
        if len(password)<6:
            messages.error(request, 'Enter a password greater than 6 characters.')
            return render( request, 'auth/setnewpass.html', context)
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(username=id)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful. You can login with the new password.')
            return redirect('login')
        except Exception as ex:
            messages.info(request, 'Something went wrong, try again.')
            return render( request, 'auth/setnewpass.html', context)