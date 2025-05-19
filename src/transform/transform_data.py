import pandas as pd
import logging

def transform_users(input_path, output_path):
    logging.info("Đang xử lý dữ liệu người dùng")
    df = pd.read_csv(input_path)
    df_clean = df[['first_name', 'email']].copy()
    df_clean.rename(columns={
        'first_name': 'name',
        'email': 'email_address'
    }, inplace=True)
    df_clean.to_csv(output_path, index=False)
    logging.info(f"Đã lưu dữ liệu đã xử lý vào {output_path}")
    return df_clean