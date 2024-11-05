import os
import ctypes
import sys
from tkinter import Tk, Label, Button, filedialog, messagebox, StringVar, OptionMenu
from tkinter import font as tkFont
from PIL import Image


class ImageConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Converter")
        if sys.platform == "win32":
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Enable DPI awareness
            except Exception as e:
                print(f"Could not set DPI awareness on Windows: {e}")
        self.root.geometry("500x300")
        self.root.resizable(True, True)

        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=13)

        optionmenu_font = tkFont.Font(size=13)

        self.input_path = None
        self.output_path = None


        # Output Format Dropdown
        self.output_format = StringVar(root)
        self.output_format.set("JPEG")  # Default value
        self.format_label = Label(root, text="Select Output Format: ")
        self.format_label.pack(pady=5)

        formats = ["JPEG", "PNG", "BMP", "GIF", "TIFF", "WEBP"]
        self.format_menu = OptionMenu(root, self.output_format, *formats)
        self.format_menu.config(font=optionmenu_font)
        self.format_menu.pack(pady=5)

        menu = self.root.nametowidget(self.format_menu.menuname)
        menu.config(font=optionmenu_font)

        # Input Image Label
        self.input_label = Label(root, text="Input Image: ")
        self.input_label.pack(pady=5)

        self.select_input_button = Button(root, text="Select Input Image", command=self.select_input_image)
        self.select_input_button.pack(pady=5)

        self.convert_button = Button(root, text="Convert Image", command=self.convert_image)
        self.convert_button.pack(pady=5)

    def select_input_image(self):
        self.input_path = filedialog.askopenfilename(title="Select Image", filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif *.webp")])
        if self.input_path:
            self.input_label.config(text=f"Selected: {os.path.basename(self.input_path)}")

    def convert_image(self):
        if not self.input_path:
            messagebox.showerror("Error", "Please select an input image.")
            return

        input_file_name = os.path.basename(self.input_path)
        base_name, ext = os.path.splitext(input_file_name)
        output_file_name = f"{base_name}.{self.output_format.get().lower()}"

        output_dir = os.path.dirname(self.input_path)
        output_path = os.path.join(output_dir, output_file_name)
        counter = 1
        while os.path.exists(output_path):
            output_file_name = f"{base_name} ({counter}).{self.output_format.get().lower()}"
            output_path = os.path.join(output_dir, output_file_name)
            counter += 1

        self.output_path = filedialog.asksaveasfilename(
            initialfile=output_file_name,
            defaultextension=f".{self.output_format.get().lower()}",
            filetypes=[(f"{self.output_format.get()} files",
                        f"*.{self.output_format.get().lower()}")]
        )
        if not self.output_path:
            return

        try:
            image = Image.open(self.input_path)

            # Check if the output format supports transparency and handle conversion
            if self.output_format.get() in ["JPEG", "BMP", "WEBP"]:
                if image.mode == 'RGBA':
                    # Create a white background and blend the RGBA image with it
                    background = Image.new("RGBA", image.size, (255, 255, 255, 1))
                    image = Image.alpha_composite(background, image).convert("RGB")
                elif image.mode != 'RGB':
                    # Convert non-RGBA images to RGB directly
                    image = image.convert('RGB')

            image.save(self.output_path, format=self.output_format.get())
            messagebox.showinfo("Success", f"Image converted to {self.output_format.get()} successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert image: {e}")


if __name__ == "__main__":
    root = Tk()
    app = ImageConverter(root)
    root.mainloop()
