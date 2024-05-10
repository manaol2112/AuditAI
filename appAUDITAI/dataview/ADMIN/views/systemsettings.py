from appAUDITAI.dataview.MISC.imports import *

class SystemSettingsView(AdminPermissionMixin, View):
    
    template_name = 'pages/ADMIN/system-settings.html'

    def get(self, request):
        group_exist = Group.objects.exists()
        context = {'group_exist': group_exist}
        return render(request, self.template_name, context)
    
class ManageHRRecordView(AdminPermissionMixin, View):
    template_name = 'pages/ADMIN/manage-hr-record.html'

    def get(self,request):
        try:
            companies = COMPANY.objects.all()
        except COMPANY.DoesNotExist:
            companies = None
        
        context = {
            'companies':companies
        }

        return render(request,self.template_name,context)
    
class ManageHRRecordDetailsView(AdminPermissionMixin, View):
    template_name = 'pages/ADMIN/manage-hr-record-details.html'

    def get(self,request,comp_id):
        try:
            companies = COMPANY.objects.all()
        except COMPANY.DoesNotExist:
            companies = None

        try:
            selected_company = COMPANY.objects.get(id = comp_id)
            sftp_check = HR_LIST_SFTP.objects.get(COMPANY_ID = selected_company)
        except Exception as e:
            selected_company = None
            sftp_check = None
            pass

        try:
            job_sched_check = HR_JOB_PULL.objects.get(COMPANY_ID=selected_company)
        except:
            job_sched_check = None

        context = {
            'companies':companies,
            'comp_id':comp_id,
            'sftp_check':sftp_check,
            'job_sched_check':job_sched_check
        }

        return render(request,self.template_name,context)
    
    def post(self, request, comp_id):
        form = request.POST.get('form_id')
        if form == 'hr_sftp_create_form':
            self.hr_sftp_upload(request, comp_id)
        elif form == 'hr_manual_upload':
            self.hr_manual_upload(request,comp_id)
        else:
            pass

        return self.get(request, comp_id)
    
    def parse_date(self, date_str, date_formats):
        for date_format in date_formats:
            try:
                return datetime.strptime(date_str, date_format)
            except ValueError:
                pass
        # If none of the formats match, return a default date
        return datetime(1900, 1, 1)
    
    def hr_manual_upload(self,request,comp_id):
        user = request.user
        date_formats = ["%Y-%m-%d", "%d/%m/%Y",
                                "%m/%d/%Y", "%Y%m%d", "%m/%d/%y"] 
        
        user_id_mapped = request.POST.get('user_id_mapped')
        email_mapped = request.POST.get('email_mapped')
        first_name_mapped = request.POST.get('first_name_mapped')
        last_name_mapped = request.POST.get('last_name_mapped')
        job_title_mapped = request.POST.get('job_title_mapped')
        department_mapped = request.POST.get('department_mapped')
        manager_mapped = request.POST.get('manager_mapped')
        emp_type_mapped = request.POST.get('emp_type_mapped')
        status_mapped = request.POST.get('status_mapped')
        date_hired_mapped = request.POST.get('date_hired_mapped')
        date_rehired_mapped = request.POST.get('date_rehired_mapped')
        date_revoked_mapped = request.POST.get('date_revoked_mapped')

        form = MANUAL_USER_UPLOAD_FORM(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file_name']
            # Check if the uploaded file is a CSV file
            if uploaded_file.name.endswith('.csv'):
                file_path = default_storage.save('temp/' + uploaded_file.name, uploaded_file)
                # Get the absolute file path
                absolute_file_path = default_storage.path(file_path)
                with open(absolute_file_path, 'r', encoding='utf-8-sig',newline='') as file:
                    csv_rows = csv.reader(file)
                    # Extract headers from the CSV file

                    # Clean headers to handle various newline characters
                    headers = [header.strip().replace('\r', '').replace('\n', '') for header in next(csv_rows, [])]
                    # Clean mapping variables and headers to handle whitespace and newline characters
                    user_id_mapped_cleaned = user_id_mapped.strip().replace('\r', '').replace('\n', '')
                    email_mapped_cleaned = email_mapped.strip().replace('\r', '').replace('\n', '')
                    first_name_mapped_cleaned = first_name_mapped.strip().replace('\r', '').replace('\n', '')
                    last_name_mapped_cleaned = last_name_mapped.strip().replace('\r', '').replace('\n', '')
                    job_title_mapped_cleaned = job_title_mapped.strip().replace('\r', '').replace('\n', '')
                    department_mapped_cleaned = department_mapped.strip().replace('\r', '').replace('\n', '')
                    manager_mapped_cleaned = manager_mapped.strip().replace('\r', '').replace('\n', '')
                    emp_type_mapped_cleaned = emp_type_mapped.strip().replace('\r', '').replace('\n', '')
                    status_mapped_cleaned = status_mapped.strip().replace('\r', '').replace('\n', '')
                    date_hired_mapped_cleaned = date_hired_mapped.strip().replace('\r', '').replace('\n', '')
                    date_rehired_mapped_cleaned = date_rehired_mapped.strip().replace('\r', '').replace('\n', '')
                    date_revoked_mapped_cleaned = date_revoked_mapped.strip().replace('\r', '').replace('\n', '')


                    # Get indices of mapped values in headers
                    try:
                        user_id_index = headers.index(user_id_mapped_cleaned)
                        email_index = headers.index(email_mapped_cleaned)
                        first_name_index = headers.index(first_name_mapped_cleaned)
                        last_name_index = headers.index(last_name_mapped_cleaned)
                        job_title_index = headers.index(job_title_mapped_cleaned)
                        department_index = headers.index(department_mapped_cleaned)
                        manager_index = headers.index(manager_mapped_cleaned)
                        emp_type_index = headers.index(emp_type_mapped_cleaned)
                        status_index = headers.index(status_mapped_cleaned)
                        date_hired_index = headers.index(date_hired_mapped_cleaned)
                        date_rehired_index = headers.index(date_rehired_mapped_cleaned)
                        date_revoked_index = headers.index(date_revoked_mapped_cleaned)

                    except ValueError as e:
                        print(f"Error: {e}. Mapped value not found in headers.")
                    try:
                        for row in csv_rows:
                        # Access the value in the 'USER_ID' column
                            user_id_value = row[user_id_index]
                            email_value = row[email_index]
                            first_name_value = row[first_name_index]
                            last_name_value = row[last_name_index]
                            job_title_value= row[job_title_index]
                            department_value= row[department_index]
                            manager_value= row[manager_index]
                            emp_type_value= row[emp_type_index]
                            status_value= row[status_index]

                            date_hired_value = row[date_hired_index]
                            date_hired_value = timezone.make_aware(self.parse_date(
                                        str(date_hired_value), date_formats))
                            date_rehired_value = row[date_rehired_index]
                            date_rehired_value = timezone.make_aware(self.parse_date(
                                        str(date_rehired_value), date_formats))
                            date_revoked_value = row[date_revoked_index]
                            date_revoked_value = timezone.make_aware(self.parse_date(
                                        str(date_revoked_value), date_formats))
                            
                            try:
                                selected_company = COMPANY.objects.get(id=comp_id)
                            except COMPANY.DoesNotExist:
                                selected_company = None

                            if selected_company:
                                try:
                                    hr_record, created = HR_RECORD.objects.get_or_create(COMPANY_ID = selected_company.id, USER_ID = user_id_value)
                                    hr_record.EMAIL_ADDRESS = email_value
                                    hr_record.FIRST_NAME = first_name_value
                                    hr_record.LAST_NAME = last_name_value
                                    hr_record.JOB_TITLE = job_title_value
                                    hr_record.DEPARTMENT = department_value
                                    hr_record.MANAGER = manager_value
                                    hr_record.EMP_TYPE = emp_type_value
                                    hr_record.STATUS = status_value
                                    hr_record.HIRE_DATE = date_hired_value
                                    hr_record.REHIRE_DATE = date_rehired_value
                                    hr_record.TERMINATION_DATE = date_revoked_value

                                    if created:  # Check if the record was just created
                                        hr_record.CREATED_BY = user.username
                                        hr_record.CREATED_ON = timezone.now()
                                    else:
                                        hr_record.MODIFIED_BY = user.username
                                        hr_record.LAST_MODIFIED = timezone.now()
                                    
                                    hr_record.save()  # Save the changes to the database

                                except ValueError as e:
                                    print('Error:', e)
                                except Exception as e:
                                    # Handle exceptions appropriately
                                    print("Error:", e)
                    except Exception as e:
                        print(str(e))
            else:
                return HttpResponse("Uploaded file is not a CSV.")
        else:
            return HttpResponse("Form is not valid.")
        
    def hr_sftp_upload(self,request,comp_id):
        try:
            try:
                company = COMPANY.objects.get(id=comp_id)
            except COMPANY.DoesNotExist:
                company = None

            host_name = request.POST.get('host_name')
            host_name = host_name if host_name else None

            sftp_directory = request.POST.get('sftp_directory')
            sftp_directory = sftp_directory if sftp_directory else None
            
            sftp_username = request.POST.get('sftp_username')
            sftp_username = sftp_username if sftp_username else None

            sftp_password = request.POST.get('sftp_password')
            sftp_password = sftp_password if sftp_password else None

            monday = request.POST.get('job_monday') == 'on'
            monday = monday if monday else None

            tuesday = request.POST.get('job_tuesday') == 'on'
            tuesday = tuesday if tuesday else None

            wednesday = request.POST.get('job_wednesday') == 'on'
            wednesday = wednesday if wednesday else None

            thursday = request.POST.get('job_thursday') == 'on'
            thursday = thursday if thursday else None

            friday = request.POST.get('job_friday') == 'on'
            friday = friday if friday else None

            saturday = request.POST.get('job_saturday') == 'on'
            saturday = saturday if saturday else None

            sunday = request.POST.get('job_sunday') == 'on'
            sunday = sunday if sunday else None

            job_time = request.POST.get('job_time')
            job_time = job_time if job_time else None

            user = request.user

            try:
                sftp, created = HR_LIST_SFTP.objects.get_or_create(COMPANY_ID=company)
                sftp.HOST_NAME = host_name
                sftp.SFTP_DIRECTORY = sftp_directory
                sftp.SFTP_USERNAME = sftp_username
                sftp.SFTP_PW_HASHED = sftp_password
                sftp.SETUP_COMPLETE = True
                if sftp.CREATED_BY:
                        sftp.MODIFIED_BY = user.username
                        sftp.LAST_MODIFIED = timezone.now()
                else:
                    sftp.CREATED_BY = user.username
                    sftp.CREATED_ON = timezone.now()
               
                sftp.SETUP_COMPLETE = True
                sftp.save()
                try:
                    company_id = COMPANY.objects.get(id = comp_id)
                    job, created = HR_JOB_PULL.objects.get_or_create(COMPANY_ID=company_id)
                    job.JOB_NAME = str(company_id.COMPANY_ID) + "_HR_DATA_PULL"
                    job.MONDAY = monday
                    job.TUESDAY = tuesday
                    job.WEDNESDAY = wednesday
                    job.THURSDAY = thursday
                    job.FRIDAY = friday
                    job.SATURDAY = saturday
                    job.SUNDAY = sunday
                    if job_time != 'Select time':
                        try:
                            parsed_time = timezone.datetime.strptime(job_time, '%H:%M')
                            job.SCHEDULE_TIME = parsed_time.time()
                        except ValueError:
                            error_message = "Invalid time format. Please select a valid time."
                    else:
                        job_time = parsed_time('12:00')

                    if job.CREATED_BY:
                        job.MODIFIED_BY = user.username
                        job.LAST_MODIFIED = timezone.now()
                    else:
                        job.CREATED_BY = user.username
                        job.CREATED_ON = timezone.now()
                    job.save()
                except APP_JOB_PULL.DoesNotExist:
                    job = None
                except Exception as e:
                    print('Error',str(e))

            except Exception as e:
                print('Error:',e)
    
        except:
            pass

class ManageRolesListView(AdminPermissionMixin, View):
    template_name = 'pages/ADMIN/manage-roles-view.html'
    def get(self,request):
        try:
            active_roles = Group.objects.all()
        except Group.DoesNotExist:
            active_roles = None
        role_id = 0
        context = {
            'active_roles':active_roles,
            'role_id':role_id
        }
        return render(request, self.template_name,context)
    

class ManageRolesView(AdminPermissionMixin, View):
    
    template_name = 'pages/ADMIN/manage-roles.html'

    def get(self, request, role_id):
        context = self.common_data(request, role_id)
        return render(request, self.template_name, context)
    
    def common_data(self, request, role_id):
        permissions_in_group = None
        permissions_not_in_group = None
        group = None
        if role_id:
            group = Group.objects.get(id=role_id)
            if group:
                group = group
            else:
                group = None
            permissions_in_group = group.permissions.all()
        
        else:
            permissions_in_group = []

        all_permissions = Permission.objects.all()
        permissions_not_in_group = all_permissions.exclude(id__in=[permission.id for permission in permissions_in_group])
       
        context = {
            'group':group,
            'permissions_in_group': permissions_in_group,
            'permissions_not_in_group': permissions_not_in_group
        }
        return context

    
    def post(self, request, role_id):

        form = request.POST.get('manage_role')
        permission_ids = request.POST.getlist('permissions')
        assigned_permisions = request.POST.getlist('assigned_permissions')

        if form == 'assign_role':
            try:
                role_exist = Group.objects.get(id=role_id)
                # Update permissions for existing role
                for permission_id in permission_ids:
                    try:
                        permission = Permission.objects.get(id=permission_id)
                        role_exist.permissions.add(permission)
                    except Permission.DoesNotExist:
                        # Handle the case where the permission does not exist
                        pass
            except Group.DoesNotExist:
                role_name = request.POST.get('assigned_roles')
                if role_name:
                    user_role, created = Group.objects.get_or_create(name=role_name)
                    user_role.save()
                    # Assign permissions to the default group
                    for permission_id in permission_ids:
                        try:
                            permission = Permission.objects.get(id=permission_id)
                            user_role.permissions.add(permission)
                        except Permission.DoesNotExist:
                            # Handle the case where the permission does not exist
                            pass
                else:
                    role_name = None
                    pass   
        elif form == 'remove_role':
            role_name = request.POST.get('remove_roles')
            try:
                role_exist = Group.objects.get(id=role_id)
                # Update permissions for existing role
                for permission_id in assigned_permisions:
                    try:
                        permission = Permission.objects.get(id=permission_id)
                        role_exist.permissions.remove(permission)
                    except Permission.DoesNotExist:
                        # Handle the case where the permission does not exist
                        pass
            except Group.DoesNotExist:
                pass

        else:
            pass

        return redirect('appAUDITAI:manage-roles-view')

class ManageUsersandRolesDetailsView(AdminPermissionMixin, View):
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

                        UserToken.objects.create(user=selected_user)

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

class ManageUsersandRolesView(AdminPermissionMixin, View):

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
            
        except:
            pass
        return render(request, self.template_name, context)
        
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
    try:
        required_pw = PASSWORDCONFIG.objects.all()
        for pw in required_pw:
            if len(new_password) >= int(pw.MIN_LENGTH):
                if any(char in special_characters for char in new_password):
                    if any(char.isdigit() for char in new_password):
                        if any(char.isupper() for char in new_password):
                            if any(char.islower() for char in new_password):
                                return True
                            return False
    except PASSWORDCONFIG.DoesNotExist:
        required_pw = None
        pass
   
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

class ManageSecurityView(AdminPermissionMixin, View):

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
    
class ManageCompaniesView(AdminPermissionMixin, View):

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
        
class ManageCompaniesDetailsView(AdminPermissionMixin, View):

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
    
        
class ManageIntegrationsView(AdminPermissionMixin, View):

    template_name = 'pages/ADMIN/manage-integrations.html'

    def get(self,request):
        context = {

        }
        return render(request, self.template_name, context)

    
class ManageRiskandControlView(AdminPermissionMixin, View):

    template_name = 'pages/ADMIN/manage-riskandcontrols.html'

    def get(self,request):
        context = {

        }
        return render(request, self.template_name, context)