#!/usr/bin/python
"""
tool created: 2013-03-17
pwgen.py - Allow the user to specify length of password and whether to use special characters
and generate a pseudo-random password.  The resulting password is copied to the user's clipboard
automatically.
Makes use of PyObjC - http://pythonhosted.org/pyobjc/install.html
Only work in OS X at the moment.
@Dagorim - www.dagorim.com
"""
from optparse import OptionParser
from AppKit import NSPasteboard, NSArray
import random
import string

pb = NSPasteboard.generalPasteboard()
pb.clearContents()

parser = OptionParser()
parser.add_option("-l", "--length", dest="pwLength",
				help="Specify password length in characters")
parser.add_option("-s", "--special", dest="pwSpecial", 
				help="Specify whether to use special characters",
				default=False, action='store_true')

(options, args) = parser.parse_args()
strSpecial = '!@#$%^&*()'
char_set = string.ascii_uppercase + string.ascii_lowercase + string.digits

def f_pwGen(size=8, chars=char_set):
	return ''.join(random.choice(chars) for x in range(int(options.pwLength)))
def f_pwGenSpecial(size=8, chars=char_set + strSpecial):
	return ''.join(random.choice(chars) for x in range(int(options.pwLength)))

print 'Password length: ', options.pwLength
print 'Special Characters?: ', options.pwSpecial
print 'Generated Password: '
if(options.pwSpecial):
	myPass = f_pwGenSpecial(int(options.pwLength), )
	a = NSArray.arrayWithObject_(myPass)
	print myPass
	pb.writeObjects_(a)
else:
	myPass = f_pwGen(int(options.pwLength), )
	a = NSArray.arrayWithObject_(myPass)
	print myPass
	pb.writeObjects_(a)
