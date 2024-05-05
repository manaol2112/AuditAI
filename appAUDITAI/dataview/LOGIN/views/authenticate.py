from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User, Group
from appAUDITAI.models import MULTIPLE_COMPANY
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.contrib import messages
from appAUDITAI.dataview.LOGIN.forms.authenticate_form import LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from appAUDITAI.models import USERROLES,USER_LOCKOUT,PASSWORDCONFIG
from django.template import TemplateDoesNotExist

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

class AuthenticateUsers(View):

    model = User
    template_name = 'login/login.html'
    dashboard_name = 'pages/DASHBOARD/client-select.html'

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
                            return render(request, template_name, context)
                        elif 'Auditor' in group_names:
                            context = {'user':user, 'group_names':group_names}
                            template_name = 'pages/DASHBOARD/auditor-dashboard.html'
                            return render(request, template_name, context)
                        elif 'Process Owner' in group_names:
                            context = {'user':user, 'group_names':group_names}
                            template_name = 'pages/DASHBOARD/processowner-dashboard.html'
                            return render(request, template_name, context)
                        elif 'Compliance' in group_names:
                            context = {'user':user, 'group_names':group_names}
                            template_name = 'pages/DASHBOARD/compliance-dashboard.html'
                            return render(request, template_name, context)
                        elif 'Access Requestor' in group_names:
                            context = {'user':user, 'group_names':group_names}
                            template_name = 'pages/TICKETS/ticket-home.html'
                            #return redirect('appAUDITAI:access-request-home', context)
                            return render(request,template_name, context)
                        else:
                            if user.is_superuser:
                                context = {'user':user, 'group_names':group_names}
                                template_name = 'pages/DASHBOARD/admin-dashboard.html'
                                return render(request, template_name, context)
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
        else:
            context = {'user': user}
            return render(request, self.template_name,context)

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
                login(request, user)
                
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
