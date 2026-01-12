from flask import Flask

app = Flask(__name__)

@app.route("/")
def landing():
    return "Server is up and running"



if __name__ == "__main__":
    app.run()
    print("Closing Server")

