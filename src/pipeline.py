import logging
from utils.helpers import load_config
from extract.extract_data import extract_users
from transform.transform_data import transform_users
from load.load_data import load_to_mysql

logging.basicConfig(level=logging.INFO)

def main():
    config = load_config("../config/pipeline_config.yaml")

    # Extract
    extract_users(config["api_url"], config["raw_csv"])

    # Transform
    df_clean = transform_users(config["raw_csv"], config["processed_csv"])

    # Load
    load_to_mysql(df_clean, config["mysql"])

if __name__ == "__main__":
    main()