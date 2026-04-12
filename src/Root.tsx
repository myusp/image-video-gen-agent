import "./index.css";
import { Composition, staticFile } from "remotion";
import type { CalculateMetadataFunction } from "remotion";
import type { SceneConfig } from "./Main";
import { Main } from "./Main";
import type { CaptionStyle } from "./CaptionOverlay";

const FPS = 30;

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const MainComp = Main as React.ComponentType<any>;

interface MainProps {
  sceneConfig: SceneConfig[];
  withCaptions: boolean;
  captionStyle?: CaptionStyle;
}

interface VideoConfig {
  orientation?: "portrait" | "landscape";
  width?: number;
  height?: number;
}

const getDimensions = (config: VideoConfig) => {
  if (config.width && config.height) {
    return { width: config.width, height: config.height };
  }
  if (config.orientation === "landscape") {
    return { width: 1920, height: 1080 };
  }
  return { width: 1080, height: 1920 }; // portrait default
};

const loadSceneConfig = async (): Promise<{
  sceneConfig: SceneConfig[];
  totalFrames: number;
  width: number;
  height: number;
}> => {
  const resp = await fetch(staticFile("scene-config.json"));
  const raw = await resp.json();

  // Support both array format and object format with videoConfig
  let sceneConfig: SceneConfig[];
  let videoConfig: VideoConfig = {};

  if (Array.isArray(raw)) {
    sceneConfig = raw;
  } else {
    sceneConfig = raw.scenes;
    videoConfig = raw.videoConfig || {};
  }

  const { width, height } = getDimensions(videoConfig);
  // Do NOT subtract transition overlap from total frames.
  // Instead, Main.tsx extends each non-last scene by +TRANSITION_FRAMES so
  // the TransitionSeries total == sum(durationSeconds * FPS) == audio full length.
  const totalFrames = sceneConfig.reduce(
    (sum, s) => sum + Math.round(s.durationSeconds * FPS),
    0,
  );
  return { sceneConfig, totalFrames, width, height };
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const calculateMetadata: CalculateMetadataFunction<any> = async () => {
  const { sceneConfig, totalFrames, width, height } = await loadSceneConfig();
  return {
    durationInFrames: totalFrames,
    width,
    height,
    props: { sceneConfig, withCaptions: true } satisfies MainProps,
  };
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const calculateMetadataNoCaptions: CalculateMetadataFunction<any> =
  async () => {
    const { sceneConfig, totalFrames, width, height } =
      await loadSceneConfig();
    return {
      durationInFrames: totalFrames,
      width,
      height,
      props: { sceneConfig, withCaptions: false } satisfies MainProps,
    };
  };

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const calculateMetadataPlainCaptions: CalculateMetadataFunction<any> =
  async () => {
    const { sceneConfig, totalFrames, width, height } =
      await loadSceneConfig();
    return {
      durationInFrames: totalFrames,
      width,
      height,
      props: {
        sceneConfig,
        withCaptions: true,
        captionStyle: "plain",
      } satisfies MainProps,
    };
  };

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="main"
        component={MainComp}
        fps={FPS}
        width={1080}
        height={1920}
        defaultProps={{ sceneConfig: [], withCaptions: true }}
        calculateMetadata={calculateMetadata}
      />
      <Composition
        id="main-plain-captions"
        component={MainComp}
        fps={FPS}
        width={1080}
        height={1920}
        defaultProps={{
          sceneConfig: [],
          withCaptions: true,
          captionStyle: "plain" as const,
        }}
        calculateMetadata={calculateMetadataPlainCaptions}
      />
      <Composition
        id="main-no-captions"
        component={MainComp}
        fps={FPS}
        width={1080}
        height={1920}
        defaultProps={{ sceneConfig: [], withCaptions: false }}
        calculateMetadata={calculateMetadataNoCaptions}
      />
    </>
  );
};
