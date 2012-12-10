import nose, os

def main():
  print os.getcwd()
  os.chdir("..")
  print os.getcwd()
  x=raw_input() #This is just so I can see the output of the cwd before it launches into testing everything it can find.
  result = nose.run(argv=['nosetestall.py',
                          '-v',
                          '--exclude-dir-file=exclude_dirs.txt',
                          '--with-coverage']) 
  x=raw_input()
  
if __name__ == '__main__':
  main()
