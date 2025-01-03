import tkinter as tk
from tkinter import filedialog, messagebox
import os
import tkinter.ttk as ttk  # Progressbar를 위해 import
import threading

search_cancelled = False  # 검색 취소 플래그

def select_directory():
    folder_selected = filedialog.askdirectory(title="Select Directory")
    directory_entry.delete(0, tk.END)
    directory_entry.insert(0, folder_selected)

def select_output_file():
    file_selected = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("All files", "*.*"), ("Text files", "*.txt")]  # 모든 확장자를 기본으로 보이도록 순서 변경
    )
    output_entry.delete(0, tk.END)
    output_entry.insert(0, file_selected)

def cancel_search():
    global search_cancelled
    search_cancelled = True
    cancel_button.config(state=tk.DISABLED)
    status_label.config(text="Cancelling search...")

def search_files_thread():
    global search_cancelled
    search_cancelled = False  # 검색 시작 시 플래그 초기화
    start_button.config(state=tk.DISABLED)
    cancel_button.config(state=tk.NORMAL)
    status_label.config(text="Preparing to search files...")
    progress_bar["value"] = 0
    root.update()
    search_files()
    start_button.config(state=tk.NORMAL)
    cancel_button.config(state=tk.DISABLED)

def search_files():
    global search_cancelled
    directory = directory_entry.get()
    keywords_text = keywords_text_widget.get("1.0", tk.END).strip()
    keywords = [kw.strip() for kw in keywords_text.splitlines() if kw.strip()]
    output_file = output_entry.get()
    case_sensitive = case_var.get()
    file_extensions_text = file_extension_entry.get().strip()
    file_extensions = [ext.strip() for ext in file_extensions_text.split(',') if ext.strip()]
    recursive_search = recursive_var.get()
    show_full_path = full_path_var.get()

    if not directory:
        status_label.config(text="Please select a directory.")
        return
    if not keywords:
        status_label.config(text="Please enter search keywords.")
        return
    if not output_file:
        status_label.config(text="Please select an output file path.")
        return

    status_label.config(text="Preparing to search files...")
    root.update()

    total_files = 0
    files_to_search = []
    if recursive_search:
        for root_dir, _, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root_dir, file)
                # 결과 파일은 검색 대상에서 제외
                if os.path.abspath(filepath) == os.path.abspath(output_file):
                    continue
                if file_extensions:
                    if any(file.endswith(ext) for ext in file_extensions):
                        files_to_search.append(filepath)
                else:
                    if file.endswith(('.log', '.txt', '.csv')):
                        files_to_search.append(filepath)
    else:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            # 결과 파일은 검색 대상에서 제외
            if os.path.abspath(filepath) == os.path.abspath(output_file):
                continue
            if file_extensions:
                if any(filename.endswith(ext) for ext in file_extensions):
                    files_to_search.append(filepath)
            else:
                if filename.endswith(('.log', '.txt', '.csv')):
                    files_to_search.append(filepath)

    total_files = len(files_to_search)
    progress_bar["maximum"] = total_files
    progress_bar["value"] = 0

    status_label.config(text="Searching files...")
    root.update()

    files_processed = 0
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for filepath in files_to_search:
                if search_cancelled:
                    status_label.config(text="Search cancelled by user.")
                    return

                # 결과 파일 크기 확인 (1GB 초과 시 중단)
                if os.path.exists(output_file) and os.path.getsize(output_file) > 1024 * 1024 * 1024:
                    status_label.config(text="Search stopped: Output file size reached 1GB.")
                    messagebox.showinfo("Stopped", "Output file size reached 1GB. The search has been stopped.")
                    return

                filename = os.path.basename(filepath)
                process_file(filepath, filename, keywords, case_sensitive, outfile, show_full_path)
                files_processed += 1
                progress_bar["value"] = files_processed
                root.update()

        if not search_cancelled:
            status_label.config(text="Search completed and results saved.")
    except Exception as e:
        print(f"Error: {e}")
        status_label.config(text=f"Error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        progress_bar["value"] = 0 # 완료 후 progress bar 초기화

def process_file(filepath, filename, keywords, case_sensitive, outfile, show_full_path):
    try:
        with open(filepath, 'r', encoding='utf-8') as infile:
            for line in infile:
                for keyword in keywords:
                    display_filename = filepath if show_full_path else filename
                    keyword_present = False
                    if case_sensitive:
                        if keyword in line:
                            keyword_present = True
                    else:
                        if keyword.lower() in line.lower():
                            keyword_present = True

                    if keyword_present:
                        outfile.write(f"[{display_filename} - {keyword}] {line}")
                        break  # 한 줄에 하나의 키워드만 기록하고 다음 줄로 넘어감
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        status_label.config(text=f"Error: An error occurred while reading file {filename}")

# Main window
root = tk.Tk()
root.title("File Keyword Search")

# Directory selection
directory_label = tk.Label(root, text="Search Directory:")
directory_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
directory_entry = tk.Entry(root, width=50)
directory_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")
directory_button = tk.Button(root, text="Browse", command=select_directory)
directory_button.grid(row=0, column=2, padx=5, pady=5)

# File type input
file_extension_label = tk.Label(root, text="File Types (e.g., .log,.txt):")
file_extension_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
file_extension_entry = tk.Entry(root, width=50)
file_extension_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")

# Keyword input (Text widget)
keywords_label = tk.Label(root, text="Search Keywords (one per line):")
keywords_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
keywords_text_widget = tk.Text(root, height=5, width=40)
keywords_text_widget.grid(row=2, column=1, padx=5, pady=5, sticky="we")

# Recursive search option
recursive_var = tk.BooleanVar()
recursive_check = tk.Checkbutton(root, text="Search in Subdirectories", variable=recursive_var)
recursive_check.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# Case sensitive option (moved down)
case_var = tk.BooleanVar()
case_check = tk.Checkbutton(root, text="Case Sensitive", variable=case_var)
case_check.grid(row=4, column=1, padx=5, pady=5, sticky="w")

# Output file path selection
output_label = tk.Label(root, text="Output File Path:")
output_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=5, column=1, padx=5, pady=5, sticky="we")
output_button = tk.Button(root, text="Browse", command=select_output_file)
output_button.grid(row=5, column=2, padx=5, pady=5)

# Show full path option
full_path_var = tk.BooleanVar()
full_path_check = tk.Checkbutton(root, text="Show Full Path", variable=full_path_var)
full_path_check.grid(row=6, column=1, padx=5, pady=5, sticky="w")

# Buttons Frame
buttons_frame = tk.Frame(root)
buttons_frame.grid(row=7, column=1, padx=5, pady=10, sticky="ew")  # sticky="ew" 추가

# Search button
start_button = tk.Button(buttons_frame, text="Start Search", command=lambda: threading.Thread(target=search_files_thread).start())
start_button.pack(side=tk.LEFT, padx=(0, 5))  # 오른쪽 여백 추가

# Cancel button
cancel_button = tk.Button(buttons_frame, text="Cancel Search", command=cancel_search, state=tk.DISABLED)
cancel_button.pack(side=tk.LEFT)

# Progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

# Status label
status_label = tk.Label(root, text="")
status_label.grid(row=9, column=0, columnspan=3, padx=5, pady=5)

# Grid layout configuration (make the middle column expandable)
root.columnconfigure(1, weight=1)
buttons_frame.columnconfigure(0, weight=1) # buttons_frame의 첫 번째 컬럼에 weight 부여 (가운데 정렬)

root.mainloop()