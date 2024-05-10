from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.urls import reverse

class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if (not self.request.user.is_authenticated):
            return redirect_to_login(self.request.get_full_path(),self.get_login_url(), self.get_redirect_field_name())
        
        if not self.has_permission():
            user_dashboard_url = reverse('appAUDITAI:authenticate-user') 
            return redirect('appAUDITAI:authenticate-user')
        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)
    
class AuditorPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'appAUDITAI:authenticate-user' 

    def test_func(self):
        user = self.request.user
        return user.groups.filter(name='Auditor').exists()

    def handle_no_permission(self):
        user_dashboard_url = reverse('appAUDITAI:no_permission')  
        return redirect(user_dashboard_url)
    
class ProcessOwnerPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'appAUDITAI:authenticate-user' 

    def test_func(self):
        user = self.request.user
        return user.groups.filter(name='Process Owner').exists()

    def handle_no_permission(self):
        user_dashboard_url = reverse('appAUDITAI:no_permission')  
        return redirect(user_dashboard_url)
    
class AdminPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'appAUDITAI:authenticate-user' 

    def test_func(self):
        user = self.request.user
        return user.groups.filter(name='Administrator').exists() or user.is_superuser

    def handle_no_permission(self):
        user_dashboard_url = reverse('appAUDITAI:no_permission')  
        return redirect(user_dashboard_url)
    
class AccessRequestor(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'appAUDITAI:authenticate-user' 

    def test_func(self):
        user = self.request.user
        return user.groups.filter(name='Access Requestor').exists()

    def handle_no_permission(self):
        user_dashboard_url = reverse('appAUDITAI:no_permission')  
        return redirect(user_dashboard_url)