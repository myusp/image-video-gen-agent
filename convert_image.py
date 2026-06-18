import os
import sys
import glob
import subprocess

def main():
    if len(sys.argv) < 3:
        print("Usage: python convert_image.py <scene_num> <image_name_base>")
        sys.exit(1)
        
    scene_num = sys.argv[1]
    img_name_base = sys.argv[2]
    
    artifact_dir = "/Users/yusup/.gemini/antigravity-ide/brain/8910cdab-0604-4491-aa30-6b759a309cdd"
    dest_dir = f"output/20260603_mindset-video/scene_{scene_num}"
    dest_file = f"{dest_dir}/image_{scene_num}.jpeg"
    
    os.makedirs(dest_dir, exist_ok=True)
    
    # Search for the generated image in artifacts
    pattern = os.path.join(artifact_dir, f"{img_name_base}.*")
    matches = glob.glob(pattern)
    
    if not matches:
        print(f"[ERROR] No generated image found matching pattern: {pattern}")
        sys.exit(1)
        
    src_file = matches[0]
    print(f"Found source image: {src_file}")
    
    # Convert/copy to dest_file using FFmpeg
    cmd = ["ffmpeg", "-y", "-i", src_file, dest_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"[OK] Converted and saved: {dest_file}")
        # Clean up source file
        try:
            os.remove(src_file)
        except Exception as e:
            print(f"[WARN] Failed to remove source file {src_file}: {e}")
    else:
        print(f"[ERROR] FFmpeg conversion failed: {result.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    main()
