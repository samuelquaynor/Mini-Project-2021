from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CreateStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(CreateStudentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
# class FacultyForm(ModelForm):
#     class Meta:
#         model = Faculty
#         fields = '__all__'
#         exclude = ['user']
#     def __init__(self, *args, **kwargs):
#         super(FacultyForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'    

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control"
            }
        ))
    firstname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Firstname",                
                "class": "form-control"
            }
        ))
    lastname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Lastname",                
                "class": "form-control"
            }
        ))
    registration_id = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Registration ID",                
                "class": "form-control"
            }
        ))
    faculty = forms.ChoiceField(
        widget=forms.Select(
            attrs={               
                "class": "form-control"
            }),
        choices=Teacher.Faculty
    )
    department = forms.ChoiceField(
        widget=forms.Select(
            attrs={               
                "class": "form-control"
            }),
        choices=Teacher.Department
    )
    course = forms.ChoiceField(
        widget=forms.Select(
            attrs={               
                "class": "form-control"
            }),
        choices=Teacher.Course
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password check",                
                "class": "form-control"
            }
        ))

    class Meta:
        model = Teacher
        fields = ('username', 'email','firstname', 'lastname','registration_id', 'faculty','department', 'password1', 'password2')

    def save(self, commit=True):
        teacher = super(SignUpForm, self).save(commit=False)
        teacher.email = self.cleaned_data['email']
        if commit:
            teacher.save()
        return teacher