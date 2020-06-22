import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from student_management_app.EmailBackEnd import EmailBackEnd


# Create your views here.
def showDemoPage(request):
    return render(request, "demo.html")


def showloginPage(request):
    return render(request, "login_page.html")


def dologin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
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
    data = 'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
           'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js");' \
 \
 \
           'var firebaseConfig = {' \
           'apiKey: "YOUR_API_KEY",' \
           'authDomain: "YOUR_FIREBASE_DOMAIN_NAME",' \
           'databaseURL: "YOUR_FIREBASE_DATBASE_URL",' \
           'projectId: "YOUR_FIREBASE_PROJECT_ID",' \
           'storageBucket: "YOUR_FIREBASE_STORAGE_BUCKET END WITH appspot.com",' \
           'messagingSenderId: "YOUR SENDER ID",' \
           'appId: "YOUR APP ID",' \
           'measurementId: "YOUR MEASUREMENT ID"' \
           '};' \
 \
           'firebase.initializeApp(firebaseConfig);' \
           'const messaging=firebase.messaging();' \
 \
           'messaging.setBackgroundMessageHandler(function (payload) {' \
           'console.log(payload);' \
           'const notification=JSON.parse(payload);' \
           'const notificationOption={' \
           'body:notification.body,' \
           'icon:notification.icon' \
           '};' \
           'return self.registration.showNotification(payload.notification.title,notificationOption);' \
           '});'
    return HttpResponse(data,content_type="text/javascript")
