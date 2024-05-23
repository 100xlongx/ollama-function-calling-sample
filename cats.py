from flask import Flask, request, jsonify
import random

app = Flask(__name__)

cat_facts = [
    "Cats have five toes on their front paws, but only four toes on their back paws.",
    "A group of cats is called a clowder.",
    "Cats can rotate their ears 180 degrees.",
    "A cat's nose is as unique as a human's fingerprint."
]

@app.route('/api/cat_facts', methods=['POST'])
def get_cat_facts():
    data = request.json
    amount = data.get('amount', 1)
    
    facts = random.sample(cat_facts, min(amount, len(cat_facts)))
    
    return jsonify(facts)

if __name__ == '__main__':
    app.run(port=5002)
