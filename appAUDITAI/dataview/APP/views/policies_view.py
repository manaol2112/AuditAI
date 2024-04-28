from django.shortcuts import render
from django.views import View
from appAUDITAI.models import POLICIES, APP_LIST, CONTROLS, USERROLES,COMPANY,PASSWORDPOLICY,TERMINATIONPOLICY
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
from django.utils import timezone

class PoliciesView(View):
    model_name = POLICIES
    template_name = 'pages/POLICIES/compliance-policies-au.html'

    def get(self, request):
        app = APP_LIST.objects.filter(APP_NAME__isnull=False)
        policies = POLICIES.objects.filter(POLICY_NAME__isnull=False)
        context = {'policies':policies,
                   'app':app}
        return render(request,self.template_name,context)
    
    def post(self,request):
        if request.method == 'POST':
            policy_name = request.POST['policy_name']
            policy_description = request.POST['policy_description']
        
            selected_values_json = request.POST.get('control_selected_values', '[]')

            control_ids = json.loads(selected_values_json)
            
            existing_record = POLICIES.objects.filter(POLICY_NAME=policy_name).first()

            if existing_record:
                existing_record.POLICY_DESCRIPTION = policy_description
                existing_record.CONTROL_ID.set(
                    [item['value'] for item in control_ids]
                )
                existing_record.save()
            else:

                new_record = POLICIES.objects.create(
                    POLICY_NAME=policy_name,
                    POLICY_DESCRIPTION=policy_description,
                )

                new_record.CONTROL_ID.set(
                    [item['value'] for item in control_ids]
                )

class PoliciesAuthView(View):
    model_name = CONTROLS
    template_name = 'pages/POLICIES/compliance-policies-authentication.html'

    def get(self, request):
        user = request.user
        entities= USERROLES.objects.filter(USERNAME=user)
        company_names = []
        for user_role in entities:
            company_names.extend(user_role.COMPANY_ID.all())
        app = self.model_name.objects.filter(CONTROL_ID__isnull=False)
        context = {'app':app,
                   'company_names':company_names}
        return render(request,self.template_name,context)
    
    def post(self, request):
        user = request.user
        template_name = 'pages/POLICIES/compliance-policies-authentication.html'

        selected_companies = request.POST.getlist('entity_select')
        companies = COMPANY.objects.filter(id__in=selected_companies)

        # Check if a PASSWORDPOLICY record already exists for the selected company
        existing_pw_policy = PASSWORDPOLICY.objects.filter(COMPANY_ID__in=companies).first()

        if existing_pw_policy:
            # Update the existing record
            existing_pw_policy.COMPLEXITY_ENABLED = bool(request.POST.get('pass_complexity', False))
            existing_pw_policy.LENGTH = int(request.POST.get('pass_length', 0))
            existing_pw_policy.UPPER = 'upper_case' in request.POST
            existing_pw_policy.LOWER = 'lower_case' in request.POST
            existing_pw_policy.NUMBER = 'number' in request.POST
            existing_pw_policy.SPECIAL_CHAR = 'special_character' in request.POST
            existing_pw_policy.AGE = int(request.POST.get('pass_age', 0))
            existing_pw_policy.HISTORY = int(request.POST.get('pass_history', 0))
            existing_pw_policy.LOCKOUT_ATTEMPT = int(request.POST.get('pass_lockout', 0))
            existing_pw_policy.LOCKOUT_DURATION = request.POST.get('pass_lockout_duration', '')
            existing_pw_policy.MFA_ENABLED = bool(request.POST.get('multifactor_enabled', False))
            existing_pw_policy.MODIFIED_BY = user.username
            existing_pw_policy.LAST_MODIFIED = timezone.now()
            # Save the changes to the existing record
            existing_pw_policy.save()
        else:
            # Create a new PASSWORDPOLICY record
            new_pw_policy = PASSWORDPOLICY.objects.create(
                COMPLEXITY_ENABLED=bool(request.POST.get('pass_complexity', False)),
                LENGTH=int(request.POST.get('pass_length', 0)),
                UPPER='upper_case' in request.POST,
                LOWER='lower_case' in request.POST,
                NUMBER='number' in request.POST,
                SPECIAL_CHAR='special_character' in request.POST,
                AGE=int(request.POST.get('pass_age', 0)),
                HISTORY=int(request.POST.get('pass_history', 0)),
                LOCKOUT_ATTEMPT=int(request.POST.get('pass_lockout', 0)),
                LOCKOUT_DURATION=request.POST.get('pass_lockout_duration', ''),
                MFA_ENABLED=bool(request.POST.get('multifactor_enabled', False)),
                CREATED_BY = user,
                CREATED_ON = timezone.now()
            )
            # Associate the PASSWORDPOLICY with selected companies
            new_pw_policy.COMPANY_ID.set(companies)

        entities= USERROLES.objects.filter(USERNAME=user)
        company_names = []
        for user_role in entities:
            company_names.extend(user_role.COMPANY_ID.all())
        app = self.model_name.objects.filter(CONTROL_ID__isnull=False)
        context = {'app':app,
                    'company_names':company_names}
        return render(request,template_name,context)

