from appAUDITAI.dataview.MISC.imports import *


class ALLMODELS:

    def all_company(**kwargs):
        companies = COMPANY.objects.all()
        for key, value in kwargs.items():
            if value is not None:  
                filter_criteria = {f"{key}__exact": value} 
                companies = companies.filter(**filter_criteria)
        return companies
    
    def all_apps(**kwargs):
        applications = APP_LIST.objects.all()

        for key, value in kwargs.items():
            if value is not None:  
                filter_criteria = {f"{key}__exact": value} 
                applications = applications.filter(**filter_criteria)
        return applications
    
    def all_auditlist(**kwargs):
        audit_list = AUDITLIST.objects.all()

        for key, value in kwargs.items():
            if value is not None:  
                filter_criteria = {f"{key}__exact": value} 
                audit_list = audit_list.filter(**filter_criteria)
        return audit_list
    




  
