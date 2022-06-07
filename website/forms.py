from django import forms
from website.models import *

from django.contrib.auth.models import User


class trainingform(forms.ModelForm):
    name = forms.CharField()
    start = forms.DateTimeField()
    end = forms.DateTimeField()
    team = forms.ModelChoiceField(queryset = teammodel.objects.all())

    class Meta:
        model = trainingmodel
        fields = [
            "name",
            "start",
            "end",
            "team"
        ]

class gameform(forms.ModelForm):
    name = forms.CharField()
    start = forms.DateTimeField()
    end = forms.DateTimeField()
    team = forms.ModelChoiceField(queryset = teammodel.objects.all())
    enemy = forms.CharField()
    teamgoals = forms.IntegerField()
    enemygoals = forms.IntegerField()

    class Meta:
        model = gamemodel
        fields = [
            "name",
            "start",
            "end",
            "team",
            "enemy",
            "teamgoals",
            "enemygoals"
        ]

class teamform(forms.ModelForm):
    name = forms.CharField()
    trainer = forms.ModelChoiceField(queryset = User.objects.all())
    echelon = forms.ModelChoiceField(queryset = echelonmodel.objects.all())

    class Meta:
        model = teammodel
        fields = [
            "name",
            "trainer",
            "echelon"
        ]

class echelonform(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = echelonmodel
        fields = [
            "name"
        ]

class clubform(forms.ModelForm):
    name = forms.CharField()
    image = forms.ImageField()
    description = forms.CharField()
    about = forms.CharField()
    contact = forms.CharField()

    class Meta:
        model = clubmodel
        fields = [
            "name",
            "image",
            "description",
            "about",
            "contact"
        ]