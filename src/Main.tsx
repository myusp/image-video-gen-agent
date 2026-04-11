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
    const durationInFrames = Math.round(scene.durationSeconds * FPS);
    children.push(
      <TransitionSeries.Sequence
        key={`scene-${scene.sceneNumber}`}
        durationInFrames={durationInFrames}
      >
        <AbsoluteFill>
          <SceneImage
            imagePath={scene.imagePath}
            effect={scene.motionEffect}
          />
          <Audio src={staticFile(scene.audioPath)} />
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
      <TransitionSeries>{children}</TransitionSeries>
      {withCaptions && <CaptionOverlay captionStyle={captionStyle} />}
    </AbsoluteFill>
  );
};
