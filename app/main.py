import os
import httpx
from fastapi import FastAPI, Query
from dotenv import load_dotenv

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

YOUTRACK_BASE_URL = "https://bigabid.youtrack.cloud"
YOUTRACK_TOKEN = "perm-ZGVla3NoYS5z.NTUtMjE=.cpxN0iA1p9M5KOJbr9u6roxJRvRB9s"

HEADERS = {
    "Authorization": f"Bearer {YOUTRACK_TOKEN}",
    "Accept": "application/json"
}

# --------------------------------------------------
# FastAPI app
# --------------------------------------------------
app = FastAPI(
    title="YouTrack FastAPI Service",
    description="Unified API for YouTrack Agile, Sprints, Tickets, and Knowledge Base",
    version="1.0.0"
)

# --------------------------------------------------
# Shared HTTP client
# --------------------------------------------------
async def yt_get(path: str, params: dict | None = None):
    async with httpx.AsyncClient(headers=HEADERS, timeout=30) as client:
        response = await client.get(
            f"{YOUTRACK_BASE_URL}{path}",
            params=params
        )
        response.raise_for_status()
        return response.json()

# --------------------------------------------------
# Health / Connectivity
# --------------------------------------------------
@app.get("/health")
async def health():
    """
    Verify token and YouTrack connectivity
    """
    user = await yt_get(
        "/api/users/me",
        params={"fields": "login,name"}
    )
    return {
        "status": "ok",
        "connected_user": user
    }

# --------------------------------------------------
# Agile Boards
# --------------------------------------------------
@app.get("/agile/boards")
async def get_agile_boards():
    """
    List all agile boards
    """
    return await yt_get(
        "/api/agiles",
        params={"fields": "id,name,projects(name)"}
    )

# --------------------------------------------------
# Sprints for a Board
# --------------------------------------------------
@app.get("/agile/{board_id}/sprints")
async def get_sprints(board_id: str):
    """
    List sprints for a specific agile board
    """
    return await yt_get(
        f"/api/agiles/{board_id}/sprints",
        params={
            "fields": "id,name,isActive,start,finish"
        }
    )

# --------------------------------------------------
# Issues by Team Member (optionally sprint)
# --------------------------------------------------
@app.get("/issues/by-user")
async def issues_by_user(
    username: str = Query(..., description="YouTrack login"),
    sprint: str | None = Query(None, description="Sprint name (optional)")
):
    """
    Get issues assigned to a specific team member
    """
    query = f"Assignee: {username}"
    if sprint:
        query += f" Sprint: {sprint}"

    return await yt_get(
        "/api/issues",
        params={
            "query": query,
            "fields": "idReadable,summary,created,customFields(name,value(name))"
        }
    )

# --------------------------------------------------
# Issues by Sprint
# --------------------------------------------------
@app.get("/issues/by-sprint")
async def issues_by_sprint(sprint_name: str):
    """
    Get all issues in a sprint
    """
    return await yt_get(
        "/api/issues",
        params={
            "query": f"Sprint: {sprint_name}",
            "fields": "idReadable,summary,assignee(login)"
        }
    )

# --------------------------------------------------
# Generic Issue Search (IMPORTANT)
# --------------------------------------------------
@app.get("/issues/search")
async def search_issues(
    query: str = Query(..., description="YouTrack query language")
):
    """
    Generic search endpoint for all important use cases
    Example:
    - project:DATAOPS State:Open
    - Sprint:SP-12 Assignee:deeksha
    """
    return await yt_get(
        "/api/issues",
        params={
            "query": query,
            "fields": "idReadable,summary,assignee(login),created"
        }
    )

# --------------------------------------------------
# Knowledge Base Articles
# --------------------------------------------------
@app.get("/kb/articles")
async def get_kb_articles():
    """
    List knowledge base articles
    """
    return await yt_get(
        "/api/articles",
        params={
            "fields": "id,title,created,updated"
        }
    )

# --------------------------------------------------
# Single Knowledge Base Article
# --------------------------------------------------
@app.get("/kb/articles/{article_id}")
async def get_kb_article(article_id: str):
    """
    Fetch a single knowledge base article
    """
    return await yt_get(
        f"/api/articles/{article_id}",
        params={
            "fields": "id,title,content"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
