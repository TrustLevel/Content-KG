import mgclient

def connect_to_memgraph():
    connection = mgclient.connect(host='127.0.0.1', port=7687)
    return connection.cursor()

def create_article_node(connection, title, author, publisher, bias_score):
    query = """
    CREATE (a:Article {title: $title, author: $author, publisher: $publisher, bias_score: $bias_score})
    """
    connection.execute(query, {"title": title, "author": author, "publisher": publisher, "bias_score": bias_score})

def create_entity_node(connection, name):
    query = "CREATE (e:Entity {name: $name})"
    connection.execute(query, {"name": name})

def create_relationship(connection, article_title, entity_name):
    query = """
    MATCH (a:Article {title: $article_title}), (e:Entity {name: $entity_name})
    CREATE (a)-[:MENTIONS]->(e)
    """
    connection.execute(query, {"article_title": article_title, "entity_name": entity_name})