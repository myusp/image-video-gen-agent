import {
  whoosh,
  whip,
  pageTurn,
  ding,
  vineBoom,
  uiSwitch,
  mouseClick,
} from "@remotion/sfx";

// Maps a scene-config `sfx` string to a @remotion/sfx hosted URL.
// Keys are the strings used in scene-config.json `in.sfx` / `out.sfx`.
export const SFX_MAP: Record<string, string> = {
  whoosh,
  whip,
  pageTurn,
  ding,
  vineBoom,
  uiSwitch,
  mouseClick,
};
