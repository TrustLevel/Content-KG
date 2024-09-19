import streamlit as st
import pandas as pd
import spacy
from memgraph import Memgraph

# Initialize SpaCy model
nlp = spacy.load("en_core_web_sm")

# Connect to Memgraph
memgraph = Memgraph()

def add_article_to_graph(article, entities):
    query = """
    MERGE (a:Article {title: $title, trust_score: $trust_score})
    WITH a
    UNWIND $entities as entity
    MERGE (e:Entity {name: entity})
    MERGE (a)-[:MENTIONS]->(e)
    """
    memgraph.execute(query, {'title': article['title'], 'trust_score': article['trust_score'], 'entities': entities})

def process_article(content):
    doc = nlp(content)
    entities = [ent.text for ent in doc.ents]
    return entities

# Function to search for articles mentioning a specific entity and sort by trust score
def query_articles_by_entity(entity):
    query = """
    MATCH (a:Article)-[:MENTIONS]->(e:Entity {name: $entity})
    RETURN a.title AS title, a.trust_score AS trust_score
    ORDER BY a.trust_score DESC
    """
    result = memgraph.execute(query, {'entity': entity})
    return result

# Streamlit interface
st.title("Knowledge Graph App")

# CSV file uploader
csv_file = st.file_uploader("Upload a CSV file with articles", type=["csv"])

if csv_file:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Process each article
    for _, row in df.iterrows():
        article = {'title': row['title'], 'content': row['content'], 'trust_score': row['trust_score']}
        entities = process_article(article['content'])
        add_article_to_graph(article, entities)
    
    st.success("Articles and entities added to the graph!")

# Entity search input
entity_search = st.text_input("Enter an entity to search for articles mentioning it:")

if entity_search:
    try:
        # Query articles mentioning the entity
        articles = query_articles_by_entity(entity_search)

        if articles:
            st.write(f"Articles mentioning '{entity_search}':")
            for article in articles:
                st.write(f"Title: {article['title']} - Trust Score: {article['trust_score']}")
        else:
            st.write(f"No articles mention '{entity_search}'.")
    except ServiceUnavailable:
        st.error("Memgraph service is not available. Ensure Memgraph is running and connected.")
