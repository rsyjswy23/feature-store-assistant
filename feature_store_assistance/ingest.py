import os
import pandas as pd
import minsearch

DATA_PATH = os.getenv("DATA_PATH", "../data/feature_store_data.csv")

def load_index(data_path=DATA_PATH):
    df = pd.read_csv(data_path)

    documents = df.to_dict(orient="records")

    index = minsearch.Index(
        text_fields=[
            "feature_name",
            "feature_group", 
            "computation_logic",
            "data_source",
            "update_frequency",
            "serving_store",
            "models_using_feature",
            "feature_description"
        ],
        keyword_fields=["id"],
    )

    index.fit(documents)
    return index