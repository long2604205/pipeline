import requests
import pandas as pd
import logging
import fitz
import pytesseract
from PIL import Image
import io
import cv2
import numpy as np

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

def extract_person_data(api_url, token, output_path):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    logging.info("Gọi API để lấy danh sách persons")
    response = requests.get(api_url, headers=headers)

    if response.status_code != 200:
        logging.error(f"Lỗi khi gọi API: {response.status_code} - {response.text}")
        return

    data = response.json()['data']['employee']

    persons = []
    for person in data:
        if (person['job_id'] is None
                or person['level'] is None
                or person['team'] is None):
            continue
        if not (isinstance(person.get("level"), dict) and "name" in person["level"]):
            continue
        persons.append({
            'id': person['id'],
            'full_name': person['last_name'] + " " + person['first_name'],
            'account_status': person['account_status'],
            'job' : person['job']['name'],
            'level': person['level']['name'],
        })

    df = pd.DataFrame(persons)
    df.to_csv(output_path, index=False)
    logging.info(f"Đã lưu dữ liệu thô vào {output_path}")


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        # Convert PDF page to pixmap image (300 dpi)
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))

        # Convert PIL image to OpenCV format
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # Grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31, 11
        )

        # OCR with pytesseract
        text = pytesseract.image_to_string(thresh, lang="vie+eng")
        full_text += text + "\n"

    return full_text