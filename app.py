from flask import Flask, jsonify
from gensim.models import Word2Vec
import psycopg2
import os

app = Flask(__name__)

# Load the trained embeddings model
model = Word2Vec.load('product_embeddings.model')


@app.route('/recommend', methods=['GET'])

def recommend():
    """
    Generate product recommendations based on purchase history.
    This function connects to a PostgreSQL database to retrieve distinct product IDs from the purchases table.
    It then uses a pre-trained word2vec model to find similar products for each product ID and returns the recommendations
    in JSON format.
    """
    
    connection = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
        port=os.getenv("PORT") 
    )

    # Create a cursor object using the connection
    cursor = connection.cursor()

    # Get distinct product IDs from the purchases table
    cursor.execute("SELECT DISTINCT product_id FROM purchases")
    data = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Extract product IDs from database
    product_ids = [str(record[0]) for record in data]

    # Find similar products for each product_id in the database
    recommendations = {}

    """
    Returns:
        JSON: A JSON object containing product recommendations. Each key is a product ID, and the value is a list of 
        similar products with their similarity scores. If a product ID is not found in the embeddings, an error message 
        is returned for that product ID.
    """

    for product_id in product_ids:
        if product_id in model.wv:
            similar_products = model.wv.most_similar(product_id, topn=5)
            recommendations[product_id] = [
                {'product_id': prod, 'similarity': score} for prod, score in similar_products
            ]
        else:
            recommendations[product_id] = {
                "error": "Product not found in embeddings."}

    return jsonify(recommendations)

if __name__ == '__main__':
     port = int(os.getenv("PORT_APP", 5000))  # Use PORT environment variable if it exists
     app.run(host="0.0.0.0", port=port, debug=True)