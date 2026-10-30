from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import asyncpg

app = FastAPI()


# Функция для подключения к базе данных
async def get_db_connection():
    conn = await asyncpg.connect(
        user="username", password="password", database="name", host="127.0.0.1"
    )
    return conn


from pydantic import BaseModel


class Issue(BaseModel):
    name_issue: str
    reason_issue: str
    description: str


@app.post("/add_issue")
async def add_issue(issue: Issue):
    conn = await get_db_connection()
    try:
        await conn.execute(
            "INSERT INTO issues (name_issue, reason_issue, description) VALUES ($1, $2, $3)",
            issue.name_issue,
            issue.reason_issue,
            issue.description,
        )
        return {"message": "Issue added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()


@app.get("/check_issue/{issue_id}")
async def check_issue(issue_id: int):
    conn = await get_db_connection()
    issue = await conn.fetchrow("SELECT * FROM issues WHERE id = $1", issue_id)
    await conn.close()
    if issue:
        return {"issue": issue}
    return {"error": "Issue not found"}


@app.post("/analyze_issue")
async def analyze_issue():
    # Путь к файлу, который необходимо отправить
    file_path = "feature_lines.txt"

    # Проверяем, существует ли файл
    try:
        return FileResponse(file_path, media_type="text/plain", filename=file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5002)
