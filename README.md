#check_website

Tool to check if a website is down
Using check-host.net
----------------------------------------

Enter the URL to check (example: https://google.com) or 'exit' to finish: https://google.com

Results for: https://google.com

✓ us-east1.check-host.net: Online (Response time: 0.052s)

✓ us-west1.check-host.net: Online (Response time: 0.048s)

✓ eu-west1.check-host.net: Online (Response time: 0.075s)

----------------------------------------

### Notes:

- The tool relies on the public API of check-host.net, which may have usage limits or change in the future.

- The results show the status from different global nodes, giving you an idea of whether the site is down only in certain regions or globally.

### Instructions for use on Linux:
1. Make sure you have Python installed:
  
   sudo apt update && sudo apt install python3 python3-pip  

### On Debian/Ubuntu-based distributions
   
2. Install requests:
  
   pip3 install requests
   
3. run:

python3 check_website.py
   
### Instructions for use on Termux:
1. Update Termux and install Python:
  
   pkg update && pkg install python
   
2. Install requests:
  
   pip install requests

3. run:

python check_website.py
