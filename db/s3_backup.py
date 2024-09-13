import boto3
from botocore.exceptions import ClientError
import os
from core.config import settings
import threading
import time

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY
)

DB_FILENAME = 'sql_app.db'
S3_KEY = 'database_backup.db'

def backup_to_s3():
    try:
        s3_client.upload_file(DB_FILENAME, settings.BUCKET_NAME, S3_KEY)
        print(f"Database backed up to s3://{settings.BUCKET_NAME}/{S3_KEY}")
    except ClientError as e:
        print(f"Error backing up database to S3: {e}")

def restore_from_s3():
    try:
        s3_client.download_file(settings.BUCKET_NAME, S3_KEY, DB_FILENAME)
        print(f"Database restored from s3://{settings.BUCKET_NAME}/{S3_KEY}")
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The database backup does not exist in S3. Starting with a fresh database.")
        else:
            print(f"Error restoring database from S3: {e}")

def ensure_db_exists():
    if not os.path.exists(DB_FILENAME):
        restore_from_s3()
    else:
        print("Using existing local database file.")


def periodic_backup():
    while True:
        time.sleep(3600)  # Sleep for 1 hour
        backup_to_s3()

def start_periodic_backup():
    thread = threading.Thread(target=periodic_backup, daemon=True)
    thread.start()