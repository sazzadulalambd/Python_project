import cv2
import pytesseract
from PIL import Image
from tkinter import Tk



# Set the path to the Tesseract OCR executable (change this based on your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

def capture_image():
    # Open a connection to the camera (0 represents the default camera)
    cap = cv2.VideoCapture(0)

    # Capture a single frame
    ret, frame = cap.read()

    # Save the captured frame to an image file
    cv2.imwrite("card_image.png", frame)

    # Release the camera
    cap.release()

def extract_card_number(image_path):
    # Use Tesseract to perform OCR on the image and extract text
    extracted_text = pytesseract.image_to_string(Image.open(image_path))

    # Filter out non-digit characters to get the card number
    card_number = ''.join(filter(str.isdigit, extracted_text))

    return card_number

def copy_to_clipboard(text):
    # Use Tkinter to copy text to the clipboard
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text)
    r.update()
    r.destroy()

if __name__ == "__main__":
    # Capture an image from the camera
    capture_image()

    # Extract the card number from the captured image
    card_number = extract_card_number("card_image.png")

    # Copy the card number to the clipboard
    copy_to_clipboard(card_number)

    print(f"Card Number: {card_number} copied to clipboard.")
