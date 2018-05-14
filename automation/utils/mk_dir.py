# -*- coding: utf-8 -*-
import logging
import paramiko

def mk_dir(username, hostname):

    # setup a SSHClient object
    ssh = paramiko.SSHClient()

    # 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # connect to host
    try:
        ssh.connect(hostname=hostname, port=22, username='seluser', password='seluser')
    except Exception as e:
        logging.error(e)
    else:
        dir_name = '/home/seluser/Downloads/' + username

        try:
            stdin, stdout, stderr = ssh.exec_command('mkdir ' + dir_name)
        except Exception as e:
            logging.error(e)

        # logging the output
        logging.debug('stdout: %s, \nstderr: %s'%(stdout, stderr))
    # close the connection
    ssh.close()

    return dir_name