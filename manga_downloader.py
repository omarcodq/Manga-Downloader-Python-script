import os
import requests
from bs4 import BeautifulSoup
import urllib.parse
import tkinter as tk
from tkinter import messagebox

# Function to download the manga chapter and image
def download_manga():
    # Get the URL from the user
    url = url_entry.get()

    # Define headers with User-Agent and Referer
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Referer': 'https://chapmanganato.com/'  # You may need to adjust this Referer
    }

    # Create a session to persist headers and cookies
    session = requests.Session()

    # Send a GET request to the URL with headers
    response = session.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the chapter title for creating the folder
        chapter_title = soup.title.text.strip()

        # Replace characters that are not allowed in folder names on Windows
        invalid_chars = ':*?"<>|\\/'
        for char in invalid_chars:
            chapter_title = chapter_title.replace(char, '-')

        # Create a folder with the chapter title if it doesn't exist
        chapter_folder = os.path.join(os.getcwd(), chapter_title)
        if not os.path.exists(chapter_folder):
            os.makedirs(chapter_folder)

        # Find all image tags in the HTML
        img_tags = soup.find_all('img')

        # Download and save each image
        for img_tag in img_tags:
            img_url = img_tag.get('src')
            if img_url:
                # Make sure the URL is absolute
                img_url = urllib.parse.urljoin(url, img_url)

                # Extract the image filename from the URL
                img_filename = os.path.basename(img_url)

                # Send an HTTP GET request to the image URL with headers
                img_response = session.get(img_url, headers=headers)

                # Check if the image download was successful
                if img_response.status_code == 200:
                    img_path = os.path.join(chapter_folder, img_filename)
                    with open(img_path, 'wb') as img_file:
                        img_file.write(img_response.content)
                else:
                    messagebox.showerror("Error", f"Failed to download: {img_url}")

        messagebox.showinfo("Download Complete", "Manga chapter and images downloaded successfully.")
    else:
        messagebox.showerror("Error", f"Failed to fetch URL: {url}")

# Create a simple GUI
window = tk.Tk()
window.title("Manga Downloader")

# Label and entry for entering the URL
url_label = tk.Label(window, text="Enter Manga Chapter URL:")
url_label.pack()
url_entry = tk.Entry(window, width=50)
url_entry.pack()

# Button to start the download
download_button = tk.Button(window, text="Download", command=download_manga)
download_button.pack()

# Run the GUI
window.mainloop()
