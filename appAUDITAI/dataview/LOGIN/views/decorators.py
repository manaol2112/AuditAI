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
            user_dashboard_url = reverse('authenticate-user')  # Replace 'user_profile' with the actual name of your user profile URL pattern
            return redirect(user_dashboard_url)
        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)
    
class AuditorPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'authenticate-user'  #Replace with your actual login URL

    def test_func(self):
        user = self.request.user
        return user.groups.filter(name='Auditor').exists()

    def handle_no_permission(self):
        user_dashboard_url = reverse('appAUDITAI:mydashboard')  
        return redirect(user_dashboard_url)
    
class ProcessOwnerPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'authenticate-user' 

    def test_func(self):
        user = self.request.user
        return user.groups.filter(name='Process Owner').exists()

    def handle_no_permission(self):
        user_dashboard_url = reverse('appAUDITAI:mydashboard') 
        return redirect(user_dashboard_url)
    

class AdminPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'authenticate-user' 

    def test_func(self):
        user = self.request.user
        return user.groups.filter(name='Administrator').exists()

    def handle_no_permission(self):
        user_dashboard_url = reverse('appAUDITAI:mydashboard') 
        return redirect(user_dashboard_url)