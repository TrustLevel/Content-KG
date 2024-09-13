from flask import Flask, request, jsonify
import spacy
import pandas as pd
from grpc.service import get_bias_score
from neo4j import GraphDatabase

# Initialize Flask app
app = Flask(__name__)

# Load NER model
nlp = spacy.load("en_core_web_sm")

# Neo4j connection - Add your password!
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

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
    for index, row in df.iterrows():
        text = row['Text']

        # NER processing
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        # Bias detection using gRPC
        bias_score = get_bias_score(text)

        # Add article and entities to Knowledge Graph
        add_to_knowledge_graph(row['Headline'], row['Author'], row['Publisher'], bias_score, entities)

        results.append({
            'article': row['Headline'],
            'entities': entities,
            'bias_score': bias_score
        })

    return jsonify(results)

def add_to_knowledge_graph(title, author, publisher, bias_score, entities):
    with driver.session() as session:
        session.write_transaction(create_article_node, title, author, publisher, bias_score)
        for entity, label in entities:
            session.write_transaction(create_entity_node, entity, label)
            session.write_transaction(create_relationship, title, entity)

def create_article_node(tx, title, author, publisher, bias_score):
    query = """
    MERGE (a:Article {title: $title})
    SET a.author = $author, a.publisher = $publisher, a.bias_score = $bias_score
    """
    tx.run(query, title=title, author=author, publisher=publisher, bias_score=bias_score)

def create_entity_node(tx, entity, label):
    query = """
    MERGE (e:Entity {name: $entity})
    SET e.label = $label
    """
    tx.run(query, entity=entity, label=label)

def create_relationship(tx, title, entity):
    query = """
    MATCH (a:Article {title: $title})
    MATCH (e:Entity {name: $entity})
    MERGE (a)-[:MENTIONS]->(e)
    """
    tx.run(query, title=title, entity=entity)

if __name__ == '__main__':
    app.run(debug=True)