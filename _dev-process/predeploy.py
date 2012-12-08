#!/usr/bin/env python

#HACK: [i] Can't commit using Github for Windows (can usin Git itself, though...) , so deploy and commit are separate. Note that all deploys should have a commit (ideally using Git tags with the version number), but not all commits are deployed.

#TODO: [c] Load test strut and check unit tests.
#TODO: [c] If tests fail, do not deploy (if you really want to deploy with a failed test (bad, bad practice), can use the GAE Launcher instead.
#TODO: [i] Make change to app.yaml?
#TODO: [c] Change to deploy, and add line to deploy using dataforschools admin email account.
#TODO: [e] Run code analysis.
#TODO: [i] Make change to app.yaml?
#TODO: [d] Make local backup.

#TODO: [e] Do not deploy if critical items exist (once past initial development).

#TODO: [i] Explore some performance testing. Possible to use http://jspro.com/apis/profiling-page-loads-with-the-navigation-timing-api/ OR http://jspro.com/apis/discovering-the-high-resolution-time-api/ ? Would need to do postdeploy, probably.

print("Predeploy")
