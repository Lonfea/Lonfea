import { convertToModelMessages, streamText, type UIMessage } from "ai";

export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();
  const model = process.env.MODEL_ID ?? "openai/gpt-6-luna";

  const result = streamText({
    model,
    system:
      "You are a concise AI engineering copilot. Be explicit about uncertainty and failures.",
    messages: await convertToModelMessages(messages),
    abortSignal: req.signal,
  });

  return result.toUIMessageStreamResponse({
    onError: () => "The model request failed. Please retry.",
  });
}
