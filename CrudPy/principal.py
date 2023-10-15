from tkinter import *
from database import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog  # Agrega esta línea


class App:
    def __init__(self, master):
        self.frame = master
        self.DrawLabel()
        self.DrawEntry()
        self.DrawButtons()
        # self.loadImage()  # Commented out as the method is not defined
        self.DrawList()
        self.data = Data()  # Crea una instancia de la clase Data

    def DrawLabel(self):
        self.lbl_ed = Label(
            self.frame, foreground="white", font=(8), background="#314252", text="Edad"
        ).place(x=40, y=110)
        self.lbl_ent = Label(
            self.frame,
            foreground="white",
            font=(8),
            background="#314252",
            text="Entubado",
        ).place(x=40, y=160)
        self.lbl_neu = Label(
            self.frame,
            foreground="white",
            font=(8),
            background="#314252",
            text="Neumonia",
        ).place(x=40, y=210)

    def DrawEntry(self):
        self.ed = StringVar()
        self.ent = StringVar()
        self.neu = StringVar()
        self.txt_ed = Entry(
            self.frame,
            font=("Arial", 12),
            relief="flat",
            background="#E7E7E7",
            textvariable=self.ed,
        ).place(x=140, y=110, height=25, width=150)
        self.txt_ent = Entry(
            self.frame,
            font=("Arial", 12),
            relief="flat",
            background="#E7E7E7",
            textvariable=self.ent,
        ).place(x=140, y=160, height=25, width=150)
        self.txt_neu = Entry(
            self.frame,
            font=("Arial", 12),
            relief="flat",
            background="#E7E7E7",
            textvariable=self.neu,
        ).place(x=140, y=210, height=25, width=150)

    def DrawButtons(self):
        self.btn_confirm = Button(
            self.frame,
            foreground="white",
            text="Guardar",
            borderwidth=2,
            relief="flat",
            cursor="hand1",
            overrelief="raise",
            background="#3CFF33",
            command=lambda: self.confirmProcess(),
        ).place(x=350, y=340, width=90)
        self.btn_cancel = Button(
            self.frame,
            text="Cancelar",
            foreground="white",
            borderwidth=2,
            relief="flat",
            cursor="hand1",
            overrelief="raise",
            background="#E81123",
            command=lambda: self.canceProcess(),
        ).place(x=550, y=340, width=90)
        self.btn_import = Button(
            self.frame,
            foreground="white",
            text="Importar",
            borderwidth=2,
            relief="flat",
            cursor="hand1",
            overrelief="raise",
            background="#3CFF33",
            command=lambda: self.importFile(),
        ).place(x=650, y=340, width=90)

    def DrawList(self):
        self.list_elements = ttk.Treeview(
            self.frame, columns=(1, 2, 3), show="headings", height="8"
        )

        # --- STYLE ---
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview.Heading", background="#FF5B33", relief="flat", foreground="white"
        )
        style.map(
            "Treeview",
            background=[("selected", "yellow")],
            foreground=[("selected", "black")],
        )

        # --- Event ---
        self.list_elements.bind("<Double 1>", self.getRow)
        # ---- end ---

        self.list_elements.heading(1, text="ed")
        self.list_elements.heading(2, text="ent")
        self.list_elements.heading(3, text="neu")
        self.list_elements.column(1, anchor=CENTER)
        self.list_elements.column(2, anchor=CENTER)
        self.list_elements.column(3, anchor=CENTER)

        # -- FILL LIST --
        # Assuming Data class is defined elsewhere in your code
        d = Data()
        self.rows = d.returnAllElements()
        for i in self.rows:
            self.list_elements.insert("", "end", values=i)
        # ----- end -----5

        self.list_elements.place(x=340, y=90)

    def getRow(self, event):
        ed = StringVar()
        ent = StringVar()
        neu = StringVar()
        rowName = self.list_elements.identify_row(event.y)
        item = self.list_elements.item(self.list_elements.focus())
        n = item["values"][0]
        e = item["values"][1]
        c = item["values"][2]
        ed.set(n)
        ent.set(e)
        neu.set(c)
        pop = Toplevel(self.frame)
        pop.geometry("400x200")
        lbl_n = Entry(pop, textvariable=ed).place(x=40, y=40)
        lbl_e = Entry(pop, textvariable=ent).place(x=40, y=80)
        lbl_c = Entry(pop, textvariable=neu).place(x=40, y=120)
        btn_change = Button(
            pop,
            text="Actualizar",
            relief="flat",
            background="#00CE54",
            foreground="white",
            command=lambda: self.editar(n, ed.get(), ent.get(), neu.get()),
        ).place(x=180, y=160, width=90)
        btn_delete = Button(
            pop,
            text="Eliminar",
            relief="flat",
            background="red",
            foreground="white",
            command=lambda: self.eliminar(n),
        ).place(x=290, y=160, width=90)

    def eliminar(self, n):
        # Assuming Data class is defined elsewhere in your code
        d = Data()
        d.Delete(n)
        messagebox.showinfo(title="Actualizacion", message="Se han eliminado los datos")
        self.ClearList()
        self.DrawList()
        self.ClearEntry()

    def editar(self, n, ed, ent, neu):
        arr = [ed, ent, neu]
        # Assuming Data class is defined elsewhere in your code
        d = Data()
        d.UpdateItem(arr, n)
        messagebox.showinfo(
            title="Actualizacion", message="Se han actualizado los datos"
        )
        self.ClearList()
        self.DrawList()
        self.ClearEntry()

    def ClearList(self):
        self.list_elements.delete(*self.list_elements.get_children())

    def cancelProcess(self):
        self.ClearEntry()

    def ClearEntry(self):
        self.ed.set()
        self.ent.set()
        self.neu.set("")

    def confirmProcess(self):
        if self.ed.get() != "" and self.ent.get() != "" and self.neu.get() != "":
            # Assuming Data class is defined elsewhere in your code
            d = Data()
            arr = [self.ed.get(), self.ent.get(), self.neu.get()]
            d.InsertItems(arr)
            messagebox.showinfo(title="Alerta", message="Se inserto correctamente!")
            self.ClearList()
            self.DrawList()
            self.ClearEntry()
        else:
            messagebox.showinfo(
                title="Error", message="Debe llenar los campos para poder guardar!"
            )

    # Agregar estos métodos con la indentación correcta
    def exportFile(self):
        filename = filedialog.asksaveasfilename()
        if filename:
            self.data.exportData(filename)

    def importFile(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.data.importData(filename)


root = Tk()
root.title("CRUD")
root.config(background="#314252")
root.geometry("1000x400")
application = App(root)
root.mainloop()
