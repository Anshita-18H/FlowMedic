import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FlowMedic Live — Recovery Studio",
  description:
    "Watch real workflows run, diagnose integration failures, and recover safely with FlowMedic Live.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
