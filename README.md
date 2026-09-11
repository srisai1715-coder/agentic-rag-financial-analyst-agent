# Financial Analyst AI Agent

An **Agentic RAG-based Financial Analyst AI Agent** that answers financial questions using Microsoft's 2025 Annual Report, performs deterministic financial calculations and ratio analysis, analyzes risks, retrieves current financial data, verifies results, and presents source citations and agent activity through a web interface.

## 1. Project Overview

The user can ask questions such as:

- What was Microsoft's revenue in FY2025?
- How much did revenue grow from FY2024 to FY2025?
- What was Microsoft's operating margin?
- What are Microsoft's major cybersecurity risks?
- What is Microsoft's current stock price?

The system does not use one fixed RAG pipeline for every question. The **LangGraph AI Agent understands the user's question and decides which tool or sequence of tools is required**.

Examples:

```text
Revenue fact
    ↓
Annual Report RAG Tool
    ↓
Verification
    ↓
Final Answer
```

```text
Revenue growth
    ↓
Annual Report RAG Tool
    ↓
Financial Calculation Tool
    ↓
Verification
    ↓
Final Answer
```

```text
Operating margin
    ↓
Annual Report RAG Tool
    ↓
Financial Ratio Tool
    ↓
Verification
    ↓
Final Answer
```

```text
Major risks
    ↓
Annual Report RAG Tool
    ↓
Risk Analysis Tool
    ↓
Verification
    ↓
Final Answer
```

```text
Current stock price
    ↓
External Financial Data Tool
    ↓
Alpha Vantage
    ↓
Final Answer
```

## 2. Why This Is Agentic AI

The key distinction is:

```text
RAG
    ↓
Retrieve information

Agent
    ↓
Decide what action to take

Agentic RAG
    ↓
Agent decides when/how to use RAG
    +
Other tools
    +
Verification
    +
Final response
```

RAG is one capability inside the agent. The Annual Report RAG Tool retrieves grounded evidence, while LangGraph decides when RAG and other tools are needed.

### Interview answer

> I call it an Agentic AI project because the system doesn't follow a single fixed RAG pipeline. The LangGraph agent interprets the user's goal, dynamically selects the appropriate tools, can execute multiple tools in sequence, verifies the result, and then produces the final response.

## 3. Complete Architecture

![Financial Analyst AI Agent Architecture](docs/architecture.png)

The architecture image shows the complete flow from the user question to the final verified answer.

## 4. High-Level System Flow

```text
                         USER
                           │
                           ↓
                 React + Vite Frontend
                           │
                           │ HTTP Request
                           ↓
                ┌──────────────────────┐
                │ FastAPI Backend      │
                │ Docker API Container │
                └──────────┬───────────┘
                           │
                           ↓
                    LangGraph Agent
                           │
                Understand user query
                           │
                           ↓
                 Select appropriate tool(s)
                           │
              ┌────────────┼──────────────┐
              ↓            ↓              ↓
          RAG Tool    Calculation Tool  Ratio Tool
              │
              ↓
           Qdrant

              ┌────────────┼──────────────┐
              ↓            ↓              ↓
        Risk Analysis   External Data   Verification
                            │
                            ↓
                       Alpha Vantage
                           │
                           ↓
                    Verified Result
                           │
                           ↓
                    Final Answer
                           │
              ┌────────────┼────────────┐
              ↓            ↓            ↓
          Citations   Agent Activity  PostgreSQL
```

## 5. Document Ingestion and RAG Pipeline

```text
Microsoft 2025 Annual Report PDF
            ↓
         PyMuPDF
            ↓
      Extract text page-wise
            ↓
       Text processing
            ↓
      Page-aware chunks
            ↓
 NVIDIA Nemotron Embeddings
            ↓
          Vectors
            ↓
          Qdrant
```

The annual report is approximately 79 pages.

### Why PyMuPDF?

PyMuPDF extracts text from PDF pages. Page-level processing is important because the application needs citations such as:

```text
2025_AnnualReport.pdf — Page 21
```

### Why chunk the document?

The complete report should not be sent to the LLM for every question.

