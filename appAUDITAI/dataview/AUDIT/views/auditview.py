from appAUDITAI.dataview.MISC.imports import *
from django.shortcuts import render, redirect
from django.views import View
from appAUDITAI.dataview.LOGIN.views.authenticate import UserRoleView
from appAUDITAI.dataview.LOGIN.views.decorators import UserAccessMixin
from appAUDITAI.models import APP_LIST, COMPANY, PASSWORD,PASSWORDPOLICY, HR_RECORD, APP_RECORD, TERMINATIONPOLICY,USERROLES, AUDITLIST
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.serializers import serialize
from django.utils import timezone
from datetime import date
from django.db.models import Q
from django.db.models import F
from appAUDITAI.dataview.LOGIN.views.decorators import AuditorPermissionMixin
from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.core.files.storage import default_storage
from django.http import FileResponse
from django.utils.html import escape
import html


class RiskAndControls(AuditorPermissionMixin,View):
    template_name = 'pages/AUDIT/audit-risk-and-controls.html'

    def get(self,request):
        return render(request, self.template_name)
    
class CreateRisk(AuditorPermissionMixin,View):
    template_name = 'pages/AUDIT/audit-create-risk.html'

    def get(self,request):

        try:
            risk_list = RISKLIST.objects.all()
        except RISKLIST.DoesNotExist:
            risk_list = None

        context = {'risk_list':risk_list}
        return render(request, self.template_name,context)
    
    def post(self, request):

        risk_id = request.POST.get('risk_id')
        risk_description = request.POST.get('risk_description')
        risk_template = request.POST.get('risk_template')

        create_risk,created = RISKLIST.objects.update_or_create(RISK_ID = risk_id)
        create_risk.RISK_DESCRIPTION = risk_description
        create_risk.RISK_TYPE = risk_template
        create_risk.save()

        try:
            risk_list = RISKLIST.objects.all()
        except RISKLIST.DoesNotExist:
            risk_list = None

        context = {'risk_list':risk_list}

        return render(request, self.template_name,context)
    
class CreateControl(AuditorPermissionMixin,View):
    template_name = 'pages/AUDIT/audit-create-control.html'

    def get(self,request):

        try:
            control_list = CONTROLLIST.objects.all()
        except CONTROLLIST.DoesNotExist:
            control_list = None
        context = {'control_list':control_list}

        return render(request, self.template_name,context)
    
    def post(self, request):

        control_id = request.POST.get('control_id')
        control_title = request.POST.get('control_title')
        control_description = request.POST.get('control_description')
        control_template = request.POST.get('control_template')
        control_domain = request.POST.get('control_domain')
        control_relevance = request.POST.get('control_relevance')

        create_control,created = CONTROLLIST.objects.update_or_create(CONTROL_ID = control_id)
        create_control.CONTROL_TITLE = control_title
        create_control.CONTROL_DESCRIPTION = control_description
        create_control.CONTROL_TYPE = control_template
        create_control.CONTROL_DOMAIN = control_domain
        create_control.CONTROL_RELEVANCE = control_relevance

        create_control.save()

        control_list = CONTROLLIST.objects.all()
        context = {'control_list':control_list}

        return render(request, self.template_name,context)
    
class CreateProcedures(AuditorPermissionMixin,View):
    template_name = 'pages/AUDIT/audit-test-procedures.html'

    def get(self,request):

        try:
            procedure_list = TEST_PROCEDURES.objects.all()
        except TEST_PROCEDURES.DoesNotExist:
            procedure_list = None

        # Decode HTML entities in DESIGN_PROCEDURES field
        if procedure_list:
            for procedure in procedure_list:
                procedure.DESIGN_PROCEDURES = html.unescape(procedure.DESIGN_PROCEDURES)
                procedure.INTERIM_PROCEDURES = html.unescape(procedure.INTERIM_PROCEDURES)
                procedure.ROLLFORWARD_PROCEDURES = html.unescape(procedure.ROLLFORWARD_PROCEDURES)

        try:
            control_list = CONTROLLIST.objects.all()
        except CONTROLLIST.DoesNotExist:
            control_list = None

        context = {'procedure_list':procedure_list,
                   'control_list':control_list}

        return render(request, self.template_name,context)
    
    def post(self, request):

        control_id = request.POST.get('control_id')
        procedure_name = request.POST.get('procedure_name')
        design_procedures_html = request.POST.get('design_procedures_html','')
        interim_procedures_html = request.POST.get('interim_procedures_html')
        rollforward_procedures_html = request.POST.get('rollforward_procedures_html')

        # Ensure HTML content is escaped to prevent XSS attacks
        design_procedures = escape(design_procedures_html)
        interim_procedures = escape(interim_procedures_html)
        rollforward_procedures = escape(rollforward_procedures_html)

        try:
            controlID = CONTROLLIST.objects.get(id = control_id)
        except CONTROLLIST.DoesNotExist:
            controlID = None

        try:
            procedure,created = TEST_PROCEDURES.objects.update_or_create(CONTROL_ID = controlID, PROCEDURE_NAME = procedure_name)
            procedure.DESIGN_PROCEDURES = design_procedures
            procedure.INTERIM_PROCEDURES = interim_procedures
            procedure.ROLLFORWARD_PROCEDURES = rollforward_procedures

            if created:
                procedure.save()
        except TEST_PROCEDURES.DoesNotExist:
            procedure = None

        return redirect('appAUDITAI:procedures-create')

    
