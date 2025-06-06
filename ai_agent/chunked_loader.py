from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import CharacterTextSplitter

def load_and_chunk(file_path):
    loader = CSVLoader(file_path=file_path)
    docs = loader.load()
    splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    return splitter.split_documents(docs)

def load_all_chunks():
    vehicle_chunks = load_and_chunk("../data/vehicle_data.csv")
    land_chunks = load_and_chunk("../data/land_data.csv")
    return vehicle_chunks + land_chunks