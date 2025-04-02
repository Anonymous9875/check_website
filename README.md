### Code Explanation:

1. Libraries used:
   - requests: For making HTTP requests to the check-host.net API.
   - json: For processing the response in JSON format.
   - urllib.parse.quote: For encoding the URL and avoiding issues with special characters.

2. **Function check_website_status**:
   - Takes a URL as input.
   - Constructs the request to the check-host.net API.
   - Includes a User-Agent header to simulate a request from a browser.
   - Processes the response and displays whether the site is online or offline from different global nodes.

3. **Function main**:
   - Provides a simple interface for the user to enter URLs.
   - Allows exiting the program by typing "exit".
   - Automatically adds "https://" if the user omits the protocol.

**Error handling**:
   - Captures connection errors, timeouts, and issues when processing the JSON response.

### How to use the tool:
1. Make sure to have the requests library installed. You can install it with:
  
   pip install requests
   
2. Save the code in a file (for example, check_website.py).
3. Run the script:
  
   python check_website.py
   
4. Enter the URL you want to check (for example, https://google.com) and press Enter.

### Example Output:

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
