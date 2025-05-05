from flask import Flask, render_template, request, jsonify, Response, stream_with_context, send_from_directory
import os
from fb2new2 import perform_facebook_tasks
from insta import perform_scraping ,generate_summary_and_apply_filter,generate_pdf
from X import perform_x_tasks
import logging
import types
from threading import Lock

scraping_locks = {}
lock = Lock()  # Protect access to the `scraping_locks` dictionary



app = Flask(__name__)
app.template_folder = "templates"
app.static_folder = "static"

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# FB_OUTPUT_FOLDER = os.path.join(BASE_DIR, "FbOutput")
# INSTA_OUTPUT_FOLDER = os.path.join(BASE_DIR, "Output")
# XDATA_FOLDER = os.path.join(BASE_DIR, "XOutput")

# Ensure required folders exist
# os.makedirs(FB_OUTPUT_FOLDER, exist_ok=True)
# os.makedirs(INSTA_OUTPUT_FOLDER, exist_ok=True)



@app.route('/')
def home():
    """Serve the home page."""
    return render_template('index.html')


@app.route('/<platform>')
def platform_login(platform):
    """Serve the login page for the selected platform."""
    if platform == "Facebook":
        return render_template('login_fb.html', platform="Facebook")
    elif platform == "Instagram":
        return render_template('login.html', platform="Instagram")
    elif platform == "X":
        return render_template('login_x.html', platform="X")
    else:
        return jsonify({"error": "Platform not supported"}), 404


@app.route('/card/<platform>')
def card(platform):
    """Serve the card page for the selected platform."""
    if platform == "Facebook":
        return render_template('card_fb.html')
    elif platform == "Instagram":
        return render_template('card_test.html')
    elif platform == "X":
        return render_template('card_x.html')
    else:
        return jsonify({"error": "Platform not supported"}), 404


