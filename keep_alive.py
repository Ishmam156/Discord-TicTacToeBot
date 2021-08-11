from flask import Flask
from threading import Thread

# Initializing Flask Server
app = Flask('')

# Adding a root route to check if server is running
@app.route('/')
def main():
    return "Your bot is alive!"

# Defining the host and port
def run():
  app.run(host="0.0.0.0", port=8080)

# Start the server
def keep_alive():
    server = Thread(target=run)
    server.start()