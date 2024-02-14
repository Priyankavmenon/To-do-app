from django import forms
from django.contrib.auth.models import User
from Reminder.models import Task
class Register(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","password","first_name","last_name","email"]
class Login(forms.Form):
    username=forms.CharField()
    password=forms.CharField()   
class Todo(forms.ModelForm):
    class Meta:
        model=Task
        fields=['name']