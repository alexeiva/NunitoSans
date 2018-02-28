import os
import sys
from itertools import imap
from distutils.util import strtobool

BASEDIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir))

export_dir = '%s/fonts/TTF' % BASEDIR

ref_file = '%s/sources/ttfa_hinting_reference/Nunito-Regular.ttf ' % BASEDIR # reference file for hinting
settings = "-v -a nnn --reference=%s" % ref_file    # TTFAutohint settings

source_dir = BASEDIR + '/fonts/TTF-unhinted' # Folder with unhinted fonts

# small function to collect all files with (a) particular extension(s) in a directory
def getFiles(root, ext):
   files = []
   allfiles = os.listdir(root)
   for myfile in allfiles:
      if os.path.splitext(myfile)[1] in ext:
         files.append(os.path.join(root, myfile))
   return files

def hint(filenames):
   print 'Autohinting fonts with following parameters: ttfautohint %s \n' % settings   
   for n in filenames:
      print 'Autohinting file %s ...' % n.split('/')[-1]
      run_ttfautohint = "ttfautohint " + settings + n + " " + export_dir + '/' + n.split('/')[-1]
      os.system(run_ttfautohint)
   print '\nDone. %i files exported to %s\n' % (len(filenames), export_dir)
   return None

def overwrite():
    sys.stdout.write('Existing files will be overwritten. Proceed [Y/n]? ')
    while True:
        try:
            return strtobool(raw_input().lower())
        except ValueError:
            sys.stdout.write("Please respond with 'y/t/1' or 'n/f/0'.\n")

# check if unhinted files exist in [fonts/TTF-unhinted]

if not os.path.exists(source_dir):
   print "First, export unhinted TTFs into [fonts/TTF-unhinted] folder."
   sys.exit(0)
else:
   ext = ['.ttf']
   filenames = getFiles(source_dir, ext)

# create export directory if it doesn't exist
if not os.path.exists(export_dir):
    os.makedirs(export_dir)
    print 'Created export directory %s' % export_dir
    hint(filenames)

elif len(os.listdir(export_dir)) == 0:
   print 'Export directory [fonts/TTF] exists.'
   hint(filenames)

elif any('.ttf' in b for b in os.listdir(export_dir)):
   print 'Export directory [fonts/TTF] exists and contains TTFs.'
   proceed = overwrite()
   if proceed:
      hint(filenames)
   else:
      print 'Aborting'
      sys.exit(0)