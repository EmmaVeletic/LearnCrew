from django.forms import ModelForm
from .models import Korisnici, Predmeti
from django.contrib.auth.hashers import make_password
from django import forms

class UserForm(ModelForm):
    class Meta:
        model = Korisnici
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'uloga', 'status']

    def clean_password(self):
        password = make_password(self.cleaned_data.get('password'))
        return password

class SubjectForm(ModelForm):
    class Meta:
        model = Predmeti
        fields = '__all__'
        #fields = ['name', 'kod', 'program', 'ects', 'sem_red', 'sem_izv', 'izborni', 'nositelj']

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        self.fields['nositelj'].queryset = Korisnici.objects.filter(uloga__uloga='prof')



