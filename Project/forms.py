# myapp/forms.py

from django import forms
from .models import Standard,Project,Sample

class StandardForm(forms.ModelForm):
    class Meta:
        model = Standard
        fields = ['BroadCategory', 'Category', 'Project', 'StandardName', 'StandardNumber', 'ClauseNumber']
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['BroadCategory', 'Category', 'Project', 'StandardName', 'StandardNumber', 'ClauseNumber','Staff','Equipment','Procedure','Sample']
class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ['Sample', 'Specification', 'Manufacturer', 'BatchNumber']
