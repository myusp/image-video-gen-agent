import "./index.css";
import { Composition, staticFile } from "remotion";
import type { CalculateMetadataFunction } from "remotion";
import type { SceneConfig } from "./Main";
import { Main } from "./Main";
import type { CaptionStyle } from "./CaptionOverlay";

const FPS = 30;
const TRANSITION_FRAMES = 15;

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const MainComp = Main as React.ComponentType<any>;

interface MainProps {
  sceneConfig: SceneConfig[];
  withCaptions: boolean;
  captionStyle?: CaptionStyle;
}

const loadSceneConfig = async (): Promise<{
  sceneConfig: SceneConfig[];
  totalFrames: number;
}> => {
  const resp = await fetch(staticFile("scene-config.json"));
  const sceneConfig: SceneConfig[] = await resp.json();
  const totalFrames =
    sceneConfig.reduce(
      (sum, s) => sum + Math.round(s.durationSeconds * FPS),
      0,
    ) -
    TRANSITION_FRAMES * (sceneConfig.length - 1);
  return { sceneConfig, totalFrames };
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const calculateMetadata: CalculateMetadataFunction<any> = async () => {
  const { sceneConfig, totalFrames } = await loadSceneConfig();
  return {
    durationInFrames: totalFrames,
    props: { sceneConfig, withCaptions: true } satisfies MainProps,
  };
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const calculateMetadataNoCaptions: CalculateMetadataFunction<any> =
  async () => {
    const { sceneConfig, totalFrames } = await loadSceneConfig();
    return {
      durationInFrames: totalFrames,
      props: { sceneConfig, withCaptions: false } satisfies MainProps,
    };
  };

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const calculateMetadataPlainCaptions: CalculateMetadataFunction<any> =
  async () => {
    const { sceneConfig, totalFrames } = await loadSceneConfig();
    return {
      durationInFrames: totalFrames,
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
