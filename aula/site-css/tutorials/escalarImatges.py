#easy_install pil
import Image

def scale (fname, width, height, fname_scaled):
   try:
      img = Image.open (fname)
   except:
      print 'Unable to open ' + fname
      
   print "width:" + str(width) + "height:" + str(height)
   img = img.resize((width, height), Image.ANTIALIAS)
   
   try:
      img.save(fname_scaled)
   except:
      'Unable to save in ' + fname_scaled
         

import os
for file in os.listdir("."):
    if file.endswith(".png") or file.endswith(".jpg"):
         print file
         fitxerDesti = "s_" + file
         img = Image.open (file, mode='r')
         new_width = 800
         new_height = new_width * img. size[1] / img. size[0]
         scale(file, new_width, new_height, fitxerDesti)
