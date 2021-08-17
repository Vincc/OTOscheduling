from django import forms
  
class datesForm(forms.Form):
    new_date = forms.DateField()
    
class timesForm(forms.Form):
    new_time = forms.TimeField()
