import webbrowser
import time
import os

# Define the URL of the web page you want to print
url = 'https://jira.dt.renault.com/browse/CCSEXT-121861'

# Open the web page in a new tab in your default web browser
webbrowser.open_new_tab(url)

# Wait for the web page to load (you may need to adjust this delay depending on your connection speed)
time.sleep(5)

# Send the keyboard shortcut to trigger the print dialog box (Ctrl + P on Windows, Command + P on Mac)
if os.name == 'nt':
    # Windows
    os.startfile(url, "print")
elif os.name == 'posix':
    # macOS
    os.system("lp -d {0} {1}".format("<your_printer_name>", url))

# Wait for the web page to finish printing (you may need to adjust this delay depending on your system and printer)
time.sleep(10)
