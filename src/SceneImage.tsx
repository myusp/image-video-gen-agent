import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { useMemo } from "react";

export type MotionEffect =
  | "zoom_in"
  | "zoom_out"
  | "pan_left_right"
  | "pan_right_left"
  | "pan_up_down"
  | "pan_down_up"
  | "ken_burns"
  | "none";

export type RenderMode = "auto" | "cover_subtle" | "contain_blur";

const ASPECT_RATIO_TOLERANCE = 0.05;

type MotionValues = {
  scale: number;
  translateX: string;
  translateY: string;
};

function computeMotion(
  effect: MotionEffect,
  progress: number,
  mode: "cover_full" | "cover_subtle",
): MotionValues {
  if (mode === "cover_full") {
    // Original zoom ranges — used when contain_blur is active (safe because
    // contain doesn't crop — an image outside the visible box is invisible,
    // so zoom/pan inside a contain box is decorative cropping of hidden overflow.)
    switch (effect) {
      case "none":
        return { scale: 1, translateX: "0%", translateY: "0%" };
      case "zoom_in":
        return { scale: interpolate(progress, [0, 1], [1.0, 1.5]), translateX: "0%", translateY: "0%" };
      case "zoom_out":
        return { scale: interpolate(progress, [0, 1], [1.5, 1.0]), translateX: "0%", translateY: "0%" };
      case "pan_left_right":
        return { scale: 1.5, translateX: `${interpolate(progress, [0, 1], [10, -10])}%`, translateY: "0%" };
      case "pan_right_left":
        return { scale: 1.5, translateX: `${interpolate(progress, [0, 1], [-10, 10])}%`, translateY: "0%" };
      case "pan_up_down":
        return { scale: 1.5, translateX: "0%", translateY: `${interpolate(progress, [0, 1], [10, -10])}%` };
      case "pan_down_up":
        return { scale: 1.5, translateX: "0%", translateY: `${interpolate(progress, [0, 1], [-10, 10])}%` };
      case "ken_burns":
        return {
          scale: interpolate(progress, [0, 1], [1.0, 1.4]),
          translateX: `${interpolate(progress, [0, 1], [0, 5])}%`,
          translateY: `${interpolate(progress, [0, 1], [0, 3])}%`,
        };
    }
  }

  // cover_subtle — reduced zoom to minimise cropping
  switch (effect) {
    case "none":
      return { scale: 1, translateX: "0%", translateY: "0%" };
    case "zoom_in":
      return { scale: interpolate(progress, [0, 1], [1.0, 1.10]), translateX: "0%", translateY: "0%" };
    case "zoom_out":
      return { scale: interpolate(progress, [0, 1], [1.10, 1.0]), translateX: "0%", translateY: "0%" };
    case "pan_left_right":
      return { scale: 1.12, translateX: `${interpolate(progress, [0, 1], [4, -4])}%`, translateY: "0%" };
    case "pan_right_left":
      return { scale: 1.12, translateX: `${interpolate(progress, [0, 1], [-4, 4])}%`, translateY: "0%" };
    case "pan_up_down":
      return { scale: 1.12, translateX: "0%", translateY: `${interpolate(progress, [0, 1], [4, -4])}%` };
    case "pan_down_up":
      return { scale: 1.12, translateX: "0%", translateY: `${interpolate(progress, [0, 1], [-4, 4])}%` };
    case "ken_burns":
      return {
        scale: interpolate(progress, [0, 1], [1.0, 1.08]),
        translateX: `${interpolate(progress, [0, 1], [0, 2])}%`,
        translateY: `${interpolate(progress, [0, 1], [0, 1])}%`,
      };
  }
}

interface Props {
  imagePath: string;
  effect: MotionEffect;
  sceneDurationInFrames: number;
  renderMode?: RenderMode;
  frameWidth: number;
  frameHeight: number;
}

export const SceneImage: React.FC<Props> = ({
  imagePath,
  effect,
  sceneDurationInFrames,
  renderMode: renderModeProp = "auto",
  frameWidth,
  frameHeight,
}) => {
  const frame = useCurrentFrame();

  const easing = Easing.bezier(0.45, 0, 0.55, 1);

  const progress = interpolate(frame, [0, sceneDurationInFrames], [0, 1], {
    easing,
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Determine effective render mode
  const mode = useMemo(() => {
    if (renderModeProp === "cover_subtle" || renderModeProp === "contain_blur") {
      return renderModeProp;
    }
    // auto: detect AR match
    // Assume image AR matches frame AR (Pollinations generates at requested size).
    // If image AR is unknown, we treat it as matching — safe for most cases.
    // When image has a known different AR (set via scene config), compute here.
    const frameAr = frameWidth / frameHeight;
    // We don't have image dimensions at runtime unless stored in scene-config.
    // Default assumption: Pollinations always produces images at the requested
    // video dimensions, so AR = frame AR. Still allow a detected mismatch via
    // a scene-level override.
    const imageAr = frameAr; // match by default
    if (Math.abs(imageAr - frameAr) / frameAr < ASPECT_RATIO_TOLERANCE) {
      return "cover_subtle";
    }
    return "contain_blur";
  }, [renderModeProp, frameWidth, frameHeight]);

  const motion = computeMotion(effect, progress, mode === "contain_blur" ? "cover_full" : "cover_subtle");

  if (mode === "contain_blur") {
    return (
      <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#000" }}>
        {/* Blurred background layer — fills entire frame */}
        <Img
          src={staticFile(imagePath)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            transform: `scale(${motion.scale}) translate(${motion.translateX}, ${motion.translateY})`,
            transformOrigin: "center center",
            filter: "blur(30px)",
            opacity: 0.8,
          }}
        />
        {/* Foreground layer — image fully visible, no crop */}
        <Img
          src={staticFile(imagePath)}
          style={{
            position: "absolute",
            inset: 0,
            width: "100%",
            height: "100%",
            objectFit: "contain",
          }}
        />
      </AbsoluteFill>
    );
  }

  // cover_subtle: single layer with reduced zoom
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <Img
        src={staticFile(imagePath)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${motion.scale}) translate(${motion.translateX}, ${motion.translateY})`,
          transformOrigin: "center center",
        }}
      />
    </AbsoluteFill>
  );
};
