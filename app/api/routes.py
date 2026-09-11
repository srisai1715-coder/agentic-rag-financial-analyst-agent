from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.observability.tracing import build_trace_config

router = APIRouter()


class RAGSearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)
    min_score: float | None = Field(default=None, ge=-1.0, le=1.0)


class AgentRequest(BaseModel):
    query: str = Field(min_length=1)


@router.post("/rag/search")
def rag_search(request: RAGSearchRequest):
    try:
        from app.tools.rag_tool import AnnualReportRAGTool

        return AnnualReportRAGTool().run(
            request.query,
            request.top_k,
            request.min_score,
        )
    except (ValueError, FileNotFoundError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/agent/ask")
def agent_ask(request: AgentRequest):
    try:
        from app.agent.graph import build_graph
        from app.agent.trace import build_tool_trace

        result = build_graph().invoke(
            {"user_query": request.query},
            config=build_trace_config(request.query),
        )
        tool_calls = result.get("tool_calls", [])

        return {
            "query": request.query,
            "answer": result.get("final_answer", ""),
            "sources": result.get("sources", []),
            "tool_calls": tool_calls,
            "tool_trace": build_tool_trace(tool_calls),
            "calculation": result.get("calculation"),
            "ratio": result.get("ratio"),
            "risk_analysis": result.get("risk_analysis"),
            "verification": result.get("verification"),
        }
    except (ValueError, FileNotFoundError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
