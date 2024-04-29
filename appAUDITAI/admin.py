from django.contrib import admin

from .models import HR_RECORD, APP_RECORD, CSV,SAP_USR02,APP_LIST, POLICIES, CONTROLS, COMPANY, MULTIPLE_COMPANY, USERROLES,PASSWORD,PWCONFIGATTACHMENTS
from .models import USER_LOCKOUT,PROVISIONINGPOLICY,PASSWORDPOLICY,TERMINATIONPOLICY,APP_USER_UPLOAD, APP_NEW_USER_APPROVAL, ADMIN_ROLES_FILTER,PASSWORDCONFIG,APP_USER_SFTP,APP_JOB_PULL,APP_JOB_USER_LOG,APP_JOB_USER_LOG_PROCESS,HR_LIST_SFTP,HR_JOB_PULL,HR_JOB_USER_LOG
# Register your models here.
admin.site.register(HR_RECORD)
admin.site.register(APP_RECORD)
admin.site.register(CSV)
admin.site.register(SAP_USR02)
admin.site.register(APP_LIST)
admin.site.register(POLICIES)
admin.site.register(CONTROLS)
admin.site.register(COMPANY)
admin.site.register(MULTIPLE_COMPANY)
admin.site.register(USERROLES)
admin.site.register(PASSWORD)
admin.site.register(PWCONFIGATTACHMENTS)
admin.site.register(PASSWORDPOLICY)
admin.site.register(TERMINATIONPOLICY)
admin.site.register(APP_USER_UPLOAD)
admin.site.register(APP_NEW_USER_APPROVAL)
admin.site.register(ADMIN_ROLES_FILTER)
admin.site.register(PASSWORDCONFIG)
admin.site.register(APP_USER_SFTP)
admin.site.register(APP_JOB_PULL)
admin.site.register(APP_JOB_USER_LOG)
admin.site.register(APP_JOB_USER_LOG_PROCESS)
admin.site.register(PROVISIONINGPOLICY)
admin.site.register(USER_LOCKOUT)

