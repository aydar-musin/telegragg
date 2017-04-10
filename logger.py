__author__ = 'aydar'
import datetime


def info(msg):
    file = open('info.log','w')
    file.write(str(datetime.datetime.now())+'\t'+msg+'\n')
    file.close()


def error(msg):
    file = open('error.log','w')
    file.write(str(datetime.datetime.now())+'\t'+msg+'\n')
    file.close()