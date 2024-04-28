from django.shortcuts import render, redirect
from django.views import View
from appAUDITAI.models import COMPANY, USERROLES
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password


class CreateUserView(View):
    template_name = 'pages/ADMIN/user-list.html'

    def get(self, request):
        userslist = User.objects.filter(is_active=True)
        groups = Group.objects.all()
        companies = COMPANY.objects.all()
        context = {
            'userslist': userslist,
            'groups':groups,
            'companies':companies
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        username = request.POST['username']
        user = User.objects.filter(username=username)
        if user.exists():
            pass
        else:
            #Create User 
            new_user = User.objects.create(
            username=username,
            first_name=request.POST.get('first_name', ''), 
            last_name=request.POST.get('last_name', ''), 
            email=request.POST.get('email_address', ''), 
            password='12345678' #This to be updated
        )
            new_user.save()

            #Assign Group
            selected_groups = request.POST.getlist('role_selected_values')
            groups = Group.objects.filter(id__in=selected_groups)
            new_user.groups.set(groups)

            # Assign Companies
            selected_companies = request.POST.getlist('company_selected_values')
            companies = COMPANY.objects.filter(id__in=selected_companies)
            user_roles = USERROLES.objects.create(USERNAME=new_user)
            user_roles.COMPANY_ID.set(companies)
            
        return redirect('appAUDITAI:all-users')

