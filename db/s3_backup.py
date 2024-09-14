import datetime
import os
import shutil
import tarfile
from pathlib import Path
import boto3
from botocore.client import Config
from core.config import settings
import logging
import tempfile
import platform


logger = logging.getLogger(__name__)

def backup_sqlite_to_s3():
    # Configuration
    aws_bucket = settings.BUCKET_NAME
    aws_folder = 'database_backups'
    db_path = Path(settings.LOCAL_DATABASE_URL.replace("sqlite:///", ""))
    
    try:
        # Use a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            backup_dir = Path(temp_dir)
            
            # Backup the database
            backup_file = backup_dir / db_path.name
            if platform.system() == 'Windows':
                os.system(f'sqlite3 "{db_path}" ".backup \'{backup_file}\'"')
            else:
                os.system(f"sqlite3 {db_path} .dump > '{backup_file}'")
            
            # Create archive
            today = datetime.date.today().isoformat()
            archive_name = f"{db_path.stem}_{today}.tar.gz"
            archive_path = backup_dir / archive_name
            
            with tarfile.open(archive_path, "w:gz") as tar:
                tar.add(backup_file, arcname=backup_file.name)
            
            logger.info(f"Created archive: {archive_path}")
            
            # Upload to S3
            s3_client = boto3.client(
                's3',
                 region_name="eu-north-1",
                aws_access_key_id=settings.S3_ACCESS_KEY,
                aws_secret_access_key=settings.S3_SECRET_KEY,
                config=Config(signature_version="s3v4"),
            )
            
            s3_key = f"{aws_folder}/{today}/{archive_name}"
            s3_client.upload_file(str(archive_path), aws_bucket, s3_key)
            
            logger.info(f"Uploaded {archive_name} to S3 bucket {aws_bucket}")
        
        logger.info("Backup completed successfully")
        
    except Exception as e:
        logger.error(f"Backup failed: {str(e)}")

def restore_from_s3():
    aws_bucket = settings.BUCKET_NAME
    aws_folder = 'database_backups'
    db_path = Path(settings.LOCAL_DATABASE_URL.replace("sqlite:///", ""))
    
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY
        )
        
        # List objects in the bucket to find the latest backup
        response = s3_client.list_objects_v2(Bucket=aws_bucket, Prefix=aws_folder)
        if 'Contents' in response:
            latest_backup = max(response['Contents'], key=lambda x: x['LastModified'])
            latest_key = latest_backup['Key']
            
            # Download the latest backup
            temp_dir = Path('/tmp/restore_db')
            temp_dir.mkdir(exist_ok=True)
            temp_file = temp_dir / "latest_backup.tar.gz"
            
            s3_client.download_file(aws_bucket, latest_key, str(temp_file))
            
            # Extract the backup
            with tarfile.open(temp_file, "r:gz") as tar:
                tar.extractall(path=temp_dir)
            
            # Restore the database
            extracted_db = next(temp_dir.glob("*.sqlite3"))
            shutil.copy(extracted_db, db_path)
            
            logger.info(f"Database restored from S3 backup: {latest_key}")
            
            # Clean up
            shutil.rmtree(temp_dir)
        else:
            logger.warning("No backups found in S3")
    
    except Exception as e:
        logger.error(f"Restore failed: {str(e)}")

def ensure_db_exists():
    db_path = Path(settings.LOCAL_DATABASE_URL.replace("sqlite:///", ""))
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY
    )
    
    try:
        # Check if there are any backups in S3
        response = s3_client.list_objects_v2(Bucket=settings.BUCKET_NAME, Prefix='database_backups')
        
        if 'Contents' in response and len(response['Contents']) > 0:
            logger.info("Existing backups found in S3. Attempting to restore.")
            restore_from_s3()
            logger.info("Database restored from S3 backup")
        else:
            logger.info("No existing backups found in S3.")
            if not db_path.exists():
                logger.info("Creating new empty database file")
                db_path.touch()
            else:
                logger.info("Using existing local database file")
            
            logger.info("Creating initial backup")
            backup_sqlite_to_s3()
    
    except Exception as e:
        logger.error(f"Error in ensure_db_exists: {str(e)}")
        if not db_path.exists():
            logger.info("Creating new empty database file due to error")
            db_path.touch()
        else:
            logger.info("Using existing local database file due to error")