from django.contrib.auth import forms
from django.shortcuts import render, redirect 
from django.http import HttpResponse 
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm 
from django.contrib.auth import login, authenticate, logout 
from django.contrib import messages 
from django.contrib.auth import update_session_auth_hash 
from . import forms
from . import models

def renderTimes(request):
	if request.user.is_authenticated:



		return render(request, 'otrender/render.html')
	else:
		return redirect('login')

def scheduleSettings(request):
	if  request.user.is_superuser:
		if request.method == "POST":
			if "dateAddButton" in request.POST:
				form = forms.datesForm(data=request.POST)
				if form.is_valid():
					inputDate = form.cleaned_data.get('new_date')
					newDateEntry = models.sessiondates(date=inputDate)
					newDateEntry.save()
					return redirect("changeSchedule")
			if "timeAddButton" in request.POST:
				form = forms.timesForm(data=request.POST)
				if form.is_valid():
					inputTime = form.cleaned_data.get('new_time')
					newTimeEntry = models.sessionTimes(time=inputTime)
					newTimeEntry.save()
					return redirect("changeSchedule")
		dateform = forms.datesForm()
		timeform = forms.timesForm()
		times = [i for i in models.sessionTimes.objects.all()]
		dates = [i for i in models.sessiondates.objects.all()]
		return render(request, "otrender/adminSettings/schedulechange.html", {"dateform":dateform,"timeform":timeform, "dateslist":dates, "timeslist":times})
		
	else:
		return redirect("renderTimes")
	
def deleteDate(request, id):
	models.sessiondates.objects.filter(id=id).delete()
	return redirect("changeSchedule")
def deleteTime(request, id):
	models.sessionTimes.objects.filter(id=id).delete()
	return redirect("changeSchedule")
	
def userSettings(request):
	if  request.user.is_superuser:
		users = [i for i in models.user.objects.all()]
		return render(request, "otrender/adminSettings/userchange.html", {"userslist":users})

	else:
		return redirect("renderTimes")

def login_request(request): 
	if request.method == "POST": 
		form = AuthenticationForm(request, data=request.POST) 
		if form.is_valid(): 
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("renderTimes")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request, "otrender/registration/login.html", {"login_form":form})
	
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("renderTimes")

def change_Password(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = PasswordChangeForm(request.user, request.POST)
			if form.is_valid():
				user = form.save()
				update_session_auth_hash(request, user) 
				messages.success(request, 'Your password is changed')
				return redirect('renderTimes')
			else:
				messages.error(request, 'Error:')
		else:
			form = PasswordChangeForm(request.user)
		return render(request, 'otrender/registration/changepass.html', {'form': form})
	else:
		return redirect('login')