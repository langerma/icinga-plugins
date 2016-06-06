import os
import time

print "last accessed on" + str(time.ctime(os.path.getatime('/home/langerma/.vim/vimrc')))
print "last modified on" + str(time.ctime(os.path.getmtime('/home/langerma/.vim/vimrc')))
print "last asdjlaj  on" + str(time.ctime(os.path.getctime('/home/langerma/.vim/vimrc')))

