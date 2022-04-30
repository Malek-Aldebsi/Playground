from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationFrom
from django.contrib.auth.decorators import login_required
from .models import Profile

from django.http import HttpResponse


def homePage(request):
    context = {}
    return render(request, 'pages/homePage.html', context)


def loginUser(request):

    if request.user.is_authenticated:  # if user already signin
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)  # check if user and pass are correct

            if user is not None:
                login(request, user)

                return redirect(request.GET['next'] if 'next' in request.GET else 'home')
            else:
                messages.error(request, 'Username or password is incorrect')

        except:
            messages.error(request, 'Username does not exist')

    return render(request, 'login/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationFrom()

    if request.method == 'POST':
        form = CustomUserCreationFrom(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'An error has occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'login/login_register.html', context)


@login_required(login_url='login')
def ticket(request):
    profile = request.user.profile
    ticketID = str(profile.ticket.id)[:8]

    context = {'user': profile, 'ticketID': ticketID}
    return render(request, 'ticket/ticket.html', context)


@login_required(login_url='login')
def buyTicket(request):
    profile = request.user.profile
    userTicket = profile.ticket

    if userTicket.haveOne==True:
        return ticket(request)

    elif request.method == 'POST':
        userTicket.haveOne = True
        userTicket.save()
        return redirect('ticket')  # ticketPage

    context = {}
    return render(request, 'ticket/buyTicket.html', context)


def ticketState(request, pk):
    try:
        user = Profile.objects.get(id=pk)

        if request.user.is_superuser:
            userTicket = user.ticket

            context = {'user': user, 'ticket': userTicket}
            return render(request, 'ticket/ticketValidation.html', context)
        elif user:
            havingTicket = user.ticket.haveOne
            return HttpResponse(str(havingTicket)+"  "+str(user))
    except:
        return HttpResponse("No such ticket")


def ticketChecker(request, pk):
    user = Profile.objects.get(id=pk)
    ticket = user.ticket
    ticket.numberOfScans += 1
    ticket.save()

    return HttpResponse("Done")


def map(request):
    return render(request, 'services/map.html')
