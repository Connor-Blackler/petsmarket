from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


@login_required(login_url="account_login")
def my_profile(request):
    my_profile = request.user.profile

    context = {"profile": my_profile}
    return render(request, 'users/user-account.html', context)
