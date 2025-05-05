from flask import Flask, render_template, request, jsonify, send_from_directory, Response, stream_with_context
import os
# from insta import perform_scraping as scrape_instagram
from fb2new2 import perform_facebook_tasks  # Placeholder for Facebook tasks

app = Flask(__name__)
app.template_folder = "templates"
app.static_folder = "static"




# Define base directory and output folder for PDFs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(BASE_DIR, "FbOutput")

# Ensure the output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)



@app.route('/')
def home():
    """Serve the home page (index.html)."""
    return render_template('index.html')


@app.route('/Facebook')
def instagram_login():
    """Serve the facebook login page."""
    return render_template('login_fb.html', platform="Facebook")


@app.route('/card_fb')
def card():
    """Serve the card.html page for displaying scraping progress."""
    return render_template('card_fb.html')
@app.route('/features')
def features():
    
    return render_template('features.html')


@app.route('/submit', methods=['POST'])
def process_login():
    """
    Handle login credentials and platform selection from the frontend.
    Redirect to the progress card page.
    """
    try:
        # Parse JSON data from the request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400

        platform = data.get('platform')
        username = data.get('username')
        password = data.get('password')

        # Validate the incoming data
        if not platform or not username or not password:
            return jsonify({"error": "Missing required fields (platform, username, password)"}), 400

        # Redirect to the card page for scraping progress
        return jsonify({"success": True, "redirect": "/card_fb", "username": username, "password": password})

    except Exception as e:
        app.logger.error(f"Unexpected error during login processing: {e}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route('/scrape-progress', methods=['GET'])
def scrape_progress():
    """
    Stream scraping progress messages using Server-Sent Events (SSE).
    """
    username = request.args.get('username')
    password = request.args.get('password')

    # Validate required parameters
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    @stream_with_context
    def generate():
        try:
            # Call the scraping function for Instagram
            for message in perform_facebook_tasks(username, password):
                yield f"data: {message}\n\n"
        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"

    return Response(generate(), content_type="text/event-stream")

@app.route('/download/<filename>')
def download_file(filename):
    """
    Serve the generated PDF file from the Output folder.
    """
    try:
        # Ensure filename is valid
        safe_filename = os.path.basename(filename)
        return send_from_directory(OUTPUT_FOLDER, safe_filename, as_attachment=True)
    except Exception as e:
        app.logger.error(f"Error while serving file {filename}: {e}")
        return jsonify({"error": f"Unable to download file: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
