from appAUDITAI.dataview.MISC.imports import *

class SystemSettingsView(View):
    
    template_name = 'pages/ADMIN/system-settings.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)
    

class ManageUsersandRolesDetailsView(View):
    template_name = 'pages/ADMIN/manage-user-roles-details.html'
    
    def get(self, request,user_id):
        context = self.common_data(request,user_id)
        return render(request, self.template_name, context)
    
    def common_data(self, request, user_id):
        try:
            selected_user = User.objects.get(id=user_id)
            selected_groups = selected_user.groups.all()
            non_selected_groups = Group.objects.exclude(id__in=selected_groups.values_list('id', flat=True))

             # Get the USERROLES instances related to the selected user
        
            selected_companies = selected_user.userroles_set.all()

            for user_role in selected_companies:
                selected_company = user_role.COMPANY_ID.all()

            non_selected_companies = COMPANY.objects.exclude(id__in=selected_company)

            context = {
                'selected_user': selected_user,
                'selected_groups': selected_groups,
                'non_selected_groups':non_selected_groups,
                'selected_company':selected_company,
                'non_selected_company':non_selected_companies
            }
        except Exception as e:
            context = {
                'selected_user': None,
                'selected_groups': [],
                'selected_company': [],
            }
            print("Error:", e)
        return context
    
    def post(self,request,user_id):
        try:
            form_identifier = request.POST.get('form_identifier')
            selected_user = User.objects.get(id=user_id)
            user_name = request.POST.get('user_name')
            email_address = request.POST.get('email_address')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            selected_groups = request.POST.getlist('role_list')
            selected_companies = request.POST.getlist('company_list')
            status = request.POST.get('status') == 'on'

            if form_identifier == 'update_user_form':
                try:
                    if selected_user.username != user_name:
                        pass
                    else:
                        selected_user.first_name = first_name
                        selected_user.email = email_address
                        selected_user.first_name = first_name
                        selected_user.last_name = last_name
                        selected_user.is_active = status
                        selected_user.save()

                        #Assign Group
                        selected_groups = request.POST.getlist('role_list')
                        groups = Group.objects.filter(id__in=selected_groups)
                        selected_user.groups.set(groups)

                        # Assign Companies
                        selected_companies = request.POST.getlist('company_list')
                        print(selected_companies)

                        companies = COMPANY.objects.filter(id__in=selected_companies)
                        # Check if USERROLES object already exists
                        user_roles, created = USERROLES.objects.get_or_create(USERNAME=selected_user)
                        user_roles.COMPANY_ID.set(companies)

                except Exception as e:
                    print("An error occurred:", e)
            elif form_identifier == 'delete_user_form':
                    selected_user.delete()
                    return redirect('appAUDITAI:manage-user-roles')
        except Exception as e:
            print("An error occurred:", e)

        context = self.common_data(request,user_id)
        return render(request, self.template_name, context)

class ManageUsersandRolesView(View):

    template_name = 'pages/ADMIN/manage-user-roles.html'
    
    def get(self, request):
        context = self.common_data(request)
        return render(request, self.template_name, context)
    
    def common_data(self, request):
        users = User.objects.all()  # Fetch all users
        groups = Group.objects.all()
        companies = COMPANY.objects.all()
        context = {
            'users': users,
            'groups': groups,
            'companies': companies,
        }
        return context
    
    def post(self, request):
        try:
            username = request.POST.get('user_name')
            user = User.objects.filter(username=username)
            if user.exists():
                pass
            else:
                # Create User
                new_user = User.objects.create(
                    username=username,
                    first_name=request.POST.get('first_name', ''), 
                    last_name=request.POST.get('last_name', ''), 
                    email=request.POST.get('email_address', ''), 
                    password='12345678', # This to be updated
                    is_active=False,
                )
                # Generate token for email verification
                uid = urlsafe_base64_encode(force_bytes(new_user.pk))
                token = default_token_generator.make_token(new_user)
                # Construct verification URL
                verification_url = reverse('email_verification', args=[uid, token])
                # Email subject
                subject = 'ACTION REQUIRED: Verify your AuditAI account'
                # Email body
                message = render_to_string('email/email_verification.html', {
                    'user': new_user,
                    'verification_url': request.build_absolute_uri(verification_url),
                })
                # Send email verification
                send_mail(subject, message, 'auditai-support@audit-ai.net', [new_user.email])
                # Save the user
                new_user.save()

                #Assign Group
                selected_groups = request.POST.getlist('role_list')
                groups = Group.objects.filter(id__in=selected_groups)
                new_user.groups.set(groups)

                # Assign Companies
                selected_companies = request.POST.getlist('company_list')
                companies = COMPANY.objects.filter(id__in=selected_companies)
                user_roles = USERROLES.objects.create(USERNAME=new_user)
                user_roles.COMPANY_ID.set(companies)

            context = self.common_data(request)
            return render(request, self.template_name, context)
        except:
            pass
        
