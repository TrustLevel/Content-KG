import pandas as pd
from kg_helpers import connect_to_memgraph, create_article_node, create_entity_node, create_relationship
from ner_module.ner import extract_entities
from grpc_bias_service.service import get_bias_score

def ingest_data(data: pd.DataFrame):
    connection = connect_to_memgraph()

    for _, row in data.iterrows():
        title = row['Headline']
        text = row['Text']

        # Extract NER entities
        entities = extract_entities(text)

        # Get bias score via gRPC
        bias_score = get_bias_score(text)

        # Insert data into Memgraph
        create_article_node(connection, title, row['Author'], row['Publisher'], bias_score)
        for entity in entities:
            create_entity_node(connection, entity)
            create_relationship(connection, title, entity)

if __name__ == "__main__":
    data = pd.read_csv("../data/input.csv")
    ingest_data(data)