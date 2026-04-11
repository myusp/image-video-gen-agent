import { useCallback, useEffect, useMemo, useState } from "react";
import {
  AbsoluteFill,
  Sequence,
  continueRender,
  delayRender,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { parseSrt } from "@remotion/captions";
import type { Caption } from "@remotion/captions";

const ENTRIES_PER_PAGE = 2;
const HIGHLIGHT_COLOR = "#FFE600";
/**
 * Offset (ms) applied to all caption times to compensate for edge-tts word
 * boundary timing being slightly late relative to the audible speech.
 * Negative = captions appear earlier.
 */
const CAPTION_OFFSET_MS = -150;

export type CaptionStyle = "tiktok" | "plain";

interface CaptionGroup {
  entries: Caption[];
  startMs: number;
  endMs: number;
}

const TikTokCaptionDisplay: React.FC<{ group: CaptionGroup }> = ({
  group,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentTimeMs = group.startMs + (frame / fps) * 1000;

  return (
    <div
      style={{
        fontSize: 56,
        fontWeight: "bold",
        fontFamily: "Arial, sans-serif",
        textAlign: "center",
        textShadow:
          "2px 2px 0 #000, -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 0 3px 6px rgba(0,0,0,0.8)",
        lineHeight: 1.3,
        padding: "0 48px",
        maxWidth: "100%",
        overflowWrap: "break-word",
        wordBreak: "break-word",
      }}
    >
      {group.entries.map((entry, i) => {
        const isActive =
          currentTimeMs >= entry.startMs && currentTimeMs < entry.endMs;
        return (
          <span
            key={i}
            style={{ color: isActive ? HIGHLIGHT_COLOR : "white" }}
          >
            {entry.text}
            {i < group.entries.length - 1 ? " " : ""}
          </span>
        );
      })}
    </div>
  );
};

const PlainCaptionDisplay: React.FC<{ group: CaptionGroup }> = ({ group }) => {
  const text = group.entries.map((e) => e.text).join(" ");
  return (
    <div
      style={{
        fontSize: 52,
        fontWeight: "bold",
        fontFamily: "Arial, sans-serif",
        textAlign: "center",
        color: "white",
        textShadow:
          "2px 2px 0 #000, -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 0 3px 6px rgba(0,0,0,0.8)",
        lineHeight: 1.3,
        padding: "0 48px",
        maxWidth: "100%",
        overflowWrap: "break-word",
        wordBreak: "break-word",
      }}
    >
      {text}
    </div>
  );
};

interface CaptionOverlayProps {
  captionStyle?: CaptionStyle;
}

export const CaptionOverlay: React.FC<CaptionOverlayProps> = ({
  captionStyle = "tiktok",
}) => {
  const [captions, setCaptions] = useState<Caption[] | null>(null);
  const { fps } = useVideoConfig();
  const [handle] = useState(() => delayRender("Loading subtitles.srt"));

  const fetchCaptions = useCallback(async () => {
    try {
      const resp = await fetch(staticFile("subtitles.srt"));
      if (!resp.ok) {
        console.warn("subtitles.srt not found, skipping captions");
        continueRender(handle);
        return;
      }
      const text = await resp.text();
      const { captions: parsed } = parseSrt({ input: text });
      // Apply timing offset to compensate for TTS word-boundary delay
      const adjusted = parsed.map((c) => ({
        ...c,
        startMs: Math.max(0, c.startMs + CAPTION_OFFSET_MS),
        endMs: Math.max(0, c.endMs + CAPTION_OFFSET_MS),
      }));
      setCaptions(adjusted);
      continueRender(handle);
    } catch (e) {
      continueRender(handle);
      console.error("Failed to load captions", e);
    }
  }, [handle]);

  useEffect(() => {
    fetchCaptions();
  }, [fetchCaptions]);

  const groups = useMemo((): CaptionGroup[] => {
    if (!captions || captions.length === 0) return [];
    const result: CaptionGroup[] = [];
    for (let i = 0; i < captions.length; i += ENTRIES_PER_PAGE) {
      const entries = captions.slice(i, i + ENTRIES_PER_PAGE);
      result.push({
        entries,
        startMs: entries[0].startMs,
        endMs: entries[entries.length - 1].endMs,
      });
    }
    return result;
  }, [captions]);

  if (!captions || groups.length === 0) return null;

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          position: "absolute",
          bottom: 140,
          left: 0,
          right: 0,
          display: "flex",
          justifyContent: "center",
        }}
      >
        {groups.map((group, index) => {
          const startFrame = Math.floor((group.startMs / 1000) * fps);
          const nextGroup = groups[index + 1];
          const endFrame = nextGroup
            ? Math.floor((nextGroup.startMs / 1000) * fps)
            : Math.ceil((group.endMs / 1000) * fps);
          const durationInFrames = endFrame - startFrame;
          if (durationInFrames <= 0) return null;

          return (
            <Sequence
              key={index}
              from={startFrame}
              durationInFrames={durationInFrames}
              layout="none"
            >
              {captionStyle === "tiktok" ? (
                <TikTokCaptionDisplay group={group} />
              ) : (
                <PlainCaptionDisplay group={group} />
              )}
            </Sequence>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
