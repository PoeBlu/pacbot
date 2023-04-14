from core.terraform.resources.aws.s3 import S3BucketObject
from resources.s3.bucket import BucketStorage
from core.terraform.utils import get_terraform_scripts_and_files_dir
from core.config import Settings
import os


BATCH_JOB_FILE_NAME = "pacbot-submitBatchjob"




class UploadLambdaSubmitJobZipFile(S3BucketObject):
    bucket = BucketStorage.get_output_attr('bucket')
    key = f"{Settings.RESOURCE_NAME_PREFIX}/{BATCH_JOB_FILE_NAME}.zip"
    source = os.path.join(
        get_terraform_scripts_and_files_dir(), f"{BATCH_JOB_FILE_NAME}.zip"
    )
