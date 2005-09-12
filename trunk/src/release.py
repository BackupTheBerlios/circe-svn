#!/usr/bin/python

import shutil, os, tarfile, sys, ftplib, cStringIO as StringIO

def upload(path):
    ftp = ftplib.FTP('ftp.berlios.de')
    ftp.set_debuglevel(3)
    ftp.login()
    ftp.cwd('incoming')
    sio = StringIO.StringIO()
    ftp.retrlines("LIST", sio.write)
    print sio.getvalue()
    ftp.storbinary("STOR %s" % os.path.basename(path), open(path).read)
    ftp.quit()
    print "%s uploaded to ftp://ftp.berlios.de/incoming" % path
def export(src, dest):
    shutil.copytree(src, dest)
    
def prompt():
    rn = raw_input("Name of release: ")
    vn = raw_input("Version: ")
    return [rn, vn]
rn, vn = prompt()

name = "%s-%s" % (rn, vn)
path = "%s/%s" % (os.environ["HOME"], name)
tfpath = "%s.tar.gz" % path

print "Are you sure you want to make release %s? [y/N]" % name,

answer = raw_input()
answer = answer.lower()
if not answer or answer[0] != "y":
    print "Aborting!"
    sys.exit()
if os.path.exists(path):
    print "=> Cleaning out %s" % path
    shutil.rmtree(path)
print "=> Exporting %s to %s" % (os.getcwd(), path)
export(os.getcwd(), path)
os.chdir(path)
os.unlink('release.py')
s = open('setup.py')
d = s.read()
s.close()
s = open('setup.py', 'w')
s.write(d % (rn, vn))
s.close()
os.chdir(os.environ["HOME"])
tf = tarfile.open(tfpath, 'w:gz')
tf.add(path)
tf.close()

