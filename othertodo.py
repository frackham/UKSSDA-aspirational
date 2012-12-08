#othertodo.py


#AUTH and SECURITY
#TODO: [c] Move all nav blocks to auth by user.
#TODO: [d] Move auth to separate library, including get user code. Make GAE agnostic, with GAE interface to user in DAL_User library further included in DAL.


#RENDERING
#TODO: [d] Explore http://demos.kendoui.com/dataviz/scatter-charts/scatter-line.html as alternative to jqPlot.
#TODO: [i] Make sure all renderings have accessible alternatives (e.g. JS rendered as per http://jspro.com/raw-javascript/javascript-accessibility-101/). Optional parameter to analysis.render() call could be accessibilty=text, where default = false. If true, text alternatives rendered alongside.
#TODO: [d] Explore processing.js as alternative to jqPlot.
#TODO: [e] Move rendering of charts and analysis to separate Python classes and file. NOT edu objects!
#TODO: [i] Use NC (National Strategy?) colours! E.g. if rendering English, use Yellow. Means that matches user expectations.


#DISTRIBUTION 
#TODO: [d] Add distribute to email (requires email property on staff). 
#TODO: [i] Add non-staff distribution contacts (both inherit from superclass or use aggregation).
#TODO: [d] Add single PDF output - where items for same person are in order, with either (a) footer identifying who it is for, or (b) coversheet with list of pages and who it is for.

#EDU OBJECT CLASS PROPERTIES/METHODS
#TODO: [d] Get tutor group members (iterate through staff and students). Probably one to cache at System or collection level?





#EXTENSIONS (all idealistic).
# (A) MAPPING
#TODO: [i] Map to image map http://www.algonet.se/~ug/html+pycgi/img.html