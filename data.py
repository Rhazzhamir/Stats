from typing import Optional, Tuple, Union
import customtkinter as ctk
from text_to_array import sanitize_input, resource_path
from PIL import Image
import os


class DataScreen(ctk.CTkFrame):
    def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        textbox_style = {
            'width': 600,
            'height': 300,
            'fg_color': 'white',
            'corner_radius': 10,
            'text_color': 'black',
            'border_color': 'black',
            'border_width': 1,
            'border_spacing': 15,
            'font': ctk.CTkFont(size=16)
        }
        button_frame_style = {
            'fg_color': 'transparent',
            'height': 50,
        }

        # Container for textbox and textbox label
        self.input_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.input_frame.pack(expand=True)

        self.textbox = ctk.CTkTextbox(self.input_frame, **textbox_style)
        self.textbox.pack(expand=True)

        self.input_label = ctk.CTkLabel(self.input_frame, text='comma separated input values')
        self.input_label.pack(anchor=ctk.E, padx=(0, 10))

        # Container for buttons
        self.button_frame = ctk.CTkFrame(self.input_frame, **button_frame_style)
        self.button_frame.pack(fill='x')

        self.clear_btn = ctk.CTkButton(self.button_frame, text='Clear', width=90)
        self.clear_btn.pack(side=ctk.LEFT, padx=10)

        self.result_btn = ctk.CTkButton(self.button_frame, text='Generate Result')
        self.result_btn.pack(side=ctk.RIGHT, padx=10, pady=10)

        self.sanitize_btn = ctk.CTkButton(self.button_frame, text='Sanitize Input', command=lambda: replace_text(self.textbox))
        self.sanitize_btn.pack(side=ctk.RIGHT)

        self.expand_img = ctk.CTkImage(light_image=Image.open(resource_path('expand.png')), size=(30, 30))
        self.compress_img = ctk.CTkImage(light_image=Image.open(resource_path('compress.png')), size=(30, 30))
        self.fullscreen = False

        self.screen_ctrl_btn = ctk.CTkButton(self, text='', height=30, width=30, image=self.expand_img, compound='right')
        self.screen_ctrl_btn.configure(command=self.toggle_screen)
        self.screen_ctrl_btn.place(relx=0.88, rely=0.01)
        self.screen_ctrl_btn.lift()
    
    def toggle_screen(self):
        if not self.fullscreen:
            self.expand_screen()
        else:
            self.compress_screen()
        self.fullscreen = not self.fullscreen
        self.screen_ctrl_btn.lift()
    
    def compress_screen(self):
        self.screen_ctrl_btn.configure(image=self.expand_img)
        self.place_configure(relx=0.05, rely=0, relwidth=0.4, relheight=1)
    
    def expand_screen(self):
        self.screen_ctrl_btn.configure(image=self.compress_img)
        self.place_configure(relx=0, rely=0, relheight=1, relwidth=1)
        self.lift()


def replace_text(textbox: ctk.CTkTextbox):
    replacement_text = sanitize_input(textbox.get('1.0', 'end'))
    textbox.delete('1.0', 'end')
    textbox.insert('1.0', replacement_text)
