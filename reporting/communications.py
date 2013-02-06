

def alertMessageHTML(sMessage, messageType="Info"):
  #Using  http://twitter.github.com/bootstrap/components.html#alerts
  if messageType == "Info": #Message types determined by Bootstrap framework.
    sType = "alert-info"
    sText = "info-text"
    sbackColourClass = "info-bg"
  elif messageType == "Error":
    sType = "alert-error"
    sText = "error-text"
    sbackColourClass = "error-bg"
  elif messageType == "Success":
    sType = "alert-success"
    sText = "success-text"
    sbackColourClass = "success-bg"
  elif messageType == "Warning":
    sType = "alert"
    sText = "alert-text"
    sbackColourClass = "alert-bg"
  else:
    sType = "infomessage"
    sText = "info-text"
    sbackColourClass = "info-bg"
  sRetString = "<div class=\"alert " + sType + "\">"
  sRetString +="<button type=\"button\" class=\"close\" data-dismiss=\"alert\">&times;</button>"
  sRetString +="<p class=\"" + sbackColourClass + " " + sText + "\">" + sMessage + "</p>"
  sRetString +="</div>"
  return sRetString