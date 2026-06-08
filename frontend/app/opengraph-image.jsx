import { ImageResponse } from "next/og";

export const alt = "CurriculumMind — your study board, reasoned by AI";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OpengraphImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          padding: "72px",
          backgroundColor: "#FBF8F6",
          backgroundImage:
            "radial-gradient(circle at 18% 18%, #ffe3e7 0%, transparent 42%), radial-gradient(circle at 90% 0%, #ffd6dc 0%, transparent 40%)",
          fontFamily: "sans-serif",
        }}
      >
        {/* Logo row */}
        <div style={{ display: "flex", alignItems: "center", gap: "20px" }}>
          <div
            style={{
              width: "84px",
              height: "84px",
              borderRadius: "24px",
              background: "#E60023",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "white",
              fontSize: "40px",
              fontWeight: 800,
              letterSpacing: "-2px",
            }}
          >
            CM
          </div>
          <div style={{ display: "flex", fontSize: "40px", fontWeight: 800 }}>
            <span style={{ color: "#1F1A1D" }}>Curriculum</span>
            <span style={{ color: "#E60023" }}>Mind</span>
          </div>
        </div>

        {/* Headline */}
        <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              fontSize: "74px",
              fontWeight: 800,
              color: "#1F1A1D",
              lineHeight: 1.05,
              letterSpacing: "-2px",
              maxWidth: "960px",
            }}
          >
            <span>Pin your goal. We&apos;ll build the&nbsp;</span>
            <span style={{ color: "#E60023" }}>study board.</span>
          </div>
          <div style={{ display: "flex", fontSize: "30px", color: "#6E6168" }}>
            A verified, week-by-week study plan reasoned by 5 AI agents.
          </div>
        </div>

        {/* Footer tags */}
        <div style={{ display: "flex", gap: "16px" }}>
          {["Microsoft Agent Framework", "Azure AI Foundry", "Foundry IQ"].map(
            (t) => (
              <div
                key={t}
                style={{
                  display: "flex",
                  fontSize: "24px",
                  fontWeight: 700,
                  color: "#1F1A1D",
                  background: "white",
                  border: "1px solid #EDE7E3",
                  padding: "12px 24px",
                  borderRadius: "999px",
                }}
              >
                {t}
              </div>
            )
          )}
        </div>
      </div>
    ),
    { ...size }
  );
}
