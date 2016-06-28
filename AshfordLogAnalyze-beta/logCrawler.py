
import paramiko,time,datetime
import ConfigParser
import os
config = ConfigParser.RawConfigParser()
config.read('conf.properties')

instancesConf=config.get('General', 'instances').strip()
username=config.get('LogInfo', 'username').strip()
password=config.get('LogInfo', 'password').strip()
logRemainDate =config.get('General', 'logRemainDate').strip()
localDirectory=config.get('General', 'localDirectory').strip()
logLevel=config.get('General', 'logLevel').strip()
def download_file(instance,line):
    print 'downloading ' + line + '...'
    filelocalPath = localDirectory + instance + '/'
    d = os.path.dirname(filelocalPath)
    if not os.path.exists(d):
        os.makedirs(d)
    ftp.get(logpath + '/' + line,
            filelocalPath + line)

def isServerLog(line):
    types = logLevel.split(' ')
    line = str(line)
    for type in types:
        isHit = isDownloadLogType(line,type)
        if(isHit):
            return True
    return

def isDownloadLogType(line,type):
    strlogFormat = type+'.log'
    if strlogFormat in line:
        try:
            if len(line) > len(strlogFormat):
                if line == strlogFormat + '.gz':
                    return True
                if '.gz' in line:
                    filedateStr = line[len(strlogFormat)+1:-3]
                else:
                    filedateStr = line[len(strlogFormat)+1:]
                if len(filedateStr) > 10:
                    filedateStr = filedateStr[:-7]
                fileTimeStamp = time.mktime(datetime.datetime.strptime(filedateStr, "%Y-%m-%d").timetuple())
                currentTimeStamp = time.time()
                if currentTimeStamp - fileTimeStamp <= 86400 * int(logRemainDate):
                    return True
            else:
                return True
        except Exception:
             print("Unsupport file format: " + line + "::" + filedateStr)
             return

def connectFTP(ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, username=username, password=password)
    ftp = ssh.open_sftp()
    return ftp



instances = instancesConf.split(' ')
for instance in instances:
    instanceKeyPair = config.get('LogInfo', instance).strip()
    ip = instanceKeyPair.split(':')[0]
    logpath = instanceKeyPair.split(':')[1]
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, username=username, password=password)
    ftp = ssh.open_sftp()
    dirlist = ftp.listdir(logpath)
    print ('Check the logs of last '+ str(logRemainDate) +' days on server of '+ instance + ' Waiting ... ')
    for line in dirlist:
        line = str(line)
        if(isServerLog(line)):
            download_file(instance,line)



