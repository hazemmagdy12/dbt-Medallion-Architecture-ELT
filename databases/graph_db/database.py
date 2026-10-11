import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

class Neo4jConnection:
    def __init__(self):
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USERNAME")  # التعديل حصل هنا
        pwd = os.getenv("NEO4J_PASSWORD")
        
        self.driver = GraphDatabase.driver(uri, auth=(user, pwd))

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters=None):
        """دالة عامة لتنفيذ أي أمر Cypher"""
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]

db = Neo4jConnection()