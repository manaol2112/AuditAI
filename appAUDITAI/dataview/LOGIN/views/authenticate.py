from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth.models import User, Group
from appAUDITAI.models import EmailVerification,UserToken
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.contrib import messages
from appAUDITAI.dataview.LOGIN.forms.authenticate_form import LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from appAUDITAI.models import USERROLES,USER_LOCKOUT,PASSWORDCONFIG
from django.template import TemplateDoesNotExist
import random
import string
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.utils.timezone import make_aware

class UserRoleView(LoginRequiredMixin, View):

    def get_user_role(self):
        user = self.request.user
        group_names = user.groups.values_list('name', flat=True)
        
        if 'Administrator' in group_names:
            return 'Administrator'
        elif 'Auditor' in group_names:
            return 'Auditor'
        elif 'System Admin' in group_names:
            return 'System Admin'
        elif 'Compliance' in group_names:
            return 'Compliance'
        else:
            return 'User'
        
    def dispatch(self, request, *args, **kwargs):
        self.user_role = self.get_user_role()
        return super().dispatch(request, *args, **kwargs)
    
def generate_verification_code(length=6):
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))
    
from django.utils import timezone

class MultiFactorAuth(View):
    template_name = 'login/mfa.html'
    
    def get(self, request, token):
        user_token = get_object_or_404(UserToken, token=token)
        user = user_token.user
       
        context = {
            'user': user,
            'token':token
        }

        return render(request, self.template_name, context)
    
    def post(self,request,token):
        code_provided = request.POST.get('mfa_code')
        print(code_provided)
        try:
            user = UserToken.objects.get(token = token)
        except UserToken.DoesNotExist:
            user = None
            pass

        try:
            email_verification = EmailVerification.objects.get(user=user.user)
            if email_verification.code == code_provided:
                if email_verification.expires_at >= timezone.now():
                    user = email_verification.user
                    login(request, user)
                    return redirect('appAUDITAI:authenticate-user')
                else:
                    # Handle case where code is expired
                    messages.error(request, 'The code you provided is not valid')
            else:
                # Handle case where provided code doesn't match
                 messages.error(request, 'The code you provided is not valid')
        except EmailVerification.DoesNotExist:
            # Handle case where EmailVerification object doesn't exist for the user
            email_verification = None
            pass

        context = {
            'user': user,
            'token':token
        }

        return render(request,self.template_name,context)
    
        