@app.route('/submit', methods=['POST'])
def process_login():
    """Handle login credentials and platform selection from the frontend."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400

        platform = data.get('platform')
        username = data.get('username')
        password = data.get('password')

        if not platform or not username or not password:
            return jsonify({"error": "Missing required fields"}), 400

        return jsonify({"success": True, "redirect": f"/card/{platform}", "username": username, "password": password})
    except Exception as e:
        app.logger.error(f"Error during login processing: {e}")
        return jsonify({"error": str(e)}), 500


# @app.route('/scrape-progress/<platform>', methods=['GET'])
# def scrape_progress(platform):
#     """Stream scraping progress messages for the selected platform using SSE."""
#     username = request.args.get('username')
#     password = request.args.get('password')

#     if not username or not password:
#         return jsonify({"error": "Missing username or password"}), 400

#     @stream_with_context
#     def generate():
#         try:
#             app.logger.info(f"Starting scrape for {platform} with username: {username}")
            
#             # Platform-specific tasks
#             if platform == "Facebook":
#                 for message in perform_facebook_tasks(username, password):
#                     app.logger.info(f"Facebook task message: {message}")
#                     yield f"data: {message}\n\n"
#             elif platform == "Instagram":
#                 for message in scrape_instagram(username, password):
#                     app.logger.info(f"Instagram task message: {message}")
#                     yield f"data: {message}\n\n"
#             elif platform == "X":
#                 for message in perform_x_tasks(username, password):
#                     app.logger.info(f"X task message: {message}")
#                     yield f"data: {message}\n\n"
#             else:
#                 yield f"data: Error: Platform not supported\n\n"
#         except Exception as e:
#             app.logger.error(f"Error during scraping: {str(e)}")
#             yield f"data: Error: {str(e)}\n\n"

#     return Response(generate(), content_type="text/event-stream")

logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

@app.route('/scrape-progress/<platform>', methods=['GET'])
def scrape_progress(platform):
    """Stream scraping progress messages for the selected platform using SSE."""
    username = request.args.get('username')
    password = request.args.get('password')

    if not username or not password:
        app.logger.error("Missing username or password.")
        return jsonify({"error": "Missing username or password"}), 400

    # Generate a unique key for the scraping session
    user_key = f"{username}-{platform}"

    @stream_with_context
    def generate():
        try:
            # Acquire the lock for the current user and platform
            with lock:
                if user_key in scraping_locks:
                    yield "data: Error: Scraping is already in progress for this user.\n\n"
                    return

                scraping_locks[user_key] = True  # Mark scraping as in progress

            app.logger.info(f"Starting scrape for {platform} with username: {username}")

            if platform == "Instagram":
                # Perform Instagram scraping
                scraper = perform_scraping(username, password)

                if scraper is None:
                    yield "data: Error: Scraper returned None\n\n"
                    return

                for message in scraper:
                    yield f"data: {message}\n\n"

                yield "data: Scraping complete!\n\n"
            elif platform == "Facebook":
                # Perform Facebook scraping
                for message in perform_facebook_tasks(username, password):
                    yield f"data: {message}\n\n"
            elif platform == "X":
                # Perform X scraping
                for message in perform_x_tasks(username, password):
                    yield f"data: {message}\n\n"
            else:
                yield f"data: Error: Platform {platform} not supported\n\n"
        except Exception as e:
            app.logger.error(f"Error during scraping: {str(e)}")
            yield f"data: Error: {str(e)}\n\n"
        finally:
            # Release the lock after scraping is complete
            with lock:
                scraping_locks.pop(user_key, None)

    return Response(generate(), content_type="text/event-stream")



# Define the OUTPUT_FOLDER
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(BASE_DIR, "Output")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)  # Ensure the folder exists

@app.route('/generate-pdf/<platform>', methods=['POST'])
def generate_pdf_route(platform):
    try:
        data = request.get_json()

        username = data.get("username")
        filter_text = data.get("filter")
        summary_enabled = data.get("summary", False)

        if not username:
            app.logger.error("Username is required for PDF generation.")
            return jsonify({"error": "Username is required for PDF generation."}), 400

        # Generate the summary and apply filters
        summary, result = generate_summary_and_apply_filter(
            filter_enabled=bool(filter_text),
            filter_text=filter_text,
            summary_enabled=bool(summary_enabled)
        )

        app.logger.info(f"Generated summary: {summary}, result: {result}")  # Debugging log

        # Check that result and summary are dictionaries (or similar objects with .get())
        if isinstance(result, str):
            return jsonify({"error": f"Unexpected result: {result}"}), 400

        if isinstance(summary, str):
            return jsonify({"error": f"Unexpected summary: {summary}"}), 400

        # Generate the PDF
        pdf_response = generate_pdf(username, summary, result)

        # Log the type of pdf_response
        app.logger.info(f"pdf_response type: {type(pdf_response)}")

        # If it's a generator, collect the final result
        if isinstance(pdf_response, types.GeneratorType):
            pdf_response = list(pdf_response)[-1]  # Collect the final result
        elif isinstance(pdf_response, dict):
            # If it's already a dictionary, no need to convert
            pass
        else:
            raise ValueError("Unexpected pdf_response type: {}".format(type(pdf_response)))

        # Check if PDF generation was successful
        if pdf_response.get("success"):
            filename = f"{username}_{platform}_Report.pdf"
            pdf_filepath = os.path.join(OUTPUT_FOLDER, filename)

            # Ensure the PDF file exists in the Output folder
            if not os.path.exists(pdf_filepath):
                raise Exception("PDF file was not created successfully.")

            # Return the filename for download
            return jsonify({
                "success": True,
                "filename": filename  # This will be used by the frontend to download the file
            })
        else:
            raise Exception(f"PDF generation failed: {pdf_response.get('error', 'Unknown error')}")

    except Exception as e:
        app.logger.error(f"Exception during PDF generation: {e}")
        return jsonify({"error": f"Exception during PDF generation: {e}"}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """
    Serve the generated PDF file from the Output folder.
    """
    try:
        return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)
    except Exception as e:
        app.logger.error(f"Error while serving file {filename}: {e}")
        return jsonify({"error": f"Unable to download file: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
