# Streaming Copilot UI

A Next.js copilot interface built around the Vercel AI SDK streaming protocol.

## Reliability behaviors

- response tokens render as they arrive;
- sent user messages appear immediately;
- explicit "connecting" and "streaming" states;
- user can abort a slow request;
- failures are visible rather than silently swallowed;
- the last request can be regenerated after an error;
- server-side errors are mapped to a safe client message;
- request abort signals propagate to model generation.

## Run

    npm install
    cp .env.example .env.local
    npm run dev

The default model ID uses the AI Gateway-style provider/model form and is configurable with `MODEL_ID`.

## Production upgrades

- persistent conversation store;
- authentication;
- source/citation components for RAG responses;
- request IDs linked to OpenTelemetry traces;
- offline fallback to the local-first Ollama service.
