from tkinter import *

class Application:
    def __init__(self, title, dimensions):
        self._current_page = 0
        self._pages = [] # changed from {} to []
        self._pages_names = []
        self.master = Tk()
        self.master.title(title)
        self.master.geometry(dimensions)
        self.width = int(dimensions.split('x')[0])
        self.height = int(dimensions.split('x')[1])
    
    def add_page(self, page, pageName):
        self._pages.append(page)
        self._pages_names.append(pageName)

    def clear_pages(self):
        for frame in self.master.winfo_children():
            frame.pack_forget()

    def start_app(self):
        if len(self._pages) < 1:
            print("WARNING: NO PAGES ADDED TO APPLICATION\nCANNOT START")
        else:
            self.set_Page(self._current_page)
            self.master.mainloop()

    def set_Page(self, window):
        self.clear_pages()
        if type(window) == int:
            index = window
        if window in self._pages_names:
            index = self._pages_names.index(window)
            
        page = self._pages[index]
        page.enter()
        c_frame = page._frame
        c_frame.master = self.master
        c_frame.pack(fill="both",expand=True)
        
    def error_page(self, error):
        self.clear_pages()
        output = Frame(self.master)
        output.config(background="#614f4f")

        #back button
        out_button = Button(output, text="back", command=lambda: self.set_Frame(self._current_page))
        out_button.config(
            font=('Helvetica',10),
            width=4,
            height=1)
        out_button.place(x=5,y=5)

        #error title
        out_title = Label(output, text="ERROR")
        out_title.config(
            font=('Helvetica',40),
            bg="#614f4f",
            fg="white")
        out_title.pack(pady=50)

        #error description
        out_text = Label(output, text=error)
        out_text.config(
            font=('Helvetica',15),
            bg="#614f4f",
            fg="white",
            wraplength=self.width*0.9)
        out_text.pack()

        #final push of pages
        output.pack(fill="both", expand=True)
        
class Page:
    def __init__(self,application):
        self.onEnter = lambda:print("")
        self._frame = Frame(bg="pink")
        self._vars = {}
        self._reloading = False
        self._entering = True
        self._app = application
        self._promised_frame = lambda:Frame()

    def enter(self):
        self.onEnter()
        self._frame = self._promised_frame()
        self._entering = False

    def reload(self):
        if not self._reloading:
            self._reloading = True
            self._frame = self._promised_frame()
            self._reloading = False
            self._app.clear_pages()
            c_frame = self._frame
            c_frame.master = self._app.master
            c_frame.pack(fill="both",expand=True)

    def set_var(self, name, value):
        self._vars[name] = value
        #print('variable "' + name + '" has been set to [' + str(value) + ']')
        if not self._entering:
            self.reload()

    def get_var(self, name):
        try:
            return self._vars[name]
        except:
            return None
        
    def set_frame(self, frm):
        if callable(frm):
            self._promised_frame = frm
        else:
            print("set_frame() must take a function")
