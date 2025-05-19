from sqlalchemy import create_engine
import logging

def load_to_mysql(df, mysql_config):
    logging.info("Đang đẩy dữ liệu vào MySQL")
    conn_str = f"mysql+pymysql://{mysql_config['user']}:{mysql_config['password']}@{mysql_config['host']}/{mysql_config['database']}"
    engine = create_engine(conn_str)
    df.to_sql(mysql_config['table'], con=engine, if_exists='append', index=False)
    logging.info("Đã đẩy dữ liệu thành công vào MySQL")