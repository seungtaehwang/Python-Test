from flask import Flask, jsonify
import os
import random
from flask_cors import CORS
import oracledb


app = Flask(__name__)
CORS(app) # 모든 경로(route)에 대해 CORS 활성화

# Oracle DB 연결 정보 설정
# 실제 환경에서는 환경 변수 등을 사용하여 보안을 강화하는 것이 좋습니다.
DB_USER = "your_username"
DB_PASSWORD = "your_password"
# Easy Connect 문자열 형식: hostname:port/service_name
DB_DSN = "localhost:1521/xe" # 예시: 'localhost:1521/orclpdb1'

def get_db_connection():
    """Oracle 데이터베이스 연결을 생성합니다."""
    try:
        connection = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
        return connection
    except Exception as e:
        print(f"데이터베이스 연결 실패: {e}")
        return None

@app.route("/")
def read_root():
    return {"Hello": "World"}

@app.route('/items', methods=['GET'])
def get_items():
    """데이터베이스에서 아이템 목록을 조회하는 API 엔드포인트."""
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        # 예시 쿼리: 실제 테이블 이름과 컬럼에 맞게 수정하세요.
        sql_query = "SELECT id, description, done FROM todoitem"
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        # 결과를 JSON 형식으로 변환
        items = []
        for row in rows:
            items.append({
                "id": row[0],
                "description": row[1],
                "done": bool(row[2])
            })
        print(items)
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/api/chartdata', methods=['GET'])
def get_chartdata():

    try:
        names = [{"name": "a"}, {"name": "b"}, {"name": "c"}]
        items = []
        for name in names:
            for i in range(10):   
                items.append({
                    "name": name["name"],
                    "xvalue": random.randint(1,100) ,
                    "yvalue": random.randint(50,100)
                })
        print(items)
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Flask 애플리케이션 실행 (개발 모드)
    app.run(debug=True)