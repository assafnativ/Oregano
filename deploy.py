import baker
import rpyc
import time
from glob import glob
import sys
import os

def uploadFile(src, target, remote):
    if remote.modules.os.path.isfile(target):
        try:
            remote.modules.os.remove(target)
        except:
            tempName = target
            pos = tempName.rfind('.')
            if -1 == pos:
                tempName += str(int(time.time()))
            else:
                tempName = tempName[:pos] + str(int(time.time())) + tempName[pos:]
            remote.modules.os.rename(target, tempName)
    targetPath = remote.modules.os.path.dirname(target)
    if '' != targetPath:
        if not remote.modules.os.path.isdir(targetPath):
            remote.modules.os.makedirs(targetPath)
    print "Uploading %s to %s" % (src, target)
    remote.builtins.open(target, 'wb').write(
            open(src, 'rb').read())

def uploadDir(src, target, remote, filterTempFiles=True):
    for fileName in glob(src + '\\*'):
        baseName = os.path.basename(fileName)
        if filterTempFiles:
            if fileName.endswith('~'):
                continue
            if fileName.endswith('.pyc'):
                continue
            if fileName.endswith('.bak'):
                continue
        if os.path.isdir(fileName):
            uploadDir(fileName, target + '\\' + baseName, remote)
        else:
            uploadFile(fileName, target + '\\' + baseName, remote)

def getConnection(target=None):
    if None == target:
        target = 'win8tester'
    return rpyc.classic.connect(target)
    

@baker.command
def updateDriver(target=None, debug=True):
    FILES_TO_DEPLOY = ['Oregano.sys', 'Oregano.pdb', 'Oregano.inf']
    remote = getConnection(target)
    print "Deploing to %s" % target
    remote.modules.os.system('sc stop oregano')
    is64 = '64' in remote.modules.platform.machine()
    binaryDir = 'output\\'
    if is64:
        binaryDir += 'AMD64\\'
    else:
        binaryDir += 'x86\\'
    if debug:
        binaryDir += 'Debug\\'
    else:
        binaryDir += 'Release\\'
    targetDir = 'C:\\Program Files\\'
    for fileName in FILES_TO_DEPLOY:
        uploadFile(binaryDir + fileName, targetDir + fileName, remote)
    remote.modules.os.system('c:\System32\InfDefaultInstall.exe %soregano.inf' % targetDir)
    remote.modules.os.system('sc start oregano')
    remote.close()

@baker.command
def updatePython(target=None):
    remote = getConnection(target)
    src = 'PyOregano'
    dst = 'c:\\temp\\pyOregano'
    uploadDir(src, dst, remote)
    remote.modules.os.chdir('c:\\temp\\pyOregano')
    print "Installing Oregano Python module"
    remote.modules.os.system('python setup.py install')
    remote.close()

@baker.command
def updateTests(target=None):
    remote = getConnection(target)
    uploadDir('tests', 'c:\\temp\\tests', remote)
    remote.close()

@baker.command
def updateAll(target=None, debug=True):
    updateDriver(target, debug)
    updatePython(target)
    updateTests(target)

@baker.command
def runTest(testName=None, target=None):
    remote = getConnection(target)
    print "Running tests on %s" % target
    if None == testName:
        testName = 'notepadTest.py'
    testFile = 'tests\\' + testName
    remoteDir = 'c:\\temp\\tests'
    remoteFile = remoteDir + '\\' + testName
    uploadFile(testFile, remoteFile, remote)
    originalStdout = remote.modules.sys.stdout
    originalStdin  = remote.modules.sys.stdin
    originalStderr = remote.modules.sys.stderr
    remote.modules.sys.stdout = sys.stdout
    remote.modules.sys.stdin  = sys.stdin
    remote.modules.sys.stderr = sys.stderr
    remote.builtins.execfile(remoteFile)
    remote.modules.sys.stdout = originalStdout
    remote.modules.sys.stdin  = originalStdin
    remote.modules.sys.stderr = originalStderr
    remote.close()

@baker.command
def restart(target=None):
    remote = getConnection(target)
    remote.modules.os.system('shutdown /r /t 1')
    remote.close()

baker.run()
