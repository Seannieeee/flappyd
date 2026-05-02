from PIL import Image

def remove_background(input_path, output_path):
    with Image.open(input_path) as img:
        frames = []
        try:
            while True:
                frame = img.convert("RGBA")
                width, height = frame.size
                
                bg_color = frame.getpixel((0, 0))
                
                to_process = set()
                for x in range(width):
                    to_process.add((x, 0))
                    to_process.add((x, height - 1))
                for y in range(height):
                    to_process.add((0, y))
                    to_process.add((width - 1, y))
                
                visited = set()
                bg_pixels = set()
                
                while to_process:
                    x, y = to_process.pop()
                    if (x, y) in visited:
                        continue
                    visited.add((x, y))
                    
                    if x < 0 or x >= width or y < 0 or y >= height:
                        continue
                        
                    pixel = frame.getpixel((x, y))
                    if abs(pixel[0]-bg_color[0]) < 10 and abs(pixel[1]-bg_color[1]) < 10 and abs(pixel[2]-bg_color[2]) < 10:
                        bg_pixels.add((x, y))
                        to_process.add((x+1, y))
                        to_process.add((x-1, y))
                        to_process.add((x, y+1))
                        to_process.add((x, y-1))
                
                data = list(frame.getdata())
                new_data = []
                for i, item in enumerate(data):
                    x = i % width
                    y = i // width
                    if (x, y) in bg_pixels:
                        new_data.append((255, 255, 255, 0))
                    else:
                        new_data.append(item)
                
                frame.putdata(new_data)
                frames.append(frame)
                
                img.seek(img.tell() + 1)
        except EOFError:
            pass
        
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            loop=0,
            duration=img.info.get('duration', 100) * 4,
            disposal=2
        )
        print("Background removed and saved to", output_path)

remove_background("c:/flappyshits/character/eagle.gif", "c:/flappyshits/character/eagle_transparent.gif")
