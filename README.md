# TrustLevel Knowledge Graph with Bias Detection and NER

This repository provides a system that processes articles, extracts named entities, detects bias using a gRPC API, and ingests the data into a Knowledge Graph (Memgraph). You can query the Knowledge Graph using a Streamlit interface.

## Features
- **Ingestion**: Load articles, entities, and bias scores into Memgraph.
- **Named Entity Recognition (NER)**: Extract entities from article text.
- **Bias Detection**: Analyze article bias via a gRPC API.
- **Querying**: Use a Streamlit interface to query articles and related entities from Memgraph.

## Prerequisites
- **Python 3.8+**
- **Docker** (for Memgraph and Memgraph Lab)
- **pip** (for Python dependencies)

## Setup

Follow these steps to set up the application:


1. Clone the Repository
```
git clone https://github.com/your-username/trustlevel-app.git
cd trustlevel-app
```

2. Install Python Dependencies
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Set Up Environment Variables
Copy the example environment file and adjust the variables as needed:
```
cp server.env
```

4. Start Memgraph Using Docker
Use Docker Compose to start Memgraph and Memgraph Lab:
```
docker-compose up
```

• Memgraph will run on bolt://localhost:7687.
• Memgraph Lab will be available at http://localhost:3000.
 
5. Ingest Data into Memgraph
     a. Run the Streamlit app, which handles both CSV file uploads and querying:
      ```
      streamlit run src/app.py
      ```
     b. Upload a CSV file containing articles in the Streamlit interface.
     Example CSV Format:
      ```
      Headline,Author,Publisher,Text
      "Sample Headline","Author Name","Publisher Name","This is the article text."
      ```
      c. The app will extract entities, calculate bias scores, and ingest the data into Memgraph.


6. Query the Knowledge Graph

Once the data is ingested, you can use the Streamlit interface to query articles and entities based on a search term.

	1.	Enter a keyword or entity (e.g., “Trump”, “Israel”, “Gaza”).
	2.	The results will show related articles, extracted entities, and bias scores.

7. Explore the Knowledge Graph Visually

If you want to visualize and explore the data in the graph database, you can use Memgraph Lab:
	1. Visit http://localhost:3000 to access the Memgraph Lab interface.
	2. Use Cypher queries to explore the relationships between articles and entities.


## Testing
Run the tests for the application using pytest:
```
Run unit and integration tests using pytest:
pytest tests/
```
## Example Workflow

1. Upload CSV: The user uploads a CSV file of news articles.
2. Process Articles: The app processes each article:
	a. Extracts named entities (persons, organizations, locations) using the NER model.
	b. Calculates a bias score using the gRPC Bias Detection API.
	c. Stores the articles, entities, and bias scores in Memgraph.
3. Query and Explore: The user can search the Knowledge Graph through Streamlit and explore relationships between articles and entities in Memgraph Lab.


## Troubleshooting
1. gRPC Bias Detection: Ensure the gRPC Bias Detection API is running and accessible at the URL provided in your .env file.
2. Memgraph Connection Issues: If Memgraph isn’t connecting, ensure that Docker is running and that Memgraph is up and running on the correct port (7687).
3. File Upload Errors: Ensure that the uploaded CSV file matches the expected format (with columns for Headline, Author, Publisher, and Text).

## License
This project is licensed under the Apache-2.0 License - see the LICENSE file for details.

## Authors
TrustLevel Team
Let us know if you’d like any further adjustments or details!
