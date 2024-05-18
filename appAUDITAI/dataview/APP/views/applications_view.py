from appAUDITAI.dataview.MISC.imports import *
from django.http import JsonResponse
from paramiko import SSHClient, AuthenticationException, SSHException
from django.core.files.storage import default_storage
from collections import Counter

class GrantTicketDetails(ProcessOwnerPermissionMixin, View):
    template_name = 'pages/APP/process-owner-granting-details.html'

    def get(self, request, request_id):
        access_request = get_object_or_404(ACCESSREQUEST, id=request_id)
        
        try:
            access_request_comments = ACCESSREQUESTCOMMENTS.objects.filter(REQUEST_ID=request_id).order_by('DATE_ADDED')

        except ACCESSREQUESTCOMMENTS.DoesNotExist:
            access_request_comments = None
            pass

        context = {
            'access_request': access_request,
            'access_request_comments':access_request_comments
        }
        return render(request, self.template_name, context)
    
    def post(self, request, request_id):
        user = request.user
        form = request.POST.get('form_id')

        if form == 'comment_form':
            comment_details = request.POST.get('request_comment')
            access_request = get_object_or_404(ACCESSREQUEST, id=request_id)
            comment = ACCESSREQUESTCOMMENTS(
                REQUEST_ID=access_request,
                CREATOR=user.email, 
                COMMENT_DETAILS=comment_details,
                DATE_ADDED=timezone.now()
            )
            comment.save()

        access_request_comments = ACCESSREQUESTCOMMENTS.objects.filter(REQUEST_ID=access_request).order_by('DATE_ADDED')

        context = {
            'access_request': access_request,
            'access_request_comments': access_request_comments
        }
        return render(request, self.template_name, context)

class AccessGranting(ProcessOwnerPermissionMixin, View):
    template_name = 'pages/APP/process-owner-granting.html'

    def get(self, request):
        user = request.user
        try:
            access_request = ACCESSREQUEST.objects.filter(ASSIGNED_TO = user.email)
        except ACCESSREQUEST.DoesNotExist:
            access_request = None
            pass
        except ObjectDoesNotExist:
            access_request = None
            pass

        try:
            approved_request_list = ACCESSREQUEST.objects.filter(
                ASSIGNED_TO=user.email
            ).exclude(
                Q(STATUS='Pending Approval') | Q(STATUS='Rejected')
            ).order_by('-DATE_REQUESTED')

            approval_count = len(approved_request_list)

        except Exception:
            pass
        context = {
            'user': user,
            'access_request':access_request,
            'approved_request_list':approved_request_list
        }
        
        return render(request, self.template_name, context)



class AppComplianceProv(ProcessOwnerPermissionMixin, View):
    template_name = 'pages/APP/process-owner-compliance-prov.html'

    def get(self, request, comp_id, app_id):
        try:
            company_name = COMPANY.objects.get(id = comp_id)
        except COMPANY.DoesNotExist:
            company_name = None

        try:
            selected_app = APP_LIST.objects.get(id = app_id)
        except COMPANY.DoesNotExist:
            selected_app = None

        current_year = timezone.now().year

        try:
            new_roles = APP_RECORD.objects.filter(APP_NAME = selected_app, DATE_GRANTED__year = current_year )
        except APP_RECORD.DoesNotExist:
            new_roles = None

        try:
            no_approval_list = []
            late_approval_set = set()  # Using a set to store unique late approvals
            for role in new_roles:
                approval = ACCESSREQUEST.objects.filter(REQUESTOR=role.EMAIL_ADDRESS, ROLES=role.ROLE_NAME)
                if not approval.exists():
                    no_approval_list.append(role)  # Append role to the list if no approval exists
                else:
                    for approve in approval:
                        if approve.DATE_APPROVED is not None and role.DATE_GRANTED is not None:
                            if approve.DATE_APPROVED > role.DATE_GRANTED:
                                late_approval_set.add(role)
                                
                                
                                
                                
                                 # Add role to the set if it's a unique late approval
                        # Handle the case where one or both DATE_APPROVED values are None
                        else:
                            # Add handling logic here if needed
                            pass
        except AttributeError:
            # Handle the case where new_roles is None or has no attribute DATE_APPROVED
            pass

        no_approval_list = sorted(no_approval_list, key=lambda role: role.DATE_GRANTED, reverse=True)
        no_approval_count = len(no_approval_list)
        late_approval_count = len(late_approval_set)  # Count of unique late approvals


        context = {
            'comp_id':comp_id,
            'app_id':app_id,
            'company_name':company_name,
            'selected_app':selected_app,
            'no_approval_list':no_approval_list,
            'no_approval_count':no_approval_count,
            'late_approval_list':late_approval_set,
            'late_approval_count':late_approval_count
        }
        return render(request,self.template_name, context)

        

class AppComplianceAuth(ProcessOwnerPermissionMixin,View):
    template_name = 'pages/APP/process-owner-compliance-auth.html'

    def get(self,request, comp_id, app_id):
        try:
            company_name = COMPANY.objects.get(id = comp_id)
        except COMPANY.DoesNotExist:
            company_name = None

        try:
            selected_app = APP_LIST.objects.get(id = app_id)
        except COMPANY.DoesNotExist:
            selected_app = None
            pass

        try:
            pw_configured = PASSWORD.objects.get(APP_NAME = selected_app)
        except PASSWORD.DoesNotExist:
            pw_configured = None
            pass

        try: 
            pw_policy = PASSWORDPOLICY.objects.get(COMPANY_ID = comp_id)
        except PASSWORDPOLICY.DoesNotExist:
            pw_policy = None
            pass

        if pw_policy.LENGTH <= pw_configured.LENGTH and pw_policy.AGE >= pw_configured.AGE and pw_policy.HISTORY <= pw_configured.HISTORY and pw_policy.LOCKOUT_ATTEMPT >= pw_configured.LOCKOUT_ATTEMPT and pw_policy.LOCKOUT_DURATION <= pw_configured.LOCKOUT_DURATION and pw_policy.SPECIAL_CHAR == pw_configured.SPECIAL_CHAR and pw_policy.UPPER and pw_configured.UPPER and pw_policy.LOWER == pw_configured.LOWER and pw_policy.NUMBER == pw_configured.NUMBER and pw_policy.MFA_ENABLED == pw_configured.MFA_ENABLED:
            auth_compliant = 'Yes'
        else:
            auth_compliant = 'No'

        context = {
            'comp_id':comp_id,
            'app_id':app_id,
            'company_name':company_name,
            'selected_app':selected_app,
            'pw_configured':pw_configured,
            'pw_policy':pw_policy,
            'auth_compliant':auth_compliant
        }
        return render(request,self.template_name, context)


class AppListByCompany(ProcessOwnerPermissionMixin,View):
    template_name = 'pages/APP/processowner-company.html'

    def get(self, request):
        active_user = request.user
        user_roles = USERROLES.objects.filter(USERNAME=active_user)
        for user_role in user_roles:
            company_ids = user_role.COMPANY_ID.all()
            for company_id in company_ids:
                context = {
                    'company_ids':company_ids
                }
        return render(request, self.template_name, context)