class AuthenticateUsers(View):
    model = User
    template_name = 'login/login.html'
    def get(self, request):
        user = request.user
        if request.user.is_authenticated:
            user = request.user
            if user: 
                group_names = user.groups.values_list('name', flat=True)
                if group_names:
                    try:   
                        if 'Administrator' in group_names:
                            context = {'user':user, 'group_names':group_names}
                            template_name = 'pages/DASHBOARD/admin-dashboard.html'
                        elif 'Auditor' in group_names:
                            user_roles = USERROLES.objects.get(USERNAME=user)
                            companies = user_roles.COMPANY_ID.all()
                            context = {'user':user, 'group_names':group_names, 'companies':companies}
                            template_name = 'pages/DASHBOARD/auditor-dashboard.html'
                        elif 'Process Owner' in group_names:
                            context = {'user':user, 'group_names':group_names}
                            template_name = 'pages/DASHBOARD/processowner-dashboard.html'
                        elif 'Compliance' in group_names:
                            context = {'user':user, 'group_names':group_names}
                            template_name = 'pages/DASHBOARD/compliance-dashboard.html'
                        elif 'Access Requestor' in group_names:
                            user_roles = USERROLES.objects.get(USERNAME=user)
                            companies = user_roles.COMPANY_ID.all()
                            context = {'user':user, 'group_names':group_names, 'companies':companies}
                            template_name = 'pages/TICKETS/ticket-select-company.html'
                        else:
                            if user.is_superuser:
                                context = {'user':user, 'group_names':group_names}
                                #template_name = 'pages/DASHBOARD/admin-dashboard.html'
                                return redirect('appAUDITAI:access-request-home', context)
                            else:
                                return redirect('appAUDITAI:authenticate-user')
                       
                    except TemplateDoesNotExist as e:
                        return redirect('appAUDITAI:authenticate-user')
                    except Exception as e:
                        return redirect('appAUDITAI:authenticate-user')
                else: 
                    if user.is_superuser:
                        context = {'user':user, 'group_names':group_names}
                        template_name = 'pages/DASHBOARD/admin-dashboard.html'
                        return render(request, template_name, context)
            else:
                user = None
                return redirect('appAUDITAI:authenticate-user')
            
            return render(request, template_name, context)
        else:
            context = {'user': user}
            return render(request,self.template_name,context)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            max_attempt = PASSWORDCONFIG.objects.all().first()
            if not max_attempt:
                PASSWORDCONFIG.objects.create(LOCKOUT=5)
                max_attempt = PASSWORDCONFIG.objects.first()  # Retrieve the newly created object
        except PASSWORDCONFIG.DoesNotExist:
            PASSWORDCONFIG.objects.create(LOCKOUT=5)
            max_attempt = PASSWORDCONFIG.objects.first()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                try:
                    user_lockout = USER_LOCKOUT.objects.get(user__username=username)
                    user_lockout.failed_attempts = 0
                    user_lockout.save()
                except USER_LOCKOUT.DoesNotExist:
                    # Create UserLockout record if it doesn't exist
                    USER_LOCKOUT.objects.create(user=User.objects.get(username=username))
                try:
                    token = UserToken.objects.get(user=user)
                except UserToken.DoesNotExist:
                    token = UserToken.objects.create(user=user)

                login(request, user)
               
    # TEMPORARILY DISABLING MULTIFACTOR AUTH
    #             

    #             verification_code = generate_verification_code()
    #             expiration_time = timezone.now() + timezone.timedelta(minutes=10)

    #             try:
    #                 user_exist = EmailVerification.objects.get(user=user)
    #                 user_exist.code = verification_code
    #                 user_exist.expires_at = expiration_time
    #                 user_exist.save()
    #             except EmailVerification.DoesNotExist:
    #                 # Create EmailVerification instance
    #                 email_verification, created = EmailVerification.objects.get_or_create(
    #                     user=user,
    #                     code=verification_code,
    #                     expires_at=expiration_time
    # )
    #         # Send email with verification code
        
    #             subject = 'AUDITAI Verification Code'
    #                     # Email body
    #             message = render_to_string('email/mfa.html', {'verification_code': verification_code})
    #                     # Send email verification
    #             send_mail(subject, message, 'auditai-support@audit-ai.net', [user.email])

    #             token_url = reverse('appAUDITAI:require-mfa', kwargs={'token': token.token})
    #             redirect_url = f"{token_url}?token={token}" 
    #             context = {
    #                 'token':token.token,
    #                  'verification_code': verification_code,
    #             }
    #             return redirect(redirect_url , context)
                
            else:
                # User is not active
                messages.error(request, 'Your account is locked. Please contact your system administrator.')
        else:
            messages.error(request, 'Incorrect username or password. Please try again.')
            # Authentication failed
            try:
                user_lockout = USER_LOCKOUT.objects.get(user__username=username)
                user_lockout.failed_attempts += 1
                user_lockout.save()
                if user_lockout.failed_attempts >= int(max_attempt.LOCKOUT):
                    user_lockout.locked_out = True
                    user_lockout.save()
                    messages.error(request, 'Your account has been locked due to multiple failed login attempts. Please contact your system administrator to reset password.')
            except USER_LOCKOUT.DoesNotExist:
                # Create UserLockout record for the user if it doesn't exist
                messages.error(request, 'Incorrect username or password. Please try again.')
                return redirect('appAUDITAI:authenticate-user') 

        # Redirect back to the login page
        return redirect('appAUDITAI:authenticate-user')  # Redirect to the login page
       
class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('appAUDITAI:authenticate-user')
