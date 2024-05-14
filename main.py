import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw, ImageFont


def refresh_window():
    window.update()
    window.update_idletasks()


def search_for_photo() -> filedialog:
    filetypes = (("png files", "*.png"),
                 ("jpg files", "*.jpg"))
    return filedialog.askopenfilename(title="Open",
                                      initialdir="C:",
                                      filetypes=filetypes)


def ask_for_directory() -> filedialog:
    return filedialog.askdirectory(title="Save",
                                   initialdir="C:")


def parse_photo(image: object) -> None:
    new_image = ImageTk.PhotoImage(image.resize((int(image.width / 2), int(image.height / 2))))
    panel.config(image=new_image)
    panel.image = new_image


def calculate_foreground_size(background: object, foreground: object) -> tuple:
    # ____________________TESTS____________________________
    """ (x = height, y = width) as for PIL.Image.resize
    Test 1. Background photo ( x > y ) && foreground photo ( x > y ) pass
    Test 2. Background photo ( x < y ) && foreground photo ( x > y ) pass
    Test 3. Background photo ( x > y ) && foreground photo ( x < y ) pass
    Test 4. Background photo ( x < y ) && foreground photo ( x < y ) pass
    Test 5. Background photo ( x = y ) && foreground photo ( x = y ) pass
    """
    if background.width >= background.height:

        if foreground.height >= foreground.width:
            proportions_height = foreground.height / foreground.width
            foreground_new_height = background.height / 7
            foreground_new_width = foreground_new_height * proportions_height

        elif foreground.height < foreground.width:
            proportions_width = foreground.width / foreground.height
            foreground_new_width = background.width / 7
            foreground_new_height = foreground_new_width * proportions_width

    else:

        if foreground.height >= foreground.width:
            proportions_height = foreground.height / foreground.width
            foreground_new_height = background.width / 7
            foreground_new_width = foreground_new_height * proportions_height

        elif foreground.height < foreground.width:
            proportions_width = foreground.width / foreground.height
            foreground_new_width = background.height / 7
            foreground_new_height = foreground_new_width * proportions_width

    return int(foreground_new_height), int(foreground_new_width)


def determine_coordinates(background: object, foreground_tuple_x_y: tuple) -> tuple:
    x = background.width - foreground_tuple_x_y[0]
    y = background.height - foreground_tuple_x_y[1]
    return x, y


def add_photo():
    def add_watermark_image(background: object):
        # Get the image obj
        foreground = Image.open(search_for_photo())
        foreground.convert('RGBA')
        half_transparent_foreground = foreground.getchannel('A').point(lambda p: p * 0.5)
        # Put the modified alpha channel back into the image
        foreground.putalpha(half_transparent_foreground)
        # sizing
        resized_values_foreground = calculate_foreground_size(background, foreground)
        water_mark_resized = foreground.resize(resized_values_foreground)
        # coordinates
        coords = determine_coordinates(background, resized_values_foreground)
        # paste onto main image
        background.paste(water_mark_resized, coords, water_mark_resized)
        parse_photo(background)
        #background.save("output.png")

    def add_watermark_text(background: Image.Image, text: str, font_path: str, font_size: int,
                           opacity: int = 20) -> Image.Image:
        """
        Adds a watermark text to the input image.

        Args:
            background (Image.Image): The input image (PIL Image object).
            text (str): The watermark text.
            font_path (str): Path to the font file (e.g., ".ttf" or ".otf").
            font_size (int): Font size for the watermark text.
            opacity (int, optional): Opacity level (0-255). Default is 50.

        Returns:
            Image.Image: Image with the watermark text added.
        """

        # Initialize drawing context
        draw = ImageDraw.Draw(background)

        # Load the font
        font = ImageFont.truetype(font_path, font_size)

        # Draw the watermark text with specified opacity
        draw.text((background.width, background.height), text, font=font, fill=(255, 255, 255, opacity), anchor="rs")

        parse_photo(background)

    def save_photo(img: object):
        a = ask_for_directory()
        img.save(fp=f"{a}/watermarked.png")

    with Image.open(search_for_photo()) as image:
        image_resized = image.resize((int(image.width / 2), int(image.height / 2)))

        parse_photo(image_resized)

        check_button = tk.Button(window,
                                 bg="green",
                                 text="add watermark image",
                                 command=lambda: add_watermark_image(image))
        check_button.grid(row=0,
                          column=1)
        check_button = tk.Button(window,
                                 bg="green",
                                 text="add watermark text",
                                 command=lambda: add_watermark_text(image,
                                                                    "Example",
                                                                    "C:\\Windows\\Fonts\\BAUHS93.TTF",
                                                                    60))
        check_button.grid(row=0,
                          column=2)
        save_button = tk.Button(window,
                                bg="green",
                                text="save",
                                command=lambda: save_photo(image_resized))
        save_button.grid(row=0,
                         column=3)


window = tk.Tk()
window.title("Watermark maker")

frame = tk.Frame(window,
                 bg="lightblue",
                 height=500,
                 width=500)
frame.grid(row=1,
           column=0,
           columnspan=4)

add_button = tk.Button(window,
                       bg="green",
                       text="add photo",
                       command=add_photo)
add_button.grid(row=0,
                column=0)

# placeholder img for init the Label
PLACEHOLDER = Image.open("dog-png-30.png")
PLACEHOLDER_IMG = ImageTk.PhotoImage(PLACEHOLDER)
PLACEHOLDER_IMG_WIDTH = PLACEHOLDER_IMG.width()
PLACEHOLDER_IMG_HEIGHT = PLACEHOLDER_IMG.height()

panel = tk.Label(frame,
                 image=PLACEHOLDER_IMG)
panel.pack()

window.mainloop()

# TODO 1. add function "add_watermark_text"
# TODO 2. add main photo
# TODO 3. make sure all functionalities work as intended
# TODO 4. make classes for everything
# TODO 5. save function
