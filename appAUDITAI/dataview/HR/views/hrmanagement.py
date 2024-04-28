from django.shortcuts import render, redirect
from django.views import View
from appAUDITAI.CSV.csvuploadform import CSVModelForm
from appAUDITAI.models import CSV, SAP_USR02,HR_RECORD
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse
from appAUDITAI.dataview.HR.forms.hrmanagementform import UpdateEmployee
from django.forms.models import model_to_dict
from django.shortcuts import render, get_object_or_404
import csv


class HRManagement(View):

    template_name = 'pages/HR/hr-data-management.html'
    def get(self, request):
        return render(request, self.template_name)

class NewHRRecord(View):

    template_name = 'pages/HR/new-hr-record.html'

    def get(self, request):
        form = CSVModelForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CSVModelForm(request.POST, request.FILES)

        if form.is_valid():
            #Code to check if the correct template is used based on file name
            if form.cleaned_data['file_name'].name != 'AUDITAI_HR_UPLOAD_CSV.csv':
                return JsonResponse({'error': 'The attached file is invalid. Make sure to use the template provided to avoid receiving this error.'})
            else:
                form.save()
                form = CSVModelForm()
                obj = CSV.objects.get(activated=False)
                date_formats = ["%Y-%m-%d", "%d/%m/%Y",
                                "%m/%d/%Y", "%Y%m%d", "%m/%d/%y"]
                with open(obj.file_name.path, 'r') as f:
                    reader = csv.reader(f)
                    header = next(reader)
                    header = [field.strip('\ufeff') for field in header]
                    expected_fields = ['COMPANY_ID', 'USER_ID', 'EMAIL_ADDRESS', 'FIRST_NAME', 'LAST_NAME', 'JOB_TITLE', 'DEPARTMENT', 'MANAGER', 'HIRE_DATE', 'EMP_TYPE', 'REHIRE_DATE', 'STATUS','TERMINATION_DATE']
                    missing_fields = [field for field in expected_fields if field not in header]
                    if missing_fields:
                        obj.delete()
                        return JsonResponse({'error': 'Missing field(s) in the attached template: {}'.format(', '.join(missing_fields))})
                        
                    else:
                        for i, row in enumerate(reader):
                                HIRE_DATE = row[8]
                                REHIRE_DATE= row[10]
                                TERMINATION_DATE= row[11]
                                if not HIRE_DATE:
                                    HIRE_DATE = datetime(1900, 1, 1)  # Assign a default date, e.g., January 1, 1990
                                else:
                                     HIRE_DATE = self.parse_date(str(HIRE_DATE), date_formats)
                                if not REHIRE_DATE:
                                    REHIRE_DATE = datetime(1900, 1, 1) 
                                else:
                                     REHIRE_DATE = self.parse_date(str(REHIRE_DATE), date_formats)
                                if not TERMINATION_DATE:
                                    TERMINATION_DATE = datetime(1900, 1, 1) 
                                else:
                                     TERMINATION_DATE = self.parse_date(str(TERMINATION_DATE), date_formats)

                                hr_record_data = {
                                'COMPANY_ID': row[0],
                                'USER_ID': row[1],
                                'EMAIL_ADDRESS': row[2],
                                'FIRST_NAME': row[3],
                                'LAST_NAME': row[4],
                                'JOB_TITLE': row[5],
                                'DEPARTMENT': row[6],
                                'MANAGER': row[7],
                                'HIRE_DATE': HIRE_DATE,
                                'EMP_TYPE': row[9],
                                'REHIRE_DATE': REHIRE_DATE,
                                'TERMINATION_DATE': TERMINATION_DATE,
                                'STATUS': row[12],
                            }
                                # Try to get an existing record or create a new one
                                hr_record, created = HR_RECORD.objects.get_or_create(
                                    USER_ID=row[1],
                                    EMAIL_ADDRESS=row[2],
                                    defaults=hr_record_data  # Data to update or create
                                )

                                # If the record already existed, update its fields
                                if not created:
                                    for field, value in hr_record_data.items():
                                        setattr(hr_record, field, value)
                                    hr_record.save()

                        obj.activated = True
                        obj.save()

                        if obj.activated:
                            form = CSVModelForm()
                            return render(request, self.template_name, {'form': form})
                        else:
                            obj.delete()
        else:
            return JsonResponse({'error': 'Invalid form data'})
        
        return render(request, self.template_name, {'form': form})

    def parse_date(self, date_str, date_formats):
        for date_format in date_formats:
            try:
                return datetime.strptime(date_str, date_format)
            except ValueError:
                pass
        # If none of the formats match, return a default date
        return datetime(1900, 1, 1)


class UpdateHRRecord(View):

    template_name = 'pages/HR/update-hr-record.html'
    model = HR_RECORD
    
    def get(self, request,user_id=0, *args, **kwargs):
        #Load all employees
        employees = HR_RECORD.objects.filter(USER_ID__isnull=False)
        context = {'employees':employees}
        return render(request,self.template_name,context)
    
class FetchHRRecord(View):
    model = HR_RECORD
    form_class = UpdateEmployee
    template_name = 'pages/HR/update-hr-record.html'

    def get(self, request, id=0, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            selected_employee = HR_RECORD.objects.get(USER_ID=id)
            employeeform_update = self.form_class(instance=selected_employee)
            context = {
                'employeeform_update': model_to_dict(employeeform_update.instance),
                'form_html': employeeform_update.as_table(),
            }
            return JsonResponse(context)

class UploadHRSetting(View):

    template_name = 'pages/HR/upload-hr-setting.html'

    def get(self, request):
        return render(request, self.template_name)


class UploadHRHistory(View):

    template_name = 'pages/HR/upload-hr-history.html'

    def get(self, request):
        return render(request, self.template_name)
