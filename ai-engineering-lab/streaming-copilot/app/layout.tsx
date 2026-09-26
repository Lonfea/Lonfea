import type { ReactNode } from "react";

export const metadata = {
  title: "Streaming AI Copilot",
  description: "Production-oriented streaming LLM interface",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
