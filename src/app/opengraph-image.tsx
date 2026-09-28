import { ImageResponse } from "next/og";
import { siteConfig } from "@/config/site";

export const size = { width: 1200, height: 630 };
export const contentType = "image/png";
// Required for `output: "export"` — this image has no per-request data, so
// it's safe to render once at build time.
export const dynamic = "force-static";

export default function OpengraphImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          padding: "80px",
          background: "#05070a",
          backgroundImage:
            "radial-gradient(circle at 12% 8%, rgba(56,189,248,0.16), transparent 45%), radial-gradient(circle at 88% 22%, rgba(129,140,248,0.14), transparent 45%)",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 12,
            fontSize: 26,
            fontWeight: 600,
            color: "#38bdf8",
            letterSpacing: 2,
          }}
        >
          <div
            style={{
              display: "flex",
              width: 40,
              height: 40,
              borderRadius: 10,
              border: "2px solid #38bdf8",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <div style={{ color: "#38bdf8", fontSize: 20 }}>&gt;_</div>
          </div>
          {siteConfig.shortName.toUpperCase()}
        </div>

        <div
          style={{
            display: "flex",
            marginTop: 48,
            fontSize: 64,
            fontWeight: 700,
            color: "#e7ecf3",
            lineHeight: 1.15,
            maxWidth: 980,
          }}
        >
          {siteConfig.headline}
        </div>

        <div
          style={{
            display: "flex",
            marginTop: 28,
            fontSize: 28,
            color: "#8b96a8",
            maxWidth: 880,
            lineHeight: 1.4,
          }}
        >
          {siteConfig.missionShort}
        </div>
      </div>
    ),
    { ...size },
  );
}
