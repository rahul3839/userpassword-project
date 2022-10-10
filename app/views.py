
from django.shortcuts import render,HttpResponseRedirect
from .forms import UserForm,EditUserProfileForm,EditAdminProfileForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm
from django.contrib.auth import authenticate ,login ,logout,update_session_auth_hash
from django.contrib.auth.models import User
# Create your views here.

#----------------------Registrtion View Function----------
def signup(request):
    if request.method == 'POST':                                # admin
        fm = UserForm(request.POST)                              #password123#
        if fm.is_valid():
          messages.success(request,'Your Account has been Created.!!!!!!')
          fm.save()
          fm =UserForm()
    else:
        fm =UserForm()
    return render(request,'app/signup.html',{'form':fm})

# --------------------------Login view Fucntion--------------------
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password'] 
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'your login sucessfully!!!')
                    return HttpResponseRedirect('/profil/')
                
        else:
            fm = AuthenticationForm()
            
        return render(request,'app/userlogin.html',{"form":fm})
    else:
        return HttpResponseRedirect('/profil/')

#---------------User profile------------------------
def user_profile(request):
    
        if request.method == 'POST':
            if request.user.is_superuser == True:
                fm = EditAdminProfileForm(request.POST,instance=request.user)
                users = User.objects.all()
            else:
                fm = EditUserProfileForm(request.POST,instance=request.user)
            if fm.is_valid():
                messages.success(request,'update successfull.!!!!')
                fm.save()
               
        else:
            if request.user.is_superuser == True:#----admin---------
                fm = EditAdminProfileForm(instance = request.user)
                users = User.objects.all()
            else:
                fm = EditUserProfileForm(instance = request.user) #----to login bydefault 
                users = None
        return render(request,'app/profil.html',{'name':request,'form':fm,'users':users})
   

 #---------------------user logout----------------------
def userlogout(request):
    logout(request) 
    return HttpResponseRedirect('/login/')


#------------------Change Password with Old Password--------------------
def change_pass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PasswordChangeForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request,fm.user)# sension controll
                messages.success(request,'Password has been change successfully...')
                return HttpResponseRedirect('/profil/')
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request,'app/changepass.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')

#------------------Change Password without Old Password--------------------
def change_pass1(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = SetPasswordForm(user=request.user,data=request.POST) # SetPasswordForm they did not show the old password   
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request,fm.user)# sension controll
                messages.success(request,'Password has been change successfully...')
                return HttpResponseRedirect('/profil/')
        else:
            fm = SetPasswordForm(user=request.user)
        return render(request,'app/changepass1.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')

#--------------------USER DETAILS------------------------------------
def user_detail(request,id):
    if request.user.is_authenticated:
        pi = User.objects.get(pk=id)
        fm = EditAdminProfileForm(instance = pi)
        return render(request,'app/userdetail.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')