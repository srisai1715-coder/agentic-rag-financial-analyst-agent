# Financial Analyst Agent — Interview Guide

## Project Summary

**Project:** Financial Analyst Agent

**Type:** Agentic RAG

**Purpose:** Analyze Microsoft's 2025 Annual Report and answer financial questions using specialized tools, verification, and current external market data.

## Architecture

```text
React
  |
FastAPI
  |
LangGraph
  |
Intelligent Tool Routing
  |
+-------------+-------------+-------------+
|             |             |             |
RAG       Calculation      Ratio       Risk
|             |             |             |
+-------------+-------------+-------------+
              |
        Verification
              |
       Answer + Sources
```

## Key Interview Questions

### What is the difference between RAG and Agentic RAG?

RAG retrieves relevant documents and gives the evidence to an LLM. Agentic RAG adds decision-making: the agent chooses which tool or sequence of tools should be used for the question.

### Give an example of tool routing.

For:

> What was revenue growth from FY2024 to FY2025?

The agent retrieves revenue values using RAG, sends those values to the calculation tool, and then verifies the result.

For:

> What is Microsoft's current stock price?

The agent routes to the external financial data tool instead of using the annual report.

### Why use an embedding model?

Embeddings convert text chunks into vectors so semantically related questions and document chunks can be matched even when their wording is different.

### Why use a vector database?

A vector database such as Qdrant efficiently searches embeddings and returns the most relevant document chunks for RAG.

### Why use Python for financial calculations?

Python gives deterministic arithmetic instead of relying on an LLM to calculate numbers.

### How do you prevent hallucinations?

The system grounds answers in retrieved evidence, uses deterministic tools for calculations, and applies a verification step with fail-closed behavior.

### How do you handle current stock price vs annual-report data?

Historical company information comes from the annual report. Current market information comes from the external financial-data tool. The response should distinguish the source and time context.

### What does LangGraph do?

LangGraph manages the agent workflow and state, including routing, tool execution, verification, and finalization.

### What does LangSmith do?

LangSmith provides tracing and observability so agent runs and tool execution can be inspected and debugged.

### Why React?

React provides the interactive user interface. It sends questions to the FastAPI backend and displays the answer, tool activity, and sources.

### Why FastAPI?

FastAPI provides the HTTP API between the frontend and the agent backend.

### Why Docker?

Docker makes the runtime reproducible and deployment-ready. It is not strictly required for local FastAPI development.

## Strong Closing Answer

> The main thing I focused on was reliability. I didn't want the LLM to invent financial numbers or perform important arithmetic itself. I separated retrieval, calculation, ratios, risk analysis, external data, and verification into tools and used LangGraph to route the questions. The result is an Agentic RAG system that is easier to trace, test, verify, and deploy.
