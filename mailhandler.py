#from google.appengine.api import mail  


#message = mail.InboundEmailMessage(self.request.body)



#Using http://stackoverflow.com/questions/616889/parsing-incoming-mail-with-google-app-engine 
#TODO: [c] Amend code here [refactor].
import logging
from google.appengine.ext import webapp2 
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import mail



#subject contains the message subject.
#sender is the sender's email address.
#to is a list of the message's primary recipients.
#cc contains a list of the cc recipients.
#date returns the message date.
#attachments is a list of file attachments, possibly empty. Each value in the list is a tuple of two elements: the filename and the file contents.
#original is the complete message, including data not exposed by the other fields such as email headers, as a Python email.message.Message.



class mailhandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender)

logging.info("Received an email. Setting up app to handle...")        
app = webapp2.WSGIApplication([mailhandler.mapping()], debug=True)
