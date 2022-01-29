import os
import typing as t
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

from ffov import const
from ffov.setters import FovSetter


class Application:
    def __init__(self, *args, **kwargs):
        self.root = tk.Tk()
        self.setter: t.Optional[FovSetter] = None
    
    def setup(self):
        self.root.title("Fallout FOV setter")
        self.root.iconbitmap(const.ICON_PATH)
        self.root.resizable(0, 0)

        self.frame = tk.Frame(self.root)
        self.frame.grid(row=0, column=0, padx=10, pady=5)

        self.gamepath_label = ttk.Label(self.frame, text="Game path")
        self.gamepath_label.grid(row=0, column=0, padx=2)

        self.gamepath_var = tk.StringVar()
        self.gamepath_entry = ttk.Entry(
            self.frame,
            textvariable=self.gamepath_var,
            state=tk.DISABLED,
            width=40,
        )
        self.gamepath_entry.grid(row=0, column=1, padx=2)

        self.gamepath_button = ttk.Button(
            self.frame,
            text="...",
            command=self.on_gamepath_button_click,
            width=3,
        )
        self.gamepath_button.grid(row=0, column=2, padx=2)

        self.fov_label = ttk.Label(self.frame, text="1st person FOV")
        self.fov_label.grid(row=1, column=0, sticky=tk.W)
        self.fov_var = tk.IntVar(value=int(const.DEFAULT_FOV))
        self.fov_scale = ttk.Scale(
            self.frame,
            from_=50,
            to=120,
            orient=tk.HORIZONTAL,
            variable=self.fov_var,
            length=220,
            command=lambda _: self.fov_entry_var.set(str(self.fov_var.get()))
        )
        self.fov_scale.grid(row=1, column=1)
        self.fov_entry_var = tk.StringVar(value=str(const.DEFAULT_FOV))
        self.fov_entry = ttk.Entry(
            self.frame,
            textvariable=self.fov_entry_var,
            state=tk.DISABLED,
            width=4,
        )
        self.fov_entry.grid(row=1, column=2)

        self.pipfov_label = ttk.Label(self.frame, text="PipBoy FOV")
        self.pipfov_label.grid(row=2, column=0, sticky=tk.W)
        self.pipfov_var = tk.IntVar(value=int(const.DEFAULT_PIP_FOV))
        self.pipfov_scale = ttk.Scale(
            self.frame,
            from_=40,
            to=70,
            orient=tk.HORIZONTAL,
            variable=self.pipfov_var,
            length=220,
            command=lambda _: self.pipfov_entry_var.set(str(self.pipfov_var.get()))
        )
        self.pipfov_scale.grid(row=2, column=1)
        self.pipfov_entry_var = tk.StringVar(value=str(const.DEFAULT_PIP_FOV))
        self.pipfov_entry = ttk.Entry(
            self.frame,
            textvariable=self.pipfov_entry_var,
            state=tk.DISABLED,
            width=4,
        )
        self.pipfov_entry.grid(row=2, column=2)

        self.termfov_label = ttk.Label(self.frame, text="Terminal FOV")
        self.termfov_label.grid(row=3, column=0, sticky=tk.W)
        self.termfov_var = tk.DoubleVar(value=const.DEFAULT_TERM_FOV)
        self.termfov_scale = ttk.Scale(
            self.frame,
            from_=.05,
            to=.40,
            orient=tk.HORIZONTAL,
            variable=self.termfov_var,
            length=220,
            command=lambda _: self.termfov_entry_var.set("{:.2f}".format(self.termfov_var.get())),
        )
        self.termfov_scale.grid(row=3, column=1)
        self.termfov_entry_var = tk.StringVar(value=str(const.DEFAULT_TERM_FOV))
        self.termfov_entry = ttk.Entry(
            self.frame,
            textvariable=self.termfov_entry_var,
            state=tk.DISABLED,
            width=4
        )
        self.termfov_entry.grid(row=3, column=2)

        self.apply_button = ttk.Button(self.frame, text="Apply", command=self.on_apply_button_click)
        self.apply_button.grid(row=4, column=0, columnspan=3, sticky=tk.E)

    def teardown(self):
        pass

    def main(self) -> t.Tuple[t.Any, t.Any, t.Any]:
        setup = self.setup()
        main = self.root.mainloop()
        teardown = self.teardown()
        return setup, main, teardown
    
    @property
    def fov(self) -> float:
        return float(self.fov_entry_var.get())
    
    @property
    def pipfov(self) -> float:
        return float(self.pipfov_entry_var.get())
    
    @property
    def termfov(self) -> float:
        return float(self.termfov_entry_var.get())

    def on_gamepath_button_click(self):
        self.gamepath_var.set(filedialog.askdirectory())
        self.setter = None

        if not self.gamepath_var.get() or not os.path.isdir(self.gamepath_var.get()):
            messagebox.showerror("Error", "Invalid path")
            self.gamepath_var.set("")
            return
        
        for name in os.listdir(self.gamepath_var.get()):
            if FovSetter.getsetter(name):
                self.setter = FovSetter.getsetter(name)(self.gamepath_var.get())
                break
        
        if self.setter is None:
            messagebox.showerror("Error", "Game executable not found, please select correct game path")
            self.gamepath_var.set("")
            return
        
        fov, pipfov, termfov = self.setter.getfovs()
        self.fov_var.set(int(fov))
        self.fov_entry_var.set(str(fov))
        self.pipfov_var.set(int(pipfov))
        self.pipfov_entry_var.set(str(pipfov))
        self.termfov_var.set(termfov)
        self.termfov_entry_var.set(str(termfov))

    def on_apply_button_click(self):
        if not self.gamepath_var.get() or not os.path.isdir(self.gamepath_var.get()):
            messagebox.showwarning("Warning", "Game path isn't selected, can't apply changes")
            return
        
        self.setter.setfovs(self.fov, self.pipfov, self.termfov)
        messagebox.showinfo("Success", "FOV settings successfully applied")


if __name__ == "__main__":
    Application().main()