```text
79-page PDF
    ↓
Smaller chunks
    ↓
Semantic retrieval
    ↓
Relevant evidence
    ↓
LLM
```

This improves retrieval efficiency, context management, grounding, and citations.

### Why page-aware chunks?

Each chunk keeps its original page information so the frontend can show document/page citations.

## 6. Embeddings and Qdrant

The project uses:

```text
nvidia/nemotron-3-embed-1b
```

An embedding converts text into a numerical vector.

```text
Text Chunk
   ↓
NVIDIA Nemotron Embedding Model
   ↓
Vector
   ↓
Qdrant
```

Qdrant is the vector database used for semantic search.

**Embeddings are stored in Qdrant, not PostgreSQL.**

Qdrant stores:

- Document embeddings
- Document chunks
- Vector-search information
- Retrieval metadata

PostgreSQL stores application-level information.

## 7. Correct RAG Retrieval Flow

An important architecture detail is that **Qdrant is accessed through the Annual Report RAG Tool**.

```text
User Question
      ↓
LangGraph Agent
      ↓
Annual Report RAG Tool
      ↓
Qdrant Retriever
      ↓
Qdrant
      ↓
Relevant document chunks
      ↓
Annual Report RAG Tool
      ↓
Evidence + page metadata
      ↓
LangGraph Agent
```

In short:

```text
Agent
  ↓
RAG Tool
  ↓
Qdrant
  ↓
RAG Tool
  ↓
Agent
```

## 8. Six Tools

### 8.1 Annual Report RAG Tool

Retrieves evidence from Microsoft's annual report by searching Qdrant.

### 8.2 Financial Calculation Tool

Performs deterministic calculations such as:

- Revenue growth
- Percentage change
- Difference
- Profit margin

Revenue growth:

```text
(Current - Previous) / Previous × 100
```

For example:

```text
FY2024 Revenue = $245.122 billion
FY2025 Revenue = $281.724 billion

Growth ≈ 14.93%
```

Python performs the arithmetic rather than relying on the LLM.

### 8.3 Financial Ratio Tool

Calculates:

- Operating Margin
- Net Margin
- ROE
- ROA
- Debt-to-Equity

Example:

```text
Operating Margin
=
Operating Income / Revenue × 100
≈ 45.62%
```

### 8.4 Risk Analysis Tool

Analyzes risks from retrieved evidence.

Categories include:

- Cybersecurity
- Competition
- Regulatory
- Privacy
- Macroeconomic
- Supply Chain
- Technology

### 8.5 Verification Tool

Checks whether:

- Evidence exists
- Required tool results exist
- Results are supportable
- Enough information exists to answer

If verification fails, the system uses safer fail-closed behavior.

### 8.6 External Financial Data Tool

Uses **Alpha Vantage** for current financial information such as:

- Current stock price
- Market data
- Real-time/current financial information

Historical annual-report data and current market data are deliberately separated.

## 9. LangGraph Agent

LangGraph connects the tools and manages the agent workflow.

```text
User Question
      ↓
Understand Query
      ↓
Select Tool(s)
      ↓
Execute Tool(s)
      ↓
Verify Result
      ↓
Generate Final Answer
```

The agent state carries information between steps.

Conceptually:

```text
state = {
    query,
    evidence,
    tool_result,
    verification,
    answer
}
```

## 10. FastAPI Backend

FastAPI exposes the agent through:

```text
POST /agent/ask
```

Example:

```json
{
  "query": "How much did Microsoft's revenue grow from FY2024 to FY2025?"
}
```

Flow:

```text
React
  ↓
FastAPI
  ↓
LangGraph Agent
  ↓
Tools
  ↓
Answer
  ↓
FastAPI
  ↓
React
```

Health endpoint:

```text
GET /health
```

## 11. React + Vite + Tailwind Frontend

The frontend provides the user interface and displays:

- User question
- Final answer
- Source citations
- Agent activity
- Tools used

Technology:

- React
- Vite
- Tailwind CSS

## 12. Agent Activity UI

The application can show the tools used during execution:

