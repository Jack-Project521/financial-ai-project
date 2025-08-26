from controller.upload_doc_chat_controller import app


if __name__ == "__main__":

    # Run web application
    app.run(host="0.0.0.0", port=8080, debug=True)