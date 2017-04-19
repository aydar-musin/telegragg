__author__ = 'aydar'
import datetime


def error(msg):
    f = open('errors.log', 'w')
    f.write(str(datetime.datetime.now())+'\t'+msg+'\n')