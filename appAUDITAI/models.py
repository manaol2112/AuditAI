from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password, check_password
import uuid
import os
from django.conf import settings


class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)  # Or adjust the length as needed
    expires_at = models.DateTimeField()

class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)

# SAP S/4HANA AND ECC MODELS ARE STORED IN THIS GROUP

class SAP_USR02(models.Model):
    BNAME = models.CharField(max_length=50,blank=True,null=True) #USERID
    MANDT = models.CharField(max_length=50,blank=True,null=True) #CLIENTCODE
    USTYP = models.CharField(max_length=2,blank=True,null=True) #USER TYPE AS TO DIALOG, SYSTEM, OR COMM
    GLTGB = models.DateTimeField() #RECORD CREATION DATE AND TIME
    GLTGV = models.DateField() #LAST LOGON OF USER
    TRDAT = models.DateTimeField() #LAST SUCCESSFUL LOGIN
    LTIME = models.DateTimeField() #LAST UNSUCCESSFUL ATTEMPT
    UFLAG = models.CharField(max_length=10,blank=True,null=False) #USER STATUS (ACTIVE OR LOCKED)
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.BNAME
    
    class Meta:
        managed = True
        db_table = 'SAP_USR02'

class SAP_AGR_USERS(models.Model):
    UNAME = models.CharField(max_length=50,blank=True,null=True) #USERID
    MANDT = models.CharField(max_length=50,blank=True,null=True) #CLIENTCODE
    AGR_NAME = models.CharField(max_length=50,blank=True,null=True) #AUTHORIZATIONS ASSIGNED
    FROM_DAT = models.DateTimeField() #VALIDITY START DATE
    TO_DAT = models.DateTimeField() #VALIDITY END DATE
    
    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.MANDT
    
    class Meta:
        managed = True
        db_table = 'SAP_AGR_USERS'

class USER_LOCKOUT(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    failed_attempts = models.IntegerField(default=0)
    locked_out = models.BooleanField(default=False)
    last_attempt_timestamp = models.DateTimeField(null=True, blank=True)
    # You can add other fields as needed, such as lockout duration, etc.

    def __str__(self):
        return self.user.username

class PASSWORDCONFIG(models.Model):
    MIN_LENGTH = models.CharField(max_length=100,blank=True,null=True)
    HISTORY = models.CharField(max_length=100,blank=True,null=True)
    AGE = models.CharField(max_length=100,blank=True,null=True)
    LOCKOUT = models.CharField(max_length=100,blank=True,null=True)
    LOCKOUT_DURATION = models.CharField(max_length=100,blank=True,null=True)
    COMPLEXITY_ENABLED =  models.BooleanField(blank=True,null=True)
    HAS_SPECIALCHAR =  models.BooleanField(blank=True,null=True)
    HAS_NUMERIC =  models.BooleanField(blank=True,null=True)
    HAS_UPPER =  models.BooleanField(blank=True,null=True)
    HAS_LOWER =  models.BooleanField(blank=True,null=True)
    MFA_ENABLED =  models.BooleanField(blank=True,null=True)
    SESSION_LENGTH = models.CharField(max_length=100,blank=True,null=True)

    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True, null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)


    class Meta:
        managed = True
        db_table = 'SYS_PWCONFIG'



