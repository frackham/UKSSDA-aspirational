import os 
import urllib 
import webapp2 
import logging
from system import *
from registry import System
 
from google.appengine.ext import blobstore 
from google.appengine.ext.webapp import blobstore_handlers 

 
#class FileHandler(webapp2.RequestHandler): 
#  def get(self): 
#    upload_url = blobstore.create_upload_url('/upload') 
#    self.response.out.write('<html><body>') 
#    self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url) 
#    self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit" 
#        name="submit" value="Submit"> </form></body></html>""") 
#
                
def fileuploaddownloaddemo():
  retString=""
  #callbackName = "serveImmediately"
  callbackName = "serveImmediately"
  upload_url = blobstore.create_upload_url('/upload/' + callbackName) 
  retString+= "<form action=\"" + upload_url + "\" method=\"POST\" enctype=\"multipart/form-data\">"
  retString+= "Upload File: <input type=\"file\" name=\"file\"><br> <input type=\"submit\" name=\"submit\" value=\"Submit\"> </form>"
  
  #logging.getLogger().setLevel(logging.DEBUG)
  return retString        
        
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler): 
  def post(self,callbackName): 
    logging.info("*upload: post: " + str(self.get_uploads('file')))
    logging.info("*upload: post: callback will be: " + str(callbackName))
    upload_files = self.get_uploads('file')  # 'file' is file upload field in the form 
    blob_info = upload_files[0] 
    #logging.info("upload: post")
    logging.info('blob_info key==: %s' % blob_info.key())
    System().SetCurrentFileBlob(blob_info.key())
    #Next action determined here:
    if callbackName == "serveImmediately":
      self.redirect('/serve/%s' % blob_info.key())
    elif callbackName == "!!!":
      s = ServeHandler(System().GetCurrentFileBlob())
    else:
      logging.error('*unrecognised callbackName during UploadHandler')
         
class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler): 
  def get(self, blob_key):
    logging.info("*download: get: " + str(urllib.unquote(blob_key))) 
    logging.info('blob_info key==: %s' % blob_key)
    resource = str(urllib.unquote(blob_key))
    #resource = blob_key
    self.send_blob(resource)
    
    
  #def get(self, resource):
    #logging.info("*download: get: " + str(urllib.unquote(resource))) 
    #resource = str(urllib.unquote(resource)) 
    #blob_info = blobstore.BlobInfo.get(resource) 
    #self.send_blob(blob_info) 
     
    
#app = webapp2.WSGIApplication([('/', MainHandler), 
#                               ('/upload', UploadHandler), 
#                               ('/serve/([^/]+)?', ServeHandler)], 
#                              debug=True)
#