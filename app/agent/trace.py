from typing import Any


def build_tool_trace(tool_calls: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Normalize agent tool calls into a simple UI-friendly trace."""
    trace = []

    for index, call in enumerate(tool_calls, start=1):
        item = {"step": index, "tool": call.get("tool", "unknown")}

        for key in ("query", "operation", "status"):
            if key in call:
                item[key] = call[key]

        trace.append(item)

    return trace
