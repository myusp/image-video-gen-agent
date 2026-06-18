import { AbsoluteFill, Sequence, staticFile } from "remotion";
import { Audio } from "@remotion/media";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import type { TransitionPresentation } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";
import { flip } from "@remotion/transitions/flip";
import { clockWipe } from "@remotion/transitions/clock-wipe";
import { none } from "@remotion/transitions/none";
import { SceneImage } from "./SceneImage";
import type { MotionEffect, RenderMode } from "./SceneImage";
import { CaptionOverlay } from "./CaptionOverlay";
import type { CaptionStyle } from "./CaptionOverlay";
import { SFX_MAP } from "./sfx";

const FPS = 30;
const DEFAULT_TRANSITION_FRAMES = 15;
const SFX_OUT_LEAD = 12; // frames before scene end that out.sfx fires (~0.4s)
const SFX_VOLUME = 0.6;

export interface SceneTransition {
  transition?: string | null;
  durationInFrames?: number;
  sfx?: string | null;
}

export interface SceneConfig {
  sceneNumber: number;
  imagePath: string;
  audioPath: string;
  durationSeconds: number;
  motionEffect: MotionEffect;
  renderMode?: RenderMode;
  in?: SceneTransition;
  out?: SceneTransition;
}

interface Props {
  sceneConfig: SceneConfig[];
  withCaptions: boolean;
  captionStyle?: CaptionStyle;
  renderMode?: RenderMode;
  frameWidth: number;
  frameHeight: number;
}

type AnyPresentation = TransitionPresentation<Record<string, unknown>>;

function buildPresentation(
  name: string | null | undefined,
  frameWidth: number,
  frameHeight: number,
): AnyPresentation {
  switch (name) {
    case "slide-from-left":
      return slide({ direction: "from-left" }) as AnyPresentation;
    case "slide-from-right":
      return slide({ direction: "from-right" }) as AnyPresentation;
    case "slide-from-top":
      return slide({ direction: "from-top" }) as AnyPresentation;
    case "slide-from-bottom":
      return slide({ direction: "from-bottom" }) as AnyPresentation;
    case "wipe-from-left":
      return wipe({ direction: "from-left" }) as AnyPresentation;
    case "wipe-from-right":
      return wipe({ direction: "from-right" }) as AnyPresentation;
    case "wipe-from-top":
      return wipe({ direction: "from-top" }) as AnyPresentation;
    case "wipe-from-bottom":
      return wipe({ direction: "from-bottom" }) as AnyPresentation;
    case "flip":
      return flip() as AnyPresentation;
    case "clock-wipe":
      return clockWipe({ width: frameWidth, height: frameHeight }) as unknown as AnyPresentation;
    case "none":
      return none() as AnyPresentation;
    case "fade":
    default:
      return fade() as AnyPresentation;
  }
}

// Resolve the single transition used at the cut between cur and next.
// Precedence: next.in.transition -> cur.out.transition -> "fade".
function resolveCut(cur: SceneConfig, next: SceneConfig) {
  const fromNext = next.in?.transition;
  if (fromNext) {
    return {
      name: fromNext,
      durationInFrames: next.in?.durationInFrames ?? DEFAULT_TRANSITION_FRAMES,
    };
  }
  const fromCur = cur.out?.transition;
  if (fromCur) {
    return {
      name: fromCur,
      durationInFrames: cur.out?.durationInFrames ?? DEFAULT_TRANSITION_FRAMES,
    };
  }
  return { name: "fade", durationInFrames: DEFAULT_TRANSITION_FRAMES };
}

export const Main: React.FC<Props> = ({
  sceneConfig,
  withCaptions,
  captionStyle = "tiktok",
  renderMode: defaultRenderMode = "auto",
  frameWidth,
  frameHeight,
}) => {
  const children: React.ReactNode[] = [];
  sceneConfig.forEach((scene, index) => {
    const isLast = index === sceneConfig.length - 1;
    const sceneDurationInFrames = Math.round(scene.durationSeconds * FPS);
    // The cut after this scene (null for the last scene).
    const cut = isLast ? null : resolveCut(scene, sceneConfig[index + 1]);
    // Extend the scene by exactly this cut's transition frames so the
    // TransitionSeries overlap cancels: total == sum(round(D*FPS)).
    const durationInFrames =
      sceneDurationInFrames + (cut ? cut.durationInFrames : 0);
    const sceneRenderMode = scene.renderMode ?? defaultRenderMode;

    const inSfx = scene.in?.sfx ? SFX_MAP[scene.in.sfx] : undefined;
    const outSfx = scene.out?.sfx ? SFX_MAP[scene.out.sfx] : undefined;

    children.push(
      <TransitionSeries.Sequence
        key={`scene-${scene.sceneNumber}`}
        durationInFrames={durationInFrames}
      >
        <AbsoluteFill>
          <SceneImage
            imagePath={scene.imagePath}
            effect={scene.motionEffect}
            sceneDurationInFrames={sceneDurationInFrames}
            renderMode={sceneRenderMode}
            frameWidth={frameWidth}
            frameHeight={frameHeight}
          />
          {inSfx && <Audio src={inSfx} volume={SFX_VOLUME} />}
          {outSfx && (
            <Sequence
              from={Math.max(0, sceneDurationInFrames - SFX_OUT_LEAD)}
              layout="none"
            >
              <Audio src={outSfx} volume={SFX_VOLUME} />
            </Sequence>
          )}
        </AbsoluteFill>
      </TransitionSeries.Sequence>,
    );

    if (cut) {
      children.push(
        <TransitionSeries.Transition
          key={`transition-${scene.sceneNumber}`}
          presentation={buildPresentation(cut.name, frameWidth, frameHeight)}
          timing={linearTiming({ durationInFrames: cut.durationInFrames })}
        />,
      );
    }
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <Audio src={staticFile("audio_full.mp3")} />
      <TransitionSeries>{children}</TransitionSeries>
      {withCaptions && <CaptionOverlay captionStyle={captionStyle} />}
    </AbsoluteFill>
  );
};