```text
Agent Activity

✓ Annual Report RAG
✓ Financial Calculation
✓ Verification
```

This makes the agentic workflow visible instead of hiding everything behind:

```text
Question → LLM → Answer
```

## 13. Citations and Source Display

The application displays evidence sources such as:

```text
[1] 2025_AnnualReport.pdf — Page 21
[2] 2025_AnnualReport.pdf — Page 25
```

Citations provide traceability and help users understand where financial information came from.

## 14. PostgreSQL

PostgreSQL stores application-level persistence:

```text
agent_runs
    ├── query
    ├── answer
    ├── verification_status
    └── created_at
```

It does **not** replace Qdrant.

| Database | Responsibility |
|---|---|
| Qdrant | Embeddings, document chunks, semantic/vector search |
| PostgreSQL | Agent runs, queries, answers, verification status, timestamps, application metadata |

## 15. Evaluation

The evaluation dataset contains representative questions covering:

- Revenue
- Revenue growth
- Operating margin
- Risk
- External financial data

Final evaluation:

```text
5 / 5 passed
100%
```

## 16. LangSmith Observability

LangSmith traces agent execution.

Example:

```text
User Question
      ↓
RAG
      ↓
Calculation
      ↓
Verification
      ↓
Final Answer
```

It helps debug:

- Retrieval failures
- Wrong tool routing
- Calculation failures
- Verification failures
- Agent performance

## 17. Docker

Docker packages the application and dependencies into a consistent environment.

Docker is useful for:

- Reproducibility
- Dependency isolation
- Deployment readiness
- Consistent runtime

FastAPI can still run directly in a Python virtual environment during development.

## 18. Docker Compose

Docker Compose manages multiple services together:

```text
Docker Compose
    │
    ├── API Container
    │      └── FastAPI + LangGraph
    │
    └── PostgreSQL Container
           └── PostgreSQL 17
```

The Qdrant data uses the project's persistent local data setup.

Commands:

```powershell
docker compose build
```

```powershell
docker compose up
```

Or:

```powershell
docker compose up --build
```

## 19. Project Structure

```text
financial-analyst-agent/
│
├── app/
│   ├── agent/
│   │   ├── graph.py
│   │   ├── state.py
│   │   └── prompts.py
│   │
│   ├── tools/
│   │   ├── rag_tool.py
│   │   ├── calculation_tool.py
│   │   ├── ratio_tool.py
│   │   ├── risk_tool.py
│   │   ├── verification_tool.py
│   │   └── financial_data_tool.py
│   │
│   ├── rag/
│   │   ├── ingestion.py
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   └── chunking.py
│   │
│   ├── database/
│   │   ├── postgres.py
│   │   └── qdrant.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   └── config.py
│
├── data/
│   └── 2025_AnnualReport.pdf
│
├── tests/
│
├── evaluation/
│   ├── dataset.json
│   └── evaluate.py
│
├── frontend/
│   ├── package.json
│   ├── index.html
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── index.css
│       └── App.jsx
│
├── docs/
│   └── architecture.png
│
├── .env
├── .env.example
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 20. Complete Development Roadmap

### Phase 1 — Project Setup + Architecture

Created the modular project structure, configuration, testing foundation, Docker files, environment files, and basic FastAPI health endpoint.

### Phase 2 — PDF Ingestion and Document Processing

Built:

```text
PDF → PyMuPDF → Text → Normalization → Page-aware Chunks
```

### Phase 3 — NVIDIA Nemotron Embeddings + Qdrant

Built:

```text
Chunks → Nemotron Embeddings → Vectors → Qdrant
```

### Phase 4 — Annual Report RAG Tool

Created the tool that searches Qdrant and returns relevant annual-report evidence with source/page metadata.

### Phase 5 — Financial Calculation Tool

Added deterministic calculations such as revenue growth, percentage change, difference, and profit margin.

### Phase 6 — Financial Ratio Tool

Added Operating Margin, Net Margin, ROE, ROA, and Debt-to-Equity calculations.

### Phase 7 — Risk Analysis Tool

Added evidence-based risk analysis for cybersecurity, competition, regulatory, privacy, macroeconomic, supply chain, and technology risks.

### Phase 8 — Verification Tool

Added verification and fail-closed behavior so unsupported answers are not presented as verified facts.

### Phase 9 — External Financial Data Tool

Added Alpha Vantage for current financial information and separated live data from historical annual-report information.

### Phase 10 — LangGraph Agent + Intelligent Tool Routing

Connected the tools through LangGraph so the agent can dynamically choose the required workflow.

### Phase 11 — Agent State, Memory and Error Handling

Added graph state so information can move between retrieval, calculations, verification, and finalization steps, along with error handling.

### Phase 12 — FastAPI Backend

Exposed the agent through REST API endpoints, including `POST /agent/ask` and `GET /health`.

### Phase 13 — React + Vite + Tailwind Frontend

Built the web interface for asking questions and displaying answers.

### Phase 14 — Agent Activity / Tool Execution UI

Made the selected and executed tools visible to the user.

### Phase 15 — Citations and Source Display

Added source/document/page citation display.

### Phase 16 — PostgreSQL Integration

Added PostgreSQL for application-level agent history and metadata while Qdrant remains responsible for vector search.

### Phase 17 — Evaluation Dataset + Agent Evaluation

Created an evaluation dataset and evaluator.

Result:

```text
5 / 5 — 100%
```

### Phase 18 — LangSmith Observability

Added tracing and observability for agent execution and debugging.

### Phase 19 — Docker + Docker Compose

Containerized the backend and PostgreSQL services and added reproducible service management.

### Phase 20 — Testing and Debugging

Ran the full automated test suite:

```powershell
python -m pytest -q
```

Final result:

```text
52 passed
2 warnings
```

The warnings were dependency/deprecation warnings, not test failures.

## 21. End-to-End Example

Question:

```text
How much did Microsoft's revenue grow from FY2024 to FY2025?
```

Workflow:

```text
1. User
   ↓
