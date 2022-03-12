from random import choices
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
    def __init__(self, currentTutor, *args, **kwargs):
        
        if currentTutor != "0000":
            self.studentChoices = sorted([(student.username,student.username) for student in models.user.objects.filter(is_teacher= False, tutorGroup = currentTutor)])
        else:
            self.studentChoices = sorted([(student.username,student.username) for student in models.user.
            objects.filter(is_teacher= False)])
        
        super(renderForm,self).__init__(*args,**kwargs)
        self.fields["studentSelected"].widget = forms.Select(choices=self.studentChoices)

    studentSelected= forms.CharField(label="Select student to render: ")

class tableView(forms.Form):
    #code goes here