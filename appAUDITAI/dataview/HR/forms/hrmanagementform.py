from django import forms
from django.contrib.auth.models import User
from appAUDITAI.models import HR_RECORD

class UpdateEmployee(forms.ModelForm):

   class Meta:
        model = HR_RECORD
        fields = ['USER_ID']