def email_verification_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('verification_success',args=[uidb64, token]))
    else:
        # Verification failed, redirect to error page
        return HttpResponseRedirect(reverse('verification_error'))
    
def verification_error_view(request):
    return render(request, 'email/verification_error.html')


def validate_password(new_password):
    # Validate password strength
    special_characters = "!@#$%^&*()_+{}:<>?[];'./,\|-="
    required_pw = PASSWORDCONFIG.objects.all()
    for pw in required_pw:
        if len(new_password) >= int(pw.MIN_LENGTH):
            if any(char in special_characters for char in new_password):
                if any(char.isdigit() for char in new_password):
                    if any(char.isupper() for char in new_password):
                        if any(char.islower() for char in new_password):
                            return True
    return False

def verification_success_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            retype_password = request.POST.get('retype_password')
            if new_password != retype_password:
                error_message = "New password and retyped password do not match."
                return render(request, 'email/verification_success.html', {'uidb64': uidb64, 'token': token, 'user': user, 'error_message': error_message})
            else:
                try:
                    if validate_password(new_password):
                        # Set the new password for the user
                        user.password = make_password(new_password)
                        user.save()
                        # Redirect the user to a different page after successful password change
                        return redirect('appAUDITAI:authenticate-user')
                    else:
                        required_pw = PASSWORDCONFIG.objects.all()
                        for pw in required_pw:
                            error_message = f"The password provided does not comply with the password policy requirement (minimum of {pw.MIN_LENGTH} characters, with both upper case and lower case and at least 1 special and 1 numeric character)"
                            return render(request, 'email/verification_success.html', {'uidb64': uidb64, 'token': token, 'user': user, 'error_message': error_message})
                
                except ValidationError as e:
                    # Password validation failed, show error message
                    error_message = str(e)
                    return render(request, 'email/verification_success.html', {'uidb64': uidb64, 'token': token, 'user': user, 'error_message': error_message})

        return render(request, 'email/verification_success.html', {'uidb64': uidb64, 'token': token, 'user': user})
    else:
        # Handle the case where user or token is invalid
        pass

class ManageSecurityView(View):

    template_name = 'pages/ADMIN/manage-security.html'

    def get(self,request):
        return render(request, self.template_name)
    
class ManagePasswordView(View):
    template_name = 'pages/ADMIN/manage-passwordreq.html'

    def get(self, request):
        context = self.common_data(request)
        return render(request, self.template_name, context)
    
    def common_data(self, request):
        pw_config = PASSWORDCONFIG.objects.all() 
        context = {
            'pw_config': pw_config,
        }
        return context
    
    def post(self, request):
        length = request.POST.get('length')
        age = request.POST.get('age')
        history = request.POST.get('history')
        lockout = request.POST.get('lockout')
        lockout_duration = request.POST.get('lockout_duration')
        special_char = request.POST.get('req_specialchar') == 'on'
        upper_case = request.POST.get('req_uppercase') == 'on'
        lower_case = request.POST.get('req_lowercase') == 'on'
        numeric = request.POST.get('req_numeric') == 'on'

        # Retrieve all PASSWORDCONFIG objects
        configs = PASSWORDCONFIG.objects.all()

        # Update and save each object separately
        for config in configs:
            config.MIN_LENGTH = length
            config.AGE = age
            config.HISTORY = history
            config.LOCKOUT = lockout
            config.LOCKOUT_DURATION = lockout_duration
            config.HAS_SPECIALCHAR = special_char
            config.HAS_UPPER = upper_case
            config.HAS_LOWER = lower_case
            config.HAS_NUMERIC = numeric

            # Check if CREATED_BY field is empty
            if config.CREATED_BY != '':
                # If not empty, update LAST_MODIFIED and MODIFIED_BY
                config.LAST_MODIFIED = timezone.now()
                config.MODIFIED_BY = request.user.username
            else:
                # If empty, update only LAST_MODIFIED
                config.LAST_MODIFIED = timezone.now()
                config.CREATED_BY = request.user.username
            config.save()

        context = self.common_data(request)
        return render(request, self.template_name, context)
    
