import os
from fabric.api import *

env.guest_user = 'ubuntu'  # Remote user
env.hosts = '192.168.50.11'  # Remote host or hosts
env.ssh_key_dir = '~/.ssh'  # Ssh keys directory on local and remote hosts
env.password = 'ubuntu'  # User password


def bootstrap():
    env.ssh_key_filepath = os.path.join(env.ssh_key_dir, env.host_string + "_key")
    local('ssh-keygen -t rsa -b 2048 -f {}'.format(env.ssh_key_filepath))
    upload_keys(env.guest_user)
    run('service ssh reload')


def upload_keys(username):
    scp_command = "scp {} {}@{}:~/.ssh/".format(
        env.ssh_key_filepath + ".pub",
        username,
        env.host_string
    )
    ssh_copy_id_command = "ssh-copy-id -i {} {}@{}".format(
        env.ssh_key_filepath + ".pub",
        username,
        env.host_string
    )
    local(scp_command)
    local(ssh_copy_id_command)
