# Search_with_keyword



# File Keyword Search Tool

This Python script provides a graphical user interface (GUI) to search for specific keywords within files in a given directory. It allows you to specify the directory to search, the keywords to look for, the file types to include, and options for recursive searching and case sensitivity. The results, including the filename and the matching lines, are saved to a specified output file.

## Features

*   **Directory Selection:** Easily select the directory you want to search using a browse dialog.
*   **Keyword Input:** Enter multiple search keywords, one per line.
*   **File Type Filtering:** Specify the file extensions to include in the search (e.g., `.log`, `.txt`, `.csv`).
*   **Recursive Search:** Optionally search within subdirectories.
*   **Case Sensitivity:** Choose whether the search should be case-sensitive or not.
*   **Output File Selection:** Specify the path and filename for saving the search results.
*   **Show Full Path:** Option to include the full file path in the output results.
*   **Progress Bar:** Visual feedback on the search progress.
*   **Cancel Search:** Ability to stop the search process mid-execution.
*   **Output File Size Limit:** Stops the search if the output file reaches 1GB to prevent excessive file sizes.

## Prerequisites

*   **Python 3.x:** This script is written in Python 3.
*   **tkinter:** The `tkinter` library is required for the GUI. It is usually included with standard Python installations.

## Usage

1. **Run the script:** Execute the Python script (`.py` file).
2. **Select Search Directory:** Click the "Browse" button next to the "Search Directory" field to choose the folder you want to search in.
3. **Enter File Types:** In the "File Types" field, enter the file extensions you want to include in the search, separated by commas (e.g., `.log,.txt`). Leave it blank to search the default extensions (`.log`, `.txt`, `.csv`).
4. **Enter Search Keywords:** In the text area labeled "Search Keywords", type the keywords you want to search for, with each keyword on a new line.
5. **Configure Search Options:**
    *   **Search in Subdirectories:** Check this box if you want to search within folders inside the selected directory.
    *   **Case Sensitive:** Check this box if you want the search to be case-sensitive (e.g., "Error" will not match "error").
    *   **Show Full Path:** Check this box to include the complete file path in the output results, otherwise only the filename will be shown.
6. **Select Output File Path:** Click the "Browse" button next to the "Output File Path" field to choose where you want to save the search results and what to name the file.
7. **Start Search:** Click the "Start Search" button to begin the search process. The progress bar will indicate the current status.
8. **Cancel Search (if needed):** If you need to stop the search before it completes, click the "Cancel Search" button.
9. **View Results:** Once the search is complete, the results will be saved in the specified output file. The status label will indicate when the process is finished.

## How to Run

1. Save the Python code to a file, for example, `file_search_tool.py`.
2. Open a terminal or command prompt.
3. Navigate to the directory where you saved the file.
4. Run the script using the command: `python file_search_tool.py`

## Contributing

Contributions to this project are welcome! Feel free to fork the repository, make changes, and submit a pull request.

## License

This project is open-source and available under the [Specify License Here, e.g., MIT License].
