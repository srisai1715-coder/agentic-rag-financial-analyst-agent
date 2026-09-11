from app.agent.graph import build_graph

def test_agent_graph_structure():
    assert build_graph() is not None
