from flask import Flask, jsonify
import mgclient

app = Flask(__name__)

def connect_to_memgraph():
    conn = mgclient.connect(host='127.0.0.1', port=7687)
    return conn

@app.route('/get_entities/<article_title>', methods=['GET'])
def get_entities(article_title):
    conn = connect_to_memgraph()
    cursor = conn.cursor()
    query = """
    MATCH (a:Article {title: $article_title})-[:MENTIONS]->(e:Entity)
    RETURN e.name, e.type
    """
    cursor.execute(query, {'article_title': article_title})
    entities = [{"name": row[0], "type": row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(entities)

if __name__ == '__main__':
    app.run(debug=True)
