import pandas as pd
import json
import os

INPUT_TABLE_NAME = "dubletten_analyse"
RENAME_COLUMNS = {
    "Dublettenset Nr": "duplicate_id",
    "Material Bez": "material_description",
}
ID_COL = "duplicate_id"

class DataProcessor:
    def __init__(self, data_dir: str, ids: list = None):
        self.data_dir = data_dir
        self.ids = ids
        self.data = self.load_and_filter_csv(f"{INPUT_TABLE_NAME}.csv", list(RENAME_COLUMNS.keys()))

    def load_and_filter_csv(self, filename: str, columns: list) -> pd.DataFrame:
        """Loads a CSV, filters columns, and returns a df."""
        path = os.path.join(self.data_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}") 
        
        try:
            df = pd.read_csv(path, sep=";", encoding="latin-1")
            filtered_df = df[columns]
            filtered_df.rename(columns=RENAME_COLUMNS, inplace=True)
            if self.ids is not None and ID_COL in filtered_df.columns:
                filtered_df = filtered_df[filtered_df[ID_COL].isin(self.ids)]
            return filtered_df

        except Exception as e:
            raise RuntimeError(f"Error processing {filename}: {e}")

    def get_duplicateset_data(self, duplicate_id: int) -> tuple[pd.DataFrame, dict]:
        """Returns data for a specific duplicate_id."""
        if ID_COL not in self.data.columns:
            raise ValueError(f"{ID_COL} column is missing in the data.")
        
        filtered_data = self.data[self.data[ID_COL] == duplicate_id]
        if filtered_data.empty:
            raise ValueError(f"No data found for {ID_COL}={duplicate_id}.")

        filtered_data = filtered_data.reset_index(drop=True)
        filtered_data.insert(0, "id", range(len(filtered_data)))

        filtered_data_json = filtered_data.drop_duplicates('material_description').drop(columns=['duplicate_id'])

        return filtered_data, filtered_data_json.to_json(orient="records")
