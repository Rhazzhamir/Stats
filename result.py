from typing import Tuple
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from solution import *
from text_to_array import text_to_float_array, resource_path
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
import os

class ResultScreen(ctk.CTkFrame):
    def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.__default_innerframe()
        self.kdeplot_fig = None
        self.histplot_fig = None

    def set_innerframe_to_default(self):
        if self.kdeplot_fig:
            plt.close(self.kdeplot_fig)
        if self.histplot_fig:
            plt.close(self.histplot_fig)
        self.inner_frame.destroy()
        self.__default_innerframe()

    def __default_innerframe(self):
        self.inner_frame = ctk.CTkLabel(
            self, text='No Result', fg_color='transparent', font=ctk.CTkFont(size=18, weight='bold'))
        self.inner_frame.pack(expand=True)
    
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
        self.place_configure(relx=0.5, rely=0, relwidth=0.5, relheight=1)
    
    def expand_screen(self):
        self.screen_ctrl_btn.configure(image=self.compress_img)
        self.place_configure(relx=0, rely=0, relheight=1, relwidth=1)
        self.lift()


def clear_input(root):
    root.data_frame.textbox.delete('1.0', 'end')
    root.result_frame.set_innerframe_to_default()


def generate_result(root):
    text = root.data_frame.textbox.get('1.0', 'end').strip(' \n\t')
    data = text_to_float_array(text)

    if text and data:
        if root.result_frame.inner_frame:
            if root.result_frame.kdeplot_fig:
                plt.close(root.result_frame.kdeplot_fig)
            if root.result_frame.histplot_fig:
                plt.close(root.result_frame.histplot_fig)
            root.result_frame.inner_frame.destroy()
            root.result_frame.inner_frame = ctk.CTkFrame(root.result_frame)
            root.result_frame.inner_frame.pack(expand=True, fill='both')

        result = ctk.CTkScrollableFrame(root.result_frame.inner_frame, fg_color='transparent')
        result.pack(expand=True, fill='both')
        data = np.array(data)

        ct = central_tendency(data)
        mol = measure_of_location(data)
        mod = measure_of_dispersion(data)
        moment = population_moment(data)

        display_result(root, result, data)
        more_info_btn = ctk.CTkButton(root.result_frame.inner_frame, text='More info...', fg_color='transparent', border_width=1, border_color='white', cursor='hand2')
        more_info_btn.configure(
            command=lambda: more_info(root, data, {
                'central tendency': ct,
                'measure of location':  mol,
                'measure of dispersion': mod,
                'moment': moment,
        }))
        more_info_btn.pack(side=ctk.BOTTOM, anchor=ctk.SE, padx=10, pady=10)
        root.result_frame.screen_ctrl_btn.lift()

    elif not text:
        CTkMessagebox(root, title='Warning', message='Textbox is Empty!')
        root.result_frame.set_innerframe_to_default()
    else:
        CTkMessagebox(root, title='Warning', message='Invalid Input!')
        root.result_frame.set_innerframe_to_default()


def more_info(root, data, calculations):
    top = ctk.CTkToplevel()
    top.geometry('600x600+600+50')
    top.title('More Info...')
    top.grab_set()
    top.resizable(False, False)
    top.protocol("WM_DELETE_WINDOW", lambda: close_top(root, top))
    mainframe = ctk.CTkScrollableFrame(top, fg_color='transparent')
    mainframe.pack(expand=True, fill='both')
    frame = ctk.CTkFrame(mainframe)
    frame.pack(expand=True, ipadx=10, ipady=10)

    ct = calculations['central tendency']
    mean = ct['mean']
    median = ct['median']

    root.result_frame.histplot_fig, ax2 = plt.subplots()
    sns.histplot(data, ax=ax2)
    ax2.set_title("Histogram Visualization")
    ax2.set_ylabel("Frequency")
    ax2.set_xlabel("Values")
    ax2.axvline(mean, color='red', linestyle='dashed', linewidth=1.5, label='mean')
    ax2.axvline(median, color='green', linestyle='dashed', linewidth=1.5, label='median')
    if root.selected_mode is not None:
        ax2.axvline(root.selected_mode, color='purple', linestyle='dashed', linewidth=1.5, label='mode')
    
    ax2.legend()

    canvas2 = FigureCanvasTkAgg(root.result_frame.histplot_fig, master=frame)
    canvas2.draw()
    canvas2.get_tk_widget().configure(width=500, height=400)
    canvas2.get_tk_widget().pack(pady=(40, 20))

    for k, v in calculations.items():
        if k != 'moment':
            title = ctk.CTkLabel(frame, text=k.title(), font=ctk.CTkFont(size=24, weight='bold'))
            title.pack(anchor=ctk.W, pady=(20, 10), ipadx=10)
            for key, val in v.items():
                label = ctk.CTkLabel(frame, text=f"{key}:  {val}", font=ctk.CTkFont(size=14))
                label.pack(anchor=ctk.W, padx=(30, 10))
        else:
            for key in ['skew', 'kurt']:
                label = ctk.CTkLabel(frame, text=f"Population {key}: {v[key]}", font=ctk.CTkFont(size=14))
                label.pack(anchor=ctk.W, padx=(30, 10))
                if (key == 'skew'):
                    label.pack_configure(pady=(50, 5))

