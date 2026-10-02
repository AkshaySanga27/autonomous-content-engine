Autonomous Content & Campaign Automation Engine

An agentic marketing-content automation API built with Python, LangGraph, Gemini, ChromaDB, FastAPI, and Pydantic.

The application takes a campaign brief, retrieves relevant brand/product information from a local vector database, generates structured campaign content with an LLM, validates the result, and automatically revises the draft when validation fails.

Portfolio project: This repository is designed to demonstrate practical Agentic AI, RAG, structured LLM output, API development, validation, and workflow orchestration.

1. What this project does

The application automates a simplified marketing campaign workflow:

Campaign Request
      |
      v
+----------------+
| Campaign Plan  |
+----------------+
      |
      v
+----------------+
| ChromaDB RAG   | <--- Brand + Product Knowledge
+----------------+
      |
      v
+----------------+
| Gemini LLM     |
| Content Agent  |
+----------------+
      |
      v
+----------------+
| Pydantic +     |
| Rule Validator |
+----------------+
      |
   valid? ---- No ----> Revision Agent
      |                      |
     Yes <-------------------+
      |
      v
 Final Campaign JSON

Main capabilities

Accept campaign requirements through a REST API.

Validate incoming requests with Pydantic.

Store brand/product knowledge in ChromaDB.

Retrieve relevant context using semantic search.

Generate structured campaign content using Gemini.

Generate email content and social-media content according to requested channels.

Validate output length and required content.

Automatically run a revision loop when validation fails.

Keep workflow state with LangGraph.

Expose interactive Swagger/OpenAPI documentation.

Run locally without requiring a separate database server.

2. Technology stack

Technology

Purpose

Python

Main programming language

FastAPI

REST API

Uvicorn

Local ASGI server

LangGraph

Agent/workflow orchestration

Gemini API

LLM generation

LangChain Core

LLM message and structured-output integration

ChromaDB

Local vector database for RAG

Pydantic

Request/output schemas and validation

python-dotenv

Environment-variable loading

Pytest

Automated tests

HTTPX

HTTP testing/client support

3. Requirements

Before installing the project, make sure you have:

Python

Use Python 3.11 or newer.

Check your installation:

python --version

Git

Check Git:

git --version

Gemini API key

The project uses Google's Gemini API. You need a Google AI API key.

The key is stored locally in .env and is intentionally excluded from Git by .gitignore.

4. Clone the repository

If the project is already on GitHub:

git clone https://github.com/YOUR_USERNAME/autonomous-content-engine.git
cd autonomous-content-engine

Replace YOUR_USERNAME with your GitHub username.

5. Create a virtual environment

A virtual environment keeps this project's Python packages separate from your other projects.

Windows

python -m venv .venv
.venv\Scripts\activate

If PowerShell blocks activation, you can use:

.\.venv\Scripts\Activate.ps1

macOS / Linux

python3 -m venv .venv
source .venv/bin/activate

After activation, your terminal should show something similar to:

(.venv) C:\...\autonomous-content-engine>

6. Install dependencies

Upgrade pip first:

python -m pip install --upgrade pip

Then install the project's dependencies:

pip install -r requirements.txt

The main packages are:

fastapi
uvicorn
langgraph
langchain-core
langchain-google-genai
chromadb
pydantic
python-dotenv
pytest
httpx

7. Configure the Gemini API key

Create a local .env file from the example file.

Windows CMD

copy .env.example .env

PowerShell

Copy-Item .env.example .env

macOS / Linux

cp .env.example .env

Open .env:

GOOGLE_API_KEY=your_google_gemini_api_key
LLM_MODEL=gemini-2.0-flash

Replace:

your_google_gemini_api_key

with your actual API key.

Important

Never commit your .env file to GitHub.

The repository already contains:

.env

So your API key should remain local.

8. Knowledge base

The RAG system reads documents from:

knowledge_base/
├── brand_guidelines.txt
└── product_information.txt

These files contain the information that the LLM should use when generating campaign content.

For example, brand_guidelines.txt can contain:

Brand voice should be clear, practical, trustworthy and concise.
Avoid unsupported claims and exaggerated marketing language.

And product_information.txt can contain product features and factual information.

Adding your own knowledge

You can add additional .txt files to:

knowledge_base/

Example:

knowledge_base/
├── brand_guidelines.txt
├── product_information.txt
├── pricing.txt
├── faq.txt
└── company_information.txt

The application automatically reads .txt files when the ChromaDB collection is first initialized.

9. How the RAG system works

The RAG implementation is in:

app/rag/retriever.py

The process is:

Knowledge Base TXT Files
          |
          v
     ChromaDB
          |
          v
Semantic Retrieval
          |
          v
Relevant Context
          |
          v
