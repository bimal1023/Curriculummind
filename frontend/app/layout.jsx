import { Bricolage_Grotesque, Hanken_Grotesk } from "next/font/google";
import "./globals.css";

const display = Bricolage_Grotesque({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
  variable: "--font-display",
  display: "swap",
});

const body = Hanken_Grotesk({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-body",
  display: "swap",
});

export const metadata = {
  metadataBase: new URL("http://localhost:3000"),
  title: "CurriculumMind — your study board, reasoned by AI",
  description:
    "Pin your goal. CurriculumMind diagnoses your gaps and builds a verified, week-by-week study board — reasoned by 5 AI agents on Microsoft Agent Framework & Azure AI Foundry.",
  keywords: [
    "study plan",
    "AI agents",
    "Microsoft Agent Framework",
    "Azure AI Foundry",
    "learning path",
  ],
  openGraph: {
    title: "CurriculumMind — your study board, reasoned by AI",
    description:
      "A verified, week-by-week study plan reasoned by 5 AI agents.",
    type: "website",
    siteName: "CurriculumMind",
  },
  twitter: {
    card: "summary_large_image",
    title: "CurriculumMind — your study board, reasoned by AI",
    description:
      "A verified, week-by-week study plan reasoned by 5 AI agents.",
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${display.variable} ${body.variable}`}>
      <body className="grain">{children}</body>
    </html>
  );
}
