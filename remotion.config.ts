import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);

// Allow per-video public directory via env variable
// Usage: REMOTION_PUBLIC_DIR=./output/my-video npx remotion render main ...
if (process.env.REMOTION_PUBLIC_DIR) {
  Config.setPublicDir(process.env.REMOTION_PUBLIC_DIR);
}
