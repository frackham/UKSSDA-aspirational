#!/usr/bin/env python
#HACK: [i] Exists because Github for Windows can't execute precommit hooks :/ .
#TODO: [e] Run codeanalysis.
#TODO: [i] Probably move codeanalysis in here.
# *Don't* make a backup using this. Point of the VCS is to manage the history...
import os
import nosetestall

print("*Precommit*")
os.chdir("tests")
print os.getcwd()
x=raw_input()
nosetestall.main()
