from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View
from django.contrib.auth.models import User
from nightlifeapp.models import *
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse

class index(TemplateView):
    template_name="index.html"
    
class usersignup(TemplateView):
    template_name="user_signup.html"

    def post(self,request,*args,**kwargs):
        full_name = request.POST["full_name"]
        email = request.POST["email"]
        phone_number = request.POST["phone"]
        address = request.POST["address"]
        username = request.POST["username"]
        password = request.POST["password"]
        if User.objects.filter(username=username).exists():
            return HttpResponse(f"<script>alert('Username already exists');window.location.href='/login/'</script>")
        else:
            user = User.objects.create_user(username=username,password=password,email=email,first_name=full_name,last_name='1')
            user.save()
            usersignup = UserSignup.objects.create(user=user,phone=phone_number,address=address)
            usersignup.save()
            userType = usertype.objects.create(user=user,type='user')
            userType.save()
            return HttpResponse(f"<script>alert('Signup Successful');window.location.href='/login/'</script>")


class organizersignup(TemplateView):
    template_name="organizer_signup.html"

    def post(self,request,*args,**kwargs):
        full_name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        image = request.FILES["image"]
        id_proof = request.FILES["id_proof"]
        username = request.POST["username"]
        password = request.POST["password"]
        if User.objects.filter(username=username).exists():
            return HttpResponse(f"<script>alert('Username already exists');window.location.href='/login/'</script>")
        else:
            user = User.objects.create_user(username=username,password=password,email=email,first_name=full_name,last_name='0')
            user.save()
            organizersignup = OrganizerSignup.objects.create(user=user,phone=phone,address=address,image=image,id_proof=id_proof)
            organizersignup.save()
            ut = usertype.objects.create(user=user,type='organizer')
            ut.save()
            return HttpResponse(f"<script>alert('Registration Successful');window.location.href='/login/'</script>")

class loginview(TemplateView):
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        if user is None:
            return HttpResponse("<script>alert('Invalid user name or password');window.location.href='/login/'</script>")

        # Admin: no verification needed
        if user.is_superuser:
            login(request, user)
            return redirect('/adminpage/')

        # Users and organizers must be verified
        if user.last_name == '1':
            login(request, user)
            user_type = usertype.objects.get(user_id=user.id).type
            if user_type == 'user':
                return redirect('/user/')
            elif user_type == 'organizer':
                return redirect('/organizer/')

        return HttpResponse("<script>alert('user account not verified');window.location.href='/login/'</script>")