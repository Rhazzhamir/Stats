from typing import Optional, Tuple, Union
import customtkinter as ctk
import matplotlib.pyplot as plt
from data import DataScreen
from result import *
import os


class App(ctk.CTk):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.geometry('1000x620')
        self.minsize(1000, 620)
        self.title('Skewness and Kurtosis Calculator')
        self.selected_mode = None

        self.script_directory = os.path.dirname(os.path.realpath(__file__))
        self.iconpath = os.path.join(self.script_directory, 'icon.ico')
        self.iconbitmap(self.iconpath)

        self.data_frame = DataScreen(self, fg_color='transparent')
        self.result_frame = ResultScreen(self)

        self.data_frame.place(relx=0.05, rely=0, relwidth=0.4, relheight=1)
        self.result_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        self.data_frame.result_btn.configure(command=lambda: generate_result(self))
        self.data_frame.clear_btn.configure(command=lambda: clear_input(self))

    def close(self):
        if self.result_frame.kdeplot_fig:
            plt.close(self.result_frame.kdeplot_fig)
        self.destroy()
        self.quit()


if __name__ == '__main__':
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.close)
    app.mainloop()
