from Oregano.tracer import *
import subprocess
import time

notepad = subprocess.Popen('notepad.exe')
time.sleep(1)
o = attach(notepad.pid)
time.sleep(10)
o.setTraceOnModule(['notepad.exe'])
time.sleep(20)
o.stop()

