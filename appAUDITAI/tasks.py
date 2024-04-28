from celery import shared_task
import paramiko
from appAUDITAI.models import APP_USER_SFTP, APP_JOB_PULL, APP_JOB_USER_LOG, APP_RECORD, APP_LIST,APP_JOB_USER_LOG_PROCESS
import os
from paramiko.ssh_exception import SSHException
from datetime import datetime
from django.utils import timezone
import csv
from django.utils.timezone import make_aware


@shared_task
def fetch_files_from_sftp():
    current_day = datetime.now().strftime('%A').upper()
    # Get current time in HH:MM:SS format
    current_time = datetime.now().strftime('%H:%M:%S')
    # Truncate seconds and milliseconds and add :00
    current_time = current_time[:5] + ":00"

    # Check if there is a job scheduled for the current day and time
    scheduled_jobs = APP_JOB_PULL.objects.filter(
        **{current_day: True},  # Filter by the current day
        SCHEDULE_TIME=current_time  # Filter by the current time
    )

    if scheduled_jobs.exists():  # Check if there are any scheduled jobs for the current day and time
        try:
            for job in scheduled_jobs:
                job_name = str(job.id) + ("_") + str(job.JOB_NAME)
                for credential in APP_USER_SFTP.objects.filter(APP_NAME=job.APP_NAME):
                    host_name = credential.HOST_NAME
                    sftp_username = credential.SFTP_USERNAME
                    # Consider more secure options for storing passwords
                    sftp_password = 'Robertjohn89'
                    sftp_directory = credential.SFTP_DIRECTORY
                    sftp_destination = os.path.join(os.getcwd(), 'destination_folder', job_name.replace(
                        ' ', '_'))  # Default destination folder in project directory
                    if not os.path.exists(sftp_destination):
                        os.makedirs(sftp_destination)

                    job_log = APP_JOB_USER_LOG.objects.create(
                        APP_NAME=job.APP_NAME,
                        JOB_NAME=job,
                        JOB_FILE_DESTINATION=sftp_destination,
                        JOB_FILE_NAME=job_name,
                        JOB_DATE=timezone.now(),
                        JOB_COMPLETE=False
                    )
                    try:
                        # Establish SFTP connection
                        transport = paramiko.Transport((host_name, 22))
                        transport.connect(username=sftp_username, password=sftp_password)
                        sftp = paramiko.SFTPClient.from_transport(transport)
                        sftp.chdir(sftp_directory)

                        # Fetch files from SFTP server
                        files = sftp.listdir_attr()
                        latest_file = None
                        latest_mtime = None

                        for file_attr in files:
                            file_name = file_attr.filename
                            mtime = file_attr.st_mtime

                            if latest_mtime is None or mtime > latest_mtime:
                                latest_file = file_name
                                latest_mtime = mtime

                        if latest_file:
                            remote_file = os.path.join(sftp_directory, latest_file)
                            # Constructing local file path
                            local_file = os.path.join(sftp_destination, latest_file)
                            sftp.get(remote_file, local_file)
                            print(f"Latest file '{latest_file}' transferred successfully.")
                        else:
                            print("No files found on the SFTP server.")

                        # Close SFTP connection
                        sftp.close()
                        transport.close()
                        job_log.JOB_ERROR = None
                        job_log.JOB_COMPLETE = True
                        job_log.save()
                    except paramiko.AuthenticationException as auth_error:
                        job_log.JOB_COMPLETE = False
                        job_log.JOB_ERROR = auth_error
                        job_log.save()
                        print(f"Authentication failed: {auth_error}")
                    except paramiko.SSHException as ssh_error:
                        job_log.JOB_COMPLETE = False
                        job_log.JOB_ERROR = ssh_error
                        job_log.save()
                        print(f"SSH error: {ssh_error}")
                    except Exception as e:
                        job_log.JOB_COMPLETE = False
                        job_log.JOB_ERROR = str(e)
                        job_log.save()
                        print(f"An error occurred: {e}")
        except Exception as e:
            print(e)
    else:
        print("No scheduled job for the current day and time.")

def parse_date(date_string, formats):
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            pass
    # If none of the formats match, return a default value
    return datetime(1900, 1, 1)