def close_top(root, window):
    plt.close(root.result_frame.histplot_fig)
    window.grab_release()
    window.destroy()


def display_result(root, result, data):
    root.result_frame.kdeplot_fig, ax = plt.subplots()
    sns.kdeplot(data, ax=ax)
    ax.set_title("Skewness & Kurtosis")
    ax.set_ylabel("Frequency")
    ax.set_xlabel("Values")

    canvas = FigureCanvasTkAgg(root.result_frame.kdeplot_fig, master=result)
    canvas.draw()
    canvas.get_tk_widget().configure(width=500, height=400)
    canvas.get_tk_widget().pack(pady=(40, 20))

    skewness = skew(data)
    kurtosis = kurt(data)

    skew_frame = ctk.CTkFrame(result)
    skew_frame.pack(ipadx=10, ipady=10)
    skew_label = ctk.CTkLabel(skew_frame, text='Skewness:', font=ctk.CTkFont(size=24, weight='bold'))
    skew_label.pack(anchor='w', pady=(5, 10), padx=10)
    label_font = ctk.CTkFont(size=14)

    for k, v in skewness.items():
        if isinstance(v, dict) and v:
            first_key = list(v.keys())[0]
            label = ctk.CTkLabel(skew_frame, text=f'{k.title()}:   {v[first_key]}', font=label_font)

            mode_frame = ctk.CTkFrame(skew_frame, fg_color='transparent')
            mode_frame.pack(anchor='w')

            mode_label = ctk.CTkLabel(mode_frame, text='Select Mode:', font=label_font)
            mode_label.pack(side=ctk.LEFT, padx=(20, 10))

            modes_menu = ctk.CTkComboBox(mode_frame, width=100, values=[str(x) for x in v.keys()], state='readonly')
            modes_menu.pack(side=ctk.LEFT)
            modes_menu.set(str(first_key))
            if v:
                root.selected_mode = first_key

            def select_mode(e, label, k, v, root):
                label.configure(text=f'{k}: {v[float(e)]}')
                root.selected_mode = float(e)

            modes_menu.configure(command=lambda e, label=label, k=k, v=v, root=root: select_mode(e, label, k, v, root))
            label.pack(anchor='w', padx=20)
        else:
            val = 'No Modal' if isinstance(v, dict) and not v else v
            label = ctk.CTkLabel(skew_frame, text=f'{k.title()}:   {val}', font=label_font)
            label.pack(anchor='w', padx=20, pady=2)

    kurt_frame = ctk.CTkFrame(result)
    kurt_frame.pack(ipadx=10, ipady=10, pady=20)
    kurt_label = ctk.CTkLabel(kurt_frame, text='Kurtosis:', font=ctk.CTkFont(size=24, weight='bold'))
    kurt_label.pack(anchor='w', pady=(5, 10), padx=10)

    for k, v in kurtosis.items():
        label = ctk.CTkLabel(kurt_frame, text=f'{k}:   {v}', font=label_font)
        label.pack(anchor='w', padx=20, pady=2)

