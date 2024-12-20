import tkinter as tk
from tkinter import filedialog, ttk
from RenameFiles import processImages

#Implements GUI for Optical Character Recognition to rename Mastery Check images from Mathnasium
#Programmer: Andrew Jones and gpt4
#Early 2023

# Constants for GUI settings
WINDOW_TITLE = "OCR File Renamer"
WINDOW_DIMENSIONS = "600x400"
STATUS_INITIAL_MESSAGE = "Status: Waiting for input..."

#opens a folder selection and updates corresponding label
def selectFolder(isInput=True):
    """
    Args:
        isInput (bool): Whether selecting the input folder (True) or output folder (False).
    """
    folderPath = filedialog.askdirectory()
    if folderPath:
        if isInput:
            inputFolderLabel.config(text=folderPath)
        else:
            outputFolderLabel.config(text=folderPath)


#initiates the OCR process using selected input and output folders
def startOCRProcess():
    inputFolder = inputFolderLabel["text"]
    outputFolder = outputFolderLabel["text"]

    if inputFolder and outputFolder:
        processImages(inputFolder, outputFolder, updateProgressBar, updateStatusMessage)
    else:
        updateStatusMessage("Error: Please select both input and output folders.")

#updates the progress bar
def updateProgressBar(progressFraction):
    """
    Args:
        progressFraction (float): Fractional progress (0.0 to 1.0).
    """
    progressBar["value"] = progressFraction * 100
    app.update_idletasks()

#updates the status message displayed in the text area
def updateStatusMessage(message):
    """
    Args:
        message (str): The status message to display.
    """
    statusText.delete(1.0, tk.END)
    statusText.insert(tk.END, message)
    app.update_idletasks()

#create main application window
app = tk.Tk()
app.title(WINDOW_TITLE)
app.geometry(WINDOW_DIMENSIONS)

#input folder selection
inputFolderButton = tk.Button(app, text="Select Input Folder", command=lambda: selectFolder(True))
inputFolderButton.pack(pady=10)
inputFolderLabel = tk.Label(app, text="No Input Folder Selected")
inputFolderLabel.pack()

#output folder selection
outputFolderButton = tk.Button(app, text="Select Output Folder", command=lambda: selectFolder(False))
outputFolderButton.pack(pady=10)
outputFolderLabel = tk.Label(app, text="No Output Folder Selected")
outputFolderLabel.pack()

#progress bar
progressBar = ttk.Progressbar(app, orient="horizontal", length=300, mode="determinate")
progressBar.pack(pady=20)

#status text area
statusText = tk.Text(app, height=5, width=50)
statusText.pack(pady=10)
statusText.insert(tk.END, STATUS_INITIAL_MESSAGE)

#start OCR button
startButton = tk.Button(app, text="Start OCR", command=startOCRProcess)
startButton.pack(pady=10)

#start main event loop
app.mainloop()
