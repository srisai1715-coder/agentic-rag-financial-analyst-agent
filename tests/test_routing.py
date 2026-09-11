from app.agent.graph import route_question

def test_routes_growth_to_calculation():
    assert route_question({"user_query":"What was Microsoft revenue growth?"})["route"]=="calculation"

def test_routes_margin_to_ratio():
    assert route_question({"user_query":"What was Microsoft operating margin?"})["route"]=="ratio"

def test_routes_risk_to_risk_tool():
    assert route_question({"user_query":"What are Microsoft major risks?"})["route"]=="risk"

def test_routes_factual_question_to_direct():
    assert route_question({"user_query":"What was Microsoft revenue in FY2025?"})["route"]=="direct"
