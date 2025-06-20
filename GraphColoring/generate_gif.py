from PIL import Image
import os

def generate_gif(frame_folder="frames", output_name="animation.gif", duration=200):
    # Sıralı olarak tüm frame görsellerini al
    frames = sorted(
        [f for f in os.listdir(frame_folder) if f.endswith(".png")],
        key=lambda x: int(x.split("_")[1].split(".")[0])
    )
    images = [Image.open(os.path.join(frame_folder, f)) for f in frames]

    if images:
        images[0].save(
            output_name,
            format='GIF',
            append_images=images[1:],
            save_all=True,
            duration=duration,
            loop=0
        )
        print(f"✅ GIF saved as {output_name}")
    else:
        print("⚠️ No frames found to create GIF.")