from appAUDITAI.dataview.MISC.imports import *
from appAUDITAI.models import APP_LIST

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

    def get(self, request, comp_id):

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

        context = {'user':user, 
                   'group_names':group_names,
                   'active_employees':active_employees,
                   'comp_id':comp_id,
                   'apps':apps
                  }
        
        return render(request, self.template_name,context)
    
def get_roles(request):

    if request.method == 'GET' and request.is_ajax():
        app_name = request.GET.get('app_name')
        roles = Role.objects.filter(application__name=app_name).values_list('name', flat=True)
        return JsonResponse(list(roles), safe=False)
    
