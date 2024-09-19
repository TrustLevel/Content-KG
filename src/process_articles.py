import csv
import mgclient
from ner_module.ner import extract_entities  # Import the NER module

def load_articles(csv_path):
    """
    Load articles from a CSV file.
    
    :param csv_path: Path to the CSV file
    :return: List of articles with title, content, and trust score
    """
    articles = []
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            articles.append({
                "title": row['title'],
                "content": row['content'],
                "trust_score": row['trust_score']
            })
    return articles

def connect_to_memgraph():
    """
    Establish a connection to the Memgraph database.
    
    :return: Connection object
    """
    conn = mgclient.connect(host='127.0.0.1', port=7687)
    return conn

def create_article_node(conn, article):
    """
    Create an article node in the knowledge graph.
    
    :param conn: Connection object
    :param article: Dictionary containing article data
    """
    cursor = conn.cursor()
    query = """
    CREATE (a:Article {title: $title, content: $content, trust_score: $trust_score})
    """
    cursor.execute(query, {
        'title': article['title'],
        'content': article['content'],
        'trust_score': float(article['trust_score'])
    })
    conn.commit()

def create_entity_node(conn, entity):
    """
    Create an entity node in the knowledge graph.
    
    :param conn: Connection object
    :param entity: Tuple containing entity name and type
    """
    cursor = conn.cursor()
    query = """
    MERGE (e:Entity {name: $name, type: $type})
    """
    cursor.execute(query, {
        'name': entity[0],
        'type': entity[1]
    })
    conn.commit()

def create_mentions_relationship(conn, article_title, entity_name):
    """
    Create a MENTIONS relationship between an article and an entity.
    
    :param conn: Connection object
    :param article_title: Title of the article
    :param entity_name: Name of the entity
    """
    cursor = conn.cursor()
    query = """
    MATCH (a:Article {title: $article_title}), (e:Entity {name: $entity_name})
    CREATE (a)-[:MENTIONS]->(e)
    """
    cursor.execute(query, {
        'article_title': article_title,
        'entity_name': entity_name
    })
    conn.commit()

def process_articles_and_entities(csv_path):
    """
    Process the articles from the CSV file, extract entities, and update the knowledge graph.
    
    :param csv_path: Path to the CSV file
    """
    conn = connect_to_memgraph()  # Connect to Memgraph
    articles = load_articles(csv_path)  # Load articles from CSV

    for article in articles:
        # Create a node for the article
        create_article_node(conn, article)
        
        # Extract entities using SpaCy
        entities = extract_entities(article['content'])
        
        # Create nodes for each entity and link them to the article
        for entity in entities:
            create_entity_node(conn, entity)
            create_mentions_relationship(conn, article['title'], entity[0])
    
    print("Knowledge graph updated with articles and entities.")
