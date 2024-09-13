from kg_helpers import connect_to_memgraph

def query_kg(search_term):
    connection = connect_to_memgraph()
    query = f"""
        MATCH (a:Article)-[:MENTIONS]->(e:Entity)
        WHERE e.name CONTAINS '{search_term}' OR a.title CONTAINS '{search_term}'
        RETURN a.title, e.name, a.bias_score
    """
    results = connection.execute_and_fetch(query)
    return list(results)