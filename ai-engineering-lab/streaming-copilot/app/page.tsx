"use client";

import { useChat } from "@ai-sdk/react";
import { DefaultChatTransport } from "ai";
import { FormEvent, useMemo, useState } from "react";

export default function Home() {
  const [input, setInput] = useState("");
  const transport = useMemo(
    () => new DefaultChatTransport({ api: "/api/chat" }),
    [],
  );
  const {
    messages,
    sendMessage,
    status,
    error,
    stop,
    regenerate,
  } = useChat({ transport });

  const submit = (event: FormEvent) => {
    event.preventDefault();
    const text = input.trim();
    if (!text) return;
    setInput("");
    sendMessage({ text });
  };

  const waiting = status === "submitted" || status === "streaming";

  return (
    <main style={{ maxWidth: 840, margin: "0 auto", padding: 32 }}>
      <h1>Streaming AI Copilot</h1>
      <p>
        Token streaming, optimistic message submission, cancellation, retry,
        latency-state feedback, and visible error recovery.
      </p>

      <section aria-live="polite">
        {messages.map((message) => (
          <article
            key={message.id}
            style={{ padding: 12, margin: "12px 0", border: "1px solid #ddd" }}
          >
            <strong>{message.role}</strong>
            {message.parts.map((part, index) =>
              part.type === "text" ? <p key={index}>{part.text}</p> : null,
            )}
          </article>
        ))}
      </section>

      {status === "submitted" && <p>Connecting to model…</p>}
      {status === "streaming" && <p>Streaming response…</p>}

      {error && (
        <div role="alert">
          <p>Request failed: {error.message}</p>
          <button onClick={() => regenerate()}>Retry last response</button>
        </div>
      )}

      <form onSubmit={submit}>
        <textarea
          rows={4}
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Ask the copilot…"
          style={{ width: "100%" }}
        />
        <div style={{ display: "flex", gap: 8 }}>
          <button type="submit" disabled={!input.trim() || waiting}>
            Send
          </button>
          {waiting && (
            <button type="button" onClick={() => stop()}>
              Stop
            </button>
          )}
        </div>
      </form>
    </main>
  );
}
