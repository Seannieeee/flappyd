from PIL import Image

def process_gif(input_path, output_path, speed_mult=1.0):
    with Image.open(input_path) as img:
        frames = []
        durations = []
        try:
            while True:
                frame = img.convert("RGBA")
                frames.append(frame)
                dur = img.info.get('duration', 100)
                durations.append(int(dur * speed_mult))
                img.seek(img.tell() + 1)
        except EOFError:
            pass
        
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            loop=0,
            duration=durations,
            disposal=2
        )
        print(f"Saved {output_path} with speed multiplier {speed_mult}")

# Slow down the new dragon
process_gif("c:/flappyshits/bosses/dragon_clean.gif", "c:/flappyshits/bosses/dragon_slow.gif", speed_mult=2.2)
