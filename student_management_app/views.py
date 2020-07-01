import datetime
import json
import os

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from student_management_app.EmailBackEnd import EmailBackEnd
from student_management_system import settings


# Create your views here.
def showDemoPage(request):
    return render(request, "demo.html")


def showloginPage(request):
    return render(request, "login_page.html")


def dologin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        captcha_token = request.POST.get("g-recaptcha-response")
        cap_url = "https://www.google.com/recaptcha/api/siteverify"
        cap_secret = "6LdRyKsZAAAAADP-mCbqbzp2AdRjNUGjWFZjLg1w"
        cap_data = {"secret": cap_secret, "response": captcha_token}
        cap_server_response = requests.post(url=cap_url, data=cap_data)
        cap_jason = json.loads(cap_server_response.text)

        if cap_jason['success'] == False:
            messages.error(request, "Invalid Captcha Try Again")
            return HttpResponseRedirect("/")
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"),
                                         password=request.POST.get("password"))
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request, "Invalid login details")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("User : " + request.user.email + " usertype : " + str(request.user.user_type))
    else:
        return HttpResponse("Please login first")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


def showFirebaseJS(request):
    data = 'importScripts("https://www.gstatic.com/firebasejs/7.15.4/firebase-app.js");' \
           'importScripts("https://www.gstatic.com/firebasejs/7.15.4/firebase-messaging.js");' \
           'var firebaseConfig = {' \
           '        apiKey: "AIzaSyByJtFBZvXE1gv35I1qPctEnZ1oNI64QYE",' \
           '        authDomain: "student-management-syste-bdbe2.firebaseapp.com",' \
           '        databaseURL: "https://student-management-syste-bdbe2.firebaseio.com",' \
           '        projectId: "student-management-syste-bdbe2",' \
           '        storageBucket: "student-management-syste-bdbe2.appspot.com",' \
           '        messagingSenderId: "1031958236957",' \
           '        appId: "1:1031958236957:web:e5b07faf9473bc9707dbf4",' \
           '        measurementId: "G-M832VZDGJC"' \
           ' };' \
           'firebase.initializeApp(firebaseConfig);' \
           'const messaging=firebase.messaging();' \
           'messaging.setBackgroundMessageHandler(function (payload) {' \
           '    console.log(payload);' \
           '    const notification=JSON.parse(payload);' \
           '    const notificationOption={' \
           '        body:notification.body,' \
           '        icon:notification.icon' \
           '    };' \
           '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
           '});'

    return HttpResponse(data, content_type="text/javascript")
