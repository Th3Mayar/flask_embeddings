# Flask Product Recommendation API

This project is a Flask-based API that provides product recommendations using Word2Vec embeddings trained on purchase history.

## Features
- Fetch purchase history from a PostgreSQL database.
- Train a Word2Vec model to generate product embeddings.
- Serve recommendations via a REST API.

## Requirements
- Python 3.8+
- PostgreSQL
- Flask
- Gensim
- Psycopg2

## Installation

### 1. Clone the repository
```sh
git clone https://github.com/your-repo/flask-recommendations.git
cd flask-recommendations
```

### 2. Create a virtual environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies
```sh
pip install -r requirements.txt
```

## Configuration

### 1. Set environment variables
Create a `.env` file and set the following environment variables:
```sh
DB_NAME=your_database
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=your_host
DB_PORT=your_port
```

## Training the Model
Run the following command to train the Word2Vec model using purchase history:
```sh
python train_embeddings.py
```
This will generate a `product_embeddings.model` file.

## Running the API
```sh
python app.py
```
The API will start at `http://127.0.0.1:5000`.

## API Endpoints

### 1. Get Product Recommendations
**Endpoint:**
```http
GET /recommend
```
**Response Example:**
```json
{
  "1": [
    {"product_id": "2", "similarity": 0.95},
    {"product_id": "3", "similarity": 0.89}
  ]
}
```

## Deployment
To run the Flask app in production, use Gunicorn:
```sh
gunicorn --bind 0.0.0.0:5000 app:app
```
