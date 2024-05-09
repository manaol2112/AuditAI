from appAUDITAI.dataview.MISC.imports import *
from appAUDITAI.models import APP_LIST, ACCESSREQUEST
from django.core.mail import send_mail
from django.template.loader import render_to_string
import uuid
from django.http import HttpResponseNotFound

class CompanySelect(View):

    template_name = 'pages/TICKETS/ticket-select-company.html'

    def get(self, request):
        user = request.user
        user_roles = USERROLES.objects.get(USERNAME=user)
        companies = user_roles.COMPANY_ID.all()

        context = {'user':user, 
                   'companies':companies
                  }
        
        return render(request, self.template_name,context)


class AccessRequestHome(View):

    template_name = 'pages/TICKETS/ticket-home.html'

    def get(self, request,comp_id):
        context = self.common_data(request, comp_id)
        return render(request, self.template_name, context)

    def common_data(self, request, comp_id):

        user = request.user
        if user:
            group_names = user.groups.values_list('name', flat=True)
            user_email = User.objects.get(id = user.id)
        try:
            selected_company = COMPANY.objects.get(id = comp_id)
        except COMPANY.DoesNotExist:
            selected_company = None
            pass

        try:
            apps = APP_LIST.objects.filter(COMPANY_ID = selected_company)
        except APP_LIST.DoesNotExist:
            apps = None
            pass
        
        try:
            active_employees = HR_RECORD.objects.filter(STATUS='ACTIVE', COMPANY_ID = selected_company).exclude(EMAIL_ADDRESS=user_email)
        except HR_RECORD.DoesNotExist:
            active_employees = None
            pass

        try:
            requestor = User.objects.get(username = user)
            requestor_email = HR_RECORD.objects.get(EMAIL_ADDRESS = requestor.email)
        except HR_RECORD.DoesNotExist:
            requestor_email = None
            pass
        except Exception as e:
            print(str(e))
            pass

        try:
            my_requests = ACCESSREQUEST.objects.filter(CREATOR = requestor_email.EMAIL_ADDRESS, COMPANY_ID = comp_id)
            if my_requests:
                print(my_requests)
            else:
                print('no email found')

        except ACCESSREQUEST.DoesNotExist:
            my_requests =  None
            pass
        except Exception as e:
            print(str(e))
        
        context = {'user':user, 
                   'group_names':group_names,
                   'active_employees':active_employees,
                   'comp_id':comp_id,
                   'apps':apps,
                   'my_requests':my_requests
                  }
        
        return context
    
    def post(self, request, comp_id):
        request_type = request.POST.get('request_type')

        if request_type == 'supervisor' or request_type == 'team_member':
            team_members = request.POST.getlist('team_member_select')
            applications = request.POST.get('applications_select')
            roles = request.POST.getlist('roles_select')
            comment = request.POST.get('request_comment')
            priority = request.POST.get('priority')

            try:
                last_access_request = ACCESSREQUEST.objects.order_by('-id').first()
            except ACCESSREQUEST.DoesNotExist:
                last_access_request = 1
                pass
            except Exception as e:
                str(e)

            if last_access_request:
                last_id = last_access_request.id
                new_request_id = f'TASK#{last_id}'
            else:
                new_request_id = 'TASK#'  # If there are no existing access requests, start with 1

            company = COMPANY.objects.get(id = comp_id)
            app_name = APP_LIST.objects.get(id = applications)
            application_owner_email = app_name.APPLICATION_OWNER.email if app_name.APPLICATION_OWNER else None
            approver = User.objects.get(username = request.user)

            for member in team_members:
                requestor = HR_RECORD.objects.get(id = member)
                for role in roles:
                    access_request, created = ACCESSREQUEST.objects.get_or_create(
                    COMPANY_ID=company,
                    REQUEST_ID=new_request_id,
                    REQUESTOR=requestor.EMAIL_ADDRESS,
                    APP_NAME=app_name.APP_NAME,
                    COMMENTS=comment,
                    PRIORITY=priority,
                    ROLES=role,
                    DATE_REQUESTED = timezone.now().date(),
                    DATE_APPROVED = timezone.now().date(),
                    STATUS = "Approved",
                    REQUEST_TYPE = 'PRE-APPROVAL',
                    BUSINESS_APPROVER = approver.email,
                    ASSIGNED_TO = application_owner_email,
                    CREATOR = approver.email

                )
                if created:  # If the object was created
                    access_request.save()  # Save the access request object

        elif request_type == 'own_access':
            approvers = request.POST.getlist('access_approver')
            applications = request.POST.get('applications_select')
            roles = request.POST.getlist('roles_select')
            comment = request.POST.get('request_comment')
            priority = request.POST.get('priority')

            try:
                last_access_request = ACCESSREQUEST.objects.order_by('-id').first()
            except ACCESSREQUEST.DoesNotExist:
                last_access_request = 1
                pass
            except Exception as e:
                str(e)

            if last_access_request:
                last_id = last_access_request.id
                new_request_id = f'TASK#{last_id}'
            else:
                new_request_id = 'TASK#1'  # If there are no existing access requests, start with 1
            
            user = request.user
            requestor = HR_RECORD.objects.get(EMAIL_ADDRESS = user.email)
            company = COMPANY.objects.get(id = comp_id)
            app_name = APP_LIST.objects.get(id = applications)
            application_owner_email = app_name.APPLICATION_OWNER.email if app_name.APPLICATION_OWNER else None

            for approver in approvers:
                approver_email = HR_RECORD.objects.get(id = approver)
                for role in roles:
                    access_request, created = ACCESSREQUEST.objects.get_or_create(
                    COMPANY_ID=company,
                    REQUEST_ID=new_request_id,
                    REQUESTOR=requestor.EMAIL_ADDRESS,
                    APP_NAME=app_name.APP_NAME,
                    COMMENTS=comment,
                    PRIORITY=priority,
                    ROLES=role,
                    DATE_REQUESTED = timezone.now().date(),
                    STATUS = "Pending Approval",
                    REQUEST_TYPE = 'NEEDS-APPROVAL',
                    BUSINESS_APPROVER = approver_email.EMAIL_ADDRESS,
                    ASSIGNED_TO = application_owner_email,
                    CREATOR = requestor.EMAIL_ADDRESS
                )
                if created:  # If the object was created
                    access_request.save()  # Save the access request object
                    access_request.approval_token = uuid.uuid4().hex
                    access_request.save()  # Save the access request object

                    verification_url = reverse('appAUDITAI:approve_access_request', args=[access_request.APPROVAL_TOKEN])

                    subject = 'ACTION REQUESTED: Access request approval for' + str(app_name.APP_NAME)
                    message = render_to_string('email/access_request_approval.html', {'access_request': access_request, 'verification_url': request.build_absolute_uri(verification_url)})
                    from_email = 'support@audit-ai.com'  # Your email
                    to_email = approver_email.EMAIL_ADDRESS  # Approver's email
                    send_mail(subject, message, from_email, [to_email], fail_silently=False)
        else:
            pass

        context = self.common_data(request, comp_id)
        return render(request, self.template_name, context)
    
def approve_access_request(request, approval_token):
    try:
        access_request = ACCESSREQUEST.objects.get(APPROVAL_TOKEN=approval_token)
        access_request.STATUS = "Approved"
        access_request.save()
        return redirect('appAUDITAI:error_404')

    except ACCESSREQUEST.DoesNotExist:
        return HttpResponseNotFound("Access request not found or invalid token.")


def get_roles(request):

    if request.method == 'GET':
        app_id = request.GET.get('app_id')
        try:
            app = APP_LIST.objects.get(id = app_id)
        except APP_LIST.DoesNotExist:
            app = None
            pass
        try:
            roles = APP_RECORD.objects.filter(APP_NAME = app).values('ROLE_NAME').distinct()
            return JsonResponse({'roles':list(roles)})
        except APP_RECORD.DoesNotExist:
            roles = None
            pass
       
    
