from utils.vecstore import get_embedding
import numpy as np


def retriever(question, conn):
    # Gerar embedding da pergunta
    embedded_question = get_embedding(question)
    
    # Query SQL para buscar os 3 mais similares
    query = """
    SELECT text_id, text, embedded_text <-> %s::vector AS distancia
    FROM documents
    ORDER BY distancia ASC
    LIMIT 3;
    """
    
    with conn.cursor() as cursor:
        cursor.execute(query, (embedded_question,))
        resultados = cursor.fetchall()  # Obtém os 3 resultados
    
    # Retorna os textos como uma lista
    return [resultado[1] for resultado in resultados] if resultados else []

def generate_answer_with_rag(client, question, retrieved_texts):
    # Combine os documentos em um único contexto
    context = "\n".join([text for text in retrieved_texts])

    # Crie o prompt com a pergunta e o contexto
    prompt = (
    "Você é um especialista em responder perguntas com base em documentos fornecidos. "
    "Seu objetivo é gerar uma resposta clara e precisa com base no contexto dado. Responda "
    "utilizando as informações mais relevantes do contexto. Não repita a pergunta e evite frases como 'a resposta é'. "
    "Caso a pergunta não tenha uma resposta direta, ou você não saiba, forneça informações relacionadas ou direcione para o que for mais relevante"
    "De forma alguma crie novo conteúdo, se atenha ao contexto dado.\n\n"
    f"Contexto:\n{context}\n\n"
    f"Pergunta: {question}\n\n"
    "Resposta:"
)

    # Envie o prompt para o modelo Groq
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_completion_tokens=300
    )

    # Retorne a resposta gerada
    return response.choices[0].message.content.strip()


def rag(conn, client, question):
    retrieved_texts = retriever(question, conn)
    
    if not retrieved_texts:
        return "Desculpe, não encontrei informações relevantes para responder sua pergunta."
    
    while True:
        answer = generate_answer_with_rag(client, question, retrieved_texts)

        verification_prompt = f"""
        Contexto fornecido:
        {retrieved_texts}

        Resposta gerada:
        {answer}

        A resposta contém apenas informações do contexto fornecido? 
        Responda apenas 'sim' se estiver correta e 'não' se houver informações novas ou inventadas.
        """

        # Usa a LLM para validar a resposta
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": verification_prompt}],
            temperature=0.7,
            max_completion_tokens=10
        )

        validation_result = response.choices[0].message.content.strip().lower()

        if "sim" in validation_result:
            return answer
