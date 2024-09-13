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

1. Clone the Repository
```bash
git clone https://github.com/your-username/trustlevel-app.git
cd trustlevel-app

2. Install Python Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Set Up Environment Variables
Copy the example environment file and adjust the variables as needed:
```bash
cp server.env

4. Start Memgraph Using Docker
Use Docker Compose to start Memgraph and Memgraph Lab:
```bash
docker-compose up

Memgraph will run on port 7687 and Memgraph Lab will be available at http://localhost:3000.

5. Ingest Data into Memgraph

Run the ingestion script to load sample data from data/input.csv:

cd src
python -m ingestion.main

6. Query the Knowledge Graph

Start the Streamlit app to query the graph:

streamlit run src/app.py

Visit http://localhost:8501 to query the articles, entities, and bias scores.

Testing

Run unit and integration tests using pytest:
pytest tests/

