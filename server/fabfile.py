import os, re
from datetime import datetime
from fabric.api import *

_TAR_FILE = 'dist/distribution.tar.gz'

def build():
    includes = ['config', 'instance', 'myapi', 'server', '*.py']
    excludes = ['.*', '*.pyc', '*.pyo']
    local('rm -f {}'.format(_TAR_FILE))
    with lcd(os.path.abspath('..')):
        cmd = ['tar', '--dereference', '-czvf', _TAR_FILE]
        cmd.extend(['--exclude=\'{}\''.format(ex) for ex in excludes])
        cmd.extend(includes)
        local(' '.join(cmd))

env.host_string = 'root@101.37.33.55'
env.password = 'hiPpo111'
_REMOTE_TMP_TAR = '/root/myproject/{}'.format(_TAR_FILE)
_REMOTE_BASE_DIR = '/root/myproject'

def deploy():
    # newdir = 'www-%s' % datetime.now().strftime('%y-%m-%d_%H.%M.%S')
    # run('rm -f %s' % _REMOTE_TMP_TAR)

    with lcd(os.path.abspath('..')):
        put(_TAR_FILE, _REMOTE_TMP_TAR)

    with cd(_REMOTE_BASE_DIR):
    #     sudo('mkdir %s' % newdir)

    # with cd('%s/%s' % (_REMOTE_BASE_DIR, newdir)):
        sudo('tar -xzvf %s' % _REMOTE_TMP_TAR)

    # with cd(_REMOTE_BASE_DIR):
    #     sudo('rm -f www')
    #     sudo('ln -s %s www' % newdir)
    #     sudo('chown www-data:www-data www')
    #     sudo('chown -R www-data:www-data %s' % newdir)

    # with settings(warn_only=True):
    #     sudo('supervisorctl stop awesome')
    #     sudo('supervisorctl start awesome')
    #     sudo('/etc/init.d/nginx reload')
