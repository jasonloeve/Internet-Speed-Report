# Internet-Speed-Report

A simple python program written to report bad internet speeds to an ISP.

This program can be setup on a public home webserver and set to be run as a cron every x times a day. The program will run a speed test using "speedtest-cli" , it will then open a connection to a mysql database and log the results, if speeds are lower than the set value (setvalue = int('50')) then the program will submit a support ticket to the ISP with the logged data of the test.

This program could also be setup to post to the ISP’s twitter feed (If ISP doesn’t response to support tickets to fix the problem (FYI. This is public , either ISP will deal with the problem with more speed or your twitter api will be banned)).

When using this program use common sense eg if your promised speed from the ISP is 100mbs set. The program to 50% eg 50mbs, your internet wont be 100mbs constantly.

TODO

I would like to rewrite this at some stage for simple setup.

If you would like to fork this project and help rebuild then go ahead.
