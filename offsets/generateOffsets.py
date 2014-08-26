
from subprocess import *
import pdbparse
from glob import glob
import os
import sys
import shutil
import win32api
import urllib2
from StringIO import StringIO
from hashlib import sha1

class Offsets(object):
    def __init__(self, name, nullAll=False):
        self.name = name
        if nullAll:
            self.version = (0, 0, 0, 0)
            self.kthread = 0
            self.ktrap_frame_size = 0
            self.eflags = 0
            self.ThreadListEntry = 0
            self.Teb = 0
            self.CrossThreadFlags = 0
            self.InitialStack = 0
            self.Cid = 0
            self.DirectoryTableBase = 0
            self.ThreadListHead = 0

    def __repr__(self):
        offsets_code = ''
        offsets_code += "\t/* %s */\n" % self.name
        offsets_code += "\t{\n"
        offsets_code += "\t\t{%d, %d, %d, %d},\n" % tuple(self.version)
        offsets_code += "\t\t{0x%x},\n" % (self.kthread)
        offsets_code += "\t\t{0x%x, 0x%x},\n" % (self.ktrap_frame_size, self.eflags)
        offsets_code += "\t\t{0x%x, 0x%x, 0x%x, 0x%x, 0x%x},\n" % (self.ThreadListEntry, self.Teb, self.CrossThreadFlags, self.InitialStack, self.Cid)
        offsets_code += "\t\t{0x%x, 0x%x},\n"         % (self.DirectoryTableBase, self.ThreadListHead)
        offsets_code += "\t},\n"
        return offsets_code

def checkout_pdb(exe_file):
    folder = os.path.dirname(exe_file)
    file_name = os.path.basename(exe_file)
    target = exe_file.replace('.exe', '.pdb')
    if os.path.isfile(target):
        #print "Alread checked out %s" % target
        return target
    print "Checkingout pdb for %s" % exe_file
    temp_folder = folder + os.sep + 'temp'
    if not os.path.isdir(folder + os.sep + 'temp'):
        os.mkdir(folder + os.sep + 'temp')
    Popen('symchk /ocx %s %s' % (temp_folder, exe_file), shell=True).communicate()
    target = exe_file.replace('.exe', '.pdb')
    temp_pdb = glob(temp_folder + os.sep + "*.pdb")
    if 1 != len(temp_pdb):
        return None
    os.rename(glob(temp_folder + os.sep + '*.pdb')[0], target)
    for deleteMe in glob(temp_folder + os.sep + '*.exe'):
        os.remove(deleteMe)
    return target

def getOffset(types, structName, varName):
    for t in types:
        if t.leaf_type=="LF_STRUCTURE" or t.leaf_type=="LF_UNION":
            if t.name == structName:
                for var in t.fieldlist.substructs:
                    if var.name == varName:
                        return var.offset
                raise Exception("Var not found in struct (%s, %s)" % (structName, varName))
    raise Exception("Struct not found (%s)" % (structName))

def getStructSize(types, structName):
    for t in types:
        if t.leaf_type=="LF_STRUCTURE" or t.leaf_type=="LF_UNION":
            if t.name == structName:
                return t.size
    raise Exception("Struct not found (%s)" % structName)

