import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken

from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
# @api_view(['POST'])
def signin(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    _, token = AuthToken.objects.create(user)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            # return render(request, "home.html")
            # return JsonResponse({"status": True, "message": "success"}, content_type="application/json")
            # return JsonResponse({"UserName": username, "Password": password},
            #                     content_type="application/json")
            return JsonResponse({"UserName": username, "Password": password, 'Token': token},
                                content_type="application/json")
        else:
            return HttpResponse("Invalid!")

    return render(request, "login.html")


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        # cpassword = request.POST['password1']
        try:
            user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                            last_name=last_name, email=email)
            user.save()
            return redirect('signin')
        except Exception as e:
            print(e)
    return render(request, "register.html")


def signout(request):
    auth.logout(request)
    return redirect(signin)


def index(request):
    return render(request, "index.html")
