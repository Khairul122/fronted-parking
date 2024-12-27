from flask import Flask, render_template
from api import api_blueprint

app = Flask(__name__)

app.register_blueprint(api_blueprint, url_prefix='/api')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/parking')
def parking():
    return render_template('parking.html')

if __name__ == '__main__':
    app.run(debug=True)
