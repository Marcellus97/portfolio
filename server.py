import os
import sys
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer

class JSONRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html' # redirect to index.html
        # Translate the path to a file system path
        file_path = self.translate_path(self.path)

        # If it's a directory, list its contents as JSON
        if os.path.isdir(file_path):
            self.send_directory_listing(file_path)
        else:
            # If it's a file, serve it as usual
            super().do_GET()

    def send_directory_listing(self, dir_path):
        try:
            # Get list of files in the directory
            file_list = os.listdir(dir_path)
            files_info = []

            for filename in file_list:
                full_path = os.path.join(dir_path, filename)

                # Get file metadata (size, last modified time)
                file_stats = os.stat(full_path)
                file_info = {
                    "name": filename,
                    "size": file_stats.st_size,
                    "last_modified": file_stats.st_mtime
                }
                files_info.append(file_info)

            # Prepare the JSON response
            # response_data = {
                # "directory": dir_path,
                # "files": files_info
            # }

            # Send the JSON response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(files_info, indent=2).encode("utf-8"))
        
        except Exception as e:
            self.send_error(500, f"Error reading directory: {str(e)}")
# use path argument


path_to_serve = sys.argv[1]

# Ensure the path is absolute
if not os.path.isabs(path_to_serve):
    path_to_serve = os.path.abspath(path_to_serve)

# Check if the specified path exists and is a directory
if not os.path.isdir(path_to_serve):
    print(f"The path {path_to_serve} is not a valid directory.")
    sys.exit(1)

# Change the working directory to the specified path
os.chdir(path_to_serve)
# Start the server
PORT = 8000
server = HTTPServer(("0.0.0.0", PORT), JSONRequestHandler)
print(f"Serving on port {PORT}")
server.serve_forever()
