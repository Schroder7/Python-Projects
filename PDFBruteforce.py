# pip3 install pikepdf
# pip3 install colorama
import time
import pikepdf
from colorama import Fore
from tkinter import Tk, filedialog
from itertools import product
import string
import os
from collections import deque


def get_pdf():
    root = Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(
        title="Please select a PDF file",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )

    return file_path

def generate_passwords(length):
    # Generate all possible passwords of the given length
    characters = string.ascii_letters + string.digits + string.punctuation
    return (''.join(p) for p in product(characters, repeat=length))

# Get the PDF file path from the file picker
encrypted_document_path = get_pdf()

# You can customize the maximum password length
max_password_length = 16

start_time = time.time()
last_update_time = start_time
timestamps = deque()


def update_print(password, last_update_time, timestamps):    
        current_time = time.time()
        if current_time - last_update_time > 0.05:  # Update the console every 0.05 seconds
            # Remove timestamps older than 2 seconds
            while timestamps and timestamps[0] < current_time - 2:
                timestamps.popleft()
            os.system('cls')  # Clear the console
            print(Fore.RED + f"Password being tested: {password}")
            print(Fore.YELLOW + f"Time Elapsed: {current_time-start_time:.2f} seconds")
            print(Fore.BLUE + f"Passwords guessed per second {len(timestamps)/2}")
            return current_time  # Update the last update time
        return last_update_time



# Try all possible passwords up to the specified length
for length in range(1, max_password_length + 1):
    for password in generate_passwords(length):
        timestamps.append(time.time())
        last_update_time = update_print(password, last_update_time, timestamps)
        try:
            with pikepdf.Pdf.open(encrypted_document_path, password=password) as pdf:
                # If the password is correct, this block will be executed
                end_time = time.time()
                print("\n")
                print(Fore.GREEN + f"Password found in {str(end_time - start_time)[:4]} seconds\nPassword is: ", end="")
                print(Fore.BLUE + f" {password}")

                # If you want to continue searching for other passwords, remove the break statement
                break
        except:
            pass
