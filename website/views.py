from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Item
from datetime import datetime
from django.core.mail import send_mail
import smtplib


def home(request):
    return render(request, 'home.html')


def login_(request):
    if request.method == 'POST':
        if 'signup' in request.POST:
            fname = request.POST['fname']
            lname = request.POST['lname']
            uname = request.POST['uname']
            email = request.POST['email']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']

            if pass1 != pass2:
                messages.warning(request, 'Password not matched!')
                return redirect('')

            elif User.objects.filter(username=uname).exists():
                messages.warning(request, 'Username already exists!')

            elif User.objects.filter(email=email).exists():
                messages.warning(request, 'Email already exists!')

            else:
                user = User.objects.create_user(
                    username=uname, password=pass1, email=email, first_name=fname, last_name=lname)
                user.save()
                messages.success(request, 'Signup Successfully!')

        else:
            uname = request.POST['uname']
            pass1 = request.POST['pass1']
            user = authenticate(username=uname, password=pass1)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login Successfully!')
                return redirect('home')
            else:
                messages.warning(request, 'Email not exists! Login first.')

        return redirect('login')

    context = {}
    return render(request, 'login.html', context)


def logout_(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')


def items(request):
    all_items = Item.objects.all()
    context = {'all_items': all_items}
    return render(request, 'items.html', context)


def notification(request, days):
    email_sender = 'foodexpirydatetracker@gmail.com'
    email_password = 'azpaqpgbbuwuqnbr'
    email_receiver = request.user.email

    subject = 'Alert!'
    body = 'The item has ' + days + ' days left to be expired.'

    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.login(email_sender, email_password)
    s.sendmail(email_sender, email_receiver, body)
    s.quit()

    messages.success(request, 'Email Sent!')
    return redirect('items')


def additem(request):
    if request.method == 'POST':
        itemname = request.POST['itemname']
        photo = request.POST['photo']
        price = request.POST['price']
        quantity = request.POST['quantity']
        date = request.POST['date']
        description = request.POST['description']
        options = request.POST['options']

        date_format = "%Y-%m-%d"
        a = datetime.strptime(str(datetime.now().date()), date_format)
        b = datetime.strptime(str(date), date_format)
        delta = b - a
        days = delta.days

        item = Item(itemname=itemname, photo=photo, price=price,
                    quantity=quantity, date=date, days=days, description=description, options=options)
        item.save()
        messages.success(request, 'New Item Added!')
        return redirect('additem')

    return render(request, 'additem.html')


def about(request):
    return render(request, 'about.html', {})
