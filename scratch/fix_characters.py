from PIL import Image, ImageChops

def clean_gif(input_path, output_path):
    print(f"Processing {input_path}...")
    with Image.open(input_path) as img:
        frames = []
        durations = []
        
        try:
            while True:
                # Get original duration
                d = img.info.get('duration', 100)
                # If it was accidentally slowed down (e.g. 400ms), bring it back to a normal speed (100ms)
                if d >= 400: d = 100 
                durations.append(d)
                
                frame = img.convert("RGBA")
                width, height = frame.size
                
                # Use the corner pixel as the reference background color
                bg_color = frame.getpixel((0, 0))
                
                # If the GIF already has transparency, we want to keep it but clean artifacts
                data = list(frame.getdata())
                new_data = []
                
                # Threshold for background removal - very tight to avoid "missing pixels"
                threshold = 15
                
                for item in data:
                    # If it's already transparent, keep it
                    if item[3] == 0:
                        new_data.append(item)
                        continue
                        
                    # Calculate distance to background color
                    dist = sum(abs(item[i] - bg_color[i]) for i in range(3))
                    
                    # If it's extremely close to background OR it's a "white/gray noise" pixel 
                    # (common artifacts from bad removals)
                    is_noise = (item[0] > 240 and item[1] > 240 and item[2] > 240) # Near white
                    
                    if dist < threshold or (is_noise and bg_color[0] > 200):
                        new_data.append((0, 0, 0, 0))
                    else:
                        new_data.append(item)
                
                frame.putdata(new_data)
                frames.append(frame)
                
                img.seek(img.tell() + 1)
        except EOFError:
            pass
        
        if not frames:
            return

        # Save with correct disposal and duration
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            loop=0,
            duration=durations,
            disposal=2,
            transparency=0
        )
        print(f"Saved cleaned GIF to {output_path}")

# Fix all 12 characters
for i in range(1, 13):
    name = f"{i:02d}"
    # Try to find the file name pattern
    import os
    folder = "c:/flappyshits/character/"
    files = [f for f in os.listdir(folder) if f.startswith(name)]
    if files:
        clean_gif(folder + files[0], folder + files[0]) # Overwrite with cleaned version

clean_gif("c:/flappyshits/character/eagle_transparent.gif", "c:/flappyshits/character/eagle_transparent.gif")
