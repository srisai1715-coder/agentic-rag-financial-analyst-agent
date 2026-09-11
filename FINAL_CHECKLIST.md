# Final Phase Checklist

## Before interview/demo

1. Start Docker:

```powershell
docker compose up
```

2. Check services:

```powershell
docker compose ps
```

3. Check API:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

4. Start frontend:

```powershell
cd frontend
npm run dev
```

5. Open:

`http://localhost:5173`

6. Run tests from project root:

```powershell
python -m pytest -q
```

## Demo questions

### RAG
What was Microsoft's total revenue in fiscal year 2025?

### Calculation
What was Microsoft's revenue growth from fiscal year 2024 to 2025?

### Ratio
What was Microsoft's operating margin in fiscal year 2025?

### Risk
What were Microsoft's major risks?

### External data
What is Microsoft's current stock price?

Show the interviewer:

- Final answer
- Agent Activity
- Sources & citations
- LangSmith trace
- Docker containers
- Test results

## Important

Do not expose:

- NVIDIA API key
- Alpha Vantage API key
- LangSmith API key
- `.env` contents
