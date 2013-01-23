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


#http://kraskniga.blogspot.co.uk/2012/06/comparison-of-javascript-data.html
#http://raphaeljs.com/
#http://stackoverflow.com/questions/12761297/javascript-issue-in-bootstrap
#http://stackoverflow.com/questions/119969/javascript-chart-library
#http://www.jqplot.com/tests/line-charts.php
#http://datatables.net/blog/Twitter_Bootstrap_2
#http://datatables.net/blog/Drill-down_rows
#http://tympanus.net/codrops/2011/06/09/grid-navigation-effects/
#http://blog.sherpawebstudios.com/2009/06/17/top-10-html-form-layout-best-practices/
#http://mathiasbynens.be/notes/localstorage-pattern
#http://mathiasbynens.be/notes/html5-levels
#http://www.whatwg.org/specs/web-apps/current-work/multipage/forms.html
#http://mathiasbynens.be/notes/html5-details-jquery

#http://www.fontsquirrel.com/fonts/modern-pictograms
#http://www.ffdingbatsfont.com/erler/index.html
#http://www.heydonworks.com/article/a-free-icon-web-font
#http://somerandomdude.com/work/iconic/
#http://somerandomdude.com/work/cue/
#http://www.fonthead.com/fonts/ClickBits
#http://fortawesome.github.com/Font-Awesome/#new-icons
#http://uxdesign.smashingmagazine.com/2012/12/04/fittss-law-and-user-experience/
#http://css-tricks.com/examples/StarRating/
#


"""
Demo plan:

Ask where someone went to school. Find on Edubase, (v quick link to search, get URN).
 - Generate School base details from URN.
 - Show that, from that single number, we already have positioned school in the web of existing data (Edubase, Performance Tables, OFSTED inspections - and estimated next inspection!).
  - Also, as a minor point, links to the Register, statement of intent (global links in System).
 - Load demo dataset, showing different sections of data (and that they may come from a single MIS, or from multiple sources).
  - Show inheritance from an existing dataset.
 - 








REQUIRED FOR THE DEMO:
- School build from URN.
 - Edubase load.
 - OFSTED load.
 - Perfomance tables load.
 - Global links.


"""