from django import forms
from . import models
class datesForm(forms.Form):
    New_Date = forms.DateField()
    
class timesForm(forms.Form):
    New_Time = forms.TimeField()

class generationForm(forms.Form):
    
    tutorsize = 0
    for teacher in models.user.objects.filter(is_teacher= True, is_admin=False):
        currentTutorGroup = teacher.tutorGroup
        size = len(models.user.objects.filter(is_teacher= False, tutorGroup = currentTutorGroup))
        if size > tutorsize:
            tutorsize = size
    Maximum_Students_Per_Tutor_Group = forms.IntegerField(min_value=tutorsize)
    Number_of_Sessions_Per_Student = forms.IntegerField(min_value=1)

class renderForm(forms.Form):
    
    studentChoices = [(c,student.username) for c,student in enumerate(models.user.objects.filter(is_teacher= False))]
    studentSelected= forms.CharField(label="Select student to render: ", widget=forms.Select(choices=studentChoices))
    
    studentSelected=""
