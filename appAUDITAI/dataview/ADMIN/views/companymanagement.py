from django.shortcuts import render, redirect
from django.views import View
from appAUDITAI.models import COMPANY


class SetupCompany(View):
    template_name = 'pages/ADMIN/system-setting.html'
    def get(self,request):
        return render(request, self.template_name)
    
    def post(self,request):
        company_code = request.POST.get('company_code')
        company_name = request.POST.get('company_name')
        company_exist = COMPANY.objects.filter(COMPANY_ID=company_code, COMPANY_NAME=company_name).first()
        if company_exist is not None:
            pass
        else:
            new_company = COMPANY(COMPANY_ID=company_code, COMPANY_NAME=company_name)
            new_company.save()
        return render(request, self.template_name)



