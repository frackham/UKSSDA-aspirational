#!/usr/bin/env python
import logging
import unittest
from google.appengine.ext import testbed

def main():
  logging.info("*******UNIT TESTS START*******")
  a=1
  b=2
  assertEqual(a, b)#TODO: [e] Placeholder for unit test strut setup, test, teardown.
  #TODO: [i] Make sure that use singular versions of assert tests (assertEqual, NOT assertEquals *S), as these undocumented versions violate single way principle, as per http://stackoverflow.com/a/931011 
  #TODO: [e] After this, save to .txt file. Will most likely need 'live' tests stored separately, as won't be able to write to a file in the filesystem on GAE.
  logging.info("*******UNIT TESTS END*******")
  
if __name__ == '__main__':
    main()
