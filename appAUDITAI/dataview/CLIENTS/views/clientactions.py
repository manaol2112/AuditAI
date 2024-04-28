from django.shortcuts import render, redirect
from django.views import View
from appAUDITAI.dataview.LOGIN.views.authenticate import UserRoleView
from appAUDITAI.models import COMPANY


class ClientActions(UserRoleView):

    def get(self,request,id):

        selected_company = COMPANY.objects.get(id=id)

        user_role = self.user_role
        if user_role == 'Administrator':
            template_name = 'pages/CLIENTS/admin-actions.html'
        elif user_role == 'Auditor':
            template_name = 'pages/CLIENTS/auditor-actions.html'
        elif user_role == 'Compliance':
            template_name = 'pages/CLIENTS/compliance-actions.html'      
        context = {'selected_company': selected_company}
        
        return render(request,template_name, context)