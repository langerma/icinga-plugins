import os
import time
import argparse


def check(filename):
    #print "last accessed on" + str(time.ctime(os.path.getatime('/home/langerma/.vim/vimrc')))
    print "last modified on" + str(time.ctime(os.path.getmtime(filename)))
    #print "last asdjlaj  on" + str(time.ctime(os.path.getctime('/home/langerma/.vim/vimrc')))


if  __name__ == '__main__':
    parser = argparse.ArgumentParser('Icinga check for fileage')
    parser.add_argument('--file', required=True, help='filename or path')
    args = parser.parse_args()
    check(file=str(args.file))