class RiskAssessment(AuditorPermissionMixin,View):
    template_name = 'pages/AUDIT/audit-risk-assessment.html'

    def get(self,request,comp_id, audit_id):
        selected_company = COMPANY.objects.get(id=comp_id)
        apps = APP_LIST.objects.filter(COMPANY_ID = selected_company)
        try:
            audit_name = AUDITLIST.objects.get(id = audit_id)
        except AUDITLIST.DoesNotExist:
            audit_name = None

        context = {'selected_company': selected_company,
                   'comp_id':comp_id,
                   'apps':apps,
                   'audit_id':audit_id,
                   'audit_name':audit_name
        }
        return render(request, self.template_name,context)
    
class AuditPerApp(AuditorPermissionMixin,View):
    template_name = 'pages/AUDIT/audit-details.html'

    def get(self,request,comp_id,audit_id, app_id):
        user = request.user
        try:
            apps = APP_LIST.objects.filter(COMPANY_ID = comp_id)
        except APP_LIST.DoesNotExist:
            apps = None

        try:
            selected_app = APP_LIST.objects.get(id = app_id)
        except APP_LIST.DoesNotExist:
            selected_app = None

        try:
            audit_name = AUDITLIST.objects.get(id = audit_id)
        except AUDITLIST.DoesNotExist:
            audit_name = None

        try:
            risk_general = RISKGENERAL.objects.get(APP_NAME = selected_app)
        except RISKGENERAL.DoesNotExist:
            risk_general = None

        try:
            app = APP_LIST.objects.get(id = app_id)
            risk_list = RISKLIST.objects.filter(RISK_TYPE = risk_general.RISK_TYPE)
            risks_with_ratings = []
            for risk in risk_list:
                rate = RISKRATING.objects.filter(APP_NAME=app, RISK_ID=risk).first()  # Use .first() to get a single rating
                risk.rate = rate.RATING if rate else 'N/A'  # Assuming 'RATING' is the field that stores the rating value
                # Count the number of control mappings for this risk
                control_mapped_count = RISKMAPPING.objects.filter(APP_NAME=app, RISK_ID=risk).count()
                risk.control_mapped_count = control_mapped_count

                risks_with_ratings.append(risk)

        except RISKLIST.DoesNotExist:
            risk_list = None

        try:
            applicable_risk = RISKRATING.objects.filter(APP_NAME=app_id).exclude(RATING='N/A').order_by('RISK_ID')   
        except RISKRATING.DoesNotExist:
            applicable_risk = None

        try:
            control_list = CONTROLLIST.objects.all()
        except CONTROLLIST.DoesNotExist:
            control_list = None

        try:
            mapped_controls = RISKMAPPING.objects.filter(APP_NAME = app_id)
        except RISKMAPPING.DoesNotExist:
            mapped_controls = None

        unmapped_controls = {}

        if control_list is not None and mapped_controls is not None:
            # Extract control IDs from mapped_controls
            mapped_control_ids = set(mapped_controls.values_list('CONTROL_ID', flat=True))
            
            # Create a dictionary of unmapped controls
            for control in control_list:
                if control.id not in mapped_control_ids:
                    unmapped_controls[control.id] = control
        
        try:
            planning_docs_all = AUDITFILE.objects.filter(AUDIT_ID = audit_id, FOLDER_NAME = 'Planning')
            today = datetime.now().date()
            for doc in planning_docs_all:
                date_sent = doc.DATE_SENT.date()
                doc.days_difference = (today - date_sent).days
                
                open_notes_count = AUDITNOTES.objects.filter(FILE_NAME=doc, STATUS='Open').count()
                doc.open_notes_count = open_notes_count

                closed_notes_count = AUDITNOTES.objects.filter(FILE_NAME=doc, STATUS='Closed').count()
                doc.closed_notes_count = closed_notes_count

                try:
                    user = User.objects.get(email=doc.CURRENTLY_WITH)
                except MultipleObjectsReturned:
                    # If multiple users are returned, get the first one
                    user = User.objects.filter(email=doc.CURRENTLY_WITH).first()

                if user:
                    intials = user.first_name[0] + user.last_name[0]
                    doc.initials = intials
                else:
                    pass

                workpaper_upload = doc.workpaper_upload
                if workpaper_upload:
                    doc.workpaper_upload_id = workpaper_upload.id
                else:
                    pass

        except AUDITFILE.DoesNotExist:
            docs = None


        try:
            planning_docs_me = planning_docs_all.filter(CURRENTLY_WITH=user.email) if planning_docs_all else None
            for doc in planning_docs_me:
                    date_sent = doc.DATE_SENT.date()
                    doc.days_difference = (today - date_sent).days
                    
                    open_notes_count = AUDITNOTES.objects.filter(FILE_NAME=doc, STATUS='Open').count()
                    doc.open_notes_count = open_notes_count

                    closed_notes_count = AUDITNOTES.objects.filter(FILE_NAME=doc, STATUS='Closed').count()
                    doc.closed_notes_count = closed_notes_count

                    try:
                        user = User.objects.get(email=doc.CURRENTLY_WITH)
                    except MultipleObjectsReturned:
                        # If multiple users are returned, get the first one
                        user = User.objects.filter(email=doc.CURRENTLY_WITH).first()

                    if user:
                        intials = user.first_name[0] + user.last_name[0]
                        doc.initials = intials
                    else:
                        pass

                    workpaper_upload = doc.workpaper_upload
                    if workpaper_upload:
                        doc.workpaper_upload_id = workpaper_upload.id
                    else:
                        pass

        except Exception as e:
             docs = None
             pass
        try:
            workpaper_docs_all = AUDITFILE.objects.filter(AUDIT_ID = audit_id, FOLDER_NAME = 'Workpapers')
            for doc in workpaper_docs_all:
                try:
                    control_id = CONTROLLIST.objects.get(CONTROL_ID = doc.file_name)
                    control = RISKMAPPING.objects.filter(CONTROL_ID = control_id, APP_NAME = selected_app)
                    doc.control = control
                except RISKMAPPING.DoesNotExist:
                    doc.control = None
                except CONTROLLIST.DoesNotExist:
                    doc.control = None

                if doc.DATE_SENT:
                    date_sent = doc.DATE_SENT.date()
                    doc.days_difference = (today - date_sent).days
                
                open_notes_count = AUDITNOTES.objects.filter(FILE_NAME=doc, STATUS='Open').count()
                doc.open_notes_count = open_notes_count

                closed_notes_count = AUDITNOTES.objects.filter(FILE_NAME=doc, STATUS='Closed').count()
                doc.closed_notes_count = closed_notes_count

                try:
                    user = User.objects.get(email=doc.CURRENTLY_WITH)
                except MultipleObjectsReturned:
                    # If multiple users are returned, get the first one
                    user = User.objects.filter(email=doc.CURRENTLY_WITH).first()
                except User.DoesNotExist:
                    user = None
                    pass

                if user:
                    intials = user.first_name[0] + user.last_name[0]
                    doc.initials = intials
                else:
                    pass
        except AUDITFILE.DoesNotExist:
            docs = None

        user = request.user
        workpaper_doc_with_me = workpaper_docs_all.filter(CURRENTLY_WITH=user.email) if workpaper_docs_all else None


        context = {
            'comp_id':comp_id,
            'audit_id':audit_id,
            'app_id':app_id,
            'selected_app':selected_app,
            'audit_name':audit_name,
            'apps':apps,
            'planning_docs_all':planning_docs_all,
            'planning_docs_me':planning_docs_me,
            'risk_general':risk_general,
            'risk_list':risk_list,
            'applicable_risk':applicable_risk,
            'control_list':control_list,
            'mapped_controls':mapped_controls,
            'unmapped_controls':unmapped_controls,
            'workpaper_docs_all':workpaper_docs_all,
            'workpaper_doc_with_me':workpaper_doc_with_me
        }
        return render(request,self.template_name,context)
    

