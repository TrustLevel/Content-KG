-> Under Construction...

# TrustLevel Knowledge Graph with Bias Detection and NER

This repository provides a system that processes articles, extracts named entities, detects bias using a gRPC API, and ingests the data into a Knowledge Graph. You can query the Knowledge Graph using a Streamlit interface.

## Features
- **Ingestion**: Load articles, entities, and bias scores into Memgraph.
- **Named Entity Recognition (NER)**: Extract entities from article text.
- **Bias Detection**: Analyze article bias via a gRPC API.
- **Querying**: Use a Streamlit interface to query articles and related entities from Memgraph.

## Prerequisites
- **Python 3.8+**
- **pip** (for Python dependencies)

## Setup
Follow these steps to set up the application:


1. Clone the Repository
```
git clone https://github.com/TrustLevel/trustlevel-app.git
cd trustlevel-app
```

2. Install Python Dependencies
```
python3 -m venv venv (windows)
source venv/bin/activate (macOS)
pip install -r requirements.txt
```

4. Start Streamlit App to handle CSV upload and extract entities:
```
streamlit run app.py
```

Streamlit will be available at http://localhost:8501.

Example CSV Format:
titel, text, author, trust_score
 
5. Close and restart Streamlit App to explore and query the Knowledge Graph:
```
streamlit run knowledge_graph.py
```
Enter a keyword or entity (e.g., “Trump”, “Israel”, “Gaza”).
The results will show related articles, and trust scores.


## License
This project is licensed under the Apache-2.0 License - see the LICENSE file for details.

## Authors
by TrustLevel Team - Let us know if you’d like any further adjustments or details!
