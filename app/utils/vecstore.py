from utils.db_operations import connect_db
from pinecone import Pinecone
import numpy as np


def get_embedding(text):
    try:
        pc = Pinecone("pcsk_2KbJLN_4VvV5r2XDHLKa4rkWebiV34cUDQom8YYF3d6n6wvzmJCiKwEARi4bSTpGVLtsUH")

        data = [{"text": text}]

        embeddings = pc.inference.embed(
            model="llama-text-embed-v2",
            inputs=[d['text'] for d in data],
            parameters={"input_type": "passage"}
        )

        vectors = []
        for d, e in zip(data, embeddings):
            vectors.append({"values": e['values']})

        return vectors[0]['values']
    
    except Exception as e:
        print(f"Erro ao gerar embedding: {str(e)}")
        return None  # Retorna None para indicar falha


def store_embeddings(document):
    try:
        conn = connect_db()
        cur = conn.cursor()

        for doc in document:
            text = doc.page_content
            embedding = get_embedding(text)

            if embedding is None:
                continue  # Pula esse documento e continua com os próximos

            cur.execute("INSERT INTO documents (text, embedded_text) VALUES (%s, %s);", (text, embedding,))

        conn.commit()
        cur.close()
        conn.close()
    
    except Exception as e:
        print(f"Erro ao armazenar embeddings: {str(e)}")
