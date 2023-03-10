import tkinter as tk
from PIL import Image
import pytesseract
import json
import time
import os
from selenium import webdriver

# Set up the Chrome driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=chrome_options)

def generate_ticket_number():
    ticket_number = entry.get()
    return ticket_number.strip()

def open_ticket_link():
    ticket_number = generate_ticket_number()
    if ticket_number:
        url = f"https://jira.dt.renault.com/browse/{ticket_number}"
        driver.get(url)

        # Wait for 5 seconds for the page to load
        time.sleep(5)

        # Take a screenshot of the entire page
        screenshot_file = f'{ticket_number}.png'
        driver.save_screenshot(screenshot_file)

        # Load the screenshot as an image
        screenshot_image = Image.open(screenshot_file)

        # Extract text from the image using pytesseract
        combined_image_text = pytesseract.image_to_string(screenshot_image)

        # Save the extracted text to a plain text file
        combined_image_text_file = f'{ticket_number}_combined.txt'
        with open(combined_image_text_file, 'w') as file:
            file.write(combined_image_text)

        # Save extracted text to JSON file
        lines = combined_image_text.splitlines()
        data = {'ticket_number': ticket_number, 'text': lines}
        json_file = f'{ticket_number}.json'
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)

        # Display message to user that screenshot has been taken and text extracted
        #root.geometry("300x100")
        #message = tk.Message(root, text="Screenshot taken and text extracted for ticket number " + ticket_number + ".")
        #message.pack()

        # Clean up temporary files
        os.remove(screenshot_file)

root = tk.Tk()
root.geometry("300x100")

label = tk.Label(root, text="Enter ticket number:")
label.pack()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Open ticket link", command=open_ticket_link)
button.pack()

root.mainloop()

# Quit the driver
driver.quit()
