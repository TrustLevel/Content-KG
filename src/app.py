from flask import Flask, request, jsonify
import pandas as pd
from ner_module import extract_entities  # Import NER function
from grpc_bias_service.service import get_bias_score  # Import gRPC function for bias detection
from kg_helpers import connect_to_memgraph, create_article_node, create_entity_node, create_relationship  # Memgraph helpers

# Initialize Flask app
app = Flask(__name__)

# Connect to Memgraph (replaces Neo4j)
connection = connect_to_memgraph()

# Upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    df = pd.read_csv(file)

    results = []
    for _, row in df.iterrows():
        text = row['Text']

        # Step 1: NER processing
        entities = extract_entities(text)

        # Step 2: Bias detection using gRPC
        bias_score = get_bias_score(text)

        # Step 3: Add article and entities to Knowledge Graph
        add_to_knowledge_graph(row['Headline'], row['Author'], row['Publisher'], bias_score, entities)

        results.append({
            'article': row['Headline'],
            'entities': entities,
            'bias_score': bias_score
        })

    return jsonify(results)

def add_to_knowledge_graph(title, author, publisher, bias_score, entities):
    # Use Memgraph connection instead of Neo4j
    # Insert article node
    create_article_node(connection, title, author, publisher, bias_score)

    # Insert entity nodes and relationships
    for entity, label in entities:
        create_entity_node(connection, entity)
        create_relationship(connection, title, entity)

if __name__ == '__main__':
    app.run(debug=True)