import requests
import pandas as pd
import logging

def extract_users(api_url, output_path):
    logging.info("Gọi API để lấy danh sách users")
    response = requests.get(api_url)
    data = response.json()['results']

    users = []
    for user in data:
        users.append({
            'first_name': user['name']['first'],
            'last_name': user['name']['last'],
            'email': user['email'],
            'country': user['location']['country']
        })

    df = pd.DataFrame(users)
    df.to_csv(output_path, index=False)
    logging.info(f"Đã lưu dữ liệu thô vào {output_path}")