Gemini Prompt
          |
          v
Generated Campaign

When the application starts using the retriever for the first time:

ChromaDB creates a persistent local database.

The .txt files inside knowledge_base/ are loaded.

Documents are added to the brand_knowledge collection.

The campaign request is converted into a search query.

ChromaDB retrieves the most relevant documents.

Retrieved information is inserted into the generation prompt.

The local database is stored in:

chroma_db/

It is ignored by Git because it can be regenerated locally.

10. Run the application

With the virtual environment activated:

python run.py

The server runs at:

http://127.0.0.1:8000

You should see a Uvicorn startup message similar to:

Uvicorn running on http://127.0.0.1:8000

11. Open Swagger API documentation

Open:

http://127.0.0.1:8000/docs

FastAPI automatically provides an interactive Swagger UI.

You can test the campaign endpoint directly from the browser without Postman.

Alternative OpenAPI documentation:

http://127.0.0.1:8000/redoc

12. Health check

The application exposes:

GET /health

Example:

curl http://127.0.0.1:8000/health

Expected response:

{
  "status": "ok"
}

13. Generate a campaign

Endpoint:

POST /api/campaign

Example request

{
  "product": "FlowTrack",
  "audience": "Small Businesses",
  "campaign_goal": "Generate product signups",
  "channels": [
    "email",
    "linkedin"
  ]
}

Using Swagger

Open http://127.0.0.1:8000/docs.

Find POST /api/campaign.

Click Try it out.

Paste the JSON request.

Click Execute.

Using curl

Windows PowerShell:

curl.exe -X POST "http://127.0.0.1:8000/api/campaign" `
  -H "Content-Type: application/json" `
  -d '{"product":"FlowTrack","audience":"Small Businesses","campaign_goal":"Generate product signups","channels":["email","linkedin"]}'

macOS/Linux:

curl -X POST http://127.0.0.1:8000/api/campaign \
  -H "Content-Type: application/json" \
  -d '{"product":"FlowTrack","audience":"Small Businesses","campaign_goal":"Generate product signups","channels":["email","linkedin"]}'

14. Supported channels

The current API accepts:

email
linkedin
twitter
instagram

Example:

{
  "product": "FlowTrack",
  "audience": "Startup Founders",
  "campaign_goal": "Increase product awareness",
  "channels": [
    "linkedin",
    "instagram"
  ]
}

The API rejects unsupported channel names through Pydantic validation.

15. Output format

The API returns a structured response containing:

{
  "request": {},
  "campaign": {},
  "validation_passed": true,
  "revision_count": 0,
  "retrieved_context": "..."
}

The campaign output contains:

campaign_summary
emails
social_posts

Email output

Each email contains:

{
  "subject": "...",
  "body": "..."
}

Social output

Each social post contains:

{
  "headline": "...",
  "body": "...",
  "call_to_action": "..."
}

16. LangGraph workflow

The workflow is implemented in:

app/graph/workflow.py

The graph contains these stages:

1. Plan

The planner combines:

product
+ audience
+ campaign goal

and sends that information to the RAG retriever.

2. Generate

The generation node calls Gemini with structured output based on the CampaignOutput Pydantic model.

3. Validate

The validator checks:

requested email channel has email content

requested social channels have social content

email subject length

email body length

social headline length

social body length

call-to-action length

4. Revision

If validation fails, the workflow sends the errors and existing draft back to the LLM.

The campaign can be revised up to two times.

5. Finish

The final validated or final-attempt campaign is returned by the API.

The simplified graph is:

plan
  |
  v
generate
  |
  v
validate
  |
  +---- valid ----> finish
  |
  +---- invalid --> revise
                       |
                       v
                    validate

17. Pydantic validation

The schemas are defined in:

app/models/schemas.py

Pydantic validates both incoming requests and generated campaign structures.

For example, this is rejected:

{
  "product": "A",
  "audience": "B",
  "campaign_goal": "C",
  "channels": ["youtube"]
}

because youtube is not currently an allowed channel.

Generated content also has maximum lengths to prevent oversized fields.

18. Project structure

autonomous-content-engine/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── graph/
│   │   ├── state.py
│   │   └── workflow.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   └── retriever.py
│   │
│   └── services/
│       ├── __init__.py
│       └── llm.py
│
├── knowledge_base/
│   ├── brand_guidelines.txt
│   └── product_information.txt
│
├── tests/
│   └── test_schemas.py
│
├── chroma_db/
│   └── generated automatically at runtime
│
├── .env
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── run.py

Important files

File

Purpose

run.py

Starts the Uvicorn server

app/main.py

Creates the FastAPI application

app/api/routes.py

REST API endpoints

app/models/schemas.py

Pydantic request/output models

app/graph/workflow.py