2. React Frontend
   ↓
3. FastAPI
   ↓
4. LangGraph Agent
   ↓
5. Agent understands the request
   ↓
6. Annual Report RAG Tool
   ↓
7. Qdrant
   ↓
8. Relevant revenue evidence
   ↓
9. Financial Calculation Tool
   ↓
10. Python calculates growth
   ↓
11. Verification Tool
   ↓
12. Final answer
   ↓
13. React displays answer
       + sources
       + agent activity
```

Example result:

```text
Microsoft's revenue increased by approximately 14.93%
from FY2024 to FY2025.
```

## 22. Important Data Separation

```text
Qdrant
  → Embeddings
  → Document chunks
  → Vector search metadata

PostgreSQL
  → Agent runs
  → User queries
  → Answers
  → Verification status
  → Timestamps

Microsoft Annual Report
  → Historical/company information

Alpha Vantage
  → Current market information
```

## 23. Technology Stack

| Technology | Why it is used |
|---|---|
| Python | Main application language |
| LangGraph | Agent workflow and tool orchestration |
| NVIDIA Nemotron | LLM and embedding models |
| Qdrant | Vector database and semantic search |
| PyMuPDF | PDF text extraction |
| FastAPI | Backend API |
| React | Frontend UI |
| Vite | Frontend development/build tool |
| Tailwind CSS | UI styling |
| PostgreSQL | Application data persistence |
| Alpha Vantage | Current financial data |
| LangSmith | Agent tracing and observability |
| Docker | Reproducible application environment |
| Docker Compose | Multi-service management |
| Pytest | Automated testing |

## 24. Running the Project

### Backend with Docker

From the project root:

```powershell
docker compose build
docker compose up
```

Backend:

```text
http://localhost:8000
```

Health:

```text
http://localhost:8000/health
```

### Frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## 25. Environment Variables

Secrets and configuration are stored in `.env`.

Important variables include:

```text
NVIDIA_API_KEY
ALPHA_VANTAGE_API_KEY
LANGSMITH_TRACING
LANGSMITH_API_KEY
LANGSMITH_PROJECT
LANGSMITH_ENDPOINT
DATABASE_URL
```

Never put real API keys directly into source code.

Use `.env.example` as the template.

## 26. Security Notes

- Keep API keys in environment variables.
- Do not commit real secrets.
- Do not expose `.env` publicly.
- The application does not perform real trading actions.
- Historical and current financial data are separated.
- Verification is used before presenting supported results.

## 27. Testing

Run:

```powershell
python -m pytest -q
```

Final result:

```text
52 passed
2 warnings
```

## 28. Interview Explanation

### 30-second answer

> I built an Agentic RAG-based Financial Analyst AI Agent using Microsoft's 2025 Annual Report as the primary knowledge source. I used PyMuPDF for document processing, NVIDIA Nemotron embeddings with Qdrant for semantic retrieval, and LangGraph to create an agent that dynamically selects tools based on the user's question. The system has tools for annual-report retrieval, financial calculations, financial ratios, risk analysis, verification, and external financial data. I exposed the agent through FastAPI and built a React frontend that displays answers, citations, and agent activity. PostgreSQL stores application-level agent history, LangSmith provides tracing, and Docker provides a reproducible deployment environment. I also created an evaluation dataset and achieved 5 out of 5 on the selected evaluation cases, with 52 automated tests passing.

### Why Python for financial calculations?

> LLMs are good at understanding intent, but important financial arithmetic should be deterministic. The agent decides what calculation is required and Python performs the calculation. This reduces arithmetic errors and makes results reproducible.

### Why Qdrant and PostgreSQL?

> They solve different problems. Qdrant is a vector database used for embeddings and semantic document retrieval. PostgreSQL is a relational database used for application-level information such as agent runs, user queries, answers, verification status, and timestamps.

### Why Docker?

> I used Docker to make the application environment reproducible and deployment-ready. Docker packages the application and its dependencies into a consistent environment, while Docker Compose allows me to manage the API and PostgreSQL services together.

### Why LangGraph?

> LangGraph lets me represent the agent as a structured workflow with state, routing, tool execution, verification, and finalization. Different financial questions require different sequences of tools, so this is more suitable than a simple LLM call.

### Why LangSmith?

> Agent workflows contain multiple steps. LangSmith lets me trace those steps and determine whether a problem came from retrieval, routing, calculation, verification, or another part of the workflow.

## 29. Final Architecture Flow

```text
PDF
 ↓
