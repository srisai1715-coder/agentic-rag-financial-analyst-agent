import { useState } from "react";

const rawApiUrl = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
const API_URL = rawApiUrl.replace(/\/+$/, "");

const examples = [
  "What was Microsoft's revenue growth from fiscal year 2024 to 2025?",
  "What was Microsoft's operating margin in fiscal year 2025?",
  "What were Microsoft's major risks?"
];

function formatToolName(name) {
  return (name || "unknown_tool")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

function describeStep(step) {
  const tool = step.tool;

  if (tool === "annual_report_rag") {
    return step.query
      ? `Retrieved evidence for: ${step.query}`
      : "Retrieved evidence from the annual report";
  }
  if (tool === "financial_calculation") {
    return step.operation
      ? `Performed ${step.operation.replaceAll("_", " ")}`
      : "Performed a financial calculation";
  }
  if (tool === "financial_ratio") {
    return step.operation
      ? `Calculated ${step.operation.replaceAll("_", " ")}`
      : "Calculated a financial ratio";
  }
  if (tool === "risk_analysis") return "Analyzed financial risks from retrieved evidence";
  if (tool === "external_financial_data") return "Retrieved current external financial data";
  if (tool === "verification") {
    return step.status === "passed"
      ? "Result verified successfully"
      : "Verification did not pass";
  }
  return "Tool completed";
}

function sourceLabel(source) {
  if (typeof source === "string") return source;
  if (!source) return "Unknown source";

  const file = source.file || source.filename || "Source document";
  const page = source.page ?? source.page_number;

  return page ? `${file}, p. ${page}` : file;
}

function sourceDetails(source) {
  if (!source || typeof source === "string") return "";
  return source.text || source.content || source.snippet || "";
}

export default function App() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [toolCalls, setToolCalls] = useState([]);
  const [toolTrace, setToolTrace] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function askAgent(question = query) {
    const q = question.trim();
    if (!q || loading) return;

    setQuery(q);
    setLoading(true);
    setError("");
    setAnswer("");
    setSources([]);
    setToolCalls([]);
    setToolTrace([]);

    try {
      const response = await fetch(`${API_URL}/agent/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q }),
      });

      if (!response.ok) {
        let message = `Request failed with status ${response.status}.`;
        try {
          const body = await response.json();
          message = body.detail || message;
        } catch {
          // Keep fallback.
        }
        throw new Error(message);
      }

      const data = await response.json();

      setAnswer(data.answer || "No answer was returned.");
      setSources(data.sources || []);
      setToolCalls(data.tool_calls || []);
      setToolTrace(data.tool_trace || []);
    } catch (err) {
      setError(
        `${err.message} Make sure the FastAPI backend is running at ${API_URL}.`
      );
    } finally {
      setLoading(false);
    }
  }

  function clear() {
    setQuery("");
    setAnswer("");
    setSources([]);
    setToolCalls([]);
    setToolTrace([]);
    setError("");
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-4">
          <div>
            <h1 className="text-xl font-bold tracking-tight">Financial Analyst Agent</h1>
            <p className="text-sm text-slate-500">
              Ask questions about Microsoft&apos;s 2025 Annual Report
            </p>
          </div>
          <div className="rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700">
            AI Agent
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-5 py-8">
        <section className="mb-8">
          <h2 className="text-3xl font-bold tracking-tight">
            Financial analysis, powered by an agent
          </h2>
          <p className="mt-2 max-w-2xl text-slate-600">
            Ask a financial question. The backend agent selects tools, retrieves
            evidence, performs calculations, and verifies the result.
          </p>
        </section>

        <div className="grid gap-6 lg:grid-cols-[1.6fr_1fr]">
          <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <form onSubmit={(event) => { event.preventDefault(); askAgent(); }}>
              <label htmlFor="question" className="mb-2 block text-sm font-semibold">
                Your question
              </label>
              <textarea
                id="question"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="e.g. What was Microsoft's revenue growth from fiscal year 2024 to 2025?"
                rows={4}
                className="w-full resize-none rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
              />
              <div className="mt-4 flex gap-3">
                <button
                  type="submit"
                  disabled={loading || !query.trim()}
                  className="rounded-xl bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {loading ? "Analyzing..." : "Ask Agent"}
                </button>
                <button
                  type="button"
                  onClick={clear}
                  className="rounded-xl border border-slate-300 px-5 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                >
                  Clear
                </button>
              </div>
            </form>

            <div className="mt-6">
              <p className="mb-3 text-sm font-semibold">Try an example</p>
              <div className="flex flex-col gap-2">
                {examples.map((question) => (
                  <button
                    key={question}
                    type="button"
                    onClick={() => askAgent(question)}
                    className="rounded-xl border border-slate-200 px-4 py-3 text-left text-sm text-slate-600 hover:border-slate-300 hover:bg-slate-50"
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          </section>

          <aside className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <h3 className="font-semibold">How it works</h3>
            <ol className="mt-4 space-y-4 text-sm text-slate-600">
              <li><b className="text-slate-900">1. Ask</b> — your question is sent to FastAPI.</li>
              <li><b className="text-slate-900">2. Route</b> — LangGraph selects the needed tool.</li>
              <li><b className="text-slate-900">3. Analyze</b> — RAG and deterministic tools produce evidence.</li>
              <li><b className="text-slate-900">4. Verify</b> — the result is checked before the answer is returned.</li>
            </ol>
          </aside>
        </div>

        {error && (
          <section className="mt-6 rounded-2xl border border-red-200 bg-red-50 p-5 text-sm text-red-700">
            <b>Could not reach the agent</b>
            <p className="mt-1">{error}</p>
          </section>
        )}

        {loading && (
          <section className="mt-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-bold">Agent activity</h2>
              <span className="text-sm text-slate-500">Working...</span>
            </div>
            <div className="mt-5 space-y-3 animate-pulse">
              <div className="h-12 rounded-xl bg-slate-100" />
              <div className="h-12 rounded-xl bg-slate-100" />
              <div className="h-12 rounded-xl bg-slate-100" />
            </div>
          </section>
        )}

        {!loading && toolTrace.length > 0 && (
          <section className="mt-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold">Agent activity</h2>
                <p className="mt-1 text-sm text-slate-500">
                  Tools selected and executed by the agent
                </p>
              </div>
              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">
                {toolTrace.length} {toolTrace.length === 1 ? "step" : "steps"}
              </span>
            </div>

            <div className="mt-5 space-y-3">
              {toolTrace.map((step, index) => (
                <div
                  key={`${step.step || index}-${step.tool}`}
                  className={`rounded-xl border p-4 ${
                    step.status === "failed"
                      ? "border-red-200 bg-red-50 text-red-700"
                      : "border-emerald-200 bg-emerald-50 text-emerald-700"
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-white text-xs font-bold shadow-sm">
                      {step.status === "failed" ? "!" : "✓"}
                    </div>
                    <div className="min-w-0 flex-1">
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <div className="font-semibold">
                          Step {step.step || index + 1}: {formatToolName(step.tool)}
                        </div>
                        <span className="text-xs font-semibold uppercase tracking-wide">
                          {step.status === "failed" ? "Failed" : "Completed"}
                        </span>
                      </div>
                      <p className="mt-1 text-sm">{describeStep(step)}</p>
                      {step.operation && (
                        <p className="mt-2 text-xs opacity-80">
                          Operation: {step.operation}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {(answer || sources.length > 0 || toolCalls.length > 0) && !loading && (
          <section className="mt-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-bold">Agent answer</h2>
            <p className="mt-5 whitespace-pre-wrap leading-7 text-slate-700">{answer}</p>

            {sources.length > 0 && (
              <div className="mt-7 border-t border-slate-200 pt-5">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <h3 className="text-sm font-bold">Sources &amp; citations</h3>
                    <p className="mt-1 text-xs text-slate-500">
                      Evidence returned by the Annual Report RAG tool
                    </p>
                  </div>
                  <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">
                    {sources.length} {sources.length === 1 ? "source" : "sources"}
                  </span>
                </div>

                <div className="mt-4 space-y-2">
                  {sources.map((source, index) => {
                    const label = sourceLabel(source);
                    const details = sourceDetails(source);

                    return (
                      <details
                        key={`${label}-${index}`}
                        className="group rounded-xl border border-slate-200 bg-slate-50"
                      >
                        <summary className="flex cursor-pointer list-none items-center justify-between gap-4 px-4 py-3 text-sm font-medium text-slate-700">
                          <span>
                            <span className="mr-2 text-xs font-bold text-slate-400">
                              [{index + 1}]
                            </span>
                            {label}
                          </span>
                          <span className="text-slate-400 transition group-open:rotate-180">
                            ▼
                          </span>
                        </summary>
                        {details && (
                          <div className="border-t border-slate-200 px-4 py-3 text-sm leading-6 text-slate-600">
                            {details}
                          </div>
                        )}
                      </details>
                    );
                  })}
                </div>
              </div>
            )}

            {toolCalls.length > 0 && (
              <div className="mt-7 border-t border-slate-200 pt-5">
                <h3 className="text-sm font-bold">Tools used</h3>
                <div className="mt-3 flex flex-wrap gap-2">
                  {toolCalls.map((call, index) => (
                    <span
                      key={`${call.tool}-${index}`}
                      className="rounded-full bg-slate-100 px-3 py-1.5 text-xs font-medium text-slate-700"
                    >
                      {formatToolName(call.tool)}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </section>
        )}
      </main>

      <footer className="mx-auto max-w-6xl px-5 pb-8 text-xs text-slate-400">
        Financial Analyst Agent • React + Vite + Tailwind
      </footer>
    </div>
  );
}