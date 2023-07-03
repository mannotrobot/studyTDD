import uuid
import sys

from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.core.mail import send_mail

#from accounts.core.mail import send_mail


def send_login_email(request):
    """выслать ссылку на логин по почте"""
    email = request.POST['email']
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    print('saving uid', 'for email', email, file=sys.stderr)
    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')
    send_mail(
        "Your login link for Superlist",
        f'Use this link to log in:\n\n{url}',
        'noreply@superlists',
        [email],
    )
    return render(request, 'login_email_sent.html')


def login(request):
    """регистрация в системе"""
    print('login view', file=sys.stderr)
    uid = request.GET.get('uid')
    user = authenticate(uid=uid)
    if user is not None:
        auth_login(request, user)
    return redirect('/')


def logout(request):
    """выход из системы"""
    auth_logout(requst)
    redirect('/')