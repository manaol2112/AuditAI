
from django import forms
from django.contrib.auth.models import User
from appAUDITAI.models import HR_RECORD,APP_LIST, APP_RECORD

class NewAPP(forms.ModelForm):

    class Meta:
        model = APP_LIST
        fields = ['APP_NAME','APP_TYPE','HOSTED']

class MappedUser(forms.ModelForm):

   class Meta:
        model = HR_RECORD
        fields = ['USER_ID']

class TagUnmappedUser(forms.ModelForm):

    class Meta:
        model = APP_RECORD
        fields = ['id']