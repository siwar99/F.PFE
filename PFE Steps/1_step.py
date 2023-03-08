import tkinter as tk
import webbrowser
from PIL import ImageGrab, Image
import pytesseract
import json
import time


def open_ticket_link():
    ticket_number = entry.get()
    if ticket_number:
        url = f"https://jira.dt.renault.com/browse/{ticket_number}"
        webbrowser.open(url)

        # Wait for 5 seconds for the page to load
        time.sleep(5)

        # Take a screenshot of the entire screen
        screenshot = ImageGrab.grab()
        screenshot_file = f'{ticket_number}.png'
        screenshot.save(screenshot_file)

        # Extract text from screenshot using pytesseract
        image = Image.open(screenshot_file)
        text = pytesseract.image_to_string(image)

        # Save extracted text to JSON file
        data = {'ticket_number': ticket_number, 'text': text}
        json_file = f'{ticket_number}.json'
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)


root = tk.Tk()
root.geometry("300x100")

label = tk.Label(root, text="Enter ticket number:")
label.pack()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Open ticket link", command=open_ticket_link)
button.pack()

root.mainloop()