PyMuPDF
 ↓
Text Processing
 ↓
Chunks
 ↓
NVIDIA Nemotron Embeddings
 ↓
Qdrant
 ↓
Retrieve Evidence
 ↓
LangGraph Agent
 ↓
Choose Tool(s)
 ↓
Calculation / Ratio / Risk / External Data / Verification
 ↓
Final Answer
 ↓
Citations + Agent Activity
 ↓
PostgreSQL Application History
 ↓
LangSmith Trace
 ↓
Docker Deployment
 ↓
Testing
```

## 30. Final Project Status

Implemented capabilities:

- PDF ingestion
- Page-aware document chunking
- NVIDIA Nemotron embeddings
- Qdrant vector search
- Annual Report RAG
- Deterministic financial calculations
- Financial ratio analysis
- Risk analysis
- Verification and fail-closed behavior
- External financial data
- LangGraph intelligent routing
- Agent state
- FastAPI backend
- React frontend
- Agent activity UI
- Source citations
- PostgreSQL persistence
- Evaluation
- LangSmith tracing
- Docker
- Docker Compose
- Automated testing

Final validation:

```text
Evaluation: 5 / 5 (100%)
Automated tests: 52 passed
Docker API: healthy
PostgreSQL: healthy
```

## 31. One Flow to Remember

```text
User
 ↓
React
 ↓
FastAPI
 ↓
LangGraph Agent
 ↓
Agent decides what to do
 ↓
RAG Tool → Qdrant → Evidence
 ↓
Other Tool(s) if required
 ↓
Verification
 ↓
Final Answer
 ↓
Citations + Agent Activity
 ↓
PostgreSQL stores application history
 ↓
LangSmith traces execution
 ↓
Docker runs the application environment
```

**This is the Financial Analyst AI Agent.**
