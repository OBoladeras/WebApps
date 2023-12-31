# File Transfer App 📁
## Overview 🚀
This is a simple file transfer app built using Flask, allowing users to upload files and share them with others through a generated download link. The app creates a unique token for each file transfer session and organizes uploaded files in a dedicated directory.<br>
A preview of the app, but not a functional one can be found here: https://oboladeras.github.io/WebApps/file_transfer/templates/

## Features ✨
- **File Upload**: Users can upload multiple files in a single session.
- **Token-based Access**: Each file transfer session is associated with a unique token, ensuring secure and private access to uploaded files.
- **Download Link Generation**: After a successful upload, the app generates a download link that users can share with others to retrieve the files.


## File Structure 📂
- **app.py**: Main application file containing the Flask app.
- **templates/**: HTML templates for rendering web pages.
- **uploads/**: Directory where uploaded files are stored, organized by tokens.

## Usage 🚀
Run the app:

```
python app.py
```

1. Open a web browser and go to *http://localhost:5000/* to access the file transfer interface.<br>
2. Fill in the required information (title, username, and files to upload).<br>
3. Upon successful upload, a download link will be generated.
