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
		return render(request, "otrender/render.html")

	else:
		return redirect("login")

def scheduleSettings(request):
	generationError = ""
	if  request.user.is_admin:
		rendersessions = []
		times = [i for i in models.sessionTimes.objects.all()]
		dates = [i for i in models.sessiondates.objects.all()]
		students = [i for i in models.user.objects.filter(is_teacher = False)]
		teachers = [i for i in models.user.objects.filter(is_teacher= True, is_admin=False)]
		if request.method == "POST":
			if "dateAddButton" in request.POST:
				form = forms.datesForm(data=request.POST)
				if form.is_valid():
					inputDate = form.cleaned_data.get("New_Date")
					newDateEntry = models.sessiondates(date=inputDate)
					newDateEntry.save()
					return redirect("changeSchedule")
			if "timeAddButton" in request.POST:
				form = forms.timesForm(data=request.POST)
				if form.is_valid():
					inputTime = form.cleaned_data.get("New_Time")
					newTimeEntry = models.sessionTimes(time=inputTime)
					newTimeEntry.save()
					return redirect("changeSchedule")

			#algorithm for generating timetables

			if "generationButton" in request.POST:
				
				form = forms.generationForm(data=request.POST)
				if form.is_valid():
					maxStudents = form.cleaned_data.get("Maximum_Students_Per_Tutor_Group")
					numSessions = form.cleaned_data.get("Number_of_Sessions_Per_Student")
					
					if int((len(times)*len(dates))/(maxStudents*numSessions)) < 1:
						generationError += "There aren't enough timeslots for all the students."	

					#verify that there are enough timeslots for all students
					
					if generationError == "":
						c = 0
						for teacher in teachers:
							currenttutor = list(filter(lambda student: (student.tutorGroup == teacher.tutorGroup), students))
							for date in dates:
								for time in times:
									if c<numSessions:
										try:
											currenttutor[c].meetingtimes.add(time)
										except IndexError:
											pass
										
										c+=1
										continue
									c=0

						generationError += "Successfully Generated."
			
			if "renderform" in request.POST:
				form = forms.renderForm(data=request.POST)
				if form.is_valid():
					currentStudent = models.user.objects.filter(username = form.cleaned_data.get("studentSelected")).first()

					rendersessions = models.sessionTimes.objects.filter(students = currentStudent).prefetch_related('students').all()
					

		generateForm = forms.generationForm()
		dateform = forms.datesForm()
		timeform = forms.timesForm()
		renderform = forms.renderForm()

		
		return render(request, "otrender/adminSettings/schedulechange.html", {"rendersessions": rendersessions, "renderform": renderform, "dateform":dateform,"timeform":timeform, "dateslist":dates, "timeslist":times, "studentlist":students, "generateForm": generateForm, "generationErrorMessage":generationError,})
		
	else:
		return redirect("renderTimes")
	





def deleteDate(request, id):
	models.sessiondates.objects.filter(id=id).delete()
	return redirect("changeSchedule")
def deleteTime(request, id):
	models.sessionTimes.objects.filter(id=id).delete()
	return redirect("changeSchedule")
	
def userSettings(request):
	if  request.user.is_admin:
		users = [i for i in models.user.objects.all()]
		return render(request, "otrender/adminSettings/userchange.html", {"userslist":users})

	else:
		return redirect("renderTimes")

def login_request(request): 
	if request.method == "POST": 
		form = AuthenticationForm(request, data=request.POST) 
		if form.is_valid(): 
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("renderTimes")
			else:
				messages.error(request,"Invalid username or password. ss")
		else:
			messages.error(request,"Invalid username or passwordsss.")
	form = AuthenticationForm()
	return render(request, "otrender/registration/login.html", {"login_form":form})
	
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("renderTimes")

def change_Password(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			form = PasswordChangeForm(request.user, request.POST)
			if form.is_valid():
				user = form.save()
				update_session_auth_hash(request, user) 
				messages.success(request, "Your password is changed")
				return redirect("renderTimes")
			else:
				messages.error(request, "Error:")
		else:
			form = PasswordChangeForm(request.user)
		return render(request, "otrender/registration/changepass.html", {"form": form})
	else:
		return redirect("login")