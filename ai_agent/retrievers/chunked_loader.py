from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import CharacterTextSplitter

def load_and_chunk(file_path):
    loader = CSVLoader(file_path=file_path)
    docs = loader.load()
    splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    return splitter.split_documents(docs)

def load_all_chunks():

    import os
    current_dir = os.path.dirname(__file__)
    csv_path_vehicle = os.path.join(current_dir, "../data/vehicle_data.csv")
    csv_path_land = os.path.join(current_dir, "../data/land_data.csv")
    vehicle_chunks = load_and_chunk(os.path.abspath(csv_path_vehicle))
    land_chunks = load_and_chunk(os.path.abspath(csv_path_land))
    # vehicle_chunks = load_and_chunk("/data/vehicle_data.csv")
    # land_chunks = load_and_chunk("/data/land_data.csv")
    return vehicle_chunks + land_chunks