from langchain_community.document_loaders import CSVLoader

def load_vehicle_data():
    loader = CSVLoader(file_path="data/vehicle_data.csv")
    return loader.load()

def load_land_data():
    loader = CSVLoader(file_path="data/land_data.csv")
    return loader.load()

def load_all_docs():
    vehicle_docs = CSVLoader(file_path="data/vehicle_data.csv").load()
    land_docs = CSVLoader(file_path="data/land_data.csv").load()
    return vehicle_docs + land_docs

if __name__ == "__main__":
    print(load_vehicle_data())