@shared_task
def process_file_from_server():
    current_day = datetime.now().date()
    try:
        completed_job = APP_JOB_USER_LOG.objects.filter(JOB_COMPLETE=True)
        for job in completed_job:
            if job:
                raw_data_path = job.JOB_FILE_DESTINATION
                try:
                    files = [file for file in os.listdir(
                        raw_data_path) if file.endswith('.csv')]
                    if files:
                        if len(files) == 1:
                            latest_file = os.path.join(raw_data_path, files[0])
                        else:
                            latest_file = max(
                                (os.path.join(raw_data_path, file) for file in files), key=os.path.getmtime)
                        if latest_file.endswith('.csv'):
                            required_columns = ['USER_ID', 'EMAIL_ADDRESS', 'FIRST_NAME', 'LAST_NAME',
                                                'ROLE_NAME', 'STATUS', 'DATE_GRANTED', 'DATE_REVOKED', 'LAST_LOGIN']
                            
                            with open(latest_file, 'r', encoding='utf-8-sig') as csv_file:
                                csv_reader = csv.reader(csv_file)
                                header = next(csv_reader)  # Get the header row
                              
                                if all(column in header for column in required_columns):
                                    for i, row in enumerate(csv_reader):
                                       
                                        date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y%m%d", "%m/%d/%y"]
                                        DATE_GRANTED = row[6]
                                        DATE_REVOKED = row[7]
                                        LAST_LOGIN = row[8]

                                        try:
                                            DATE_GRANTED = parse_date(str(DATE_GRANTED), date_formats)
                                        
                                        except Exception as e:
                                            print("Error parsing DATE_GRANTED:", e)
                                            # Handle the error gracefully, for example, by setting a default value
                                            DATE_GRANTED = datetime(1900, 1, 1)
                                        try:
                                            DATE_REVOKED = parse_date(str(DATE_REVOKED), date_formats)
                                          
                                        except Exception as e:
                                            print("Error parsing DATE_REVOKED:", e)
                                            # Handle the error gracefully, for example, by setting a default value
                                            DATE_REVOKED = datetime(1900, 1, 1)
                                        try:
                                            LAST_LOGIN = parse_date(str(LAST_LOGIN), date_formats)
                              
                                        except Exception as e:
                                            print("Error parsing LAST_LOGIN:", e)
                                            # Handle the error gracefully, for example, by setting a default value
                                            LAST_LOGIN = datetime(1900, 1, 1)
      
                                        try:
                                            app_list_instance = APP_LIST.objects.get(
                                            id=job.APP_NAME_id)
                                        except APP_LIST.DoesNotExist:
                                            print('Error: Not app not found')
                                        except Exception as e:
                                            print(str(e))
                                               
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
                                            'CREATED_BY': 'system',
                                            'CREATED_ON': timezone.now()
                                        }
                                        
                                        try:
                                            user_record, created = APP_RECORD.objects.get_or_create(
                                                APP_NAME=app_list_instance,
                                                USER_ID=row[0],
                                                EMAIL_ADDRESS=row[1],
                                                ROLE_NAME=row[4],
                                                defaults=user_record_data # Data to update or create
                                            )
                                            if not created:
                                                for field, value in user_record_data.items():
                                                    setattr(user_record, field, value)
                                                user_record.MODIFIED_BY = 'system'
                                                user_record.LAST_MODIFIED = timezone.now()
                                                user_record.save()
                                        except Exception as e:
                                            job_log, created = APP_JOB_USER_LOG_PROCESS.objects.get_or_create(
                                                APP_NAME = app_list_instance,
                                                USER_ID = row[0],
                                                JOB_DATE = timezone.now(),
                                                JOB_FILE_DESTINATION = latest_file,
                                                JOB_ERROR = str(e),
                                                JOB_COMPLETE = False
                                            )
                                            pass
                                else:
                                    print(
                                        f'Not all required columns are present in the CSV file: {latest_file}')
                        else:
                            print(
                                f'The latest file {latest_file} is not a CSV')
                    else:
                        print('No files found in the folder')

                except Exception as e:
                    files = None
                    pass
            else:
                print('No job found')
    except APP_JOB_USER_LOG.DoesNotExist:
        print('Job does not exist')
        completed_job = None