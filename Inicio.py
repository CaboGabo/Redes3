from Usuario import *
from Principal import *

def insertar():
    usuario = Usuario()
    if(contra.get()==conf.get()):
        usuario.insertar(usr.get(),contra.get())
        usr.set("")
        contra.set("")
        conf.set("")
        messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente")
    else:
        usr.set("")
        contra.set("")
        conf.set("")
        messagebox.showerror("Registro fallido", "Contraseñas invalidas")

def iniciar():
    usuario = Usuario()
    if(usuario.login(usr.get(),contra.get())):
        Inicio.destroy()
        Principal(usr.get())
    else:
        messagebox.showerror("Login fallido", "Usuario o contraseña incorrecta")

def pestIniciarSesion():
    pes0 = ttk.Frame(notebook)
    notebook.add(pes0, text="Iniciar sesion")
    Label(pes0, text="Usuario:").place(x=80, y=50)
    Label(pes0, text="Contraseña: ").place(x=80, y=100)
    Entry(pes0, textvariable=usr).place(x=210, y=50)
    Entry(pes0, textvariable=contra, show='*').place(x=210, y=100)
    Button(pes0, text="Iniciar Sesion", command=iniciar).place(x=170, y=150)

def pestInsertarUsuario():
    pes0 = ttk.Frame(notebook)
    notebook.add(pes0,text="Insertar usuario")
    Label(pes0, text="Usuario:").place(x=80, y=50)
    Label(pes0, text="Contraseña:").place(x=80, y=100)
    Label(pes0, text="Confirmar contraseña:").place(x=80, y=150)
    Entry(pes0,textvariable=usr).place(x=210, y=50)
    Entry(pes0, textvariable=contra, show="*").place(x=210, y=100)
    Entry(pes0, textvariable=conf, show='*').place(x=210, y=150)
    Button(pes0,text="Guardar", command=insertar).place(x=170, y=200)



Inicio = Tk()
Inicio.title("Agregar nuevo usuario")
usr = StringVar()
contra = StringVar()
conf = StringVar()
notebook = ttk.Notebook(Inicio)
notebook.pack(fill='both', expand='yes')

pestIniciarSesion()
pestInsertarUsuario()

Inicio.geometry("400x350")
Inicio.mainloop()
