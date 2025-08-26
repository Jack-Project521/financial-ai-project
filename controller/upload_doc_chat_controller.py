import os
import re

from flask import Flask, request, render_template, flash, redirect

from common.utils.constants import DEFAULT_N_RESULTS
from service.chat_csv_service import rag_chat_csv, add_data_from_documents
from service.chat_service import save_docs_to_db, rag_chat

# Create app object by Flask
app = Flask(__name__, template_folder="../ui/templates/")

# Configure upload folder
UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# File extensions allowed, const list and validation function
ALLOWED_EXTENSIONS = ["docx", "doc", "csv", "xls", "xlsx", "pdf"]

def allowed_file(file_name):
    return "." in file_name and file_name.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ------------------------------------------------------------------------- #

# Set collection name
collection_name = "default_collection"
name_list = os.listdir(UPLOAD_FOLDER)
if name_list:
    collection_name = name_list[0]

# Set csv file flag
is_csv = False

# ------------------------------------------------------------------------- #


# ------------------------------------------------------------------------- #
# ---------------------------   1. Upload docs  --------------------------- #
# ------------------------------------------------------------------------- #

# Upload doc page view
@app.route("/document_upload/", methods=["GET", "POST"])
def document_upload():

    # Come into the uploading page
    if request.method == "GET":
        return render_template("document_upload.html")

    # Get the file uploaded
    elif request.method == "POST":

        # Check if any files are uploaded
        if "file" not in request.files:
            flash("No file uploaded")

            # Go back to uploading page
            return redirect(request.url)

        file = request.files["file"]

        # If user did not choose a file, the browser may upload an empty file
        if file.filename == "":
            flash("No file uploaded")
            return redirect(request.url)

        # Check file type, save file to folder, save file to vector store
        if file and allowed_file(file.filename):
            # Save file to uploads folder
            file_name = file.filename
            print("file name", file_name)

            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
            print("file_path", file_path)
            file.save(file_path)

            # Add doc into vector store after uploading successfully
            global collection_name
            if file_path.endswith("csv"):
                # Add csv data to vector store
                add_data_from_documents(file_path)

                global is_csv
                is_csv = True
            else:
                collection_name = re.split(r"\.[^.]*$", file_name)[0]
                # Update global variable collection_name=collection_name, must assign it
                save_docs_to_db(file_path, collection_name=collection_name)

        return redirect(request.url)

    else:
        # Uploading failed then go back to upload page
        return render_template("document_upload.html")


# ------------------------------------------------------------------------- #
# -----------------------------   2. Chat    ------------------------------ #
# ------------------------------------------------------------------------- #

# Chat Page
@app.route("/")
@app.route("/chat/", methods=["GET", "POST"])
def chat():
    if request.method == "GET":
        return render_template("chat.html")

    elif request.method == "POST":
        # Get chat message from user
        user_query = request.json.get("message")
        print("user_query: ", user_query)

        # Retrieval
        if user_query:

            global is_csv
            if is_csv:
                response = rag_chat_csv(user_query)
                print("response: ", response)
            else:
                # Retrieving data from relevant collection
                response = rag_chat(user_query, collection_name=re.split(r"\.[^.]*$", collection_name)[0], n_results=DEFAULT_N_RESULTS)
                print("response content: ", response.content)

            return response.content

        else:
            return "Sorry, I don't know."

    # Go back to original url -> page
    return redirect(request.url)


# Chat page: change doc names by using selection label on page left-up
@app.route("/selection/", methods=["GET", "POST"])
def doc_selection():
    # Use global variable collection_name
    global collection_name

    if request.method == "GET":
        # Come into page, show all docs as default
        name_list = os.listdir(UPLOAD_FOLDER)
        if name_list:
            return {"name_list": name_list, "collection_name": collection_name}

        return {"name_list": [], "collection_name": collection_name}

    elif request.method == "POST":
        # If updating the doc in frontend, need to update doc name in backend, \
        # which is convenient to retrieve different docs in vector store
        collection_name = re.split(r"\.[^.]*$", request.json.get("collection_name"))[0]
        print("The doc is changed to: ", collection_name)

        # return {'status': 200, 'message': 'ok'}
        return redirect("/chat/")

    return redirect(request.url)


