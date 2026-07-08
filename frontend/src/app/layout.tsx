import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Livo Pronunciation Checker",
  description: "Upload English audio and prepare it for pronunciation assessment.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

