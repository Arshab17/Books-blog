from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
import string
import random
from.models import UserOTP
# Create your views here.
#user account.
def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user = User.objects.filter(username = username)
            if not user:
                User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password2,
                )

                # otp = random.randrange(1000, 9999)
                # subject = 'Account Verification'
                # message = f'One Time Password(OTP) - {otp}'
                # from_email = 'arshab98@gmail.com'
                # to = [email]
                #
                # send_mail(
                #     subject=subject,
                #     message=message,
                #     from_email=from_email,
                #     recipient_list=to,
                #     fail_silently=False
                # )
                # UserOTP.objects.create(
                #     user=user,
                #     otp=otp
                #
                # )


                messages.success(request, 'Account has been created')
                # return redirect('login_otp',username)


                return redirect('signin')
            else:
                messages.error(request, 'username exist')

        else:
            messages.error(request,'invalid password')

    return render(request,'account/signup.html')

# def login_otp(request,username):
#     user = User.objects.get(username=username)
#     if request.method == 'POST':
#         otp_obj = UserOTP.objects.get(user=user)
#         otp = request.POST.get('otp')
#
#         if otp == otp_obj.otp:
#             messages.success(request, 'otp verified')
#             return redirect('signin')
#
#         messages.error(request, 'invalid')
#         return redirect('login_otp',username)
#     return render(request, 'account/login_otp.html', {'email': user.email})

# authentication backend
# class OTPBackend:
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         user = authenticate(username=username, password=password)
#         if user:
#             try:
#                 otp_record = UserOTP.objects.get(user=user)
#                 if not otp_record.is_verified:
#                     return None
#             except UserOTP.DoesNotExist:
#                 pass
#             return user
#         return None
#
#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username= username,password=password)
        if user is not None:
            # if user.is_active:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'your account is inactive.')
        messages.error(request,'invalid username or password')
    return render(request,'account/signin.html')

def signout(request):
    logout(request)
    return redirect('signin')

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username)
        if user:
            email = user.first().email
            otp = random.randrange(1000,9999)
            subject = 'password reset'
            message = f'One Time Password(OTP) - {otp}'
            from_email = 'arshab98@gmail.com'
            to = [email]

            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=to,
                fail_silently=False
            )
            # user_otp = UserOTP.objects.filter(user=user.first())
            # if user_otp:
            #     user_otp= user_otp.first()
            #     user_otp.otp = otp
            #     user_otp.save()
            # else:
            #
            #     UserOTP.objects.create(
            #         user = user.first(),
            #         otp = otp
            # )
            UserOTP.objects.update_or_create(
                user = user.first(),
                defaults={
                    'otp':otp
                }
            )
            return redirect('otp_verify',username)
        messages.error(request,'username doesn\'t exist')


    return render(request,'account/forget.html')

def otp_verify(request,username):
    user = User.objects.get(username =username)
    if request.method == 'POST':
        otp_obj = UserOTP.objects.get(user = user)
        otp = request.POST.get('otp')

        if otp == otp_obj.otp:
            messages.success(request,'otp verified')
            return redirect('password_change',username)

        messages.error(request,'invalid')
    return render(request,'account/otp_verify.html',{'email':user.email})

def password_change(request,username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user.set_password(password1)
            user.save()
            messages.success(request,'password changed')
            return redirect('signin')
    messages.error(request,'password doesn\t match')
    return render(request,'account/password_change.html')