import os
import tempfile

from utils.models import Model
from datetime import datetime

from langchain.document_loaders import Docx2txtLoader, PyPDFLoader
from utils.custom_loader import CustomDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS


embedding =  Model.embed_model()
date_update = datetime.now().strftime('%Y-%m-%d')

def get_documents(upload_files):

    documents = []

    for file in upload_files:

        file_extension = file.name.split('.')[1]

        if file_extension == 'doc' or file_extension == 'docx':
            
            temp_dir = tempfile.gettempdir()
            temp_file_path = os.path.join(temp_dir,file.name)

            with open(temp_file_path, 'wb') as f:
                f.write(file.getbuffer())

            document = Docx2txtLoader(temp_file_path).load()
            documents.extend(document)

            os.remove(temp_file_path)

        elif file_extension == 'pdf':

            temp_dir = tempfile.gettempdir()
            temp_file_path = os.path.join(temp_dir,file.name)

            with open(temp_file_path, 'wb') as f:
                f.write(file.getbuffer())

            document = PyPDFLoader(temp_file_path).load()
            documents.extend(document)

            os.remove(temp_file_path)

        else:

            temp_dir = tempfile.gettempdir()
            temp_file_path = os.path.join(temp_dir, file.name)

            with open(temp_file_path, 'wb') as f:
                f.write(file.getbuffer())

            document = CustomDocumentLoader(temp_file_path).load()
            documents.extend(document)

            os.remove(temp_file_path)

    return documents


def get_chunks(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000,
        chunk_overlap=1000 
    )

    chunks = splitter.split_documents(documents)
    return chunks


def get_vector_store(chunks, session_id):

    vector_store = FAISS.from_documents(chunks, embedding=embedding)
    vector_store.save_local(f'./db/faiss_index_{date_update}_{session_id}')