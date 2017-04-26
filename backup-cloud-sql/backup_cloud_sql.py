"""This is a Google Cloud SQL for Backup and Restore tool

    * This code run on crontab of OpenVPN Server:
        (everyday at 4:00 am)
    * Get a backup_id for each instance
    * Restore the backup from production instance to cloned instance
"""
from subprocess import Popen, PIPE
import shlex


""" Configuration of HotelQuickly instances
"""
ALICE = 'alice-production-db'
ALICE_CLONE = 'alice-production-clone'
BRANDY = 'brandy-production-db'
BRANDY_CLONE = 'brandy-production-db-clone'


def get_backup_id(instance_name):
    """Get a backup_id from any instance

    Args:
        instance_name: identification of Cloud SQL instance

    Returns:
        The backup_id or None
    """
    args = shlex.split("gcloud beta sql backups list --instance %s" % instance_name)
    cmd = Popen(args, stdout=PIPE, stderr=PIPE)

    result = []

    for line in cmd.stdout.readlines():
        result.append(line)

    new = ''.join(result).split('\n')
    backup_id = new[1].split(' ')

    if backup_id[-1] == 'SUCCESSFUL':
        return backup_id[0]
    else:
        return None


def restore_backup(backup_id, backup_instance, restore_instance):
    """Restore a backup using a backup_id from production instance

    Args:
        backup_id: identification of Cloud SQL backup
        backup_instance: name of instance that have a backup
        restore_instance: name of instance to restore a backup
    """
    if backup_id is not None:
        if backup_instance == ALICE:
            target = open(ALICE, 'w')
            target.write("ALICE=%s" % backup_id)
            target.close()
        elif backup_instance == BRANDY:
            target = open(BRANDY, 'w')
            target.write("BRANDY=%s" % backup_id)
            target.close()
    else:
        if backup_instance == ALICE:
            target = open(ALICE, 'w')
            target.write('')
            target.close()
        elif backup_instance == BRANDY:
            target = open(BRANDY, 'w')
            target.write('')
            target.close()



if __name__ == '__main__':
    alice_backup_id = get_backup_id(ALICE)
    brandy_backup_id = get_backup_id(BRANDY)

    restore_backup(alice_backup_id, ALICE, ALICE_CLONE)
    restore_backup(brandy_backup_id, BRANDY, BRANDY_CLONE)
