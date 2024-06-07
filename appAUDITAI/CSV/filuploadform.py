from django import forms
import os
from appAUDITAI.models import PWCONFIGATTACHMENTS, APP_NEW_USER_APPROVAL, WORKPAPER_UPLOAD, DESIGN_EVIDENCE, OE_EVIDENCE, HR_MANUAL_UPLOAD

class PWCONFIG_MODELFORM(forms.ModelForm):
    class Meta:
        model = PWCONFIGATTACHMENTS
        fields = ('file_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make the file_name field not required
        self.fields['file_name'].required = False

class NEW_USER_APPROVAL_FORM(forms.ModelForm):
    class Meta:
        model = APP_NEW_USER_APPROVAL
        fields = ('file_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make the file_name field not required
        self.fields['file_name'].required = False
    # Your view logic

class MANUAL_USER_UPLOAD_FORM(forms.ModelForm):
    class Meta:
        model = APP_NEW_USER_APPROVAL
        fields = ('file_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make the file_name field not required
        self.fields['file_name'].required = False
    # Your view logic

class HR_LIST_UPLOAD_FORM(forms.ModelForm):
    class Meta:
        model = HR_MANUAL_UPLOAD
        fields = ('file_name',)

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the file_name field not required
        self.fields['file_name'].required = False


class WORKPAPER_UPLOAD_FORM(forms.ModelForm):

    class Meta:
        model = WORKPAPER_UPLOAD
        fields = ['file_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the file_name field not required
        self.fields['file_name'].required = False

class DESIGN_EVIDENCE_UPLOAD_FORM(forms.ModelForm):

    class Meta:
        model = DESIGN_EVIDENCE
        fields = ['file_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the file_name field not required
        self.fields['file_name'].required = False

    
class OE_EVIDENCE_UPLOAD_FORM(forms.ModelForm):

    class Meta:
        model = OE_EVIDENCE
        fields = ['file_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the file_name field not required
        self.fields['file_name'].required = False