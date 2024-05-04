import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import requests
from bs4 import BeautifulSoup

def scan_website():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return

    try:
        # Send GET request
        response = requests.get(url)
        response.raise_for_status()  # Error for bad response

        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Potential XSS vulnerability
        script_tags = soup.find_all('script')
        if script_tags:
            report_text.insert(tk.END, f'Potential XSS vulnerability found on {url}:\n')
            for script_tag in script_tags:
                report_text.insert(tk.END, f'Script tag found: {script_tag}\n')

        # SQL injection vulnerability
        query_parameters = response.url.split('?')[-1]
        if 'sql=' in query_parameters.lower():
            report_text.insert(tk.END, f'Potential SQL injection vulnerability found on {url}:\n')
            report_text.insert(tk.END, f'SQL parameter found in URL: {query_parameters}\n')

        # Insecure HTTP headers?
        insecure_headers = response.headers.get('Server', '').lower()
        if 'apache' in insecure_headers:
            report_text.insert(tk.END, f'Insecure server header found on {url}:\n')
            report_text.insert(tk.END, f'Server header value: {response.headers["Server"]}\n')

        messagebox.showinfo("Scan Complete", "Website scan completed successfully")

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def clear_report():
    report_text.delete('1.0', tk.END)

# Create main window
window = tk.Tk()
window.title("Website Vulnerability Scanner")

# Create URL input field
url_label = tk.Label(window, text="Enter URL:")
url_label.grid(row=0, column=0, padx=5, pady=5)
url_entry = tk.Entry(window, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)

# Create Scan button
scan_button = tk.Button(window, text="Scan Website", command=scan_website)
scan_button.grid(row=0, column=2, padx=5, pady=5)

# Create Clear button
clear_button = tk.Button(window, text="Clear Report", command=clear_report)
clear_button.grid(row=0, column=3, padx=5, pady=5)

# Create report text area
report_text = scrolledtext.ScrolledText(window, width=80, height=20, wrap=tk.WORD)
report_text.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

# Start the GUI event loop
window.mainloop()
