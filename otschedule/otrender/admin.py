from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth.models import Group

from django import forms
from .models import user, sessiondates, sessionTimes
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# Administration settings for Django backend

class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = user
        fields = ("username", "tutorGroup",  "is_teacher", "is_admin")

    def clean_password2(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):

        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin"s
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = user
        fields = ("username", "password", "tutorGroup",  "is_teacher", "is_admin")

    def clean_password(self):

        return self.initial["password"]


class UserAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("username", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Organisation", {"fields": ("tutorGroup",)}),
        ("Permissions", {"fields": ("is_admin","is_teacher")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "tutorGroup", "password1", "password2")}
        ),
    )
    search_fields = ("username",)
    ordering = ("username",)
    filter_horizontal = ()

admin.site.register(user, UserAdmin)

admin.site.unregister(Group)


admin.site.register(sessiondates)
admin.site.register(sessionTimes)



