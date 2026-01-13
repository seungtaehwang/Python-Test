from fastapi import FastAPI
from pydantic import BaseModel  

app = FastAPI()

class Item(BaseModel):
    id: int
    description: str
    done: bool

@app.get("/")
async def read_root():
    return {"Hello": "World"}   

@app.get("/items", response_model=list[Item])
async def get_items():
    """데이터베이스에서 아이템 목록을 조회하는 API 엔드포인트."""
    # 실제 데이터베이스 연결 및 쿼리 로직을 여기에 구현해야 합니다.
    # 아래는 예시 데이터입니다.
    items = [
        Item(id=1, description="Item 1", done=False),
        Item(id=2, description="Item 2", done=True),
        Item(id=3, description="Item 3", done=False),
    ]
    return items

# FastAPI 애플리케이션은 Uvicorn과 같은 ASGI 서버를 사용하여 실행해야 합니다.
# 예: uvicorn app:app --reload
