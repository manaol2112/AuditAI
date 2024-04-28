import csv
import json
import pytesseract
import re
import random
import string

from datetime import datetime
from os.path import basename
from django.template.loader import render_to_string
from PIL import Image
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils import timezone
from django.views import View
from appAUDITAI.CSV.csvuploadform import CSVModelForm, APP_USER_UPLOAD_FORM
from appAUDITAI.CSV.filuploadform import NEW_USER_APPROVAL_FORM, PWCONFIG_MODELFORM
from appAUDITAI.dataview.APP.forms.applications_form import MappedUser, NewAPP, TagUnmappedUser
from appAUDITAI.dataview.LOGIN.views.decorators import ProcessOwnerPermissionMixin
from appAUDITAI.models import (ADMIN_ROLES_FILTER, APP_LIST, APP_NEW_USER_APPROVAL,
                               APP_RECORD, APP_USER_UPLOAD, COMPANY, CSV, HR_RECORD,
                               PASSWORD, PWCONFIGATTACHMENTS, USERROLES,PASSWORDCONFIG,APP_USER_SFTP,APP_JOB_PULL,PROVISIONINGPOLICY, TERMINATIONPOLICY)
from django.http import JsonResponse
import paramiko
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages
import logging
from django.core.exceptions import ValidationError
from datetime import datetime
import pysftp
