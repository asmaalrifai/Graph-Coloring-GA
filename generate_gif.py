from PIL import Image
import os

def generate_gif(frame_folder="frames", output_name="animation.gif", duration=200):
    # Collect all PNG frames in order based on generation number
    frames = sorted(
        [f for f in os.listdir(frame_folder) if f.endswith(".png")],
        key=lambda x: int(x.split("_")[1].split(".")[0])
    )

    # Load all frame images into memory
    images = [Image.open(os.path.join(frame_folder, f)) for f in frames]

    if images:
        # Save the first frame and append the rest to create a looping GIF
        images[0].save(
            output_name,
            format='GIF',
            append_images=images[1:],
            save_all=True,
            duration=duration,
            loop=0
        )
        print(f"GIF saved as {output_name}")
    else:
        print("No frames found to create GIF.")
