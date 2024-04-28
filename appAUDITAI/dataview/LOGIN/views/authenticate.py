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
            group_names = user.groups.values_list('name', flat=True)
                
            if 'Administrator' in group_names:
                template_name = 'pages/DASHBOARD/admin-dashboard.html'
            elif 'Auditor' in group_names:
                template_name = 'pages/DASHBOARD/auditor-dashboard.html'
            elif 'Process Owner' in group_names:
                template_name = 'pages/DASHBOARD/processowner-dashboard.html'
            elif 'Compliance' in group_names:
                template_name = 'pages/DASHBOARD/compliance-dashboard.html'
            else:
                # Handle the case when the user has none of the expected roles
                template_name = 'pages/DASHBOARD/default-dashboard.html'

            context = {'user': user, 'group_names': group_names,}
            return render(request, template_name, context)
        else:
            return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)
                return redirect('appAUDITAI:mydashboard')
            else:
                messages.error(request, 'Username or password is incorrect. Please try again.')
                form.fields['username'].initial = ''
        else:
            messages.error(request, 'Form is not valid. Please check your input.')
            form.fields['username'].initial = ''
        # Re-render the form with errors and the submitted data
        return redirect('appAUDITAI:authenticate-user')

class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('appAUDITAI:authenticate-user')
