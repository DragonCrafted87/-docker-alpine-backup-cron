#!/usr/bin/python3

# System Imports
import distutils.log

from os import getenv
from pathlib import PurePath
from tarfile import open as tar_open
from shutil import move
from datetime import datetime
from distutils.dir_util import copy_tree
from distutils.dir_util import remove_tree
from logging import INFO

# Local Imports
from python_logger import create_logger

def main():
    logger = create_logger(PurePath(__file__).stem)

    logger.setLevel(INFO)
    distutils.log = logger

    base_backup_name = getenv('BACKUP_NAME','minecraft-vanillaplusplus-backup')

    date_stamp = datetime.now().strftime("%G-W%V-%u-%H-%M-%S")
    backup_name = f'{base_backup_name}-{date_stamp}.tar.xz'
    create_backup_path = f'/mnt/{backup_name}'
    backup_path = '/mnt/source/'
    final_backup_destination = f'/mnt/backups/{backup_name}'
    temp_path = '/mnt/tmp/'

    remove_tree(temp_path)

    copy_tree(
      backup_path,
      temp_path
    )

    logger.info('Creating Backup')

    with tar_open(create_backup_path, 'w:xz') as tar:
        tar.add(f'{temp_path}.', arcname='')

    logger.info('Moving Backup')
    move(create_backup_path, final_backup_destination)

    logger.info('Successfully executed cron job')

if __name__ == '__main__':
    main()
