from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, EditUserProfileForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

# Signup view function
def sign_up(request):
    if not request.user.is_authenticated:
      if request.method == 'POST':
          fm = SignUpForm(request.POST)
          if fm.is_valid():
           messages.success(request, 'Account created successfully !!')
           fm.save()

      else:
        fm = SignUpForm()
      return render(request, 'AuthApp/signup.html', {'form':fm})
    else:
      return HttpResponseRedirect('/profile/') 
 
# Login view function
def log_in(request):
   if not request.user.is_authenticated:
      if request.method == 'POST':
        fm = AuthenticationForm(request=request, data = request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username = uname, password = upass)
            if user is not None:
              login(request, user)
              return HttpResponseRedirect('/profile/')
      else:
        fm = AuthenticationForm()
      return render(request, 'AuthApp/userLogin.html', {'form':fm})
   else:
      return HttpResponseRedirect('/profile/')

#Profile View   
def user_profile(request, ):
   if request.user.is_authenticated:
      if request.method == 'POST':
         fm = EditUserProfileForm(request.POST, instance = request.user)
         if fm.is_valid():
            messages.success(request, 'Profile Updated !!')
            fm.save()
      else:
         fm = EditUserProfileForm(instance = request.user)
      return render(request, 'AuthApp/profile.html', {'name': request.user, 'form':fm})
   else:
      return HttpResponseRedirect('/login/')


#Logout View
def user_logout(request):
   logout(request)
   return HttpResponseRedirect('/login/')


#Change Password with old passwords View
def user_change_pass(request):
   if request.user.is_authenticated:
      if request.method == 'POST':
       fm = PasswordChangeForm(user=request.user, data=request.POST)
       if fm.is_valid():
         fm.save()
         update_session_auth_hash(request, fm.user)
         return HttpResponseRedirect('/profile/')
      else:
         fm = PasswordChangeForm(user = request.user)
      return render(request, 'AuthApp/changepassword.html', {'form':fm})
   
   else:
      return HttpResponseRedirect('/login/')

#Change passwords without old passwords

def user_change_pass1(request):
   if request.user.is_authenticated:
      if request.method == 'POST':
       fm = SetPasswordForm(user=request.user, data=request.POST)
       if fm.is_valid():
         fm.save()
         update_session_auth_hash(request, fm.user)
         return HttpResponseRedirect('/profile/')
      else:
         fm = SetPasswordForm(user = request.user)
      return render(request, 'AuthApp/changepassword1.html', {'form':fm})
   
   else:
      return HttpResponseRedirect('/login/')