import tkinter as tk
import fantasy_stat

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.write = tk.Button(self)
        self.write["text"] = "Write stats to\nfantasy_stat.csv"
        self.write["command"] = fantasy_stat.write_stats()
        self.write.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

root = tk.Tk()
app = Application(master=root)
app.mainloop()