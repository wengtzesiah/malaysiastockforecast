from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from malaysiastockforecast import settings
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from . tokens import generate_token

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def aboutus(request):
    return render(request, "authentication/aboutus.html")

def reg_success(request):
    return render(request, "authentication/registersuccess.html")

def signup(request):
    
    if request.method == "POST":
        # username = request.POST.get('username')
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        #verification
        # if User.objects.filter(email= email):
        #     messages.error(request, "Account already existed! Please try with other email address!")
        #     return redirect('home')
        
        if password1 != password2:
            messages.error(request, "Password entered is not match, please try again")
            return redirect('signup')


        newuser = User.objects.create_user(username, email, password1)
        newuser.first_name = fname
        newuser.last_name = lname
        newuser.is_active = False
        newuser.save()

        messages.success(request, "Your Account has been successfully created")

        # Welcome Email
        email_welcome_subject = "Welcome to QinCast"
        email_welcome_message = "Hello" + newuser.first_name + " !! \n" + "Nice to meet you."
        from_email = settings.EMAIL_HOST_USER
        to_list = [newuser.email]
        send_mail(email_welcome_subject, email_welcome_message, from_email, to_list, fail_silently=True)

        # Confirmation Email
        current_site = get_current_site(request)
        email_confirm_subject = "Account Creation Verification @ QinCast"
        email_confirm_message = render_to_string('email_confirmation.html',{
            'name' : newuser.first_name,
            'domain' : current_site.domain,
            'uid' : urlsafe_base64_encode(force_bytes(newuser.pk)),
            'token' : generate_token.make_token(newuser),
        })
        email = EmailMessage(
            email_confirm_subject,
            email_confirm_message,
            settings.EMAIL_HOST_USER,
            [newuser.email],
        )
        email.fail_silently = True
        email.send()


        return redirect('success')

    
    return render(request, "authentication/signup.html")

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password']

        user = authenticate(username=username, password=password1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname': fname})

        else:
            messages.error(request, "Bad Credentials!")
            return redirect('home')

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Sccessfully!")
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = str(urlsafe_base64_decode(uidb64), 'utf-8')
        newuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        newuser = None
    
    if newuser is not None and generate_token.check_token(newuser, token):
        newuser.is_active = True
        newuser.save()
        login(request, newuser)
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')
