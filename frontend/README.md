# Frontend

React + Vite + Tailwind CSS frontend.

From the project root:

```powershell
cd frontend
npm install
npm run dev
```

Keep the FastAPI backend running separately:

```powershell
docker compose up
```

The frontend calls `http://localhost:8000/agent/ask`.

Do not put API keys in the frontend.