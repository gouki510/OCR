

import struct
from PIL import Image, ImageEnhance
import glob, os

RECORD_SIZE = 2052 


outdir = "ETL7-img/"
if not os.path.exists(outdir): os.mkdir(outdir)


files = glob.glob("ETL7/*")
fc = 0
for fname in files:
  fc = fc + 1
  print(fname) 


  f = open(fname, 'rb')
  f.seek(0)
  i = 0
  while True:
    i = i + 1
   
    s = f.read(RECORD_SIZE)
    if not s: break
  
    r = struct.unpack('>H2sH6BI4H4B4x2016s4x', s)
    
    iF = Image.frombytes('F', (64, 63), r[18], 'bit', 4)
    iP = iF.convert('L')
    code_jis = r[3]
    dir = outdir + "/" + str(code_jis)
    if not os.path.exists(dir): os.mkdir(dir)
    fn = "{0:02x}-{1:02x}{2:04x}.png".format(code_jis, r[0], r[2])
    fullpath = dir + "/" + fn
    #if os.path.exists(fullpath): continue
    enhancer = ImageEnhance.Brightness(iP)
    iE = enhancer.enhance(16)
    iE.save(fullpath, 'PNG')
print("ok")