class ApplistByProcessOwner(ProcessOwnerPermissionMixin, View):
    template_name = 'pages/APP/processowner-applist.html'

    def get(self, request,comp_id):
        context = self.common_data(request,comp_id)
        return render(request, self.template_name, context)

    def common_data(self, request, comp_id):
        user = request.user
        app = APP_LIST.objects.filter(APPLICATION_OWNER=user, COMPANY_ID=comp_id)
        process_owner_group_name = "Process Owner"
        app_owners = User.objects.filter(
            is_active=True, groups__name=process_owner_group_name)
        company_name = COMPANY.objects.get(id=comp_id)
        context = {
            'app_owners': app_owners,
            'app': app,
            'comp_id':comp_id,
            'company_name':company_name
        }
        return context

    def post(self, request, comp_id):

        app_name = request.POST.get('app_name')
        app_type = request.POST.get('app_type')
        hosting = request.POST.get('hosting')
        risk_rating = request.POST.get('risk_rating')
        relevant_process = request.POST.get('relevant_process')
        date_implemented = request.POST.get('date_implemented')
        app_list_app_owner1 = request.POST.get('app_list_app_owner1')
        auth_type = request.POST.get('auth_type')
        company = COMPANY.objects.filter(id = comp_id)
        app_owner = User.objects.get(id = app_list_app_owner1)

        new_app, created = APP_LIST.objects.get_or_create(APP_NAME=app_name, COMPANY_ID = company.first())
        new_app.COMPANY_ID = company.first()
        new_app.APP_NAME = app_name
        new_app.APP_TYPE = app_type
        new_app.HOSTED = hosting
        new_app.RISKRATING = risk_rating
        new_app.RELEVANT_PROCESS = relevant_process
        new_app.APPLICATION_OWNER = app_owner
        new_app.AUTHENTICATION_TYPE = auth_type
        new_app.DATE_IMPLEMENTED = date_implemented
        new_app.save()

        context = self.common_data(request, comp_id)
        return render(request, self.template_name, context)
    

