import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";

export type MotionEffect =
  | "zoom_in"
  | "zoom_out"
  | "pan_left_right"
  | "pan_right_left"
  | "pan_up_down"
  | "pan_down_up"
  | "ken_burns";

interface Props {
  imagePath: string;
  effect: MotionEffect;
  sceneDurationInFrames: number;
}

export const SceneImage: React.FC<Props> = ({ imagePath, effect, sceneDurationInFrames }) => {
  const frame = useCurrentFrame();

  const easing = Easing.bezier(0.45, 0, 0.55, 1);

  const progress = interpolate(frame, [0, sceneDurationInFrames], [0, 1], {
    easing,
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  let scale = 1;
  let translateX = "0%";
  let translateY = "0%";

  switch (effect) {
    case "zoom_in":
      scale = interpolate(progress, [0, 1], [1.0, 1.5]);
      break;

    case "zoom_out":
      scale = interpolate(progress, [0, 1], [1.5, 1.0]);
      break;

    case "pan_left_right":
      scale = 1.5;
      translateX = `${interpolate(progress, [0, 1], [10, -10])}%`;
      break;

    case "pan_right_left":
      scale = 1.5;
      translateX = `${interpolate(progress, [0, 1], [-10, 10])}%`;
      break;

    case "pan_up_down":
      scale = 1.5;
      translateY = `${interpolate(progress, [0, 1], [10, -10])}%`;
      break;

    case "pan_down_up":
      scale = 1.5;
      translateY = `${interpolate(progress, [0, 1], [-10, 10])}%`;
      break;

    case "ken_burns":
      scale = interpolate(progress, [0, 1], [1.0, 1.4]);
      translateX = `${interpolate(progress, [0, 1], [0, 5])}%`;
      translateY = `${interpolate(progress, [0, 1], [0, 3])}%`;
      break;
  }

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <Img
        src={staticFile(imagePath)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${scale}) translate(${translateX}, ${translateY})`,
          transformOrigin: "center center",
        }}
      />
    </AbsoluteFill>
  );
};
