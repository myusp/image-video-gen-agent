import os
import glob
import json

project_folder = "output/20260603_mindset"
scenes = sorted(glob.glob(f"{project_folder}/scene_*"))

base_style = "vintage comic style illustration, representative scene, clean, minimal text, landscape 16:9 aspect ratio"

for scene in scenes:
    scene_num = scene.split("_")[-1]
    subtitle_file = os.path.join(scene, f"subtitles_{scene_num}.txt")
    prompt_file = os.path.join(scene, f"prompt_{scene_num}.txt")
    
    if os.path.exists(subtitle_file):
        with open(subtitle_file, "r") as f:
            text = f.read().strip()
        
        # We can extract a few keywords or just use the text as context
        prompt = f"A scene depicting: {text}. {base_style}"
        
        with open(prompt_file, "w") as f:
            f.write(prompt)
        print(f"Generated prompt for {scene_num}")
