from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import boto3
import json

app = Flask(__name__)

# Function to get database credentials from AWS Secrets Manager
def get_db_credentials(secret_name):
    client = boto3.client('secretsmanager')
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

# Replace 'your_secret_name' with your actual secret name in AWS Secrets Manager
db_credentials = get_db_credentials('your_secret_name')

# Configure SQLAlchemy with the PostgreSQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{db_credentials['username']}:{db_credentials['password']}@{db_credentials['host']}:{db_credentials['port']}/{db_credentials['dbname']}"
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

@app.route("/")
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
