#!/bin/bash

# Start Neo4j container - Add your password!
docker run -d --name neo4j -p7474:7474 -p7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest
echo "Neo4j running at http://localhost:7474 (Username: neo4j, Password: password)"