#!/usr/bin/env python
import logging
import unittest
#from google.appengine.ext import testbed
import nose


# Note that unit tests are written with this methodology in mind ( http://stackoverflow.com/questions/110430/how-do-you-organize-unit-tests ). BDD, but that's the only aspect I'm using.
# i.e. Descriptive test names, so it is clear what has failed.

#Only exception is where a test would not be idempotent, so the following is good.:
#@Test
#public void insertAndDelete() { 
#    assertTrue(/*stuff does not exist yet*/);
#    createStuff();
#    assertTrue(/*stuff does exist now*/);
#    deleteStuff();
#    assertTrue(/*stuff does not exist anymore*/);
#}




def main():
  logging.info("*******UNIT TESTS START*******")
  #a=1
  #b=2
  #unittest.TestCase.assertEqual(a, b)#TODO: [c] Placeholder for unit test strut setup, test, teardown.
  
  #BUG: [c] Checks whole OS system, not just this app :/
  
  #TODO: [i] Make sure that use singular versions of assert tests (assertEqual, NOT assertEquals *S), as these undocumented versions violate single way principle, as per http://stackoverflow.com/a/931011 
  #TODO: [e] After this, save to .txt file. Will most likely need 'live' tests stored separately, as won't be able to write to a file in the filesystem on GAE.
  args = ['--V']
  result = nose.run(argv=args)
  
  logging.info("*******UNIT TESTS END*******")
  
if __name__ == '__main__':
    main()
