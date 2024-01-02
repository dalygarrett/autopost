from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

api_key = 'a5daebf51345716fdef2d975662e868c'
base_api_url = 'https://api.yextapis.com/v2/accounts/me/posts'

@app.route('/webhook', methods=['POST'])
def webhook_receiver():
    try:
        # Get the JSON payload from the incoming webhook
        payload = request.get_json()

        # Print the received payload for debugging
        print("Received payload:", payload)

        # Verify if the payload meets the specified criteria
        if is_valid_payload(payload):
            # Execute your API call using the payload
            execute_api_call(payload)
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'error': 'Invalid payload'}), 400

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def is_valid_payload(payload):
    # Check if eventType is ENTITY_CREATED and entityType is wp_post
    return (
        payload.get('meta', {}).get('eventType') == 'ENTITY_CREATED' and
        payload.get('primaryProfile', {}).get('meta', {}).get('entityType') == 'wp_post'
    )

def execute_api_call(payload):
    # Extract relevant data from the payload
    post_excerpt = payload.get('primaryProfile', {}).get('wp_postExcerpt', {}).get('markdown', '').replace('<p>', '').replace('</p>', '')
    photo_urls = [photo.get('image', {}).get('sourceUrl', '') for photo in payload.get('primaryProfile', {}).get('photoGallery', [])]

    # Construct the API request payload
    api_request_payload = {
        "entityIds": ["23539371"],
        "publisher": "FIRSTPARTY",
        "requiresApproval": False,
        "text": post_excerpt,
        "photoUrls": photo_urls
    }

    # Make the API call
    api_url = f"{base_api_url}?api_key={api_key}&v=20240102"
    headers = {'Content-Type': 'application/json'}

    response = requests.post(api_url, json=api_request_payload, headers=headers)

    # Process the API response as needed
    print(response.text)

if __name__ == '__main__':
    # Run the Flask application on port 5000 (adjust as needed)
    app.run(port=5000)
