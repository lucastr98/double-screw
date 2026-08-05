from src.llm_client import LLMClient
from src.extractor import DataExtractor
from src.data_processor import DataProcessor
from io import StringIO
import pandas as pd
import os

# Dublettenset Nr
DUPLICATE_IDS = [12]

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
        duplicateset_data_raw, duplicateset_data = processor.get_duplicateset_data(id)
        csv_result = extractor.extract(data=duplicateset_data)

        result_df = pd.read_csv(StringIO(csv_result))
        missing = duplicateset_data_raw[~duplicateset_data_raw['id'].isin(result_df['id'])].copy()
        if missing.empty:
            extended = result_df.copy()
        else:
            # left-join to bring in gruppe_id from result_df using material_description
            missing = missing.merge(
                result_df[['material_description', 'gruppe_id']],
                on='material_description',
                how='left'
            )

            # set requested fields
            missing['confidence_score'] = 1.0
            missing['explanation'] = 'equal'

            # keep same column order as result_df
            missing = missing[result_df.columns]

            # append to the original result_df
            extended = pd.concat([result_df, missing], ignore_index=True, sort=False)

        extended.sort_values(by='id').to_csv(os.path.join(out_dir, f"duplicates_{id}_new.csv"), index=False, encoding="utf-8")

if __name__ == "__main__":
    main()
