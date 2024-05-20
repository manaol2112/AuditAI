
from appAUDITAI.dataview.LOGIN.views import authenticate
from appAUDITAI.dataview.HR.views import hrmanagement
from appAUDITAI.dataview.ADMIN.views import companymanagement, usermanagement, systemsettings,utils
from appAUDITAI.dataview.APP.views import applications_view,policies_view
from appAUDITAI.dataview.DASHBOARD.views import dashboard
from appAUDITAI.dataview.CLIENTS.views import clientactions
from appAUDITAI.dataview.AUDIT.views import auditview
from appAUDITAI.dataview.TICKETS.views import accessrequest
from django.urls import path

app_name = 'appAUDITAI'

urlpatterns = [

#--------------URL FOR ADMINISTRATORS-------------------------# 
#ADMINISTRATION
path("users/all-users",usermanagement.CreateUserView.as_view(),name="all-users"),
path("administration/systemsettings/",systemsettings.SystemSettingsView.as_view(),name="systemsettings"),
path("administration/systemsettings/manage/user-roles/",systemsettings.ManageUsersandRolesView.as_view(),name="manage-user-roles"),
path("administration/systemsettings/manage/user-roles/<int:user_id>",systemsettings.ManageUsersandRolesDetailsView.as_view(),name="manage-user-roles-details"),
path("administration/systemsettings/manage/security/",systemsettings.ManageSecurityView.as_view(),name="manage-security"),
path("administration/systemsettings/manage/security/passwordpolicy",systemsettings.ManagePasswordView.as_view(),name="manage-password-policy"),
path("administration/systemsettings/manage/companies/",systemsettings.ManageCompaniesView.as_view(),name="manage-companies"),
path("administration/systemsettings/manage/roles/<int:role_id>",systemsettings.ManageRolesView.as_view(),name="manage-roles"),
path("administration/systemsettings/manage/roles/",systemsettings.ManageRolesListView.as_view(),name="manage-roles-view"),
path("administration/systemsettings/manage/hrrecord/",systemsettings.ManageHRRecordView.as_view(),name="manage-hr-record"),
path("administration/systemsettings/manage/hrrecord/<uuid:comp_id>",systemsettings.ManageHRRecordDetailsView.as_view(),name="manage-hr-record-details"),
path("administration/systemsettings/manage/companies/<uuid:comp_id>",systemsettings.ManageCompaniesDetailsView.as_view(),name="manage-companies-details"),
path("administration/systemsettings/manage/riskandcontrols/",systemsettings.ManageRiskandControlView.as_view(),name="manage-riskandcontrols"),

#TICKETINGURLS
path('access-request/home/', accessrequest.CompanySelect.as_view(), name='access-request-home'),
path('access-request/details/<uuid:request_id>', accessrequest.AccessRequestDetails.as_view(), name='access-request-details'),
path('access-request/company/<uuid:comp_id>', accessrequest.AccessRequestHome.as_view(), name='access-request-create'),
path('access-request/company/my-approval-queue/', accessrequest.AccessApprovalHome.as_view(), name='access-request-approval'),
path('access-request/get_roles/', accessrequest.get_roles, name='access_request_get_roles'),
path('access-request/approve-access-request/<str:approval_token>', accessrequest.approve_access_request, name='approve_access_request'),

#SFTPCHECK
path('test_sftp_connection/', applications_view.test_sftp_connection, name='test_sftp'),

#--------------URL FOR AUDITORS--------------------------------# 
#CLIENTS
path("myclients/actions/<int:id>",clientactions.ClientActions.as_view(),name="client-actions"),


#AUDIT
path("myclients/actions/audit/risk-assessment/<uuid:comp_id>/<uuid:audit_id>",auditview.RiskAssessment.as_view(),name="audit-risk-assessment"),
#AUDIT
path("myclients/actions/audit/manage-period",auditview.ManageAuditPeriod.as_view(),name="audit-manage-period"),
path("myclients/actions/audit/select-audit/<uuid:comp_id>",auditview.SelectAuditPeriod.as_view(),name="audit-select-period"),
path("myclients/actions/audit/selected_app/<uuid:comp_id>/<uuid:audit_id>/<uuid:app_id>",auditview.AuditPerApp.as_view(),name="audit-per-app"),
path("myclients/actions/audit/selected_app/planning-docs/<uuid:comp_id>/<uuid:audit_id>/<uuid:app_id>",auditview.AuditPlanningDocs.as_view(),name="audit-per-app-planning-docs"),
path("myclients/actions/audit/selected_app/risk-assessment/<uuid:comp_id>/<uuid:audit_id>/<uuid:app_id>",auditview.AuditRiskMapping.as_view(),name="audit-per-app-risk-mapping"),
path("myclients/actions/audit/selected_app/workpapers/<uuid:comp_id>/<uuid:audit_id>/<uuid:app_id>",auditview.AuditWorkpapers.as_view(),name="audit-per-app-workpapers"),
path("myclients/actions/audit/selected_app/deficiencies/<uuid:comp_id>/<uuid:audit_id>/<uuid:app_id>",auditview.AuditDeficiencies.as_view(),name="audit-per-app-deficiencies"),
path("myclients/actions/audit/selected_app/reports/<uuid:comp_id>/<uuid:audit_id>/<uuid:app_id>",auditview.AuditReports.as_view(),name="audit-per-app-reports"),
path("audit/risk-and-controls/",auditview.RiskAndControls.as_view(),name="risk-and-controls"),

#AUTHENTICATION
path("myclients/actions/audit/<uuid:comp_id>",auditview.AuditHome.as_view(),name="audit-home"),
path("myclients/actions/audit/authentication/<int:id>",auditview.Audit_Authentication.as_view(),name="audit-authentication"),
path("myclients/actions/audit/authentication/pwconfigviewer/<int:id>",auditview.PWConfigViewer.as_view(),name="pwconfig-viewer"),

#TERMINATION
path("myclients/actions/audit/termination/<int:id>",auditview.Audit_Termination.as_view(),name="audit-termination"),
path("myclients/actions/audit/termination/details/<uuid:comp_id>/<uuid:app_id>",auditview.Audit_Termination_Details.as_view(),name="audit-termination-details"),

#PROVISIONING
path("myclients/actions/audit/provisioning/<int:id>",auditview.Audit_Provisioning.as_view(),name="audit-provisioning"),
path("myclients/actions/audit/provisioning/details/<uuid:comp_id>/<uuid:app_id>",auditview.Audit_Provisioning_Details.as_view(),name="audit-provisioning-details"),

#ADMINISTRATIVE ACCESS
path("myclients/actions/audit/privileged access/<int:id>",auditview.Audit_PrivilegedAccounts.as_view(),name="audit-privileged-accounts"),
#--------------URL FOR PROCESS OWNERS-------------------------#

#APPLICATION LIST
path("dashboard/company/list/",applications_view.AppListByCompany.as_view(),name="applist-company-select"),
path("dashboard/company/applications/<uuid:comp_id>/",applications_view.ApplistByProcessOwner.as_view(),name="applist-process-owner"),
path("dashboard/my-applications/details/<uuid:comp_id>/<uuid:app_id>/",applications_view.AppdetailsByProcessOwner.as_view(),name="appdetails-process-owner"),
path("dashboard/my-applications/details/setup/<uuid:comp_id>/<uuid:app_id>",applications_view.SetupNewAppView.as_view(),name="setup-new-app"),
path("dashboard/my-applications/details/<uuid:comp_id>/<uuid:app_id>/<str:username>/",applications_view.AppUserRecordView.as_view(),name="appdetails-view-user-record"),
path("dashboard/my-applications/details/app-new-users-list/<uuid:comp_id>/<uuid:app_id>/",applications_view.AppNewUserListView.as_view(),name="appdetails-new-user-list"),
path("dashboard/my-applications/details/app-new-users-list/<uuid:comp_id>/<uuid:app_id>/<int:user_id>",applications_view.AppNewUserApprovalView.as_view(),name="appdetails-new-user-approval"),
path("dashboard/my-applications/details/app-termination-list/<uuid:comp_id>/<uuid:app_id>/",applications_view.AppTerminationListView.as_view(),name="appdetails-termination-list"),
path("dashboard/my-applications/details/app-hr-mapping-list/<uuid:comp_id>/<uuid:app_id>/",applications_view.AppHRMappingListView.as_view(),name="appdetails-hr-mapping-list"),
path("dashboard/my-applications/details/administrative-accounts-list/<uuid:comp_id>/<uuid:app_id>/",applications_view.AdminAccountListView.as_view(),name="appdetails-admin-list"),
path("dashboard/my-applications/details/generic-accounts-list/<uuid:comp_id>/<uuid:app_id>/",applications_view.GenericAccountListView.as_view(),name="appdetails-generic-list"),
path("dashboard/my-applications/delete/<int:id>/",applications_view.DeletePWAttachment.as_view(),name="delete-pw-attachment"),

path("dashboard/my-applications/details/compliance/authentication/<uuid:comp_id>/<uuid:app_id>",applications_view.AppComplianceAuth.as_view(),name="app-compliance"),
path("dashboard/my-applications/details/compliance/provisioning/<uuid:comp_id>/<uuid:app_id>",applications_view.AppComplianceProv.as_view(),name="app-complianc-prov"),

path("manage/access-requests/",applications_view.AccessGranting.as_view(),name = "manage-access-request"),
path("manage/access-requests/<uuid:request_id>",applications_view.GrantTicketDetails.as_view(),name = "manage-access-request-details"),

#AJAX CALL TO POPULATE THE JOB TITLE OF THE APPROVERS
path('get_approver1_job_title/<int:id>/', applications_view.AppNewUserGetJobApprovalView.as_view(),name="get_approver1_name"),
path('get_approver2_job_title/<int:id>/', applications_view.AppNewUserGetJobApprovalView.as_view(),name="get_approver1_name"),

#LOG-IN
path("",authenticate.AuthenticateUsers.as_view(),name="authenticate-user"),
path("logout/",authenticate.LogoutUser.as_view(),name="logout-user"),
path("multi-factor-authentication/<uuid:token>", authenticate.MultiFactorAuth.as_view(),name="require-mfa"),

#COMPANY SETUP
path("system-setting/",companymanagement.SetupCompany.as_view(),name="system-setting"),

#DASHBOARD
path("home/dashboard/",dashboard.HomeView.as_view(),name="mydashboard"),

#HR Records
path("hr-management",hrmanagement.HRManagement.as_view(),name="hr-management"),
path("new-hr-record/",hrmanagement.NewHRRecord.as_view(),name="new-hr-record"),
path("update-hr-record",hrmanagement.UpdateHRRecord.as_view(),name="update-hr-record"),
path("upload-hr-setting",hrmanagement.UploadHRSetting.as_view(),name="upload-hr-setting"),
path("upload-hr-history",hrmanagement.UploadHRHistory.as_view(),name="upload-hr-history"),
path("employeerecord/<str:id>/",hrmanagement.FetchHRRecord.as_view(),name="employeerecord"),

#APP Records
path("application-list/",applications_view.ApplicationList.as_view(),name="application-list"),
path("application-details/<str:app_name>/",applications_view.FetchAPPDetails.as_view(),name="application-details"),
path("application-details/<str:id>",applications_view.FetchMappedUser.as_view(),name="application-details-email"),
path("update-user-type/<int:id>", applications_view.TagUserType.as_view(), name="update-user-type"),

#CONTROLS/POLICIES
path("policies/manage/", policies_view.PoliciesView.as_view(), name="application-policies"),
path("policies/manage/authentication/", policies_view.PoliciesAuthView.as_view(), name="policies-authentication"),
path("policies/manage/provisioning/", policies_view.PoliciesProvisionView.as_view(), name="policies-provisioning"),
path("policies/manage/termination/", policies_view.PoliciesTerminationView.as_view(), name="policies-termination"),
path("policies/manage/accessreview/", policies_view.PoliciesUserAccessReviewView.as_view(), name="policies-useraccessreview"),
path("policies/manage/adminaccounts/", policies_view.PoliciesAdminView.as_view(), name="policies-adminaccounts"),

#ERROR_PAGE

#404
path("error/page-not-found/",utils.error_404,name="error_404"),
path("error/needed-permission-not-found/",utils.no_permission.as_view(),name="no_permission"),


#AUDIT URLS


]

