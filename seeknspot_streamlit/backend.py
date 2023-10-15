from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# Existing endpoint to receive a YouTube URL
@app.route('/receive-youtube-url', methods=['POST'])
def receive_youtube_url():
    data = request.get_json()
    youtube_url = data.get('youtubeURL')
    
    # Process the YouTube URL as needed
    with open('youtube_url.text', 'w') as file:
        file.write(youtube_url)
    
    return jsonify({'message': 'YouTube URL received'})

# New endpoint to receive a URL from Streamlit
@app.route('/send-url', methods=['POST'])
def send_url():
    data = request.get_json()
    url = data.get('url')
    
    # Write the URL to a text file
    with open('url.txt', 'w') as file:
        file.write(url)
    
    # Return a response to the extension
    print(url)
    return jsonify({"message": "URL received and saved to file"})

# New endpoint to serve the content of the url.txt file
@app.route('/get-url-file', methods=['GET'])
def get_url_file():
    try:
        with open('url.txt', 'r') as file:
            url = file.read()
        return jsonify({"url": url})  # Return the URL within a JSON response
    except Exception as e:
        return jsonify({"error": str(e)})  # Handle errors and return them as JSON


if __name__ == '__main__':
    app.run(host='localhost', port=5001)