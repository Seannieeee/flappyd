from PIL import Image
import os

def trim_fire_frames(input_path, output_path):
    with Image.open(input_path) as img:
        frames = []
        durations = []
        
        # We'll check for "fire" by looking for high intensity in Red and Green (Yellow/Orange)
        # in the area where fire usually is (front of the dragon).
        
        frame_idx = 0
        try:
            while True:
                frame = img.convert("RGBA")
                width, height = frame.size
                
                # Check right half/front area for fire colors
                # Fire is usually very bright: R > 200, G > 100, B < 150
                pixels = list(frame.getdata())
                fire_pixels = 0
                for p in pixels:
                    if p[3] > 0: # not transparent
                        if p[0] > 220 and p[1] > 120 and p[2] < 150:
                            fire_pixels += 1
                
                # If less than 1% of pixels are "fire", keep it
                if fire_pixels < (width * height * 0.005):
                    frames.append(frame)
                    durations.append(img.info.get('duration', 100))
                    print(f"Frame {frame_idx}: Keeping (Fire pixels: {fire_pixels})")
                else:
                    print(f"Frame {frame_idx}: REMOVING (Fire pixels: {fire_pixels})")
                
                frame_idx += 1
                img.seek(img.tell() + 1)
        except EOFError:
            pass
        
        if frames:
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                loop=0,
                duration=durations,
                disposal=2
            )
            print(f"Saved trimmed GIF to {output_path} with {len(frames)} frames")
        else:
            print("No frames left after trimming!")

trim_fire_frames("c:/flappyshits/bosses/dragon_clean.gif", "c:/flappyshits/bosses/dragon_no_fire.gif")
