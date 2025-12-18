# YouTrack MCP Server

A Python-based **MCP (Model Context Protocol) server** that exposes key **YouTrack** capabilities—issues, Agile boards, sprints, and Knowledge Base—for seamless use with **VS Code Copilot** and other LLM-powered tools.

This project started as a **POC** and is designed to be easily extended and hosted (e.g., on AWS) for team-wide usage.

---

##  Features

* 🔍 View and search YouTrack issues
*  Create new issues
*  Access Agile boards and sprints
*  Fetch tickets per user or sprint
*  Read and summarize Knowledge Base articles
*  MCP-compatible for Copilot / LLM workflows
*  Built on FastAPI with OpenAPI support

---

##  Architecture

```
VS Code Copilot / LLM
        ↓ (MCP)
YouTrack MCP Server (FastAPI)
        ↓ (REST)
      YouTrack API
```

---

##  Tech Stack

* Python 3.10+
* FastAPI
* MCP
* httpx
* Docker
* YouTrack REST API

---

##  Getting Started

### 1. Clone the Repository

```bash
git clone <repo-url>
cd youtrack-mcp-server
```

### 2. Configure Environment Variables

Create a `.env` file:

```env
YOUTRACK_BASE_URL=https://youtrack.mycompany.com
YOUTRACK_TOKEN=perm:xxxxxxxxxxxxxxxx
```

---

##  Run Locally (Without Docker)

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open:

* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* OpenAPI spec: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

---

##  Run with Docker

### Build Image

```bash
docker build -t youtrack-fastapi .
```

### Run Container

```bash
docker run -d -p 8000:8000 --name youtrack-api youtrack-fastapi
```

---

##  MCP Integration (VS Code Copilot)

Create an `mcp.json`:

```json
{
  "name": "youtrack-fastapi",
  "description": "MCP server for YouTrack FastAPI endpoints",
  "version": "1.0.0",
  "openapi": "http://localhost:8000/openapi.json"
}
```

Register this MCP server in VS Code Copilot to start querying YouTrack using natural language.

---

##  Example Use Cases

* "Show my open tickets for the current sprint"
* "Create a YouTrack issue for a data pipeline failure"
* "Search old incidents related to Athena"
* "Summarize the onboarding KB article"

---

##  Future Enhancements

* AWS deployment (ECS / EKS)
* Authentication & rate limiting
* Caching YouTrack metadata
* Sprint velocity & burndown APIs
* Semantic search over KB articles

---

##  License

Internal / POC (update as needed)

---

##  Contributing

This project is currently a POC. Contributions and feedback are welcome as it evolves toward a shared internal tool.