def test_sftp_connection(request):
    if request.method == 'POST':
        # Retrieve POST data
        host_name = request.POST.get('host_name')
        sftp_directory = request.POST.get('sftp_directory')
        sftp_username = request.POST.get('sftp_username')
        sftp_password = request.POST.get('sftp_password')
        
        try:
            # Establish SFTP connection
            transport = paramiko.Transport((host_name, 22))
            transport.connect(username=sftp_username, password=sftp_password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.close()
            transport.close()
            return JsonResponse({'success': True})
        except AuthenticationException:
            return JsonResponse({'success': False, 'error': 'Authentication failed'})
        except SSHException as e:
            return JsonResponse({'success': False, 'error': str(e)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        finally:
            # Ensure connections are closed
            try:
                if sftp:
                    sftp.close()
            except:
                pass
            try:
                if transport:
                    transport.close()
            except:
                pass
            
    # Return error if request method is not POST
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)



class SetupNewAppView(ProcessOwnerPermissionMixin,View):
    template_name = 'pages/APP/processowner-setupnewapp.html'

    def get(self,request,comp_id,app_id):
        context = self.common_data(request, comp_id, app_id)
        return render(request, self.template_name, context)

    def common_data(self, request,comp_id,app_id):
        try:
            try: 
                company_name = COMPANY.objects.get(id=comp_id)
            except COMPANY.DoesNotExist:
                company_name = None
            try:
                selected_app = APP_LIST.objects.get(id=app_id)
            except APP_LIST.DoesNotExist:
                selected_app = None
            try:
                pw_check = PASSWORD.objects.get(APP_NAME = selected_app)
            except PASSWORD.DoesNotExist:
                pw_check = None
            try:
                sftp_check = APP_USER_SFTP.objects.get(APP_NAME=selected_app)
            except APP_USER_SFTP.DoesNotExist:
                sftp_check = None  
            try:
                job_sched_check = APP_JOB_PULL.objects.get(APP_NAME=selected_app)
            except:
                job_sched_check = None

            try: 
                selected_admins = ADMIN_ROLES_FILTER.objects.filter(APP_NAME=selected_app)
                unique_role_names = APP_RECORD.objects.filter(APP_NAME=selected_app).exclude(
                    Q(ROLE_NAME__in=selected_admins.values_list('ROLE_NAME', flat=True))
                ).values_list('ROLE_NAME', flat=True).distinct()
                    
            except ADMIN_ROLES_FILTER.DoesNotExist:
                selected_admins = None
                # Handle the case where selected_admins doesn't exist
            except ADMIN_ROLES_FILTER.DoesNotExist:
                selected_groups = None
                # Handle the case where selected_groups doesn't exist
            try:
                prov_policy = PROVISIONINGPOLICY.objects.get(APP_NAME = selected_app)
            except PROVISIONINGPOLICY.DoesNotExist:
                prov_policy = None

            try: 
                termed_policy = TERMINATIONPOLICY.objects.get(APP_NAME = selected_app)
            except TERMINATIONPOLICY.DoesNotExist:
                termed_policy = None
            form = None
            try:
                form = MANUAL_USER_UPLOAD_FORM()
            except:
                pass

            context = {
                'comp_id':comp_id,
                'app_id':app_id,
                'company_name':company_name,
                'selected_app':selected_app,
                'pw_check':pw_check,
                'sftp_check':sftp_check,
                'job_sched_check':job_sched_check,
                'unique_role_names':unique_role_names,
                'prov_policy':prov_policy,
                'termed_policy':termed_policy,
                'selected_admins':selected_admins,
                'form':form

            }
            return context
    
        except ObjectDoesNotExist as e:
            print("Object does not exist:", e)
            
            return None
        except Exception as e:
            print("Exception type:", type(e).__name__,e)
    
    def post(self, request, comp_id,app_id):
        try:
            form = request.POST.get('form_id')
            if form == 'password_create_form':
                self.password_create(request, comp_id, app_id)
            elif form == 'sftp_create_form':
                print('sftp_form')
                self.sfpt_create(request, comp_id,app_id)
            elif form == 'policy_create_form':
                self.access_policy_create(request, comp_id,app_id)
            elif form == 'manual_user_upload_form':
                self.process_manual_upload(request, comp_id,app_id)
            elif form =='review_setup_form':

                try:
                    pw_check = PASSWORD.objects.get(APP_NAME = app_id)
                except PASSWORD.DoesNotExist:
                    pw_check = None
                except Exception:
                    pass

                try: 
                    sftp_check = APP_USER_SFTP.objects.get(APP_NAME = app_id)
                except APP_USER_SFTP.DoesNotExist:
                    sftp_check = None
                except Exception:
                    pass

                try:
                    policy_check = PROVISIONINGPOLICY.objects.get(APP_NAME = app_id)
                except PROVISIONINGPOLICY.DoesNotExist:
                    policy_check = None
                except Exception:
                    pass

                if pw_check.SETUP_COMPLETE == True and sftp_check.SETUP_COMPLETE == True and policy_check.SETUP_COMPLETE == True:
                     selected_app = APP_LIST.objects.get(id=app_id)
                     selected_app.SETUP_COMPLETE =  True
                     selected_app.save()
                     return redirect('appAUDITAI:applist-process-owner', comp_id)
                else:
                    print('You are not able to finish this yet')
        
        except ValueError as e:
            print('Error:Value Error',e)
        except Exception as e:
            print(str(e))

        context = self.common_data(request, comp_id, app_id)
        return render(request, self.template_name, context)
    
    def parse_date(self, date_str, date_formats):
        for date_format in date_formats:
            try:
                return datetime.strptime(date_str, date_format)
            except ValueError:
                pass
        # If none of the formats match, return a default date
        return datetime(1900, 1, 1)

    
    def process_manual_upload(self, request, comp_id, app_id):
        user = request.user
        date_formats = ["%Y-%m-%d", "%d/%m/%Y",
                                "%m/%d/%Y", "%Y%m%d", "%m/%d/%y"] 

        user_id_mapped = request.POST.get('user_id_mapped')
        email_mapped = request.POST.get('email_mapped')
        first_name_mapped = request.POST.get('first_name_mapped')
        last_name_mapped = request.POST.get('last_name_mapped')
        roles_mapped = request.POST.get('roles_mapped')
        status_mapped = request.POST.get('status_mapped')
        date_granted_mapped = request.POST.get('date_granted_mapped')
        date_revoked_mapped = request.POST.get('date_revoked_mapped')
        last_login_mapped = request.POST.get('last_login_mapped').strip().replace('\r\n', '')
    

        form = MANUAL_USER_UPLOAD_FORM(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file_name']
            # Check if the uploaded file is a CSV file
            if uploaded_file.name.endswith('.csv'):
                # Save the uploaded file temporarily
                file_path = default_storage.save('temp/' + uploaded_file.name, uploaded_file)
                # Get the absolute file path
                absolute_file_path = default_storage.path(file_path)
                # Process the CSV file
                with open(absolute_file_path, 'r', encoding='utf-8-sig') as file:
                    csv_rows = csv.reader(file)
                    # Extract headers from the CSV file

                    headers = [header.strip().replace('\r\n', '') for header in next(csv_rows, [])]

                    # Get indices of mapped values in headers
                    try:
                        user_id_index = headers.index(user_id_mapped)
                        email_index = headers.index(email_mapped)
                        first_name_index = headers.index(first_name_mapped)
                        last_name_index = headers.index(last_name_mapped)
                        roles_index = headers.index(roles_mapped)
                        status_index = headers.index(status_mapped)
                        date_granted_index = headers.index(date_granted_mapped)
                        date_revoked_index = headers.index(date_revoked_mapped)
                        last_login_index = headers.index(last_login_mapped)
                    except ValueError as e:
                        print(f"Error: {e}. Mapped value not found in headers.")


                    for row in csv_rows:
                        # Access the value in the 'USER_ID' column
                        user_id_value = row[user_id_index]
                        email_value = row[email_index]
                        first_name_value = row[first_name_index]
                        last_name_value = row[last_name_index]
                        roles_value = row[roles_index]
                        status_value = row[status_index]
                        
                        date_granted_value = row[date_granted_index]
                        date_granted_value = timezone.make_aware(self.parse_date(
                                    str(date_granted_value), date_formats))
                        date_revoked_value = row[date_revoked_index]
                        date_revoked_value = timezone.make_aware(self.parse_date(
                                    str(date_revoked_value), date_formats))
                        last_login_value = row[last_login_index]
                        last_login_value = timezone.make_aware(self.parse_date(
                                    str(last_login_value), date_formats))
                        
                        try:
                            selected_app = APP_LIST.objects.get(id=app_id)
                        except APP_LIST.DoesNotExist:
                            selected_app = None
                        
                        if selected_app:
                            try:
                                app_record, created = APP_RECORD.objects.get_or_create(APP_NAME=selected_app,USER_ID = user_id_value, EMAIL_ADDRESS = email_value)
                                app_record.FIRST_NAME = first_name_value
                                app_record.LAST_NAME = last_name_value
                                app_record.ROLE_NAME = roles_value
                                app_record.STATUS = status_value
                                app_record.DATE_GRANTED = date_granted_value
                                app_record.DATE_REVOKED = date_revoked_value
                                app_record.LAST_LOGIN = last_login_value

                                if created:  # Check if the record was just created
                                    app_record.CREATED_BY = user.username
                                    app_record.CREATED_ON = timezone.now()
                                else:
                                    app_record.MODIFIED_BY = user.username
                                    app_record.LAST_MODIFIED = timezone.now()
                                
                                app_record.save()  # Save the changes to the database

                               
                            except ValueError as e:
                                print('Error:', e)
                            except Exception as e:
                                # Handle exceptions appropriately
                                print("Error:", e)
                    sftp, created = APP_USER_SFTP.objects.get_or_create(APP_NAME = selected_app)
                    sftp.SETUP_COMPLETE = True
                    sftp.save()
                            
                    # Further processing...
                    # Return a response or perform any necessary action
                    return HttpResponse("CSV file processed successfully.")
            else:
                return HttpResponse("Uploaded file is not a CSV.")
        else:
            return HttpResponse("Form is not valid.")
    
    def access_policy_create(self,request,comp_id,app_id):
        #ACCESS PROVISIONING POLICY
        user = request.user
        prov_approval = request.POST.get('access_approval_confirm') 
        if prov_approval == 'Yes':
            req_approval = True
        else:
            req_approval = False
        prov_rationale = request.POST.get('approval_rationale')
        manager_approval = request.POST.get('access_approval') == 'manager'
        it_approval = request.POST.get('access_approval') == 'it'
        both_approval = request.POST.get('access_approval') == 'both'
        try:
            selected_app = APP_LIST.objects.get(id=app_id)
            if selected_app:
                try:
                    policy,created = PROVISIONINGPOLICY.objects.get_or_create(APP_NAME=selected_app)
                    policy.REQ_APPROVAL = req_approval
                    if prov_rationale:
                        policy.REQ_APPROVAL_RATIONALE = prov_rationale
                    if manager_approval:
                        policy.MANAGER_APPROVAL =  True
                        policy.IT_APPROVAL =  False
                        policy.BOTH_MANAGER_IT =  False
                    elif it_approval:
                        policy.IT_APPROVAL = True
                        policy.MANAGER_APPROVAL =  False
                        policy.BOTH_MANAGER_IT =  False
                    elif both_approval:
                        policy.BOTH_MANAGER_IT = True
                        policy.MANAGER_APPROVAL =  False
                        policy.IT_APPROVAL =  False

                    if policy.CREATED_BY:
                        policy.MODIFIED_BY = user.username
                    else:
                        policy.CREATED_BY = user.username
                    
                    if policy.CREATED_ON:
                        policy.LAST_MODIFIED = timezone.now()
                    else:
                        policy.CREATED_ON = timezone.now()
                    policy.SETUP_COMPLETE = True

                    policy.save()

                except PROVISIONINGPOLICY.DoesNotExist:
                    policy = None
                    pass
                except Exception as e:
                    print(str(e))
               

            termed_days = request.POST.get('termed_days')
            if termed_days:
                termed_days = termed_days
            else:
                termed_days = None

            who_notify_hr = request.POST.get('who_notify') == 'hr'
            who_notify_manager = request.POST.get('who_notify') == 'manager'
            who_notify_automated = request.POST.get('who_notify') == 'automated'

            notify_via_email = request.POST.get('how_notify') == 'email'
            notify_via_verbal = request.POST.get('how_notify') == 'verbal'
            notify_via_automated = request.POST.get('how_notify') == 'automated'

            try:
                termed_policy, created = TERMINATIONPOLICY.objects.get_or_create(APP_NAME = selected_app)
                termed_policy.APP_NAME = selected_app
                termed_policy.DAYS_TO_TERMINATE = termed_days
                
                if who_notify_hr:
                    termed_policy.WHO_NOTIFY_HR = True
                    termed_policy.WHO_NOTIFY_MANAGER = False
                    termed_policy.WHO_NOTIFY_AUTOMATED = False
                elif who_notify_manager:
                    termed_policy.WHO_NOTIFY_HR = False
                    termed_policy.WHO_NOTIFY_MANAGER = True
                    termed_policy.WHO_NOTIFY_AUTOMATED = False
                elif who_notify_automated:
                    termed_policy.WHO_NOTIFY_HR = False
                    termed_policy.WHO_NOTIFY_MANAGER = False
                    termed_policy.WHO_NOTIFY_AUTOMATED = True
                if notify_via_email:
                    termed_policy.HOW_NOTIFY_EMAIL = True
                    termed_policy.HOW_NOTIFY_VERBAL = False
                    termed_policy.HOW_NOTIFY_AUTOMATED = False
                elif notify_via_verbal:
                    termed_policy.HOW_NOTIFY_EMAIL = False
                    termed_policy.HOW_NOTIFY_VERBAL = True
                    termed_policy.HOW_NOTIFY_AUTOMATED = False
                elif notify_via_automated:
                    termed_policy.HOW_NOTIFY_EMAIL = False
                    termed_policy.HOW_NOTIFY_VERBAL = False
                    termed_policy.HOW_NOTIFY_AUTOMATED = True

                if termed_policy.CREATED_BY:
                        termed_policy.MODIFIED_BY = user.username
                else:
                        termed_policy.CREATED_BY = user.username
                    
                if termed_policy.CREATED_ON:
                        termed_policy.LAST_MODIFIED = timezone.now()
                else:
                        termed_policy.CREATED_ON = timezone.now()

            except TERMINATIONPOLICY.DoesNotExist:
                termed_policy = None
                pass
            except Exception as e:
                print(str(e))
            termed_policy.save()

            try:
                admin_list = request.POST.getlist('admin_role_list_2')
            except ValueError as e:
                admin_list = []

            try:
                for admin in admin_list:
                    admin_roles, created = ADMIN_ROLES_FILTER.objects.get_or_create(
                    APP_NAME=selected_app, ROLE_NAME = admin)
                    admin_roles.ROLE_NAME = admin
                    admin_roles.SETUP_COMPLETE = True
                    if admin_roles.CREATED_BY:
                            admin_roles.MODIFIED_BY = user.username
                    else:
                            admin_roles.CREATED_BY = user.username
                        
                    if admin_roles.CREATED_ON:
                            admin_roles.LAST_MODIFIED = timezone.now()
                    else:
                            admin_roles.CREATED_ON = timezone.now()
                    
                    admin_roles.save()

                # Delete admin roles not in the admin_list
                existing_admin_roles = ADMIN_ROLES_FILTER.objects.filter(APP_NAME=selected_app)
                existing_role_names = set(existing_admin_roles.values_list('ROLE_NAME', flat=True))
                roles_to_delete = existing_role_names - set(admin_list)
                existing_admin_roles.filter(ROLE_NAME__in=roles_to_delete).delete()

            except ADMIN_ROLES_FILTER.DoesNotExist:
                admin_roles = None
                pass

        except APP_LIST.DoesNotExist as e:
            selected_app = None
            pass
        except Exception as e:
            print(str(e))

    def sfpt_create(self, request, comp_id,app_id):
        try:
            try:
                selected_app = APP_LIST.objects.get(id=app_id)
            except APP_LIST.DoesNotExist:
                selected_app = None

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
                sftp, created = APP_USER_SFTP.objects.get_or_create(id=selected_app.id)
                sftp.APP_NAME = selected_app
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
                    job, created = APP_JOB_PULL.objects.get_or_create(APP_NAME=selected_app)
                    job.JOB_NAME = str(sftp.APP_NAME) + "_USER_DATA_PULL"
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
                        job.SCHEDULE_TIME = '12:00'  

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
    
    def password_create(self, request, comp_id, app_id):
        try:
            auth_method = request.POST.get('authentication_method')
            auth_method = auth_method if auth_method else None

            pw_age = request.POST.get('length')
            pw_age = int(pw_age) if pw_age else None

            pw_length = request.POST.get('age')
            pw_length = int(pw_length) if pw_length else None

            pw_history = request.POST.get('history')
            pw_history = int(pw_history) if pw_history else None

            pw_lockout = request.POST.get('lockout')
            pw_lockout = int(pw_lockout) if pw_lockout else None

            pw_lockout_duration = request.POST.get('lockout_duration')
            pw_lockout_duration = int(pw_lockout_duration) if pw_lockout_duration else None

            pw_req_specialchar = request.POST.get('req_specialchar') == 'on'
            pw_req_uppercase = request.POST.get('req_uppercase') == 'on'
            pw_req_lowercase = request.POST.get('req_lowercase') == 'on'
            pw_req_numeric = request.POST.get('req_numeric') == 'on'
            pw_req_mfa = request.POST.get('req_mfa') == 'on'

            user = request.user

            if auth_method == "sso":

                selected_app = APP_LIST.objects.get(id=app_id)
                app, created = PASSWORD.objects.get_or_create(id=selected_app.id)
                app.MFA_ENABLED = pw_req_mfa
                app.AUTH_METHOD = auth_method
                app.SETUP_COMPLETE = True

                if app.CREATED_BY:
                    app.MODIFIED_BY = request.user
                    app.LAST_MODIFIED = timezone.now()
                else:
                    app.CREATED_BY = request.user
                    app.CREATED_ON = timezone.now()

                app.save()

            elif auth_method == "native" or auth_method == "bothssonative":
                try:
                    selected_app = APP_LIST.objects.get(id=app_id)
                    app, created = PASSWORD.objects.get_or_create(id=selected_app.id)
                    app.APP_NAME = selected_app
                    app.LENGTH = pw_length 
                    app.AGE = pw_age
                    app.HISTORY = pw_history
                    app.LOCKOUT_ATTEMPT = pw_lockout
                    app.LOCKOUT_DURATION = pw_lockout_duration
                    app.SPECIAL_CHAR = pw_req_specialchar
                    app.UPPER = pw_req_uppercase
                    app.LOWER = pw_req_lowercase
                    app.NUMBER = pw_req_numeric
                    app.MFA_ENABLED = pw_req_mfa
                    app.AUTH_METHOD = auth_method
                    app.SETUP_COMPLETE = True

                    if app.CREATED_BY:
                        app.MODIFIED_BY = user.username
                        app.LAST_MODIFIED = timezone.now()
                    else:
                        app.CREATED_BY = user.username
                        app.CREATED_ON = timezone.now()

                    app.save()
                except APP_LIST.DoesNotExist as e:
                    print('Error:Record does not exist',str(e))
                except Exception as e:
                    print(str(e))
            else:
                messages.error(request, 'Authentication method is required. Please select from the available options below.')
                context = self.common_data(request, comp_id, app_id)
                return render(request, self.template_name, context)
        except:
            print(str(e))

class AppdetailsByProcessOwner(ProcessOwnerPermissionMixin, View):
    
    template_name = 'pages/APP/processowner-appdetails.html'

    def common_data(self, request, comp_id, app_id):
        user = request.user
        app = APP_LIST.objects.filter(APPLICATION_OWNER=user)
        selected_app = APP_LIST.objects.get(id=app_id)
        password_exist = PASSWORD.objects.filter(APP_NAME=selected_app.id)
        attachment = PWCONFIGATTACHMENTS.objects.filter(
            APP_NAME=selected_app.id, activated=True).first()
        file_path_relative = attachment.file_name.url if attachment and attachment.file_name and attachment.file_name.url else '/media/pwconfigs/default.png'
        form = PWCONFIG_MODELFORM()
        user_upload_form = APP_USER_UPLOAD_FORM()
        app_users = APP_RECORD.objects.filter(APP_NAME=selected_app).values(
            'USER_ID', 'EMAIL_ADDRESS', 'STATUS').distinct().order_by('STATUS', 'EMAIL_ADDRESS')
        company_name = COMPANY.objects.get(id=comp_id)
        context = {
            'app': app,
            'app_users': app_users,
            'selected_app': selected_app,
            'form': form,
            'password_exist': password_exist,
            'file_path': file_path_relative,
            'user_upload_form': user_upload_form,
            'comp_id':comp_id,
            'company_name':company_name
        }
        return context

    def get(self, request, comp_id, app_id):
        selected_app = APP_LIST.objects.get(id=app_id)
        try:
            if selected_app.SETUP_COMPLETE: 
                context = self.common_data(request, comp_id, app_id)
            else:
                context = self.common_data(request, comp_id, app_id)
                return redirect('appAUDITAI:setup-new-app',comp_id,app_id)
        except AttributeError as e:  # Handle the case when the selected_app doesn't exist
            print('Attribute Error',e)
        except ValueError as e:
            print('Value Error:',e)
 
        # If the code reaches here, render the template with no context
        return render(request, self.template_name, context)

        
    def post(self, request, comp_id, app_id):
        # Check if it's an AJAX request
        is_ajax_request = request.POST.get('is_ajax_request', None)
        if is_ajax_request == 'true':
            return self.pw_to_image(request, comp_id, app_id)
        else:
            form_id = request.POST.get('form_id')
            if form_id == 'pw_attachment_upload_form':
                return self.save_pwconfig(request, comp_id, app_id)
            elif form_id == 'app_user_upload_form':
                return self.upload_app_user(request, comp_id, app_id)

    def upload_app_user(self, request, comp_id, app_id):
        user = request.user
        form = APP_USER_UPLOAD_FORM(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['file_name'].name != 'AUDITAI_USER_UPLOAD_CSV.csv':
                return JsonResponse({'error': 'The attached file is invalid. Make sure to use the template provided to avoid receiving this error.'})
            else:
                form.save()
                form = APP_USER_UPLOAD_FORM()
                obj = APP_USER_UPLOAD.objects.get(activated=False)
                date_formats = ["%Y-%m-%d", "%d/%m/%Y",
                                "%m/%d/%Y", "%Y%m%d", "%m/%d/%y"]
                with open(obj.file_name.path, 'r') as f:
                    reader = csv.reader(f)
                    header = next(reader)
                    header = [field.strip('\ufeff') for field in header]
                    expected_fields = ['USER_ID', 'EMAIL_ADDRESS', 'FIRST_NAME', 'LAST_NAME',
                                       'ROLE_NAME', 'STATUS', 'DATE_GRANTED', 'DATE_REVOKED', 'LAST_LOGIN']
                    missing_fields = [
                        field for field in expected_fields if field not in header]
                    if missing_fields:
                        obj.delete()
                        return JsonResponse({'error': 'Missing field(s) in the attached template: {}'.format(', '.join(missing_fields))})
                    else:
                        for i, row in enumerate(reader):
                            DATE_GRANTED = row[6]
                            DATE_REVOKED = row[7]
                            LAST_LOGIN = row[8]
                            if not DATE_GRANTED:
                                # Assign a default date, e.g., January 1, 1990
                                DATE_GRANTED = datetime(1900, 1, 1)
                            else:
                                DATE_GRANTED = self.parse_date(
                                    str(DATE_GRANTED), date_formats)
                            if not DATE_REVOKED:
                                DATE_REVOKED = datetime(1900, 1, 1)
                            else:
                                DATE_REVOKED = self.parse_date(
                                    str(DATE_REVOKED), date_formats)
                            if not LAST_LOGIN:
                                LAST_LOGIN = datetime(1900, 1, 1)
                            else:
                                LAST_LOGIN = self.parse_date(
                                    str(LAST_LOGIN), date_formats)

                            app_name = request.POST['selected_app']
                            app_list_instance = APP_LIST.objects.get(
                                id=app_name)

                            user_record_data = {
                                'APP_NAME': app_list_instance,
                                'USER_ID': row[0],
                                'EMAIL_ADDRESS': row[1],
                                'FIRST_NAME': row[2],
                                'LAST_NAME': row[3],
                                'ROLE_NAME': row[4],
                                'STATUS': row[5],
                                'DATE_GRANTED': DATE_GRANTED,
                                'DATE_REVOKED': DATE_REVOKED,
                                'LAST_LOGIN': LAST_LOGIN,
                                'CREATED_BY': user.username,
                                'CREATED_ON': timezone.now()
                            }
                            user_record, created = APP_RECORD.objects.get_or_create(
                                APP_NAME=app_list_instance,
                                USER_ID=row[0],
                                EMAIL_ADDRESS=row[1],
                                ROLE_NAME=row[4],
                                defaults=user_record_data  # Data to update or create
                            )

                            # If the record already existed, update its fields
                            if not created:
                                for field, value in user_record_data.items():
                                    setattr(user_record, field, value)
                                user_record.MODIFIED_BY = user.username
                                user_record.LAST_MODIFIED = timezone.now()
                                user_record.save()
                        obj.activated = True
                        obj.save()

                        if obj.activated:
                            return HttpResponseRedirect(request.path_info)
                        else:
                            obj.delete()
        else:
            return JsonResponse({'error': 'Invalid form data'})

        context = self.common_data(request,  comp_id, app_id)
        return render(request, self.template_name, context)

    def parse_date(self, date_str, date_formats):
        for date_format in date_formats:
            try:
                return datetime.strptime(date_str, date_format)
            except ValueError:
                pass
        # If none of the formats match, return a default date
        return datetime(1900, 1, 1)

    def pw_to_image(self, request, comp_id, app_id):
        template_name = 'pages/APP/processowner-appdetails.html'
        form = PWCONFIG_MODELFORM(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file_name']
            try:
                img = Image.open(uploaded_file)
            except (OSError, ValueError):
                return HttpResponse("Invalid image file")
            try:
                text = pytesseract.image_to_string(img, lang='eng')

                # Define a regular expression for extracting numbers between "age" and "days"
                max_history = re.compile(
                    r'p(?:a{0,3})s(?:s{0,3})w(?:o{0,3})r(?:d{0,3})\sh(?:i{0,3})s(?:t{0,3})o(?:r{0,3})y\s*(\d+)', re.IGNORECASE)
                max_pw_age = re.compile(
                    r'.*?M(?:a{0,3})x(?:i{0,3})m(?:u{0,3})m(?:\s*|\s*)p(?:a{0,3})s(?:s{0,3})w(?:o{0,3})r(?:d{0,3})\s*a(?:g{0,3})e(?:\s*|\s*)(\d+)\s*d(?:a{0,3})y(?:s{0,3}).*?', re.IGNORECASE)
                min_pw_age = re.compile(
                    r'.*?M(?:i{0,3})n(?:i{0,3})m(?:u{0,3})m(?:\s*|\s*)p(?:a{0,3})s(?:s{0,3})w(?:o{0,3})r(?:d{0,3})\s*a(?:g{0,3})e(?:\s*|\s*)(\d+)\s*d(?:a{0,3})y(?:s{0,3}).*?', re.IGNORECASE)
                pw_length = re.compile(
                    r'.*?M(?:i{0,3})n(?:i{0,3})m(?:u{0,3})m(?:\s*|\s*)p(?:a{0,3})s(?:s{0,3})w(?:o{0,3})r(?:d{0,3})\s*l(?:e{0,3})n(?:g{0,3})t(?:h{0,3})\s*(\d+)\s*c(?:h{0,3})a{0,3}r(?:a{0,3})c(?:t{0,3})e{0,3}r{0,3}s{0,3}.*?', re.IGNORECASE)

                # Search for matches using the regular expression
                max_history_pw_match = max_history.search(text)
                max_age_match = max_pw_age.search(text)
                min_age_match = min_pw_age.search(text)
                min_pw_length_match = pw_length.search(text)

                # Assign the extracted number and matched text to variables
                max_history_pw = max_history_pw_match.group(
                    1) if max_history_pw_match else ''
                extract_max_pw_age = max_age_match.group(
                    1) if max_age_match else ''
                extract_min_pw_age = min_age_match.group(
                    1) if min_age_match else ''
                extract_pw_length = min_pw_length_match.group(
                    1) if min_pw_length_match else ''

                response_content = (
                    f"Password History: {max_history_pw}\n"
                    f"Maximum Password Age: {extract_max_pw_age}\n"
                    f"Minimum Password Age: {extract_min_pw_age}\n"
                    f"Minimum Password Length: {extract_pw_length}"
                )
                response = HttpResponse(
                    content=response_content, content_type='text/plain')
                return HttpResponse(response)
            except pytesseract.TesseractError as e:
                return HttpResponse(f"Tesseract Error: {e}")
        context = self.common_data(request, comp_id, app_id)
        return render(request, self.template_name, context)

    def save_pwconfig(self, request, comp_id, app_id):
        form = PWCONFIG_MODELFORM(request.POST, request.FILES)
        if form.is_valid():
            APP_NAME = APP_LIST.objects.get(id=app_id)
            selected_app, created = PASSWORD.objects.get_or_create(
                APP_NAME=APP_NAME)
            # ASSIGN THE VALUE TO THE PASSWORD CONFIGURATION FIELD
            selected_app.APP_NAME = APP_NAME    
            selected_app.COMPLEXITY_ENABLED = bool(
                request.POST.get('pass_complexity', False))
            selected_app.LENGTH = int(request.POST.get('pass_length', 0))
            selected_app.UPPER = 'upper_case' in request.POST
            selected_app.LOWER = 'lower_case' in request.POST
            selected_app.NUMBER = 'number' in request.POST
            selected_app.SPECIAL_CHAR = 'special_character' in request.POST
            selected_app.AGE = int(request.POST.get('pass_age', 0))
            selected_app.HISTORY = int(request.POST.get('pass_history', 0))
            selected_app.LOCKOUT_ATTEMPT = int(
                request.POST.get('pass_lockout', 0))
            selected_app.LOCKOUT_DURATION = request.POST.get(
                'pass_lockout_duration', '')
            selected_app.MFA_ENABLED = bool(
                request.POST.get('multifactor_enabled', False))
            selected_app.save()  # Save the changes to the existing record
            existing_attachment = PWCONFIGATTACHMENTS.objects.filter(
                APP_NAME=APP_NAME).first()
            file_name = form.cleaned_data['file_name']
            # UPDATE OR UPLOAD THE ATTACHMENT
            if existing_attachment:
                # Update the existing attachment
                if file_name:
                    existing_attachment.file_name.delete()
                    existing_attachment.file_name = file_name
                    existing_attachment.attachment_file = form.cleaned_data['file_name']
                    existing_attachment.activated = True
                    existing_attachment.save()
            else:
                # Create a new attachment
                new_attachment = PWCONFIGATTACHMENTS(
                    APP_NAME=APP_NAME, file_name=file_name)
                new_attachment.save()
                new_attachment.activated = True
                new_attachment.save()

        context = self.common_data(request, comp_id, app_id,)
        return render(request, self.template_name, context)


class AppUserRecordView(ProcessOwnerPermissionMixin,View):
    template_name = "pages/APP/processowner-userrecord.html"

    def get(self, request, comp_id, app_id, username):
        selected_user = APP_RECORD.objects.filter(
            APP_NAME=app_id, USER_ID=username).first()
        mapped_user = HR_RECORD.objects.filter(
            Q(EMAIL_ADDRESS=selected_user.EMAIL_ADDRESS) |
            Q(USER_ID=selected_user.USER_ID) |
            (Q(FIRST_NAME=selected_user.FIRST_NAME)
             & Q(LAST_NAME=selected_user.LAST_NAME))
        )
        context = {
            'comp_id':comp_id, 
            'selected_user': selected_user,
            'app_id': app_id,
            'mapped_user': mapped_user
        }
        return render(request, self.template_name, context)


class AppNewUserListView(ProcessOwnerPermissionMixin,View):
    template_name = "pages/APP/processowner-appnewuserlist.html"

    def get(self, request, comp_id, app_id):
        current_date = timezone.now()
        current_year = current_date.year
        new_users = APP_RECORD.objects.filter(DATE_GRANTED__year=current_year, APP_NAME=app_id).order_by(
            'STATUS', 'DATE_GRANTED', 'EMAIL_ADDRESS')
        unique_statuses = set(user.STATUS for user in new_users)
        new_user_approval_form = NEW_USER_APPROVAL_FORM()
        selected_app = APP_LIST.objects.get(id = app_id)
        company_name = COMPANY.objects.get(id=comp_id)
        context = {
            'selected_app':selected_app,
            'new_users': new_users,
            'new_user_approval_form': new_user_approval_form,
            'app_id': app_id,
            'unique_statuses': unique_statuses,
            'comp_id':comp_id,
            'company_name':company_name
        }
        return render(request, self.template_name, context)


class AppNewUserApprovalView(ProcessOwnerPermissionMixin,View):
    template_name = 'pages/APP/processowner-appnewuserapproval.html'

    def common_data(self, request, comp_id, app_id, user_id):
        new_user_approval_form = NEW_USER_APPROVAL_FORM()
        selected_user = APP_RECORD.objects.get(id=user_id)
        existing_attachment_orig = APP_NEW_USER_APPROVAL.objects.filter(
            USER_ID=user_id).first()
        existing_attachment = basename(
            existing_attachment_orig.file_name.name) if existing_attachment_orig else None
        active_hr_users = HR_RECORD.objects.filter(STATUS__iexact='ACTIVE')
        if existing_attachment_orig:
            context = {
                'new_user_approval_form': new_user_approval_form,
                'active_hr_users': active_hr_users,
                'app_id': app_id,
                'selected_user': selected_user,
                'comp_id':comp_id,
                'existing_attachment': existing_attachment}
        else:
            context = {
                'new_user_approval_form': new_user_approval_form,
                'active_hr_users': active_hr_users,
                'app_id': app_id,
                'comp_id':comp_id,
                'selected_user': selected_user,
            }
        return context

    def get(self, request, comp_id, app_id, user_id):
        context = self.common_data(request, comp_id, app_id, user_id)
        return render(request, self.template_name, context)

    def new_user_add_attachment(self, request, comp_id, app_id, user_id):
        form = NEW_USER_APPROVAL_FORM(request.POST, request.FILES)
        if form.is_valid():
            approver1 = get_object_or_404(
                HR_RECORD, id=request.POST.get('approver1_id'))
            approver2 = get_object_or_404(
                HR_RECORD, id=request.POST.get('approver2_id'))

            date_formats = ["%Y-%m-%d", "%d/%m/%Y",
                            "%m/%d/%Y", "%Y%m%d", "%m/%d/%y"]
            date_approved = request.POST.get('date_approved')
            date_approved = timezone.make_aware(
                self.parse_date(str(date_approved), date_formats))

            selected_user, created = APP_RECORD.objects.get_or_create(
                id=user_id)
            selected_user.DATE_APPROVED = date_approved
            selected_user.ACCESS_APPROVER_NAME1 = approver1
            selected_user.ACCESS_APPROVER_NAME2 = approver2
            selected_user.APPROVAL_TYPE = request.POST.get('approval_type')
            selected_user.APPROVAL_REFERENCE = request.POST.get('approval_ref')
            selected_user.save()

            user_to_be_uploaded = APP_RECORD.objects.get(id=user_id)
            file_name = form.cleaned_data['file_name']
            if file_name:
                attach_to_user, created = APP_NEW_USER_APPROVAL.objects.get_or_create(
                    USER_ID=user_to_be_uploaded)  # Save the changes to the existing record
                attach_to_user.file_name.delete()
                attach_to_user.file_name = file_name
                attach_to_user.save()

        # RELOAD THE PAGE
        context = self.common_data(request, comp_id, app_id, user_id)
        return render(request, self.template_name, context)

    def delete_new_user_approval(self, request, comp_id, app_id, user_id):
        attachment = APP_NEW_USER_APPROVAL.objects.get(USER_ID=user_id)
        attachment.file_name.delete()
        attachment.save()
        context = self.common_data(request, comp_id, app_id, user_id)
        return render(request, self.template_name, context)

    def post(self, request, comp_id, app_id, user_id):
        form_id = request.POST.get('form_id')
        if form_id == 'new_user_add_approval':
            return self.new_user_add_attachment(request,comp_id,app_id, user_id)
        elif form_id == 'delete_new_user_attachment':
            return self.delete_new_user_approval(request, comp_id,app_id, user_id)

    def parse_date(self, date_str, date_formats):
        for date_format in date_formats:
            try:
                return datetime.strptime(date_str, date_format)
            except ValueError:
                pass
        # If none of the formats match, return a default date
        return datetime(1900, 1, 1)


class AppNewUserGetJobApprovalView(ProcessOwnerPermissionMixin,View):
    def get(self, request, id):
        user = get_object_or_404(HR_RECORD, id=id)
        job_title = user.JOB_TITLE
        context = {
            'job_title': job_title
        }
        return JsonResponse(context)

class AppTerminationListView(ProcessOwnerPermissionMixin,View):
    template_name = "pages/APP/processowner-appterminationlist.html"

    def get(self, request,comp_id,app_id):
        current_date = timezone.now()
        current_year = current_date.year
        termed_users = APP_RECORD.objects.filter(
            DATE_REVOKED__year=current_year, APP_NAME=app_id).order_by('DATE_REVOKED')
        selected_app = APP_LIST.objects.get(id = app_id)
        company_name = COMPANY.objects.get(id=comp_id)
        context = {
            'selected_app':selected_app,
            'comp_id':comp_id,
            'termed_users': termed_users,
            'app_id': app_id,
            'company_name':company_name
        }
        return render(request, self.template_name, context)
    
class AdminAccountListView(ProcessOwnerPermissionMixin,View):
    template_name = "pages/APP/processowner-adminaccounts.html"

    def common_data(self, request,comp_id,app_id):
        admin_roles = ADMIN_ROLES_FILTER.objects.filter(ROLE_NAME__isnull = False)
        active_roles = APP_RECORD.objects.filter(APP_NAME = app_id, ROLE_NAME__isnull = False).values('ROLE_NAME').distinct()
        admin_accounts = APP_RECORD.objects.filter(APP_NAME=app_id, roles_filter__in=admin_roles, STATUS__iexact = 'Active').order_by('USER_ID')
        unique_admin_accounts = ADMIN_ROLES_FILTER.objects.filter(APP_NAME=app_id).values('ROLE_NAME').distinct()
        selected_app = APP_LIST.objects.get(id = app_id)
        company_name = COMPANY.objects.get(id=comp_id)
        context = {
            'active_roles':active_roles,
            'unique_admin_accounts':unique_admin_accounts,
            'selected_app':selected_app,
            'comp_id':comp_id,
            'admin_accounts': admin_accounts,
            'app_id': app_id,
            'company_name':company_name
        }
        return context

    def get(self, request,comp_id,app_id):
        context = self.common_data(request, comp_id, app_id)
        return render(request, self.template_name, context)
 
    def post(self,request,comp_id,app_id):
        selected_roles = request.POST.getlist('role_list')
        app_names = APP_RECORD.objects.filter(APP_NAME=app_id).first()
        app_instance = APP_LIST.objects.filter(APP_NAME = app_names.APP_NAME).first()
        roles = APP_RECORD.objects.filter(APP_NAME = app_id, ROLE_NAME__in=selected_roles, ROLE_NAME__isnull = False)

        admin_roles, created = ADMIN_ROLES_FILTER.objects.get_or_create(
                APP_NAME=app_instance)
        admin_roles.APP_NAME = app_instance
        admin_roles.ROLE_NAME.set(roles)
        admin_roles.save()

        context = self.common_data(request, comp_id, app_id)
        return render(request, self.template_name, context)
    
class GenericAccountListView(ProcessOwnerPermissionMixin,View):
    template_name = "pages/APP/processowner-appgenericaccounts.html"

    def common_data(self, request,comp_id,app_id):
        app_name = APP_LIST.objects.filter(id = app_id).first()
        generic_accounts = generic_account = APP_RECORD.objects.filter(
        Q(TYPE='system_account') | Q(TYPE='integration_account'),
        Q(STATUS__iexact='ACTIVE'),APP_NAME = app_name).order_by('EMAIL_ADDRESS', 'TYPE')
        company_name = COMPANY.objects.get(id=comp_id)
        selected_app = APP_LIST.objects.get(id = app_id)
        context = {
            'generic_accounts':generic_accounts,
            'comp_id':comp_id,
            'app_id': app_id,
            'company_name':company_name,
            'selected_app':selected_app,
        }
        return context

    def get(self, request,comp_id,app_id):
        context = self.common_data(request, comp_id, app_id)
        return render(request, self.template_name, context)
        
class AppHRMappingListView(View):
    template_name = "pages/APP/processowner-apphrmapping.html"

    def get(self, request, comp_id, app_id):
        app_users = APP_RECORD.objects.filter(APP_NAME=app_id)
        selected_app = APP_LIST.objects.get(id = app_id)
        company_name = COMPANY.objects.get(id=comp_id)
        mapped_users = HR_RECORD.objects.filter(
            Q(EMAIL_ADDRESS__in=app_users.values_list('EMAIL_ADDRESS', flat=True)) |
            Q(USER_ID__in=app_users.values_list('USER_ID', flat=True)) |
            (Q(FIRST_NAME__in=app_users.values_list('FIRST_NAME', flat=True)) &
             Q(LAST_NAME__in=app_users.values_list('LAST_NAME', flat=True)))
        )
        unmapped_users = app_users.exclude(
            Q(EMAIL_ADDRESS__in=mapped_users.values_list('EMAIL_ADDRESS', flat=True)) |
            Q(USER_ID__in=mapped_users.values_list('USER_ID', flat=True)) |
            Q(TYPE__isnull = False)
        )
        context = {
            'selected_app':selected_app,
            'mapped_users': mapped_users,
            'unmapped_users': unmapped_users,
            'comp_id':comp_id,
            'app_id': app_id,
            'company_name':company_name
        }
        return render(request, self.template_name, context)


# THIS IS THE CLASS FOR PASSWORD SECTION
class DeletePWAttachment(View):
    template_name: template_name = 'pages/APP/processowner-appdetails.html'

    def get_attachment(self, id):
        selected_app = get_object_or_404(APP_RECORD, id=id)
        attachment = PWCONFIGATTACHMENTS.objects.filter(
            APP_NAME=selected_app.id, activated=True).first()
        return selected_app, attachment

    def post(self, request, id):
        selected_app, attachment = self.get_attachment(id)
        if attachment:
            attachment.delete()
            attachment.file_name.delete()
            response_data = {'message': 'Attachment deleted successfully'}
            return JsonResponse(response_data)
        else:
            # Assuming you want to send an error message if the attachment is not found
            response_data = {'error': 'Attachment not found'}
            return JsonResponse(response_data, status=404)


class ApplicationList(View):

    template_name = 'pages/APP/app-list.html'

    def get(self, request, user_id=0, *args, **kwargs):
        # Load all applications
        try:
            app = APP_LIST.objects.filter(APP_NAME__isnull=False)
        except APP_LIST.DoesNotExist:
            app = None
        except Exception as e:
            print(str(e))
            pass
        try:
            active_users = User.objects.filter(is_active=True)
        except User.DoesNotExist:
            active_users = None
        context = {'app': app,
                   'active_users': active_users}
        return render(request, self.template_name, context)

    def post(self, request, app_id=0):
        if app_id == 0:
            form = NewAPP(request.POST)
            app_ower = User.objects.get(username=request.POST['app_owner'])
            if form.is_valid():
                app = form.save(commit=False)
                app.APP_NAME = request.POST['app_name']
                app.APP_TYPE = request.POST['app_type']
                app.HOSTED = request.POST['hosting']
                app.RISKRATING = request.POST['risk_rating']
                app.RELEVANT_PROCESS = request.POST['relevant_process']
                app.DATE_IMPLEMENTED = request.POST['date_implemented']
                app.APPLICATION_OWNER = app_ower
                # Logging
                app.CREATED_BY = 'manaol2112'
                app.CREATED_ON = timezone.now()
                app.save()

                app = APP_LIST.objects.filter(APP_NAME__isnull=False)
                context = {'app': app}
                return render(request, self.template_name, context)

class FetchMappedUser(View):
    model = HR_RECORD
    template_name = 'pages/APP/app-details.html'
    form_class = MappedUser

    def get(self, request, id, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                mapped_user = HR_RECORD.objects.get(EMAIL_ADDRESS=id)
                hr_mapping = self.form_class(instance=mapped_user)
                context = {
                    'hr_mapping': model_to_dict(hr_mapping.instance),
                    'form_html': hr_mapping.as_table(),
                }
                return JsonResponse(context)
            except ObjectDoesNotExist:
                error_message = "Employee not found"
                return JsonResponse({"error": error_message}, status=404)


class FetchAPPDetails(View):
    model = APP_LIST
    template_name = 'pages/APP/app-details.html'

    def get(self, request, app_name, *args, **kwargs):
        # POPULATE THE CV FORM
        form = CSVModelForm()
        # OBTAIN THE LIST OF APPS BASED ON SELECTED VALUE
        selected_app = APP_LIST.objects.get(APP_NAME=app_name)
        # OBTAIN THE LIST OF USERS BASED ON APP
        app_users = APP_RECORD.objects.filter(APP_NAME=selected_app)
        # MATCHING USERS FROM HR RECORD
        matching_users = HR_RECORD.objects.filter(
            # Match based on USER_ID, EMAIL_ADDRESS, or a combination of FIRST_NAME and LAST_NAME
            Q(USER_ID__in=app_users.values_list('USER_ID', flat=True)) |
            Q(EMAIL_ADDRESS__in=app_users.values_list('EMAIL_ADDRESS', flat=True)) |
            (Q(FIRST_NAME__in=app_users.values_list('FIRST_NAME', flat=True)) &
             Q(LAST_NAME__in=app_users.values_list('LAST_NAME', flat=True)))
        )
        # USERS FROM APP_RECORD THAT MATCH HR_RECORD
        matched_app_users = app_users.filter(
            Q(USER_ID__in=matching_users.values_list('USER_ID', flat=True)) |
            Q(EMAIL_ADDRESS__in=matching_users.values_list(
                'EMAIL_ADDRESS', flat=True))
            # |(Q(FIRST_NAME__in=matching_users.values_list('FIRST_NAME', flat=True)) &
            # Q(LAST_NAME__in=matching_users.values_list('LAST_NAME', flat=True)))
        )

        # USERS FROM APP_RECORD THAT DO NOT MATCH HR_RECORD
        unmatched_app_users = app_users.exclude(
            Q(USER_ID__in=matching_users.values_list('USER_ID', flat=True)) |
            Q(EMAIL_ADDRESS__in=matching_users.values_list('EMAIL_ADDRESS', flat=True)) |
            Q(TYPE__isnull=False)  # Filtering for null TYPE
            # |(Q(FIRST_NAME__in=matching_users.values_list('FIRST_NAME', flat=True)) &
            # Q(LAST_NAME__in=matching_users.values_list('LAST_NAME', flat=True)))
        )

        context = {'selected_app': selected_app,
                   'form': form,
                   'app_users': app_users,
                   'matched_app_users': matched_app_users,
                   'unmatched_app_users': unmatched_app_users}
        return render(request, self.template_name, context)


class TagUserType(View):

    def get(self, request, id):
        model = APP_RECORD
        template_name = 'pages/APP/app-details.html'
        unmapped_user = model.objects.get(id=id)
        context = {
            'unmapped_user': model_to_dict(unmapped_user.instance),
            'form_html': unmapped_user.as_table(),
        }
        return JsonResponse(context)

    def post(self, request, id, *args, **kwargs):
        if request.method == 'POST':
            try:
                data = json.loads(request.body.decode('utf-8'))
                ids = data.get('checkedRecords', [])
                selected_type = data.get('selected_type')
                for id in ids:
                    unmapped_user = APP_RECORD.objects.get(id=id)
                    unmapped_user.TYPE = selected_type
                    unmapped_user.save()
                return JsonResponse({'message': 'User types updated successfully.'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