class ManageCompaniesView(View):

    template_name = 'pages/ADMIN/manage-companies.html'
    
    def get(self, request):
        context = self.common_data(request)
        return render(request, self.template_name, context)
    
    def common_data(self, request):
        companies = COMPANY.objects.all()
        context = {
            'companies':companies
        }
        return context
    
    def post(self, request):
        company_id = request.POST.get('company_id')
        company_name = request.POST.get('company_name')

        # Check if the company_id exists in the database
        try:
            company = COMPANY.objects.get(COMPANY_ID=company_id)
        except COMPANY.DoesNotExist:
            # If the company doesn't exist, create a new one
            company = COMPANY()
            company.COMPANY_ID = company_id
            company.COMPANY_NAME = company_name
            company.save()
            context = self.common_data(request)
            return render(request, self.template_name, context)
        else:
            error_message = "Company already exist."
            context = self.common_data(request)
            context['error_message'] = error_message  # Include error_message in context
            return render(request, self.template_name, context)
        
class ManageCompaniesDetailsView(View):

    template_name = 'pages/ADMIN/manage-companies-details.html'
    
    def get(self, request, comp_id):
        context = self.common_data(request,comp_id)
        return render(request, self.template_name, context)
    
    def common_data(self, request, comp_id):
        companies = COMPANY.objects.filter(id=comp_id)
        context = {
            'companies':companies,
            'comp_id':comp_id
        }
        return context
    
    def post(self, request, comp_id):
        identifier = request.POST.get('form_identifier')

        if identifier == 'update_company_form':
            print('Update Called')
            company_id = request.POST.get('company_id')
            company_name = request.POST.get('company_name')

            try:
                # Check if the company with the given ID exists
                company = COMPANY.objects.get(id=comp_id)
            except COMPANY.DoesNotExist:
                # Handle the case where the company doesn't exist
                context = {
                    'error_message': f"Company with ID {comp_id} does not exist."
                }
            else:
                # Check if the new data is different from the existing data
                if company.COMPANY_ID != company_id or company.COMPANY_NAME != company_name:
                    # Update the company's information
                    company.COMPANY_ID = company_id
                    company.COMPANY_NAME = company_name
                    company.save()
                # Always refresh the context after updating or if there are no changes
                    return redirect('appAUDITAI:manage-companies')
            
        elif identifier == 'delete_company_form':
            try:
                # Check if the company with the given ID exists
                company = COMPANY.objects.get(id=comp_id)
                # Delete the company record
                company.delete()
                return redirect('appAUDITAI:manage-companies')
            except COMPANY.DoesNotExist:
                pass
        context = self.common_data(request, comp_id)      
        return render(request, self.template_name, context)

        # Ensure that common_data() method is defined and returns the necessary data
    
        
class ManageIntegrationsView(View):

    template_name = 'pages/ADMIN/manage-integrations.html'

    def get(self,request):
        context = {

        }
        return render(request, self.template_name, context)

    
class ManageRiskandControlView(View):

    template_name = 'pages/ADMIN/manage-riskandcontrols.html'

    def get(self,request):
        context = {

        }
        return render(request, self.template_name, context)