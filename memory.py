"""
    Aishu AI Chatbot
    Copyright (C) 2024  Abhinand Dhandapani

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import chromadb
from chromadb.utils import embedding_functions
import warnings

warnings.filterwarnings("ignore")

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./Memories")

collection = client.get_or_create_collection(name="memory",metadata={"hnsw:space": "cosine"},embedding_function=sentence_transformer_ef)

def store_conversation(message: dict):
    try:
        collection.add(documents=[f"{message['time']}:: user : {message['user']}\n aishu : {message['aishu']}"],ids=[message["time"]])
        return True
    except Exception as e:
        print(e)
        return e
    
def retrieve_conversation(context: str):
    results = collection.query(
        query_texts=[f"{context}"],
        n_results=3
    )
    return results
    