def download_file(request, id):
    workpaper = get_object_or_404(WORKPAPER_UPLOAD, id=id)
    file_path = workpaper.file_name.path
    file_name = os.path.basename(file_path)  # Get the original file name

    try:
        response = FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
        return response
    except Exception as e:
        # Handle the exception
        pass

    
class AuditPlanningDocs(AuditPerApp):
    template_name = 'pages/AUDIT/audit-planning.html'

    def get(self, request, comp_id, audit_id, app_id):
        # Call the parent class's get method to retain its functionality and context
        response = super().get(request, comp_id, audit_id, app_id)

        return response

    def post(self, request, comp_id, audit_id, app_id):
        form = WORKPAPER_UPLOAD_FORM(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            workpaper_upload = form.save(commit=False)
            workpaper_upload.audit_id = audit_id
            workpaper_upload.save()

        uploaded_file = form.cleaned_data['file_name'].name
        if uploaded_file:
            file_name = uploaded_file

            planning_doc, created = AUDITFILE.objects.get_or_create(AUDIT_ID=audit_id, file_name=file_name)
            planning_doc.STATUS = 'In Preparation'
            planning_doc.CURRENTLY_WITH = user.email
            planning_doc.FOLDER_NAME = 'Planning'
            planning_doc.DATE_SENT = timezone.now()
            planning_doc.workpaper_upload = workpaper_upload

            if created:
                planning_doc.CREATED_BY = user.email
                planning_doc.CREATED_ON = timezone.now()
            else:
                planning_doc.MODIFIED_BY = user.email
                planning_doc.LAST_MODIFIED = timezone.now()
            
            planning_doc.save()

            
        response = super().get(request, comp_id, audit_id, app_id)
        return response
    
class AuditRiskMapping(AuditPerApp):
    template_name = 'pages/AUDIT/audit-risk-mapping.html'

    def get(self, request, comp_id, audit_id, app_id):
        response = super().get(request, comp_id, audit_id, app_id)
        return response
    
    def post(self,request, comp_id, audit_id, app_id ):

        form_id = request.POST.get('form_id')

        if form_id == 'risk_form_general':
            risk_rating = request.POST.get('risk_rating_general')
            risk_rationale = request.POST.get('risk_rationale')
            risk_template = request.POST.get('risk_template')

            selected_app = APP_LIST.objects.get(id = app_id)
            risk_name = 'RFA - ' + str(selected_app.APP_NAME)
            risk_details, created = RISKGENERAL.objects.update_or_create(APP_NAME = selected_app, RISK_NAME = risk_name)
            risk_details.RISK_RATING = risk_rating
            risk_details.RISK_RATIONALE = risk_rationale
            risk_details.RISK_TYPE = risk_template
            risk_details.save()

        elif form_id == 'risk_rating_form':
            counter = 1
            
            while f'risk_id_{counter}' in request.POST:

                risk_id = request.POST.get(f'risk_id_{counter}')
                risk_description = request.POST.get(f'risk_description_{counter}')
                risk_type = request.POST.get(f'risk_type_{counter}')
                risk_rating = request.POST.get(f'risk_rating_{counter}')

                try:
                    risk_id = RISKLIST.objects.get(id = risk_id)
                    app = APP_LIST.objects.get(id = app_id)

                    risk_rate, created = RISKRATING.objects.update_or_create(APP_NAME = app, RISK_ID = risk_id)
                    risk_rate.RATING = risk_rating
                    risk_rate.save()

                except RISKRATING.DoesNotExist:
                    risk_rate = None
                except RISKLIST.DoesNotExist:
                    pass
                except APP_LIST.DoesNotExist:
                    pass
                counter += 1

        else:
            user = request.user
            risk_id = request.POST.get('risk_id')
            control_ids = request.POST.getlist('assigned_controls[]')
            
            try:
                app = APP_LIST.objects.get(id = app_id)
            except APP_LIST.DoesNotExist:
                app = None

            try:
                risk = RISKRATING.objects.get(RISK_ID = risk_id, APP_NAME = app)
            except RISKRATING.DoesNotExist:
                risk = None

            if control_ids:
                for control in control_ids:
                    control_to_map = CONTROLLIST.objects.get(id = control)          
                    risk_control_mapping,created = RISKMAPPING.objects.update_or_create(CONTROL_ID = control_to_map, RISK_ID = risk.RISK_ID, APP_NAME = app)
                    risk_control_mapping.save()

                    workpaper_name = RISKMAPPING.objects.filter(CONTROL_ID = control).distinct()
                    for workpaper in workpaper_name:
                        workpapers, created = AUDITFILE.objects.update_or_create(AUDIT_ID = audit_id, file_name = workpaper.CONTROL_ID.CONTROL_ID)
                        workpapers.STATUS = 'Not Started'
                        workpapers.FOLDER_NAME = 'Workpapers'
                        if created:
                            workpapers.CREATED_BY = user.email
                            workpapers.CREATED_ON = timezone.now()
                        else:
                            workpapers.MODIFIED_BY = user.email
                            workpapers.LAST_MODIFIED = timezone.now()
                        workpapers.save()

        response = super().get(request, comp_id, audit_id, app_id)
        return response
    
class AuditWorkpapers(AuditPerApp):
    template_name = 'pages/AUDIT/audit-workpapers.html'

    def get(self, request, comp_id, audit_id, app_id):
        # Call the parent class's get method to retain its functionality and context
        response = super().get(request, comp_id, audit_id, app_id)

        # Additional logic for AuditPlanningDocs if needed

        return response
    
def get_procedure_content(request,id):
    procedure_id = request.GET.get('procedure_id')

    try:
        procedure = TEST_PROCEDURES.objects.get(id=procedure_id)
        design_procedures = html.unescape(procedure.DESIGN_PROCEDURES)
        interim_procedures = html.unescape(procedure.INTERIM_PROCEDURES)
        rollforward_procedures = html.unescape(procedure.ROLLFORWARD_PROCEDURES)
    except TEST_PROCEDURES.DoesNotExist:
        design_procedures = ''
        interim_procedures = ''
        rollforward_procedures = ''

    return JsonResponse({
        'design_procedures': design_procedures,
        'interim_procedures': interim_procedures,
        'rollforward_procedures': rollforward_procedures,
    })
    
class AuditWorkpapersDetails(AuditPerApp):
    template_name = 'pages/AUDIT/audit-workpaper-details.html'

    def get(self, request, comp_id, audit_id, app_id, control_id):
        user = request.user
        try:
            apps = APP_LIST.objects.filter(COMPANY_ID = comp_id)
        except APP_LIST.DoesNotExist:
            apps = None

        try:
            selected_app = APP_LIST.objects.get(id = app_id)
        except APP_LIST.DoesNotExist:
            selected_app = None

        try:
            audit_name = AUDITLIST.objects.get(id = audit_id)
        except AUDITLIST.DoesNotExist:
            audit_name = None

        try:
            control_name = AUDITFILE.objects.get(id = control_id)
            control_details = CONTROLLIST.objects.get(CONTROL_ID = control_name.file_name)
        except AUDITFILE.DoesNotExist:
            control_name = None

        try:
            risk_mapped = RISKMAPPING.objects.filter(APP_NAME = selected_app, CONTROL_ID = control_details)
            for risk in risk_mapped:
                risk_rating = RISKRATING.objects.get(APP_NAME = selected_app, RISK_ID = risk.RISK_ID)
                risk.risk_rating = risk_rating
        except RISKMAPPING.DoesNotExist:
            risk_mapped = None

        try:
            procedure_list = TEST_PROCEDURES.objects.filter(CONTROL_ID = control_details)
        except TEST_PROCEDURES.DoesNotExist:
            procedure_list = None

        # Decode HTML entities in DESIGN_PROCEDURES field
        if procedure_list:
            for procedure in procedure_list:
                procedure.DESIGN_PROCEDURES = html.unescape(procedure.DESIGN_PROCEDURES)
                procedure.INTERIM_PROCEDURES = html.unescape(procedure.INTERIM_PROCEDURES)
                procedure.ROLLFORWARD_PROCEDURES = html.unescape(procedure.ROLLFORWARD_PROCEDURES)

        context = {
            'comp_id':comp_id,
            'audit_id':audit_id,
            'app_id':app_id,
            'control_id':control_id,
            'apps':apps,
            'selected_app':selected_app,
            'control_name':control_name,
            'control_details':control_details,
            'audit_name':audit_name,
            'risk_mapped':risk_mapped,
            'procedure_list':procedure_list
        }
        return render(request, self.template_name, context)
    
class AuditDeficiencies(AuditPerApp):
    template_name = 'pages/AUDIT/audit-deficiencies.html'

    def get(self, request, comp_id, audit_id, app_id):
        # Call the parent class's get method to retain its functionality and context
        response = super().get(request, comp_id, audit_id, app_id)

        # Additional logic for AuditPlanningDocs if needed

        return response
    
    
class AuditReports(AuditPerApp):
    template_name = 'pages/AUDIT/audit-reports.html'

    def get(self, request, comp_id, audit_id, app_id):
        # Call the parent class's get method to retain its functionality and context
        response = super().get(request, comp_id, audit_id, app_id)

        # Additional logic for AuditPlanningDocs if needed

        return response

class SelectAuditPeriod(AuditorPermissionMixin,View):
    template_name = 'pages/AUDIT/audit-select-period.html'
    
    def get(self, request, comp_id):
        active_user = request.user
        user_roles = USERROLES.objects.filter(USERNAME=active_user)

        try:
            audit_list = AUDITLIST.objects.filter(COMPANY_ID = comp_id, STATUS = 'Active').order_by('CREATED_ON')
        except AUDITLIST.DoesNotExist:
            audit_list = None
            pass

        try:
            archived_audit_list = AUDITLIST.objects.filter(COMPANY_ID = comp_id, STATUS = 'Archived').order_by('CREATED_ON')
        except AUDITLIST.DoesNotExist:
            archived_audit_list = None
            pass

        companies = []
        for user_role in user_roles:
            companies.extend(user_role.COMPANY_ID.all())
        
        context = {'companies': companies,
                   'audit_list':audit_list,
                   'comp_id':comp_id,
                   'archived_audit_list':archived_audit_list}
        
        return render(request, self.template_name, context)
    
class ManageAuditPeriod(AuditorPermissionMixin,View):
    template_name = 'pages/AUDIT/audit-manage-period.html'
    
    def get(self, request):
        active_user = request.user
        user_roles = USERROLES.objects.filter(USERNAME=active_user)

        try:
            audit_list = AUDITLIST.objects.all().order_by('CREATED_ON')
        except AUDITLIST.DoesNotExist:
            audit_list = None
            pass

        companies = []
        for user_role in user_roles:
            companies.extend(user_role.COMPANY_ID.all())
        
        context = {'companies': companies,
                   'audit_list':audit_list}
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        user = request.user
        company_name = request.POST.get('company_name')
        audit_name = request.POST.get('audit_file_name')
        audit_date = request.POST.get('audit_period')
        audit_status = request.POST.get('audit_status')
        audit_date = datetime.strptime(audit_date, '%Y-%m-%d')
        try:
            company = COMPANY.objects.get(COMPANY_NAME=company_name)
        except COMPANY.DoesNotExist:
            company = None
        except Exception as e:
            print(str(e))

        try:
            audit_exist = AUDITLIST.objects.filter(FILE_NAME=audit_name)
            if audit_exist.exists():
                pass
            else:
                audit_create, created = AUDITLIST.objects.get_or_create(FILE_NAME=audit_name, COMPANY_ID=company)
                audit_create.PERIOD_END_DATE = audit_date
                audit_create.STATUS = audit_status
                if created:
                    audit_create.CREATED_BY = user.username
                    audit_create.CREATED_ON = timezone.now()
                else:
                    audit_create.MODIFIED_BY = user.username
                    audit_create.LAST_MODIFIED = timezone.now()
                audit_create.save()
                                    
        except Exception as e:
            print(str(e))

        return redirect('appAUDITAI:audit-manage-period')


class AuditHome(AuditorPermissionMixin, UserRoleView):
    def get(self,request,comp_id):
        user_role = self.user_role
        selected_company = COMPANY.objects.get(id=comp_id)

        if user_role == 'Auditor':
            template_name = 'pages/AUDIT/audit-home.html'
        else:
            template_name = 'pages/login/login.html'
        context = {'selected_company': selected_company,'comp_id':comp_id}

        return render(request,template_name, context)
    
#PROVISIONING TESTING
class Audit_Provisioning(AuditorPermissionMixin, View):
    template_name = 'pages/AUDIT/provisioning.html'

    def common_data(self, request, id):
        current_date = timezone.now()
        current_year = current_date.year

        selected_company = get_object_or_404(COMPANY, id=id)
        applications = APP_LIST.objects.filter(COMPANY_ID=selected_company.id)
        app_names = [app.id for app in applications]
        users = APP_RECORD.objects.filter(APP_NAME__in=app_names, DATE_APPROVED__isnull=False, DATE_GRANTED__year = current_year)

        deficient_users = [] 
        effective_users = []
        unique_deficient_users = set()
        unique_effective_users = set()
        unique_deficient_app_names = set()
        unique_effective_app_names = set()
        deficient_users_count_per_app = {} 

        for user in users:
            date_granted = user.DATE_GRANTED
            date_approved = user.DATE_APPROVED

            if date_approved > date_granted:
                deficient_users.append({
                    'user_id':user.USER_ID,
                    'app_name': user.APP_NAME,
                    'date_granted':user.DATE_GRANTED.date(),
                    'date_approved':user.DATE_APPROVED.date()
                })
                unique_deficient_app_names.add(user.APP_NAME)
                deficient_users_count_per_app[user.APP_NAME] = deficient_users_count_per_app.get(user.APP_NAME, 0) + 1
                
            elif date_approved <= date_granted:
                unique_effective_users.add(user.USER_ID)
                unique_effective_app_names.add(user.APP_NAME)
            else:
                pass

        deficient_app_with_count = [{'id': app.id, 'app_name': app, 'count': deficient_users_count_per_app.get(app, 0)} for app in unique_deficient_app_names]

        context = {
        'selected_company':selected_company,
        'unique_deficient_app_names':deficient_app_with_count,
        }
        return context

    def get(self, request, id):
        context = self.common_data(request, id)
        return render(request, self.template_name, context)
    
    def post(self, request, id):
        pass

class Audit_Provisioning_Details(AuditorPermissionMixin, View):
    template_name = 'pages/AUDIT/provisioning-details.html'
    
    def common_data(self, request, comp_id, app_id):
        current_date = timezone.now()
        current_year = current_date.year
        selected_app = APP_LIST.objects.filter(id=app_id).first()
        selected_company = get_object_or_404(COMPANY, id=comp_id)
        users = APP_RECORD.objects.filter(APP_NAME=selected_app,  DATE_APPROVED__isnull=False,DATE_GRANTED__year=current_year, DATE_GRANTED__lt=F('DATE_APPROVED'))

        context = {
        'users':users,
        'selected_company':selected_company,
        'selected_app':selected_app
        }

        return context

    def get(self, request, comp_id, app_id):
        context = self.common_data(request, comp_id, app_id)
        return render(request, self.template_name, context)
    
    def post(self, request, id):
        pass

    
#PASSWORD TESTING
class Audit_Authentication(AuditorPermissionMixin, UserRoleView):
    template_name = 'pages/AUDIT/authentication.html'

    def get(self,request,id):
    
        selected_company = get_object_or_404(COMPANY, id=id)
        applications = APP_LIST.objects.filter(COMPANY_ID = selected_company.id)
        app_names = [app.id for app in applications]
        pwconfig = PASSWORD.objects.filter(APP_NAME__in=app_names)
        matched_application_info = []
        unmatched_application_info = []
        fully_matched_apps = []
        partially_matched_unmatched_apps = []
        for password_object in pwconfig:
            password_policy = PASSWORDPOLICY.objects.filter(    
                COMPANY_ID=selected_company).first()
            if password_policy:
                # Compare fields and print matching and non-matching ones
                matching_fields = []
                non_matching_fields = []
               
                # Compare each field
                for field in PASSWORDPOLICY._meta.get_fields():
                    field_name = field.name

                     # Skip certain fields
                    if field_name not in ['id', 'CREATED_BY', 'LAST_MODIFIED', 'MODIFIED_BY']:
                        if hasattr(password_object, field_name):
                            value_in_password = getattr(password_object, field_name)
                            value_in_policy = getattr(password_policy, field_name)

                            if field_name == 'AGE':
                                if value_in_password <= value_in_policy:
                                    matching_fields.append(field_name)
                                else:
                                    non_matching_fields.append(field_name)
                            elif field_name in ['LENGTH', 'LOCKOUT_ATTEMPT', 'LOCKOUT_DURATION']:
                                if value_in_password >= value_in_policy:
                                    matching_fields.append(field_name)
                                else:
                                    non_matching_fields.append(field_name)
                            elif value_in_password == value_in_policy:
                                matching_fields.append(field_name)
                            else:
                                non_matching_fields.append(field_name)

                # Determine whether it's fully matched or partially matched/unmatched
                if len(non_matching_fields) == 0 and len(matching_fields) > 0:
                    fully_matched_apps.append(password_object.APP_NAME)
                else:
                    partially_matched_unmatched_apps.append(password_object.APP_NAME)  # Add the application to the partially matched/unmatched list
                matched_application_info.append({
                    'app_name': password_object.APP_NAME,
                    'matching_fields': matching_fields,
                    'non_matching_fields': non_matching_fields,
                    
                })

            else:
                # No matching PASSWORDPOLICY object found
                pass   

        context = {'selected_company': selected_company,
                        'applications':applications,
                        'fully_matched_apps':fully_matched_apps,
                        'partially_matched_unmatched_apps':partially_matched_unmatched_apps,
                        'matched_application_info': matched_application_info,
                        'unmatched_application_info': unmatched_application_info,
                        }
        
        return render(request,self.template_name, context)


# TERMINATION TESTING
class Audit_Termination(AuditorPermissionMixin, UserRoleView):
    template_name = 'pages/AUDIT/termination.html'

    def get(self,request,id):

        #GET THE CURRENT DATE
        current_date = timezone.now()
        current_year = current_date.year
        #GET THE SELECTED COMPANY AND USERS
        selected_company = get_object_or_404(COMPANY, id=id)
        applications = APP_LIST.objects.filter(COMPANY_ID = selected_company.id)

        app_names = [app.id for app in applications]
        app_users = APP_RECORD.objects.filter(APP_NAME__in=app_names, DATE_REVOKED__isnull=False, DATE_REVOKED__year=current_year).exclude(DATE_REVOKED__isnull=True)
        
        unmatched_users = []

         #GET THE POLICY DAYS
        policy = TERMINATIONPOLICY.objects.filter(COMPANY_ID = id).first()

        deficient_users = []
        effective_users = []
        unique_deficient_app_names = set()
        unique_effective_app_names = set()
        deficient_users_count_per_app = {} 

        for user in app_users:
        # Check if the user exists in HR_RECORD
            hr_record_exists = HR_RECORD.objects.filter(
                Q(EMAIL_ADDRESS=user.EMAIL_ADDRESS) |
                Q(USER_ID=user.USER_ID) |
                (Q(FIRST_NAME=user.FIRST_NAME) &
                 Q(LAST_NAME=user.LAST_NAME))
            ).exclude(TERMINATION_DATE=date(1900, 1, 1),STATUS='ACTIVE')

            if hr_record_exists:
                for hr_record in hr_record_exists:
                    app_name = user.APP_NAME
                    email_address = user.EMAIL_ADDRESS,
                    termination_date = hr_record.TERMINATION_DATE
                    revocation_date = user.DATE_REVOKED
                    user_id = user.USER_ID
                    date_difference = (revocation_date.date() - termination_date).days
                    last_login = user.LAST_LOGIN.date()

                    # Check if the difference is more than 5 days
                    if date_difference > policy.DAYS_TO_TERMINATE:
                        deficient_users.append({
                            'user_id': user_id,
                            'termination_date': termination_date,
                            'email_address':email_address,
                            'revocation_date': revocation_date,
                            'app_name':app_name,
                            'difference_days': abs(date_difference),
                            'last_login':last_login
                        })
                        unique_deficient_app_names.add(user.APP_NAME)
                         # Count deficient users per unique application
                        deficient_users_count_per_app[app_name] = deficient_users_count_per_app.get(app_name, 0) + 1
                    else:
                        effective_users.append({
                            'user_id': user_id,
                            'termination_date': termination_date,
                            'email_address':email_address,
                            'revocation_date': revocation_date,
                            'app_name':app_name,
                            'difference_days': abs(date_difference),
                            'last_login':last_login
                        })
                        unique_effective_app_names.add(user.APP_NAME)
            else:
              
                unique_effective_app_names.add(user.APP_NAME)

        unique_effective_app_names_not_in_deficient = unique_effective_app_names - unique_deficient_app_names
        # Add the count to the deficient_app list
        deficient_app_with_count = [{'id': app.id, 'app_name': app, 'count': deficient_users_count_per_app.get(app, 0)} for app in unique_deficient_app_names]
        context = {
            'id': id,
            'deficient_users':deficient_users,
            'effective_users':effective_users,
            'selected_company':selected_company,
            'deficient_app': deficient_app_with_count,
            'effective_app': unique_effective_app_names_not_in_deficient,
        }
        return render(request,self.template_name,context)


class Audit_Termination_Details(AuditorPermissionMixin, UserRoleView):
    template_name = 'pages/AUDIT/termination-details.html'

    def get(self,request, comp_id, app_id):

        selected_app = APP_LIST.objects.get(id=app_id)

        #GET THE CURRENT DATE
        current_date = timezone.now()
        current_year = current_date.year
        selected_company = get_object_or_404(COMPANY, id=comp_id)
        app_users = APP_RECORD.objects.filter(APP_NAME=app_id, DATE_REVOKED__isnull=False, DATE_REVOKED__year=current_year).exclude(DATE_REVOKED__isnull=True)

         #GET THE POLICY DAYS
        policy = TERMINATIONPOLICY.objects.get(COMPANY_ID = comp_id)

        deficient_users = []
        effective_users = []
        unique_deficient_app_names = set()
        unique_effective_app_names = set()
        deficient_users_count_per_app = {} 

        for user in app_users:
        # Check if the user exists in HR_RECORD
            hr_record_exists = HR_RECORD.objects.filter(
                Q(EMAIL_ADDRESS=user.EMAIL_ADDRESS) |
                Q(USER_ID=user.USER_ID) |
                (Q(FIRST_NAME=user.FIRST_NAME) &
                 Q(LAST_NAME=user.LAST_NAME))
            ).exclude(TERMINATION_DATE=date(1900, 1, 1),STATUS='ACTIVE')

            if hr_record_exists:
                for hr_record in hr_record_exists:
                    app_name = user.APP_NAME
                    email_address = user.EMAIL_ADDRESS
                    termination_date = hr_record.TERMINATION_DATE
                    revocation_date = user.DATE_REVOKED
                    user_id = user.USER_ID
                    date_difference = (revocation_date.date() - termination_date).days
                    last_login = user.LAST_LOGIN.date()
                    id = user.id

                    # Check if the difference is more than 5 days
                    if date_difference > policy.DAYS_TO_TERMINATE:
                        deficient_users.append({
                            'id':id,
                            'user_id': user_id,
                            'termination_date': termination_date,
                            'email_address':email_address,
                            'revocation_date': revocation_date,
                            'app_name':app_name,
                            'difference_days': abs(date_difference),
                            'last_login':last_login
                        })
                        unique_deficient_app_names.add(user.APP_NAME)
                         # Count deficient users per unique application
                        deficient_users_count_per_app[app_name] = deficient_users_count_per_app.get(app_name, 0) + 1
                    else:
                        effective_users.append({
                            'user_id': user_id,
                            'termination_date': termination_date,
                            'email_address':email_address,
                            'revocation_date': revocation_date,
                            'app_name':app_name,
                            'difference_days': abs(date_difference),
                            'last_login':last_login
                        })
                        unique_effective_app_names.add(user.APP_NAME)
            else:
               
                unique_effective_app_names.add(user.APP_NAME)

        unique_effective_app_names_not_in_deficient = unique_effective_app_names - unique_deficient_app_names
        # Add the count to the deficient_app list
        deficient_app_with_count = [{'id': app.id, 'app_name': app, 'count': deficient_users_count_per_app.get(app, 0)} for app in unique_deficient_app_names]
        context = {
            'id': id,
            'deficient_users':deficient_users,
            'effective_users':effective_users,
            'selected_company':selected_company,
            'deficient_app': deficient_app_with_count,
            'effective_app': unique_effective_app_names_not_in_deficient,
            'selected_app':selected_app
        }
        
        return render(request,self.template_name, context)

class Audit_PrivilegedAccounts(AuditorPermissionMixin, UserRoleView):

    template_name = 'pages/AUDIT/admin-accounts.html'
    def get(self, request, id):
        selected_company = get_object_or_404(COMPANY, id=id)
        context = {
            'id':id,
            'selected_company':selected_company,
        }
        return render(request,self.template_name, context)

class PWConfigViewer(AuditorPermissionMixin, View):
    
    def get(self, request, id):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            application_name = APP_LIST.objects.get(id=id)
            app_name = serialize('json', [application_name])
            pwconfig = PASSWORD.objects.filter(APP_NAME = application_name)
            company_id = application_name.COMPANY_ID

            matched_application_info = []

            for password_object in pwconfig:
                password_policy = PASSWORDPOLICY.objects.get(COMPANY_ID=company_id)
                if password_policy:
                    # Compare fields and print matching and non-matching ones
                    matching_fields = []
                    non_matching_fields = []
                    configured_passwords = []
                    required_passwords = []
                    # Compare each field
                    for field in PASSWORDPOLICY._meta.get_fields():
                        field_name = field.name

                        # Skip certain fields
                        if field_name not in ['id', 'CREATED_BY', 'LAST_MODIFIED', 'MODIFIED_BY']:
                            if hasattr(password_object, field_name):
                                value_in_password = getattr(password_object, field_name)
                                value_in_policy = getattr(password_policy, field_name)

                                if field_name == 'AGE':
                                    if value_in_password <= value_in_policy:
                                        matching_fields.append(field_name)
                                    else:
                                        non_matching_fields.append(field_name)
                                        configured_passwords.append(value_in_password)  # Replace with actual value
                                        required_passwords.append(value_in_policy)  # Replace with actual value
                                elif field_name in ['LENGTH', 'LOCKOUT_ATTEMPT', 'LOCKOUT_DURATION','HISTORY']:
                                    if value_in_password >= value_in_policy:
                                        matching_fields.append(field_name)
                                    else:
                                        non_matching_fields.append(field_name)
                                        configured_passwords.append(value_in_password)  # Replace with actual value
                                        required_passwords.append(value_in_policy)  # Replace with actual value
                                elif value_in_password == value_in_policy:
                                        matching_fields.append(field_name)
                                else:
                                        non_matching_fields.append(field_name)
                                        configured_passwords.append(value_in_password)  # Replace with actual value
                                        required_passwords.append(value_in_policy)  # Replace with actual value
                                
                matched_application_info.append({
                        'app_name': str(password_object.APP_NAME),
                        'matching_fields': matching_fields,
                        'non_matching_fields': non_matching_fields,
                        'configured_passwords': configured_passwords,
                        'required_passwords': required_passwords
                    })
            context = {
                'app_name':app_name,
                'matched_application_info': matched_application_info,
            }
            return JsonResponse(context)
        
