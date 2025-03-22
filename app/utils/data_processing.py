
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
import unicodedata
from langchain.docstore.document import Document

def clean_doc(doc: Document) -> Document:
    # Acessar o conteúdo do documento
    texto = doc.page_content
    
    # Remover tabulações e quebras de linha
    texto = texto.replace('\t', ' ').replace('\n', ' ')
    
    # Normalizar o texto para a forma canônica (sem acentuação e com caracteres especiais corrigidos)
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    
    # Remover múltiplos espaços em branco
    texto = re.sub(r'\s+', ' ', texto)
    
    # Remover espaços extras no início e no final
    texto = texto.strip()
    
    # Converter para minúsculas
    texto = texto.lower()
    
    # Retornar um novo documento com o texto limpo
    return Document(page_content=texto, metadata=doc.metadata)


def split_document(document, chunk_size=1000):
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=100
    )
    documents = text_splitter.split_documents([document])

    return documents
   
