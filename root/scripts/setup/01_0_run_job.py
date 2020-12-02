#!/usr/bin/python3

# System Imports
from os import getenv
from pathlib import PurePath
from tarfile import open as tar_open
from shutil import move

# 3rd Party Imports
from mcrcon import MCRcon

# Local Imports
from python_logger import create_logger

def main():
  logger = create_logger(PurePath(__file__).stem)

  date_stamp = datetime.now().strftime("%G-W%V-%u-%H-%M-%S")
  backup_name = f'minecraft-vanillaplusplus-backup-{date_stamp}.tar.lzma'
  create_backup_path = f'/mnt/minecraft/{backup_name}'
  backup_path = '/mnt/minecraft/world/.'
  final_backup_destination = f'/mnt/backups/{backup_name}'

  with MCRcon("192.168.8.3", "rcon") as mcr:
    resp = mcr.command("save-off")
    logger.info(resp)
    resp = mcr.command("save-all")
    logger.info(resp)

    logger.info('Creating Backup')

    with tar_open(create_backup_path, 'w:xz') as tar:
      tar.add(backup_path)

    resp = mcr.command("save-on")
    logger.info(resp)

  logger.info('Moving Backup')
  move(create_backup_path, final_backup_destination)

  logger.info(f'Successfully executed cron job')

if __name__ == '__main__':
  main()
