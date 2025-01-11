
from flask import Flask, render_template
from flask_socketio import SocketIO, send
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

#Store message history on the server
message_history = []  

@app.route('/')   
def index(): 
    return render_template('Server_Web_Socket.html')  
  
message_history = []  # Initialize the message history list

@socketio.on('connect')
def handle_connect():
    # Send the full message history to the newly connected client
    send({"type": "history", "data": message_history}, broadcast=True)  
    
@socketio.on('message') 
def handle_message(message):    
    print(f"Received message: {message}")
     
    storeInfo(message)  
     
    # Send the full message history as one message 
    send({"type": "history", "data": message_history}, broadcast=True)  
  
    # Send the latest message as a separate message
    send({'type': 'message', 'data': message}, broadcast=True)

def storeInfo(message): 
    # Append the message to the message history 
    message_history.append(message)
 
def run_flask():
    socketio.run(app, debug=True, host='0.0.0.0', port=80, use_reloader=False)
    
if __name__ == '__main__':
    
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
