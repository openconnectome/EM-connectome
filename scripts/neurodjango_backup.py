#!/usr/bin/python
# Copyright 2014 NeuroData (http://neurodata.io)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import os
import sys
import subprocess
import boto3
import time
import socket
sys.path.append(os.path.abspath('../django'))
import ND.settings
import django
from django.conf import settings
from ndingest.settings.settings import Settings
ndingest_settings = Settings.load()
import logging

class S3BackupFile(object):

  def __init__(self):
    self.file_name = "{}{}_{}.sql".format(settings.TEMP_INGEST_PATH, socket.gethostname(), time.strftime('%Y_%m_%d_%H_%M_%S'))
    s3 = boto3.resource('s3', endpoint_url=ndingest_settings.S3_ENDPOINT, aws_access_key_id=ndingest_settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=ndingest_settings.AWS_SECRET_ACCESS_KEY)
    self.backup_object = s3.Object(ndingest_settings.S3_BACKUP_BUCKET, self.file_name.strip(settings.TEMP_INGEST_PATH))
    self.logger = logging.getLogger('neurodjango_backup')
    self.logger.setLevel(logging.INFO)
    file_handle = logging.FileHandler('/var/log/neurodata/neurodjango_backup.log')
    self.logger.addHandler(file_handle)

  def clean(self):
    try:
      os.remove(self.file_name)
    except Exception as e:
      self.logger.error("Error in cleaning file {}. {}".format(self.file_name, e))
      raise e

  def copy(self):
    try:
      self.backup_object.put(
          Body = open(self.file_name),
          StorageClass = 'STANDARD'
      )
    except Exception as e:
      self.logger.error("Error in copying file {}. {}".format(self.file_name, e))
      raise e

  def backup(self):
    try:
      self.logger.info("Dumping file {}".format(self.file_name))
      subprocess.call("mysqldump -u{} -p{} {} > {}".format(settings.DATABASES['default']['USER'], settings.DATABASES['default']['PASSWORD'], settings.DATABASES['default']['NAME'], self.file_name), shell=True)
      self.logger.info("Copying file {}".format(self.file_name))
      self.copy()
      self.logger.info("Cleaning file {}".format(self.file_name))
      self.clean()
    except Exception as e:
      self.logger.error("Error in backing up file {}. {}".format(self.file_name, e))
      raise e

def main():

  s3_backup_file = S3BackupFile()
  s3_backup_file.backup()

if __name__ == "__main__":
  main()
