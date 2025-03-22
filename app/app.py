import os
import streamlit as st
from utils.rag_tools import rag
from utils.vecstore import *
from utils.data_processing import *
from utils.load_documents import *
from groq import Groq
import psycopg2
import json


def main():
        
    # Configuração da API
    groq_api_key = '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'  
    client = Groq(api_key=groq_api_key)

    st.title("Assistente Inteligente 📚")
    conn = connect_db()

    # Recuperar histórico do banco de dados
    with conn.cursor() as cur:
        cur.execute("SELECT historic FROM chat_history ORDER BY id ASC")  # ASC para obter tudo
        result = cur.fetchone()

    # Garantir que o histórico seja uma lista válida
    if result and result[0]:
        try:
            # Se o histórico no banco de dados já estiver em formato de lista (não uma string JSON)
            if isinstance(result[0], list):
                st.session_state.messages = result[0]
            else:
                # Se for uma string JSON, então faça o parse
                st.session_state.messages = json.loads(result[0])
        except json.JSONDecodeError:
            st.session_state.messages = []  # Se não conseguir decodificar, inicialize com uma lista vazia
    else:
        st.session_state.messages = []

    #exibir historico
    with st.expander("📜 Histórico de Chats"):
        for message in st.session_state.messages[-5:]:  # Exibir as últimas 5 mensagens
            if isinstance(message, dict) and "role" in message:  # Verifique se é um dicionário válido
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])


    # Upload de documento
    uploaded_file = st.file_uploader("Carregue um documento para adicionar ao RAG", type=["pdf", "txt", "docx"])

    if uploaded_file is not None:
        try:
            with st.spinner("Processando documento..."):
                doc_text = extract_text_from_document(uploaded_file)
                cleaned_text = clean_doc(doc_text)
                documents = split_document(cleaned_text)
                store_embeddings(documents)
            st.success("Documento processado e embeddings armazenados com sucesso!")
        except Exception as e:
            st.error(f"Erro ao processar o documento: {str(e)}")
            st.session_state.messages.append({"role": "assistant", "content": f"Erro ao processar o documento: {str(e)}"})

    # Entrada do usuário
    if user_input := st.chat_input("Faça sua pergunta..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Gerar resposta
        with st.chat_message("assistant"):
            try:
                response = rag(conn, client, user_input)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_message = f"Desculpe, ocorreu um erro ao processar sua solicitação: {str(e)} 😓"
                st.markdown(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

        # **Salvar o histórico atualizado no banco**
        with conn.cursor() as cur:
            cur.execute("INSERT INTO chat_history (historic) VALUES (%s)", (json.dumps(st.session_state.messages),))
            conn.commit()  # Confirma a transação




if __name__ =='__main__':
    main()

