from appAUDITAI.dataview.MISC.imports import *

class AccessRequestHome(View):

    template_name = 'pages/TICKETS/ticket-home.html'

    def get(self, request):

        user = request.user
        if user:
            group_names = user.groups.values_list('name', flat=True)
            user_email = User.objects.get(id = user.id)
        
        try:
            active_employees = HR_RECORD.objects.filter(STATUS='ACTIVE').exclude(EMAIL_ADDRESS=user_email)
        except HR_RECORD.DoesNotExist:
            active_employees = None
            pass

        company_ids = []

        # Fetch the user roles objects
        user_roles = USERROLES.objects.filter(USERNAME = user.id)

        # Iterate over each user role
        for user_role in user_roles:
            # Assuming COMPANY_ID is the name of the many-to-many field relating to companies
            # Get the related companies for each user role instance
            companies = user_role.COMPANY_ID.all()
            
            # Iterate over each company in the related companies
            for company in companies:
                # Assuming company_id is the attribute containing the ID of the company
                # Append the company ID to the list
                    app_list = APP_LIST.objects.filter(COMPANY_ID = company)
                  

        
        context = {'user':user, 
                   'group_names':group_names,
                   'active_employees':active_employees,
                  }
        
        return render(request, self.template_name,context)