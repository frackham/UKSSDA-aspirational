import main 
import logging

def RegisterSystem(thisSys, app):            
  registered_sys  = app.registry.get('System')
  if not registered_sys:
    # Instantiate the imported class.
    registered_sys = thisSys
    # Register the instance in the registry.
    app.registry['System'] = registered_sys #Registers the new EdSystem object so it can be globally accessed. Actual access is handled through the System() call.
    logging.info("SYSTEM object registered.")
      
def System():
  return main.SystemSettings()