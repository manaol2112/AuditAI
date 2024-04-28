from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User, Group
from appAUDITAI.models import MULTIPLE_COMPANY
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.contrib import messages
from appAUDITAI.dataview.LOGIN.forms.authenticate_form import LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from appAUDITAI.models import USERROLES
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
        form = LoginForm()
        if request.user.is_authenticated:
            user = request.user
            if user: 
                group_names = user.groups.values_list('name', flat=True)
                if group_names:
                    try:   
                        if 'Administrator' in group_names:
                            template_name = 'pages/DASHBOARD/admin-dashboard.html'
                        elif 'Auditor' in group_names:
                            template_name = 'pages/DASHBOARD/auditor-dashboard.html'
                        elif 'Process Owner' in group_names:
                            template_name = 'pages/DASHBOARD/processowner-dashboard.html'
                        elif 'Compliance' in group_names:
                            template_name = 'pages/DASHBOARD/compliance-dashboard.html'
                        else:
                            context = {'user': user, 'group_names': group_names,}
                            return render(request, template_name, context)
                    except TemplateDoesNotExist as e:
                        return render(request, self.template_name, {'form':form})
                    except Exception as e:
                        print('Something went wrong. I cant login to application right now.')
                        pass
                else:
                    group_names = None         
            else:
                user = None
                return render(request, self.template_name, {'form':form})

            context = {'user': user, 'group_names': group_names,}
            return render(request, template_name, context)
        else:
            return render(request, self.template_name, {'form':form})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('appAUDITAI:mydashboard')
            else:
                # User is not active
                messages.error(request, 'Your account is locked. We cannot access your account right now. Please reach out to your system administrator.')
        else:
            # Authentication failed
            messages.error(request, 'Username or password is incorrect. Please try again.')

        # Redirect back to the login page
        return redirect('appAUDITAI:authenticate-user')
       
       

class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('appAUDITAI:authenticate-user')
