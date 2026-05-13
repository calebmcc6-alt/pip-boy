from body import Body
import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
BODY_IMAGE_SIZE = 512


def health_state(health):
    if health == 100:
        return "healthy"
    if health > 50:
        return "hurt"
    if health > 0:
        return "critical"
    return "removed"


def health_color(health):
    if health == 100:
        return (0, 80, 0)
    if health > 50:
        return (230, 210, 0)
    return (190, 0, 0)


def recolor_black_pixels(img, color):
    recolored = img.copy().convert("RGBA")
    pixels = recolored.load()

    for y in range(recolored.height):
        for x in range(recolored.width):
            red, green, blue, alpha = pixels[x, y]
            if alpha > 0 and red < 80 and green < 80 and blue < 80:
                pixels[x, y] = (*color, alpha)

    return recolored


def main():
    root = tk.Tk()
    root.title("Pip Boy")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    body = Body()

    left_frame = tk.Frame(root, bg="lightgreen")
    left_frame.pack(side="left", expand=True, fill="both")
    right_frame = tk.Frame(root, bg="darkgray")
    right_frame.pack(side="left", expand=True, fill="both")

    body_part_images = []
    body_canvas = tk.Canvas(left_frame, bg="lightgreen", highlightthickness=0)
    body_canvas.pack(expand=True, fill="both")

    image_files = [
        ("Left Leg", "LLeg.png"),
        ("Right Leg", "RLeg.png"),
        ("Left Arm", "LArm.png"),
        ("Right Arm", "RArm.png"),
        ("Torso", "Torso.png"),
        ("Head", "Head.png"),
    ]

    original_images = {}
    body_part_states = {}

    for part, file in image_files:
        img = Image.open(BASE_DIR / "assets" / file)
        original_images[part] = img.resize((BODY_IMAGE_SIZE, BODY_IMAGE_SIZE))
        body_part_states[part] = health_state(body.body[part]["Health"])

    def draw_body(event=None):
        body_part_images.clear()
        body_canvas.delete("all")
        x = body_canvas.winfo_width() // 2
        y = body_canvas.winfo_height() // 2

        for part, _ in image_files:
            health = body.body[part]["Health"]
            if health == 0:
                continue

            colored_img = recolor_black_pixels(original_images[part], health_color(health))
            tk_img = ImageTk.PhotoImage(colored_img)
            body_part_images.append(tk_img)
            body_canvas.create_image(x, y, image=tk_img, anchor="center")

    body_canvas.bind("<Configure>", draw_body)

    def set_part_health(part, value):
        new_health = int(float(value))
        new_state = health_state(new_health)

        body.body[part]["Health"] = new_health
        if new_state == body_part_states[part]:
            return

        body_part_states[part] = new_state
        draw_body()

    controls_frame = tk.Frame(right_frame, bg="darkgray")
    controls_frame.pack(fill="x", expand=True)

    for part in body.body:
        part_frame = tk.Frame(controls_frame, bg="darkgray")
        part_frame.pack(fill="x", padx=24, pady=12)

        part_label = tk.Label(
            part_frame,
            text=f"{part}:",
            bg="darkgray",
            fg="white",
            font=("Arial", 14, "bold"),
            anchor="w",
        )
        part_label.pack(fill="x")

        health_frame = tk.Frame(part_frame, bg="darkgray")
        health_frame.pack(fill="x", pady=(4, 0))

        health_label = tk.Label(
            health_frame,
            text="Health:",
            bg="darkgray",
            fg="white",
            font=("Arial", 11),
        )
        health_label.pack(side="left")

        health_slider = tk.Scale(
            health_frame,
            from_=0,
            to=100,
            orient="horizontal",
            command=lambda value, body_part=part: set_part_health(body_part, value),
            bg="darkgray",
            fg="white",
            troughcolor="#222222",
            highlightthickness=0,
        )
        health_slider.set(body.body[part]["Health"])
        health_slider.pack(side="left", expand=True, fill="x", padx=(8, 0))

    root.mainloop()
    

if __name__== "__main__":
    main()