LangGraph agent workflow

app/graph/state.py

Workflow state definition

app/rag/retriever.py

ChromaDB RAG retrieval

app/services/llm.py

Gemini model configuration

knowledge_base/*.txt

Brand/product source knowledge

tests/

Automated tests

.env

Local secrets/configuration

requirements.txt

Python dependencies

19. Run tests

Make sure the virtual environment is activated.

Run:

pytest -q

You can also run:

python -m pytest -q

The tests currently focus on the Pydantic schemas and request validation.

20. Common problems

Problem: GOOGLE_API_KEY is missing

Make sure .env exists in the project root:

autonomous-content-engine/
├── .env
├── run.py
└── app/

And contains:

GOOGLE_API_KEY=your_actual_key

Restart the application after changing .env.

Problem: ModuleNotFoundError: No module named 'app'

Run commands from the project root:

autonomous-content-engine/

For example:

python run.py

Do not run run.py from inside the app directory.

Problem: pip is not recognized

Use:

python -m pip install -r requirements.txt

Problem: ChromaDB errors after changing knowledge files

Delete the generated local database:

chroma_db/

Then start the application again. ChromaDB will recreate the collection from the current knowledge-base files.

On Windows PowerShell:

Remove-Item -Recurse -Force chroma_db

On macOS/Linux:

rm -rf chroma_db

Problem: Port 8000 is already in use

Start the server on another port:

python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001

Then open:

http://127.0.0.1:8001/docs

21. Security notes

Do not place API keys directly inside Python source files.

Use:

GOOGLE_API_KEY=...

Do not commit:

.env
chroma_db/
.venv/
__pycache__/

These are already covered by .gitignore.

If an API key is accidentally pushed to GitHub, revoke/rotate it immediately.

22. GitHub setup

Initialize Git if necessary:

git init
git add .
git commit -m "Initial commit"

Create an empty GitHub repository named:

autonomous-content-engine

Then connect it:

git remote add origin https://github.com/YOUR_USERNAME/autonomous-content-engine.git
git branch -M main
git push -u origin main

Check the remote:

git remote -v

23. Development workflow

A typical development cycle is:

1. Activate virtual environment
        |
2. Update knowledge_base/
        |
3. Update Python code
        |
4. Run pytest
        |
5. Start FastAPI
        |
6. Test using Swagger
        |
7. Inspect generated campaign
        |
8. Commit changes
        |
9. Push to GitHub

Commands:

.venv\Scripts\activate
pytest -q
python run.py

In another terminal:

git status
git add .
git commit -m "Improve campaign workflow"
git push

24. Design decisions

Why LangGraph?

The project needs more than a single LLM call. LangGraph provides explicit workflow state and conditional transitions between generation, validation, revision, and completion.

Why ChromaDB?

ChromaDB provides a lightweight local vector store, making it convenient for a portfolio project without requiring a separate hosted vector-database service.

Why Pydantic?

LLM output can be unpredictable. Pydantic provides a strict Python data model for campaign outputs and makes API validation explicit.

Why FastAPI?

FastAPI makes the AI workflow accessible as a normal REST service and automatically generates OpenAPI/Swagger documentation.

25. Current limitations

This is a portfolio implementation rather than a production marketing platform.

Current limitations include:

The knowledge base currently uses local .txt files.

The RAG collection is initialized from local files rather than a document-management system.

The API currently runs as a single local service.

Validation is primarily rule-based rather than a separate LLM-as-judge system.

The current implementation uses LangGraph state and revision loops; it does not implement the official Model Context Protocol (MCP) specification.

Authentication, rate limiting, user accounts, campaign persistence, and production deployment are not included.

These are natural extension points for future versions.

26. Possible future improvements

- Add PostgreSQL campaign storage
- Add user authentication
- Add background task processing
- Add scheduled campaign generation
- Add additional document formats such as PDF/DOCX
- Add an LLM-based quality evaluator
- Add campaign versioning
- Add a React dashboard
- Add Docker support
- Add CI/CD with GitHub Actions
- Add observability and tracing
- Add MCP-compatible integrations where appropriate
- Add production vector database support

27. License

This project is licensed under the MIT License. See LICENSE for details.

28. Portfolio summary

Autonomous Content & Campaign Automation Engine demonstrates:

Agentic workflow design

LangGraph state orchestration

Retrieval-Augmented Generation (RAG)

ChromaDB vector search

Gemini LLM integration

Structured LLM outputs

Pydantic validation

Automated revision loops

FastAPI REST API development

Python project architecture

Automated testing

Environment and secret management

This project is suitable as a portfolio demonstration for AI Engineer, Generative AI Engineer, Agentic AI Engineer, AI Developer, Python Developer, and Backend Developer applications.