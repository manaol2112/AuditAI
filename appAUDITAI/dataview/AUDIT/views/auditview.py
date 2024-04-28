from django.shortcuts import render, redirect
from django.views import View
from appAUDITAI.dataview.LOGIN.views.authenticate import UserRoleView
from appAUDITAI.dataview.LOGIN.views.decorators import UserAccessMixin
from appAUDITAI.models import APP_LIST, COMPANY, PASSWORD,PASSWORDPOLICY, HR_RECORD, APP_RECORD, TERMINATIONPOLICY
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.serializers import serialize
from django.utils import timezone
from datetime import date
from django.db.models import Q
from django.db.models import F
from appAUDITAI.dataview.LOGIN.views.decorators import AuditorPermissionMixin

class AuditHome(AuditorPermissionMixin, UserRoleView):
    def get(self,request,id):
        user_role = self.user_role
        selected_company = COMPANY.objects.get(id=id)

        if user_role == 'Auditor':
            template_name = 'pages/AUDIT/audit-home.html'
        else:
            template_name = 'pages/login/login.html'
        context = {'selected_company': selected_company}

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
        
