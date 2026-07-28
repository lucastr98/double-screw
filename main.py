from src.llm_client import LLMClient
from src.extractor import DataExtractor
from src.data_processor import DataProcessor
import os

# Dublettenset Nr
DUPLICATE_IDS = [1]

def main():
    # Initialize components
    client = LLMClient()
    extractor = DataExtractor(client, debug=True)
    
    # Initialize data processor 
    data_dir = os.path.join(os.getcwd(), "data")
    processor = DataProcessor(data_dir, ids=DUPLICATE_IDS)
    
    out_dir = os.path.join(os.getcwd(), "out")
    os.makedirs(out_dir, exist_ok=True)

    for id in DUPLICATE_IDS:
        print(f"Processing data for Duplicate ID: {id}")
        duplicateset_data = processor.get_duplicateset_data(id)
        csv_result = extractor.extract(data=duplicateset_data)

        output_path = os.path.join(out_dir, f"duplicates_{id}.csv")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(csv_result)

if __name__ == "__main__":
    main()
