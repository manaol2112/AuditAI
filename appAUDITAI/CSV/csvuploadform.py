from django import forms
from appAUDITAI.models import CSV, APP_USER_UPLOAD

class CSVModelForm(forms.ModelForm):
    class Meta:
        model = CSV
        fields = ('file_name',)

class APP_USER_UPLOAD_FORM(forms.ModelForm):

    class Meta:
        model = APP_USER_UPLOAD
        fields = ('file_name',)

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        
        if uploaded_file:
            # Check file extension
            allowed_extensions = ['.csv', '.txt']
            file_extension = uploaded_file.name.lower().split('.')[-1]
            
            if file_extension not in allowed_extensions:
                raise forms.ValidationError('Invalid file type. Please upload a CSV or TXT file.')

            # Check the number of files
            if len(self.files.getlist('file')) != 1:
                raise forms.ValidationError('Please select only one file.')

        return uploaded_file

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            # Make the file_name field not required
            self.fields['file_name'].required = True
