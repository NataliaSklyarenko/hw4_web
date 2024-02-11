from flask import Flask, render_template, request, redirect, url_for
import socket
import json
from datetime import datetime
from threading import Thread

app = Flask(__name__)

# HTTP server routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        username = request.form['username']
        message = request.form['message']
        send_message_to_socket_server(username, message)
        return redirect(url_for('index'))
    return render_template('message.html')

# Serve static files
@app.route('/<path:filename>')
def serve_static(filename):
    return app.send_static_file(filename)

# 404 Error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

# Socket server thread function
def socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(('localhost', 5000))
        print("Socket server running on port 5000...")
        while True:
            data, _ = server_socket.recvfrom(1024)
            message_data = json.loads(data.decode())
            save_message_to_file(message_data['username'], message_data['message'])

# Save message to file
def save_message_to_file(username, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    message_data = {timestamp: {'username': username, 'message': message}}
    with open('storage/data.json', 'a+') as file:
        file.seek(0)
        try:
            messages = json.load(file)
        except json.decoder.JSONDecodeError:
            messages = {}
        messages.update(message_data)
        file.seek(0)
        json.dump(messages, file, indent=2)

# Send message to socket server
def send_message_to_socket_server(username, message):
    message_data = {'username': username, 'message': message}
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.sendto(json.dumps(message_data).encode(), ('localhost', 5000))

if __name__ == '__main__':
    # Start Socket server in a separate thread
    socket_thread = Thread(target=socket_server)
    socket_thread.daemon = True
    socket_thread.start()

    # Run HTTP server
    app.run(port=3000)
