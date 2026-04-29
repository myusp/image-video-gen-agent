import { AbsoluteFill, staticFile } from "remotion";
import { Audio } from "@remotion/media";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { SceneImage } from "./SceneImage";
import type { MotionEffect } from "./SceneImage";
import { CaptionOverlay } from "./CaptionOverlay";
import type { CaptionStyle } from "./CaptionOverlay";

const FPS = 30;
const TRANSITION_FRAMES = 15;

export interface SceneConfig {
  sceneNumber: number;
  imagePath: string;
  audioPath: string;
  durationSeconds: number;
  motionEffect: MotionEffect;
}

interface Props {
  sceneConfig: SceneConfig[];
  withCaptions: boolean;
  captionStyle?: CaptionStyle;
}

export const Main: React.FC<Props> = ({
  sceneConfig,
  withCaptions,
  captionStyle = "tiktok",
}) => {
  const children: React.ReactNode[] = [];
  sceneConfig.forEach((scene, index) => {
    const isLast = index === sceneConfig.length - 1;
    const sceneDurationInFrames = Math.round(scene.durationSeconds * FPS);
    // For all scenes except the last, add TRANSITION_FRAMES so the scene
    // "holds" visually during the fade while its audio has already ended.
    // This ensures: TransitionSeries total == sum(durationSeconds * FPS)
    // == audio_full length, with zero audio overlap between scenes.
    const durationInFrames =
      sceneDurationInFrames + (isLast ? 0 : TRANSITION_FRAMES);
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
          />
        </AbsoluteFill>
      </TransitionSeries.Sequence>,
    );
    if (index < sceneConfig.length - 1) {
      children.push(
        <TransitionSeries.Transition
          key={`transition-${scene.sceneNumber}`}
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
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
