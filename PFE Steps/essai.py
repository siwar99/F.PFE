import tkinter as tk
import webbrowser
from PIL import ImageGrab, Image
import pytesseract
import json
import time
import pyautogui


def generate_ticket_number():
    ticket_number = entry.get()
    return ticket_number.strip()


def open_ticket_link():
    ticket_number = generate_ticket_number()
    if ticket_number:
        url = f"https://jira.dt.renault.com/browse/{ticket_number}"
        webbrowser.open(url)

        # Wait for 5 seconds for the page to load
        time.sleep(5)

        # Take a screenshot of the current window
        screenshot = ImageGrab.grab(bbox=None)

        screenshot_file = f'{ticket_number}.png'
        screenshot.save(screenshot_file)

        # Use pyautogui to scroll down and take a screenshot of the full page
        width, height = pyautogui.size()
        pyautogui.moveTo(width // 2, height // 2)
        pyautogui.click()
        time.sleep(1)
        pyautogui.scroll(-8)
        time.sleep(5)
        fullpage_screenshot = ImageGrab.grab(bbox=(0, 0, width, height))
        fullpage_screenshot_file = f"{ticket_number}_fullpage.png"
        fullpage_screenshot.save(fullpage_screenshot_file)

        # Combine the two screenshots and save as a new image
        screenshot_image = Image.open(screenshot_file)
        fullpage_screenshot_image = Image.open(fullpage_screenshot_file)
        combined_image = Image.new("RGB", (width, height + screenshot_image.size[1]))
        combined_image.paste(fullpage_screenshot_image, (0, 0))
        combined_image.paste(screenshot_image, (0, fullpage_screenshot_image.size[1]))
        combined_image_file = f"{ticket_number}_combined.png"
        combined_image.save(combined_image_file)

        # Extract text from the combined image using pytesseract
        combined_image_text = pytesseract.image_to_string(combined_image)

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

        # Display message to user that screenshots have been taken and text extracted
        root.geometry("300x100")
        message = tk.Message(root, text="Screenshots taken and text extracted for ticket number " + ticket_number + ".")
        message.pack()


root = tk.Tk()
root.geometry("300x100")

label = tk.Label(root, text="Enter ticket number:")
label.pack()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Open ticket link", command=open_ticket_link)
button.pack()

root.mainloop()