class PoliciesProvisionView(View):
    model_name = CONTROLS
    template_name = 'pages/POLICIES/compliance-policies-provisioning.html'

    def get(self, request):
        user = request.user
        entities= USERROLES.objects.filter(USERNAME=user)
        company_names = []
        for user_role in entities:
            company_names.extend(user_role.COMPANY_ID.all())
        app = self.model_name.objects.filter(CONTROL_ID__isnull=False)
        context = {'app':app,
                   'company_names':company_names}
        return render(request,self.template_name,context)
    
class PoliciesTerminationView(View):
    model_name = CONTROLS
    template_name = 'pages/POLICIES/compliance-policies-termination.html'

    def get(self, request):
        user = request.user
        entities= USERROLES.objects.filter(USERNAME=user)
        company_names = []
        for user_role in entities:
            company_names.extend(user_role.COMPANY_ID.all())
        app = self.model_name.objects.filter(CONTROL_ID__isnull=False)
        context = {'app':app,
                   'company_names':company_names}
        return render(request,self.template_name,context)
    
    def post(self, request):
        user = request.user
        template_name = 'pages/POLICIES/compliance-policies-termination.html'

        selected_companies = request.POST.getlist('entity_select')
        companies = COMPANY.objects.filter(id__in=selected_companies)

        # Check if a PASSWORDPOLICY record already exists for the selected company
        existing_term_policy = TERMINATIONPOLICY.objects.filter(COMPANY_ID__in=companies).first()

        if existing_term_policy:
            existing_term_policy.DAYS_TO_TERMINATE = int(request.POST.get('terminate_days', 0))
            existing_term_policy.MODIFIED_BY = user.username
            existing_term_policy.LAST_MODIFIED = timezone.now()
            existing_term_policy.save()
        else:
         # Create a new PASSWORDPOLICY record
            new_term_policy = TERMINATIONPOLICY.objects.create(
                DAYS_TO_TERMINATE=bool(request.POST.get('terminate_days', False)),
                CREATED_BY = user,
                CREATED_ON = timezone.now()
            )
        # Associate the PASSWORDPOLICY with selected companies
            new_term_policy.COMPANY_ID.set(companies)

        entities= USERROLES.objects.filter(USERNAME=user)
        company_names = []
        for user_role in entities:
            company_names.extend(user_role.COMPANY_ID.all())
        app = self.model_name.objects.filter(CONTROL_ID__isnull=False)
        context = {'app':app,
                    'company_names':company_names}
        return render(request,template_name,context)
    
class PoliciesUserAccessReviewView(View):
    model_name = CONTROLS
    template_name = 'pages/POLICIES/compliance-policies-useraccessreview.html'

    def get(self, request):
        user = request.user
        entities= USERROLES.objects.filter(USERNAME=user)
        company_names = []
        for user_role in entities:
            company_names.extend(user_role.COMPANY_ID.all())
        app = self.model_name.objects.filter(CONTROL_ID__isnull=False)
        context = {'app':app,
                   'company_names':company_names}
        return render(request,self.template_name,context)

class PoliciesAdminView(View):
    model_name = CONTROLS
    template_name = 'pages/POLICIES/compliance-policies-adminaccounts.html'

    def get(self, request):
        app = self.model_name.objects.filter(CONTROL_ID__isnull=False)
        context = {'app':app}
        return render(request,self.template_name,context)