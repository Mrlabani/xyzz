import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, this is your Telegram bot running on Render!"

# Your existing bot code goes here...

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render sets the PORT environment variable
    app.run(host='0.0.0.0', port=port)
