from django.shortcuts import redirect, render
from django.views import View
from appAUDITAI.models import USERROLES
from appAUDITAI.dataview.LOGIN.views.authenticate import UserRoleView

class HomeView(UserRoleView):
    template_name = 'pages/DASHBOARD/dashboard.html'

    def get(self, request):
        user = request.user
        group_names = user.groups.values_list('name', flat=True)
        user_roles = USERROLES.objects.filter(USERNAME=user)
        companies = []
        user_role = None  # Initialize user_role outside the loop
        for user_role in user_roles:
            companies.extend(user_role.COMPANY_ID.all())
            
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

        context = {'user': user, 'group_names': group_names, 'companies': companies, 'user_role': user_role}
        return render(request, template_name, context)