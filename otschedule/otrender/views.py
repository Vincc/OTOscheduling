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

    if request.user.is_authenticated: #verify that user is authenticated before allowing access
        if not request.user.is_teacher:#check that user is a student
            renderSessions = request.user.meetingtimes.all()#render homepage directly
            return render(request, "otrender/render.html", {"meetingTimes": renderSessions})
        else: #setup student selection form for teachers before rendering
            rendersessions = []
            currentStudent = ""
            renderform = forms.renderForm(request.user.tutorGroup)
            if request.method == "POST":

                if "renderform" in request.POST:
                    form = forms.renderForm(request.user.tutorGroup, data=request.POST)
                    if form.is_valid():
                        
                        currentStudent = models.user.objects.filter(
                            username=form.cleaned_data.get("studentSelected")).first()
                        rendersessions = models.sessionTimes.objects.filter(
                            students=currentStudent).prefetch_related("students").all().order_by("sessiontimedate")

            return render(request, "otrender/render.html", {"currentStudent": currentStudent, "meetingTimes": rendersessions, "renderform": renderform})
    else:
        return redirect("login")


def scheduleSettings(request):
    generationError = ""
    if request.user.is_admin: #check that user is an admin before allowing access to schedule settings
        #variable definition
        rendersessions = []
        currentStudent = ""
        dates = models.sessiondates.objects.all()
        times = models.sessionTimes.objects.all().order_by("sessiontimedate", "time")
        #format datetimes to be used in schedule generation
        rendertimelist = [time for time in models.sessionTimes.objects.values_list(
            "time", flat=True).distinct()]
        timestemp = [[0 for time in rendertimelist] for date in dates]
        for c, i in enumerate(times):
            timestemp[c//len(rendertimelist)][c%len(rendertimelist)] = i
        times = timestemp
        students = models.user.objects.filter(is_teacher=False)
        
        if request.method == "POST":
            #handles adding dates
            if "dateAddButton" in request.POST:
                form = forms.datesForm(data=request.POST)
                if form.is_valid():
                    inputDate = form.cleaned_data.get("New_Date")
                    if inputDate not in models.sessiondates.objects.values_list("date", flat=True).distinct():
                        newDateEntry = models.sessiondates(date=inputDate)
                        newDateEntry.save()

                        for i in models.sessionTimes.objects.values_list("time", flat=True).distinct():
                            newTimeEntry = models.sessionTimes(
                                time=i, sessiontimedate=models.sessiondates.objects.get(date=inputDate))
                            newTimeEntry.save()

                    return redirect("changeSchedule")
            #handles adding times
            if "timeAddButton" in request.POST:
                form = forms.timesForm(data=request.POST)

                if form.is_valid():
                    inputTime = form.cleaned_data.get("New_Time")
                    for date in dates:

                        newTimeEntry = models.sessionTimes(
                            time=inputTime, sessiontimedate=date)

                        newTimeEntry.save()

                    return redirect("changeSchedule")

            # algorithm for generating timetables

            if "generationButton" in request.POST:

                form = forms.generationForm(data=request.POST)
                if form.is_valid():
                    maxStudents = form.cleaned_data.get(
                        "Maximum_Students_Per_Tutor_Group")
                    numSessions = form.cleaned_data.get(
                        "Number_of_Sessions_Per_Student")
                
                    if (len(rendertimelist)*len(dates))/(maxStudents*numSessions) < 1 or numSessions>len(dates):
                        generationError += "There aren't enough timeslots for all the students."

                    # clear generated table
                    for student in models.user.objects.all():
                        student.meetingtimes.clear()
                    # verify that there are enough timeslots for all students
                    if generationError == "":
                        for tutor in models.user.objects.filter(is_teacher=False).values_list("tutorGroup", flat=True).distinct():
                            studentc = 0
                            currenttutor = list(filter(lambda student: (
                                student.tutorGroup == tutor), students))
                            for date in times:
                                dayc = 0
                                for time in date:
                                    if len(models.sessionTimes.objects.filter(students=currenttutor[studentc % len(currenttutor)]).prefetch_related("students").all()) < numSessions and dayc < len(currenttutor):
                                        try:
                                            currenttutor[studentc % len(
                                                currenttutor)].meetingtimes.add(time)
                                        except IndexError:
                                            pass
                                        dayc +=1
                                        studentc += 1
                                        continue
                                    break
                        generationError += "Successfully Generated."


            if "renderform" in request.POST:
                form = forms.renderForm(request.user.tutorGroup, data=request.POST)
                if form.is_valid():
 
                    currentStudent = models.user.objects.filter(
                        username=form.cleaned_data.get("studentSelected")).first()

                    rendersessions = models.sessionTimes.objects.filter(
                        students=currentStudent).prefetch_related("students").all().order_by("sessiontimedate")

        generateForm = forms.generationForm()
        dateform = forms.datesForm()
        timeform = forms.timesForm()
        renderform = forms.renderForm(request.user.tutorGroup)
        
        
        return render(request, "otrender/adminSettings/schedulechange.html", {"currentStudent": currentStudent, "rendersessions": rendersessions, "renderform": renderform, "dateform": dateform, "timeform": timeform, "dateslist": dates, "timeslist": rendertimelist, "studentlist": students, "generateForm": generateForm, "generationErrorMessage": generationError, })

    else:
        return redirect("renderTimes")


def deleteDate(request, id):
    models.sessiondates.objects.filter(id=id).delete()
    return redirect("changeSchedule")


def deleteTime(request, time):
    models.sessionTimes.objects.filter(time=time).all().delete()
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
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "otrender/registration/login.html", {"login_form": form})


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
