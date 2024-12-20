import os
import re
from PIL import Image
import pytesseract

#Uses Optical Character Recognition to rename Mastery Check images from Mathnasium
#to include the student's name, date, and module number
#Programmer: Andrew Jones and gpt4
#Early 2023


# Set the path to the Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Constants
UNKNOWN_NAME = "Unknown"
UNKNOWN_DATE = "Unknown"
UNKNOWN_MODULE_CODE = "Unknown"
VALID_IMAGE_PREFIX = "SCN"
IMAGE_EXTENSION = ".jpg"

#reformats the name from Last, First to First Last
def reformatName(name: str) -> str:
    """
    Args:
        name (str): Name in the format "Last, First".

    Returns:
        str: Name reformatted as "First Last".
    """
    try:
        lastName, firstName = name.split(", ")
        return f"{firstName} {lastName}"
    except ValueError:
        return UNKNOWN_NAME

#Uses regular expressions to find within the OCR the 
def extractInfoWithRegex(text: str) -> tuple:
    """
    Extracts name, date, and module code from the given text using regex.

    Args:
        text (str): Text extracted from an image.

    Returns:
        tuple: (name, date, moduleCode), where each element is a string.
    """
    # Extract name in the format "Last, First"
    nameMatch = re.search(r"\d{2}/\d{2}/\d{4} (\w+, \w+)", text)
    name = reformatName(nameMatch.group(1)) if nameMatch else UNKNOWN_NAME

    # Extract date in the format "MM/DD/YYYY"
    dateMatch = re.search(r"(\d{2}/\d{2}/\d{4})", text)
    date = dateMatch.group(1).replace("/", "-") if dateMatch else UNKNOWN_DATE

    # Extract module code in the format "Pk_XXXX_"
    moduleCodeMatch = re.search(r"Pk_(\d{4})_", text)
    moduleCode = moduleCodeMatch.group(1) if moduleCodeMatch else UNKNOWN_MODULE_CODE

    return name, date, moduleCode


def processImages(inputFolder: str, outputFolder: str, updateProgress, updateStatus):
    """
    Processes image files in the input folder, extracts text using OCR, and renames the files
    based on the extracted information.

    Args:
        inputFolder (str): Path to the folder containing input images.
        outputFolder (str): Path to the folder for renamed images.
        updateProgress (function): Callback function to update progress.
        updateStatus (function): Callback function to update status messages.
    """
    # Filter valid JPEG files
    imageFiles = [f for f in os.listdir(inputFolder) if f.endswith(IMAGE_EXTENSION) and f.startswith(VALID_IMAGE_PREFIX)]
    totalFiles = len(imageFiles)
    processedCount = 0

    for filename in imageFiles:
        imagePath = os.path.join(inputFolder, filename)

        try:
            # Open the image
            image = Image.open(imagePath)
        except Image.UnidentifiedImageError:
            updateStatus(f"Cannot identify image file: {filename}. Skipping.")
            continue

        # Perform OCR
        extractedText = pytesseract.image_to_string(image)

        # Extract required information
        name, date, moduleCode = extractInfoWithRegex(extractedText)

        # Construct the new filename
        newFilename = f"{name} {moduleCode} {date}{IMAGE_EXTENSION}"
        newPath = os.path.join(outputFolder, newFilename)

        try:
            # Rename the file
            os.rename(imagePath, newPath)
        except FileExistsError:
            updateStatus(f"File already exists: {newFilename}. Skipping.")

        # Update progress and status
        processedCount += 1
        updateProgress(processedCount / totalFiles)
        updateStatus(f"Processing {filename}...")

    # Final status update
    updateStatus("Processing completed.")
