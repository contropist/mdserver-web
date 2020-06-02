# coding:utf-8

import sys
import io
import os
import time
import shutil

sys.path.append(os.getcwd() + "/class/core")
import public

app_debug = False
if public.isAppleSystem():
    app_debug = True


def getPluginName():
    return 'shadowsocks'


def getPluginDir():
    return public.getPluginDir() + '/' + getPluginName()


def getServerDir():
    return public.getServerDir() + '/' + getPluginName()


def getArgs():
    args = sys.argv[2:]
    tmp = {}
    args_len = len(args)

    if args_len == 1:
        t = args[0].strip('{').strip('}')
        t = t.split(':')
        tmp[t[0]] = t[1]
    elif args_len > 1:
        for i in range(len(args)):
            t = args[i].split(':')
            tmp[t[0]] = t[1]

    return tmp


def checkArgs(data, ck=[]):
    for i in range(len(ck)):
        if not ck[i] in data:
            return (False, public.returnJson(False, '参数:(' + ck[i] + ')没有!'))
    return (True, public.returnJson(True, 'ok'))


def status():
    cmd = "ps -ef|grep ssserver |grep -v grep | awk '{print $2}'"
    data = public.execShell(cmd)
    if data[0] == '':
        return 'stop'
    return 'start'


def start():
    path = getPathFile()
    shell_cmd = 'ssserver -c ' + path + ' -d start'

    data = public.execShell(shell_cmd)

    if data[0] == '':
        return 'ok'
    return data[1]


def stop():
    path = getPathFile()
    shell_cmd = 'ssserver -c ' + path + ' -d stop'

    data = public.execShell(shell_cmd)
    if data[0] == '':
        return 'ok'
    return data[1]


def restart():
    path = getPathFile()
    shell_cmd = 'ssserver -c ' + path + ' -d restart'
    data = public.execShell(shell_cmd)
    if data[0] == '':
        return 'ok'
    return data[1]


def reload():
    path = getPathFile()
    shell_cmd = 'ssserver -c ' + path + ' -d restart'
    data = public.execShell(shell_cmd)
    if data[0] == '':
        return 'ok'
    return data[1]


def getPathFile():
    return getServerDir() + '/shadowsocks.json'


def getInitDTpl():
    path = getPluginDir() + "/init.d/" + getPluginName() + ".tpl"
    return path


def initDreplace():

    file_tpl = getInitDTpl()
    service_path = os.path.dirname(os.getcwd())

    initD_path = getServerDir() + '/init.d'
    if not os.path.exists(initD_path):
        os.mkdir(initD_path)
    file_bin = initD_path + '/' + getPluginName()

    # initd replace
    content = public.readFile(file_tpl)
    content = content.replace('{$SERVER_PATH}', service_path)
    public.writeFile(file_bin, content)
    public.execShell('chmod +x ' + file_bin)

    return file_bin


def getInitDFile():
    if app_debug:
        return '/tmp/' + getPluginName()
    return '/etc/init.d/' + getPluginName()


def initdStatus():
    if not app_debug:
        if public.isAppleSystem():
            return "Apple Computer does not support"
    initd_bin = getInitDFile()
    if os.path.exists(initd_bin):
        return 'ok'
    return 'fail'


def initdInstall():
    import shutil
    if not app_debug:
        if public.isAppleSystem():
            return "Apple Computer does not support"

    source_bin = initDreplace()
    initd_bin = getInitDFile()
    shutil.copyfile(source_bin, initd_bin)
    public.execShell('chmod +x ' + initd_bin)
    public.execShell('chkconfig --add ' + getPluginName())
    return 'ok'


def initdUinstall():
    if not app_debug:
        if public.isAppleSystem():
            return "Apple Computer does not support"

    public.execShell('chkconfig --del ' + getPluginName())
    initd_bin = getInitDFile()
    os.remove(initd_bin)
    return 'ok'

if __name__ == "__main__":
    func = sys.argv[1]
    if func == 'status':
        print status()
    elif func == 'start':
        print start()
    elif func == 'stop':
        print stop()
    elif func == 'restart':
        print restart()
    elif func == 'reload':
        print reload()
    elif func == 'conf':
        print getPathFile()
    elif func == 'initd_status':
        print initdStatus()
    elif func == 'initd_install':
        print initdInstall()
    elif func == 'initd_uninstall':
        print initdUinstall()
    else:
        print 'error'
