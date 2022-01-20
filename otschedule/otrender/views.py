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
		if not request.user.is_teacher:
			renderSessions = request.user.meetingtimes.all()
			return render(request, "otrender/render.html", {"meetingTimes":renderSessions})
		else:
			rendersessions = []
			renderform = forms.renderForm()
			if request.method == "POST":
				
				if "renderform" in request.POST:
					form = forms.renderForm(data=request.POST)
					if form.is_valid():
						
						currentStudent = models.user.objects.filter(username = form.cleaned_data.get("studentSelected")).first()
						
						rendersessions = models.sessionTimes.objects.filter(students = currentStudent).prefetch_related("students").all()
					
			return render(request, "otrender/render.html", {"meetingTimes": rendersessions, "renderform": renderform})
	else:
		return redirect("login")

def scheduleSettings(request):
	generationError = ""
	if  request.user.is_admin:
		rendersessions = []
		times = models.sessionTimes.objects.all().order_by('sessiontimedate', "time")
		dates = models.sessiondates.objects.all()
		students = models.user.objects.filter(is_teacher = False)
		
		if request.method == "POST":
			if "dateAddButton" in request.POST:
				form = forms.datesForm(data=request.POST)
				if form.is_valid():
					inputDate = form.cleaned_data.get("New_Date")
					if inputDate not in models.sessiondates.objects.values_list("date", flat=True).distinct():
						newDateEntry = models.sessiondates(date=inputDate)
						newDateEntry.save()
						print("saved")
						for i in models.sessionTimes.objects.values_list("time", flat=True).distinct():
							newTimeEntry = models.sessionTimes(time = i, sessiontimedate = models.sessiondates.objects.get(date = inputDate))
							newTimeEntry.save()
					
					return redirect("changeSchedule")
			if "timeAddButton" in request.POST:
				form = forms.timesForm(data=request.POST)
				
				if form.is_valid():
					inputTime = form.cleaned_data.get("New_Time")
					for date in dates:	
						print(date)
						print(inputTime)
						
						newTimeEntry = models.sessionTimes(time=inputTime, sessiontimedate = date)
						print(newTimeEntry.id)
						newTimeEntry.save()
						print(models.sessionTimes.objects.first().time)
					return redirect("changeSchedule")

			#algorithm for generating timetables

			if "generationButton" in request.POST:
				
				form = forms.generationForm(data=request.POST)
				if form.is_valid():
					maxStudents = form.cleaned_data.get("Maximum_Students_Per_Tutor_Group")
					numSessions = form.cleaned_data.get("Number_of_Sessions_Per_Student")
					
					if int((len(times)*len(dates))/(maxStudents*numSessions)) < 1:
						generationError += "There aren't enough timeslots for all the students."	

			
					#clear generated table
					for student in models.user.objects.all():

						student.meetingtimes.clear()


					#verify that there are enough timeslots for all students
					
					if generationError == "":
							
						for tutor in models.user.objects.filter(is_teacher = False).values_list("tutorGroup", flat=True).distinct():
							studentc = 0
							currenttutor = list(filter(lambda student: (student.tutorGroup == tutor), students))
							for time in times: 
								if len(models.sessionTimes.objects.filter(students = currenttutor[studentc%len(currenttutor)]).prefetch_related("students").all())<numSessions:
									try: 
										currenttutor[studentc%len(currenttutor)].meetingtimes.add(time)
									except IndexError:
										pass
										
									studentc+=1
									continue
								break	
				
						generationError += "Successfully Generated."
			
			if "renderform" in request.POST:
				form = forms.renderForm(data=request.POST)
				if form.is_valid():
					
					currentStudent = models.user.objects.filter(username = form.cleaned_data.get("studentSelected")).first()

					rendersessions = models.sessionTimes.objects.filter(students = currentStudent).prefetch_related("students").all()
					

		generateForm = forms.generationForm()
		dateform = forms.datesForm()
		timeform = forms.timesForm()
		renderform = forms.renderForm()
		rendertimelist = [time for time in models.sessionTimes.objects.values_list("time", flat=True).distinct()]
		print(rendertimelist)
		return render(request, "otrender/adminSettings/schedulechange.html", {"rendersessions": rendersessions, "renderform": renderform, "dateform":dateform,"timeform":timeform, "dateslist":dates, "timeslist":rendertimelist, "studentlist":students, "generateForm": generateForm, "generationErrorMessage":generationError,})
		
	else:
		return redirect("renderTimes")
	





def deleteDate(request, id):
	models.sessiondates.objects.filter(id=id).delete()
	return redirect("changeSchedule")
def deleteTime(request, id):
	models.sessionTimes.objects.filter(time=models.sessionTimes.objects.get(id=id).time).delete()
	return redirect("changeSchedule")
	


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