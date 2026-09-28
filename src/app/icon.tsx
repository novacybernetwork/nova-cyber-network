import { ImageResponse } from "next/og";

export const size = { width: 32, height: 32 };
export const contentType = "image/png";
// Required for `output: "export"` — this icon has no per-request data, so
// it's safe to render once at build time.
export const dynamic = "force-static";

export default function Icon() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: "#05070a",
          borderRadius: 7,
        }}
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
          <path
            d="M12 2 L4.5 5.3 V11 C4.5 16 7.6 19.9 12 21.5 C16.4 19.9 19.5 16 19.5 11 V5.3 Z"
            stroke="#38bdf8"
            strokeWidth="1.6"
            strokeLinejoin="round"
          />
          <path
            d="M8.7 12.2 L10.8 14.3 L15.3 9.4"
            stroke="#38bdf8"
            strokeWidth="1.6"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>
    ),
    { ...size },
  );
}