def getAllOffsets(filesLocation):
    allOffsets32 = []
    allOffsets64 = []
    for ntos in glob(filesLocation + os.sep + 'ntoskrnl*.exe'):
        offsets = Offsets(ntos)
        # 1. Get Ntos version
        versionInfo = win32api.GetFileVersionInfo(ntos, '\\')
        offsets.version = [
                versionInfo['FileVersionMS'] >> 16, 
                versionInfo['FileVersionMS'] & 0xff, 
                versionInfo['FileVersionLS'] >> 16, 
                versionInfo['FileVersionLS'] & 0xff ]
        print "Parsing file: %s of version %s" % (ntos, repr(offsets.version))
        # 2. Get PDB
        pdb_file = checkout_pdb(ntos)
        if None == pdb_file:
            print "Failed to get PDB for %s" % ntos
            continue
        pdb = pdbparse.parse(pdb_file)
        types = pdb.streams[2].types.values()
        # 3. Find intresting offsets
        try:
            prcbDataOffset = getOffset(types, '_KPCR', 'PrcbData')
        except:
            if 'x86' in ntos:
                prcbDataOffset = 0x120
            elif 'x64' in ntos:
                prcbDataOffset = 0x180
            else:
                raise Exception("WTF")
        offsets.kthread =  prcbDataOffset +\
                  getOffset(types, '_KPRCB', 'CurrentThread')
        
        if 'x86' in ntos:
            offsets.ktrap_frame_size = 0x29c
        elif 'x64' in ntos:
            offsets.ktrap_frame_size = getStructSize(types, '_KTRAP_FRAME')
        else:
            raise Exception("WTF")
        offsets.eflags              = getOffset(types, '_KTRAP_FRAME', 'EFlags')
        offsets.ThreadListEntry     = getOffset(types, '_ETHREAD',  'ThreadListEntry')
        offsets.Teb                 = getOffset(types, '_KTHREAD',  'Teb')
        offsets.CrossThreadFlags    = getOffset(types, '_ETHREAD',  'CrossThreadFlags')
        offsets.InitialStack        = getOffset(types, '_KTHREAD',  'InitialStack')
        offsets.Cid                 = getOffset(types, '_ETHREAD',  'Cid')
        offsets.DirectoryTableBase  = getOffset(types, '_KPROCESS', 'DirectoryTableBase')
        offsets.ThreadListHead      = getOffset(types, '_EPROCESS', 'ThreadListHead')
        # 4. Generate code
        if 'x86' in ntos:
            allOffsets32.append(offsets)
        elif 'x64' in ntos:
            allOffsets64.append(offsets)
        else:
            raise Exception("WTF")
    return (allOffsets32, allOffsets64)

def parseDriveData(data):
    START_PATTERN = "viewerItems: ["
    END_PATTERN = "]\n,};"
    startPos = data.find(START_PATTERN)
    if -1 == startPos:
        return None
    startPos += len(START_PATTERN)
    endPos = data.find(END_PATTERN, startPos)
    if -1 == endPos:
        return None
    data = data[startPos:endPos]
    pos = data.find('[')
    endPos = data.find(']', pos)
    files = []
    while pos != -1:
        line = data[pos+1:endPos]
        line = line.split(',')
        fname = line[2].replace('"', '').replace(',', '')
        fid = line[7].replace('"', '').replace(',', '')
        files.append((fname, fid))
        pos = data.find('[', pos+1)
        endPos = data.find(']', pos)
    return files
    
def downloadDriveFile(fileId, target):
    print "Downloading %s" % os.path.basename(target)
    remote = urllib2.urlopen("https://docs.google.com/uc?export=download&id=" + fileId)
    file(target, 'wb').write(remote.read())
    remote.close()
    
def downloadDlls(url, localDir):
    url = urllib2.urlopen(url)
    data = url.read()
    url.close()
    remoteFiles = parseDriveData(data)
    if not os.path.isdir(localDir):
        os.mkdir(localDir)
    localFiles = [os.path.basename(x) for x in glob(localDir + os.sep + '*.exe')]
    for fileName, fileId in remoteFiles:
        if fileName not in localFiles:
            downloadDriveFile(fileId, localDir + os.sep + fileName)
    
def shouldRecreate(outputFile, data):
    searchFor = '// data hash: '
    if not os.path.isfile(outputFile):
        return True
    line = ''
    for line in file(outputFile, 'rb').readlines():
        if line.startswith(searchFor):
            break
    if not searchFor.startswith(searchFor):
        return True
    currentHash = sha1(data).digest().encode('hex')
    oldHash = line[len(searchFor):][:len(currentHash)]
    if currentHash != oldHash:
        return True
    return False

def makeOffsetsFile(allOffsets, outputFile):
    allData = ''.join([repr(x) for x in allOffsets])
    if shouldRecreate(outputFile, allData):
        output = file(outputFile, 'wb')
        output.write("// data hash: %s\n" % sha1(allData).digest().encode('hex'))
        output.write('\n')
        output.write("/* This file is auto generated, do not change it. */\n")
        output.write("windows_offsets all_offsets[] = {\n")
        for offsets in allOffsets:
            output.write(repr(offsets))
        empty = Offsets("EMPTY", nullAll=True)
        output.write(repr(empty))
        output.write('};\n')
        output.close()

os.chdir(os.path.dirname(os.path.abspath(__file__)))
downloadDlls('https://drive.google.com/folderview?id=0B5833Zxi4DMTNk1LOWkyak9OQWM&usp=sharing', 'NtosVersions')
allOffsets = getAllOffsets('NtosVersions')
makeOffsetsFile(allOffsets[0], os.sep.join(['..', 'tracer', 'offsets_X86.auto.h']))
makeOffsetsFile(allOffsets[1], os.sep.join(['..', 'tracer', 'offsets_AMD64.auto.h']))