#COMPANY
class COMPANY(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    COMPANY_ID = models.CharField(max_length=100,blank=True,null=True)
    COMPANY_NAME = models.CharField(max_length=1000,blank=True,null=True)
    SELECTED = models.BooleanField(blank=True,null=True)

    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True, null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.COMPANY_NAME
    
    class Meta:
        managed = True
        db_table = 'COMPANY'

    #AUDITPROJECT

class AUDITFILE(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    FILE_NAME = models.CharField(max_length=1000,blank=True,null=True)
    STATUS = models.CharField(max_length=100,blank=True,null=True)
    CURRENTLY_WITH = models.CharField(max_length=100,blank=True,null=True)
    FOLDER_NAME = models.CharField(max_length=1000,blank=True,null=True)
    AUDIT_ID = models.CharField(max_length=100,blank = True, null=True)
    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True, null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)
    
    class Meta:
        managed = True
        db_table = 'AUDITFILE'


class PREPARERSIGNOFF(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    FILE_NAME = models.ForeignKey(AUDITFILE, on_delete=models.CASCADE, null= True, blank = True)
    PREPARER = models.CharField(max_length=100,blank=True,null=True)
    DATE_SIGNEDOFF = models.DateTimeField(null=True)

    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True, null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)
    
    class Meta:
        managed = True
        db_table = 'PREPARERSIGNOFF'


class REVIEWSIGNOFF(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    FILE_NAME = models.ForeignKey(AUDITFILE, on_delete=models.CASCADE, null= True, blank = True)
    REVIEWER = models.CharField(max_length=100,blank=True,null=True)
    DATE_SIGNEDOFF = models.DateTimeField(null=True)

    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True, null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)
    
    class Meta:
        managed = True
        db_table = 'REVIEWSIGNOFF'


class AUDITNOTES(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    FILE_NAME = models.ForeignKey(AUDITFILE, on_delete=models.CASCADE, null= True, blank = True)
    STATUS = models.CharField(max_length=100,blank=True,null=True)
    TYPE = models.CharField(max_length=100,blank=True,null=True)

    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True, null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)
    
    class Meta:
        managed = True
        db_table = 'AUDITNOTES'

class AUDITNOTESREPLY(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    FILE_NAME = models.ForeignKey(AUDITFILE, on_delete=models.CASCADE, null= True, blank = True)
    OG_NOTE = models.ForeignKey(AUDITNOTES, on_delete= models.CASCADE, null=True, blank=True)
    STATUS = models.CharField(max_length=100,blank=True,null=True)
    TYPE = models.CharField(max_length=100,blank=True,null=True)
    CREATED_BY = models.CharField(max_length=100,blank=True,null=True)

    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True, null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)
    
    class Meta:
        managed = True
        db_table = 'AUDITNOTESREPLY'

def workpaper_upload_to(instance, filename):
    # Assuming instance has an audit_id attribute
    audit_id = instance.audit_id
    return f'workpapers/{audit_id}/{filename}'

class WORKPAPER_UPLOAD(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_name = models.FileField(upload_to=workpaper_upload_to)
    upload_date = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)
    audit_id = models.UUIDField(null=True, blank=False)

    def __str__(self):
        return f"File id: {self.id}"

class AUDITLIST(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    FILE_NAME = models.CharField(max_length=100,blank=True,null=True)
    COMPANY_ID = models.ForeignKey(COMPANY,on_delete=models.CASCADE,blank=True,null=True)
    PERIOD_END_DATE = models.DateField(blank=True, null=True)
    STATUS = models.CharField(max_length=50,blank=True,null=True)

    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True, null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)
    
    class Meta:
        managed = True
        db_table = 'AUDIT_LIST'

class RequestIDCounter(models.Model):
    counter = models.IntegerField(default=0)

    @classmethod
    def get_next_id(cls):
        counter_obj, created = cls.objects.get_or_create(pk=1)
        if not created:
            counter_obj.counter += 1
            counter_obj.save()
        return counter_obj.counter

class ACCESSREQUEST(models.Model):
  
    REQUEST_ID = models.CharField(max_length=100, null=True, blank=False)
    COMPANY_ID = models.ForeignKey(COMPANY, on_delete=models.DO_NOTHING, null=True)
    APP_NAME = models.CharField(max_length=100, null=True, blank=False)
    REQUESTOR = models.CharField(max_length=100, null=True, blank=False)
    ROLES = models.CharField(max_length=1000, null=True, blank=False)
    BUSINESS_APPROVER = models.CharField(max_length=100, null=True, blank=False)
    IT_APPROVER = models.CharField(max_length=100, null=True, blank=False)
    DATE_REQUESTED = models.DateTimeField(null=True)
    DATE_APPROVED = models.DateTimeField(null=True)
    DATE_REJECTED = models.DateTimeField(null=True)
    STATUS = models.CharField(max_length=100, null=True, blank=False)
    ASSIGNED_TO = models.CharField(max_length=100, null=True, blank=False)
    COMMENTS = models.CharField(max_length=1000, null=True, blank=False)
    REJECTION_REASON = models.CharField(max_length=1000, null=True, blank=False)
    REQUEST_TYPE = models.CharField(max_length=100, null=True, blank=False)
    PRIORITY = models.CharField(max_length=100, null=True, blank=False)
    CREATOR = models.CharField(max_length=100, null=True, blank=False)
    APPROVAL_TOKEN = models.UUIDField(default=uuid.uuid4, editable=False)
    DATE_GRANTED = models.DateTimeField(null=True)
    GRANTED_BY = models.CharField(max_length=100, null=True, blank=False)

    APPROVED_BY = models.CharField(max_length=100, null=True, blank=False)
    LAST_MODIFIED = models.DateTimeField(null=True)

    class Meta:
        managed = True
        db_table = 'ACCESS_REQUEST'

    def save(self, *args, **kwargs):
        if not self.REQUEST_ID:
            self.REQUEST_ID = f'REQ#000{RequestIDCounter.get_next_id()}'
        super().save(*args, **kwargs)


class ACCESSREQUESTCOMMENTS(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    REQUEST_ID = models.ForeignKey(ACCESSREQUEST, on_delete=models.CASCADE)
    CREATOR = models.CharField(max_length=100, null=True, blank=False)
    COMMENT_DETAILS = models.CharField(max_length=100, null=True, blank=False)
    DATE_ADDED = models.DateTimeField(null=True)

    class Meta:
            managed = True
            db_table = 'ACCESS_REQUEST_COMMENTS'

class MULTIPLE_COMPANY(models.Model):
    MULTIPLE = models.BooleanField(blank=True,null=True)

    def bool(self):
        return self.MULTIPLE
    
    class Meta:
        managed = True
        db_table = 'MULTIPLE_COMPANY'

# Create your models here.
class USERROLES(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    COMPANY_ID = models.ManyToManyField(COMPANY,blank=True,null=True)
    USERNAME = models.ForeignKey(User,on_delete=models.CASCADE)

    #LOG
    CREATED_BY =  models.CharField(max_length=150,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True, null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY =  models.CharField(max_length=150,blank=True,null=True)

    def __str__(self):
      return str(self.USERNAME.username) if self.USERNAME else ''
    
    class Meta:
        managed = True
        db_table = 'USERROLES'
    
#HR SYSTEM MODELS ARE IN THIS GROUP

class HR_RECORD(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    COMPANY_ID = models.CharField(max_length=1000,blank=True,null=True)
    USER_ID = models.CharField(max_length=50,blank=True,null=True)
    EMAIL_ADDRESS = models.CharField(max_length=50,blank=True,null=True)
    FIRST_NAME = models.CharField(max_length=50,blank=True,null=True)
    LAST_NAME = models.CharField(max_length=50,blank=True,null=True)
    JOB_TITLE = models.CharField(max_length=50,blank=True,null=True)
    DEPARTMENT = models.CharField(max_length=50,blank=True,null=True)
    MANAGER = models.CharField(max_length=50,blank=True,null=True)
    HIRE_DATE = models.DateField(null=True)
    EMP_TYPE =  models.CharField(max_length=10,blank=True,null=True)
    REHIRE_DATE = models.DateField(null=True)
    STATUS = models.CharField(max_length=50,blank=True,null=True)
    TERMINATION_DATE = models.DateField(null=True)
    
    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True, null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return f"{self.FIRST_NAME} {self.LAST_NAME}"
    
    class Meta:
        managed = True
        db_table = 'HR_RECORD'

class APP_USERS(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    USER_ID = models.CharField(max_length=100,blank=True,null=True)
    FIRST_NAME = models.CharField(max_length=100,blank=True,null=True)
    LAST_NAME = models.CharField(max_length=100,blank=True,null=True)
    EMAIL_ADDRESS = models.CharField(max_length=100,blank=True,null=True)
    STATUS = models.CharField(max_length=100,blank=True,null=True)
    LOCKED = models.CharField(max_length=100,blank=True,null=True)


class APP_LIST(models.Model):
    #APPLICATION LIST
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    COMPANY_ID = models.ForeignKey(COMPANY,on_delete=models.CASCADE,max_length=100,blank=True,null=True)
    APP_NAME = models.CharField(max_length=100,blank=True,null=True)
    APP_DESCRIPTION = models.CharField(max_length=1000,blank=True,null=True)
    APP_TYPE = models.CharField(max_length=100,blank=True,null=True)
    HOSTED = models.CharField(max_length=50,blank=True,null=True)
    RISKRATING = models.CharField(max_length=50,blank=True,null=True)
    RELEVANT_PROCESS = models.CharField(max_length=100,blank=True,null=True)
    DATE_IMPLEMENTED = models.CharField(max_length=100,blank=True,null=True)
    DATE_TERMINATED = models.DateField(null=True,blank=True)
    APPLICATION_OWNER = models.ForeignKey(User,on_delete=models.DO_NOTHING,blank=True,null=True)
    AUTHENTICATION_TYPE = models.CharField(max_length=50,blank=True,null=True)
    SETUP_COMPLETE = models.BooleanField(blank=True, null=True)

     #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,default=False,null=True)

    def __str__(self):
        return self.APP_NAME
    
    def get_owner_name(self):
        if self.APPLICATION_OWNER:
            return f"{self.APPLICATION_OWNER.first_name} {self.APPLICATION_OWNER.last_name}"
        else:
            return "No Owner"
    
    class Meta:
        managed = True
        db_table = 'APP_LIST'

class APP_USER_SFTP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    APP_NAME = models.ForeignKey(APP_LIST, on_delete=models.CASCADE,max_length=100,null=True,blank=True)
    HOST_NAME = models.CharField(max_length=1000,blank=True,null=True)
    SFTP_USERNAME = models.CharField(max_length=128,blank=True)
    SFTP_PW_HASHED = models.CharField(max_length=128,blank=True,null=True)
    def set_password(self,raw_password):
            self.SFTP_PW_HASHED = make_password(raw_password)
    def check_password(self,raw_password):
            return check_password(raw_password,self.SFTP_PW_HASHED)
    SFTP_DIRECTORY = models.CharField(max_length=1000,blank=True,null=True)
    SFTP_DESTINATION = models.CharField(max_length=1000,blank=True,null=True)
    SETUP_COMPLETE = models.BooleanField(default=False)

    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)

    class Meta:
        managed = True
        db_table = 'SFTP_USER'

class APP_JOB_PULL(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    APP_NAME = models.ForeignKey(APP_LIST, on_delete=models.CASCADE,max_length=100,blank=True)
    JOB_NAME = models.CharField(max_length=1000,blank=True,null=True)
    MONDAY = models.BooleanField(default=False,null=True)
    TUESDAY = models.BooleanField(default=False,null=True)
    WEDNESDAY = models.BooleanField(default=False,null=True)
    THURSDAY = models.BooleanField(default=False,null=True)
    FRIDAY = models.BooleanField(default=False,null=True)
    SATURDAY = models.BooleanField(default=False,null=True)
    SUNDAY = models.BooleanField(default=False,null=True)
    SCHEDULE_TIME = models.TimeField(null=True,blank=True)
    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)

    class Meta:
        managed = True
        db_table = 'USER_JOB_SCHEDULE'

class APP_JOB_USER_LOG(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    APP_NAME = models.ForeignKey(APP_LIST, on_delete=models.CASCADE,max_length=100,blank=True,null=True)
    JOB_NAME = models.ForeignKey(APP_JOB_PULL,on_delete=models.DO_NOTHING,blank=True)
    JOB_FILE_NAME = models.CharField(max_length=1000,null=True,blank=True)
    JOB_FILE_DESTINATION = models.CharField(max_length=1000,null=True,blank=True)
    JOB_DATE = models.DateTimeField(null=True,blank=False)
    JOB_COMPLETE = models.BooleanField(default=False,null=True)
    JOB_ERROR = models.CharField(max_length=1000,null=True,blank=True)

    class Meta:
        managed = True
        db_table = 'APP_JOB_USER_LOG'

class APP_JOB_USER_LOG_PROCESS(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    APP_NAME = models.ForeignKey(APP_LIST, on_delete=models.CASCADE,max_length=100,blank=True,null=True)
    USER_ID = models.CharField(max_length=128, null=True, blank=True)
    JOB_DATE = models.DateTimeField(null=True,blank=False)
    JOB_FILE_DESTINATION = models.CharField(max_length=1000,null=True,blank=True)
    JOB_ERROR = models.CharField(max_length=1000,null=True,blank=True)
    JOB_COMPLETE = models.BooleanField(default=False,null=True)

    class Meta:
        managed = True
        db_table = 'APP_JOB_USER_LOG_PROCESS'


class HR_LIST_SFTP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    COMPANY_ID = models.ForeignKey(COMPANY,on_delete=models.CASCADE,blank=True,null=True)
    HOST_NAME = models.CharField(max_length=1000,blank=True,null=True)
    SFTP_USERNAME = models.CharField(max_length=128,blank=True)
    SFTP_PW_HASHED = models.CharField(max_length=128,blank=True,null=True)
    def set_password(self,raw_password):
            self.SFTP_PW_HASHED = make_password(raw_password)
    def check_password(self,raw_password):
            return check_password(raw_password,self.SFTP_PW_HASHED)
    SFTP_DIRECTORY = models.CharField(max_length=1000,blank=True,null=True)
    SFTP_DESTINATION = models.CharField(max_length=1000,blank=True,null=True)
    SETUP_COMPLETE = models.BooleanField(default=False)

    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)

    class Meta:
        managed = True
        db_table = 'SFTP_HR'

class HR_JOB_PULL(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    COMPANY_ID = models.ForeignKey(COMPANY,on_delete=models.CASCADE,blank=True,null=True)
    JOB_NAME = models.CharField(max_length=1000,blank=True,null=True)
    MONDAY = models.BooleanField(default=False)
    TUESDAY = models.BooleanField(default=False)
    WEDNESDAY = models.BooleanField(default=False)
    THURSDAY = models.BooleanField(default=False)
    FRIDAY = models.BooleanField(default=False)
    SATURDAY = models.BooleanField(default=False)
    SUNDAY = models.BooleanField(default=False)
    SCHEDULE_TIME = models.TimeField(null=True,blank=True)

     #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)

    class Meta:
        managed = True
        db_table = 'HR_JOB_SCHEDULE'

class HR_JOB_USER_LOG(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    JOB_NAME = models.ForeignKey(APP_JOB_PULL,on_delete=models.DO_NOTHING,blank=True)
    JOB_DATE = models.DateTimeField
    JOB_COMPLETE = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'HR_JOB_USER_LOG'


class APP_RECORD(models.Model):
    #GENERAL USER INFORMATION
    TOKEN = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    APP_NAME = models.ForeignKey(APP_LIST,on_delete=models.CASCADE,max_length=100,blank=True,null=True)
    APP_TYPE = models.CharField(max_length=50,blank=True,null=True)
    USER_ID =  models.CharField(max_length=50,blank=True,null=True)
    EMAIL_ADDRESS = models.CharField(max_length=50,blank=True,null=True)
    FIRST_NAME = models.CharField(max_length=50,blank=True,null=True)
    LAST_NAME = models.CharField(max_length=50,blank=True,null=True)
    ROLE_NAME = models.CharField(max_length=100,blank=True,null=True)
    STATUS = models.CharField(max_length=50,blank=True,null=True)
    TYPE = models.CharField(max_length=50,blank=True,null=True) #USER_ACCOUNT, SYSTEM_ACCOUNT, OTHER
    OWNER_IF_SYSTEM = models.CharField(max_length=50,blank=True,null=True) 
    OWNER_IF_REGULAR = models.CharField(max_length=50,blank=True,null=True) 
    IS_ADMIN = models.CharField(max_length=50,blank=True,null=True)

    #PROVISIONING
    DATE_GRANTED = models.DateTimeField(null=True)
    DATE_APPROVED = models.DateTimeField(null=True)
    ACCESS_APPROVER_NAME1 = models.ForeignKey(HR_RECORD,on_delete=models.DO_NOTHING,max_length=100,blank=True,null=True, related_name='access_approver_name1')
    ACCESS_APPROVER_TITLE1 = models.ForeignKey(HR_RECORD,on_delete=models.DO_NOTHING,max_length=100,blank=True,null=True, related_name='access_approver_title1')
    ACCESS_APPROVER_NAME2 = models.ForeignKey(HR_RECORD,on_delete=models.DO_NOTHING,max_length=100,blank=True,null=True, related_name='access_approver_name2')
    ACCESS_APPROVER_TITLE2 = models.ForeignKey(HR_RECORD,on_delete=models.DO_NOTHING,max_length=100,blank=True,null=True,related_name='access_approver_title2')
    APPROVAL_TYPE = models.CharField(max_length=100,blank=True,null=True) #TICKET, EMAIL, OR OTHER
    APPROVAL_REFERENCE = models.CharField(max_length=100,blank=True,null=True)
    APPROVAL_SUPPORT = models.CharField(max_length=1000,blank=True,null=True)

    #TERMINATION
    DATE_REVOKED = models.DateTimeField(null=True)
    LAST_LOGIN = models.DateTimeField(null=True)
    HR_NOTIFICATION_DATE = models.DateTimeField(null=True)
    NOTIFICATION_TYPE = models.CharField(max_length=100,blank=True,null=True) #TICKET, EMAIL, OR OTHER
    NOTIFICATION_SUPPORT = models.CharField(max_length=100,blank=True,null=True) #LINK

    #USER ACCESS REVIEW
    DATE_LAST_CERTIFIED = models.DateTimeField(null=True)
    CERTIFIED_BY = models.CharField(max_length=50,blank=True,null=True)
    TAGGED_INAPPROPRITE = models.CharField(max_length=50,blank=True,null=True)
    DATE_TAGGED_INAPPROPRIATE = models.DateTimeField(null=True)

    #MAPPING TO HR
    MAPPED_TO_HR = models.CharField(max_length=50,blank=True,null=True)
    MAPPED_HR_FNAME = models.CharField(max_length=50,blank=True,null=True)
    MAPPED_HR_LNAME = models.CharField(max_length=50,blank=True,null=True)
    MAPPED_HR_EMAIL = models.CharField(max_length=50,blank=True,null=True)
    MAPPED_USING = models.CharField(max_length=100,blank=True,null=True)

    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return f"{self.APP_NAME} - {self.USER_ID}" 
    
    def approval_duration(self):
        if self.DATE_APPROVED and self.DATE_GRANTED:
            duration = self.DATE_APPROVED - self.DATE_GRANTED
            return duration.days
        return None
    
    class Meta:
        managed = True
        db_table = 'APP_RECORD'

class CSV_UPLOAD_FIELDS(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    APP_NAME = models.ForeignKey(APP_LIST,on_delete=models.CASCADE,max_length=100,blank=True,null=True)
    FIELD_NAME = models.CharField(max_length=128,blank=True,null=True)
    DATE = models.DateTimeField(null=True, blank=True)

     #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)

    class Meta:
        managed = True
        db_table = 'CSV_UPLOAD_FIELDS'

class CSV_MAPPING_TABLE(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    APP_NAME = models.ForeignKey(APP_LIST,on_delete=models.CASCADE,max_length=100,blank=True,null=True)
    USER_ID = models.CharField(max_length=128,blank=True,null=True)
    FIRST_NAME = models.CharField(max_length=128,blank=True,null=True)
    LAST_NAME = models.CharField(max_length=128,blank=True,null=True)
    ROLE = models.CharField(max_length=128,blank=True,null=True)
    STATUS = models.CharField(max_length=128,blank=True,null=True)
    DATE_GRANTED = models.CharField(max_length=128,blank=True,null=True)
    DATE_REVOKED = models.CharField(max_length=128,blank=True,null=True)
    LAST_LOGIN = models.CharField(max_length=128,blank=True,null=True)

     #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)

    class Meta:
        managed = True
        db_table = 'CSV_MAPPING_TABLE'


class ADMIN_ROLES_FILTER(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    APP_NAME = models.ForeignKey(APP_LIST,on_delete=models.CASCADE,max_length=100,blank=True,null=True)
    ROLE_NAME = models.CharField(max_length=50,blank=True,null=True)
    SETUP_COMPLETE = models.BooleanField(default=False,null=True)

    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)

    class Meta:
        managed = True
        db_table = 'ADMIN_ROLE_FILTER'


class SYSTEM_ACCOUNTS(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    APP_NAME = models.ForeignKey(APP_LIST,on_delete=models.CASCADE,max_length=100,blank=True,null=True)
    USER_ID = models.ForeignKey(APP_RECORD,on_delete=models.CASCADE,max_length=100, blank=True,null=True)
    IS_SYSTEM_ACCOUNT = models.BooleanField(blank=True, null=True)

    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)

class INTEGRATION_ACCOUNTS(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    APP_NAME = models.ForeignKey(APP_LIST,on_delete=models.CASCADE,max_length=100,blank=True,null=True)
    USER_ID = models.ForeignKey(APP_RECORD,on_delete=models.CASCADE,max_length=100, blank=True,null=True)
    IS_INTEGRATION_ACCOUNT = models.BooleanField(blank=True, null=True)

    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)

class APP_USER_UPLOAD(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_name = models.FileField(upload_to='app_users/')
    APP_NAME = models.ForeignKey(APP_RECORD,on_delete=models.CASCADE,max_length=100,blank=True,null=True)
    activated = models.BooleanField(default=False)
    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return f"{self.file_name}"  
    
    class Meta:
        managed = True
        db_table = 'USER_UPLOAD_ATTACHMENTS'

class APP_NEW_USER_APPROVAL(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_name = models.FileField(upload_to='new_users_approval/')
    USER_ID = models.ForeignKey(APP_RECORD,on_delete=models.CASCADE,max_length=100,blank=True,null=True)
    activated = models.BooleanField(default=False)
    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return f"{self.file_name}"  
    
    class Meta:
        managed = True
        db_table = 'NEW_USER_APPROVAL'
        
class CSV(models.Model):
    file_name = models.FileField(upload_to='csvs')
    upload_date = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"File id: {self.id}"

    
class PWCONFIGATTACHMENTS(models.Model):
    APP_NAME = models.ForeignKey(APP_LIST,on_delete=models.CASCADE,null=True)
    file_name = models.FileField(upload_to='pwconfigs/',null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"File id: {self.id}"
    

class CONTROLS(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    COMPANY_ID = models.ForeignKey(COMPANY,on_delete=models.CASCADE)
    CONTROL_ID = models.CharField(max_length=50,blank=True,null=True)
    CONTROL_NAME = models.CharField(max_length=50,blank=True,null=True)
    CONTROL_DESCRIPTION = models.CharField(max_length=50,blank=True,null=True)
    APP_NAME = models.ManyToManyField(APP_RECORD)

    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
            return self.CONTROL_NAME
    
    class Meta:
        managed = True
        db_table = 'CONTROLS'
    
class POLICIES(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    POLICY_NAME = models.CharField(max_length=50,blank=True,null=True)
    POLICY_DESCRIPTION = models.CharField(max_length=1000,blank=True,null=True)
    CONTROL_ID = models.ManyToManyField(CONTROLS)
    LAST_UPDATED = models.DateField(null=True)
  
    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
            return self.POLICY_NAME
    
    class Meta:
        managed = True
        db_table = 'POLICIES'


#MODELS FOR THE POLICIES ARE SAVED IN HERE

class PASSWORDPOLICY(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    COMPANY_ID = models.ManyToManyField(COMPANY,blank=True,null=True)
    COMPLEXITY_ENABLED = models.BooleanField(default=False) 
    LENGTH = models.IntegerField(blank=True, null=True)
    UPPER = models.BooleanField(default=False) 
    LOWER = models.BooleanField(default=False) 
    NUMBER = models.BooleanField(default=False) 
    SPECIAL_CHAR = models.BooleanField(default=False)  
    AGE = models.IntegerField(blank=True, null=True)
    HISTORY = models.IntegerField(blank=True, null=True)
    LOCKOUT_ATTEMPT = models.IntegerField(blank=True, null=True)
    LOCKOUT_DURATION = models.CharField(max_length=50, blank=True, null=True)
    MFA_ENABLED = models.BooleanField(default=False) 
    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True) 

def __str__(self):
    return str(self.id)

class Meta:
        managed = True
        db_table = 'PASSWORDPOLICY'


class PROVISIONINGPOLICY(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    APP_NAME = models.ForeignKey(APP_LIST, on_delete=models.CASCADE, null=True, blank=True)
    REQ_APPROVAL = models.BooleanField(null=True,blank=False)
    REQ_APPROVAL_RATIONALE = models.CharField(max_length=1000,null=True,blank=True)
    MANAGER_APPROVAL = models.BooleanField(null=True, blank=True)
    IT_APPROVAL = models.BooleanField(null=True, blank=True)
    BOTH_MANAGER_IT = models.BooleanField(null=True, blank=True)
    SETUP_COMPLETE = models.BooleanField(default=False,null=True, blank=True)
    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True) 

class TERMINATIONPOLICY(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    APP_NAME = models.ForeignKey(APP_LIST, on_delete=models.CASCADE, null=True, blank=True)
    DAYS_TO_TERMINATE = models.IntegerField(blank=True, null= True)
    WHO_NOTIFY_HR = models.BooleanField(null=True,blank=True)
    WHO_NOTIFY_MANAGER = models.BooleanField(null=True,blank=True)
    WHO_NOTIFY_AUTOMATED = models.BooleanField(null=True,blank=True)
    HOW_NOTIFY_EMAIL = models.BooleanField(null=True,blank=True)
    HOW_NOTIFY_VERBAL = models.BooleanField(null=True,blank=True)
    HOW_NOTIFY_AUTOMATED = models.BooleanField(null=True,blank=True)

     #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True) 

class Meta:
        managed = True
        db_table = 'TERMINATIONPOLICY'
    
class PASSWORD(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    APP_NAME = models.ForeignKey(APP_LIST, on_delete=models.CASCADE, blank=True, null=True)
    CONTROL_ID = models.ForeignKey(CONTROLS, on_delete=models.CASCADE, blank=True, null=True)
    COMPLEXITY_ENABLED = models.BooleanField(default=False) 
    LENGTH = models.IntegerField(blank=True, null=True)
    UPPER = models.BooleanField(default=False) 
    LOWER = models.BooleanField(default=False) 
    NUMBER = models.BooleanField(default=False) 
    SPECIAL_CHAR = models.BooleanField(default=False)  
    AGE = models.IntegerField(blank=True, null=True)
    HISTORY = models.IntegerField(blank=True, null=True)
    LOCKOUT_ATTEMPT = models.IntegerField(blank=True, null=True)
    LOCKOUT_DURATION = models.CharField(max_length=50, blank=True, null=True)
    MFA_ENABLED = models.BooleanField(default=False)
    AUTH_METHOD = models.CharField(max_length=50,blank=True,null=True)
    SETUP_COMPLETE = models.BooleanField(default=False,null=True)  
    #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)

def __str__(self):
    return str(self.CONTROL_ID)

class Meta:
        managed = True
        db_table = 'PASSWORD'

class TERMINATION(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CONTROL_ID = models.ForeignKey(CONTROLS,on_delete=models.DO_NOTHING)
    REQUIRED_DAYS = models.IntegerField(null=True)

     #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
            return self.REQUIRED_DAYS
    
    class Meta:
        managed = True
        db_table = 'TERMINATION'
    
class PROVISIONING(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CONTROL_ID = models.ForeignKey(CONTROLS,on_delete=models.DO_NOTHING)
    REQUIRED_APPROVERS = models.CharField(max_length=50,blank=True,null=True)

     #LOG
    CREATED_BY = models.CharField(max_length=50,blank=True,null=True)
    CREATED_ON = models.DateField(auto_now_add=True,null=True,blank=True)
    LAST_MODIFIED = models.DateTimeField(null=True)
    MODIFIED_BY = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
            return self.REQUIRED_APPROVERS
    
    class Meta:
        managed = True
        db_table = 'PROVISIONING'


    
