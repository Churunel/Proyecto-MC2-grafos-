from tkinter import *
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.colors as mcolors
from collections import deque

# Configuración de la ventana principal
raiz = Tk()
raiz.title("Proyecto de MC2")
window_width = 1080
window_height = 700
raiz.geometry(f"{window_width}x{window_height}")

#icono = PhotoImage(file="icono.png")  # Reemplaza con la ruta de tu archivo
#raiz.iconphoto(False, icono)

# Canvas principal
canvas = Canvas(raiz, width=window_width, height=window_height, bg='green')
canvas.pack(fill="both", expand=True)
miFrame = Frame(canvas, width=window_width, height=window_height, bg="green")
miFrame.place(x=0, y=0)

# Estilo de botones y etiquetas
style = ttk.Style()
style.configure("Rounded.TButton", background="#87ceeb", foreground="black", borderwidth=0, relief="flat")
style.configure("Rounded.TLabel", background="#87ceeb", foreground="black", borderwidth=2, relief="flat")

# Variables
verticeNuevo = StringVar()
verticeSalida = StringVar()
verticeLlegada = StringVar()
ordenVisita = StringVar()
ordenVisitaProfundidad = StringVar()
ListaVertices = []
G = nx.Graph()

# Funciones principales
def AgregarVertice():
    verticeNuevoValor = verticeNuevo.get().upper()
    if verticeNuevoValor and verticeNuevoValor not in ListaVertices:
        ListaVertices.append(verticeNuevoValor)
        G.add_node(verticeNuevoValor)
        verticeNuevo.set("")
        CampoVertices.delete("1.0", END)
        for i in ListaVertices:
            CampoVertices.insert(END, f"{i}\n")

def AgregarArista():
    verticeSalidaNuevo = verticeSalida.get().upper()
    verticeLlegadaNuevo = verticeLlegada.get().upper()
    if verticeSalidaNuevo in ListaVertices and verticeLlegadaNuevo in ListaVertices and verticeSalidaNuevo != verticeLlegadaNuevo:
        G.add_edge(verticeSalidaNuevo, verticeLlegadaNuevo)
        verticeSalida.set("")
        verticeLlegada.set("")
        graficar_grafo(G, None, 40)

def color_degradado(num_nodos, total_nodos):
    # color de cmap orange
    cmap = plt.cm.get_cmap('Oranges')
    # cmap = plt.cm.Oranges
    norm = mcolors.Normalize(vmin=0, vmax=total_nodos - 1)
    return cmap(norm(num_nodos))

def BusquedaAncho(grafo, inicio):
    queue = deque([inicio])
    visited = set()
    order = []
    while queue:
        node = queue.popleft()
        if node not in visited:
            order.append(node)
            visited.add(node)
            neighbors = sorted(grafo.neighbors(node))
            queue.extend(neighbors)
    return order

def BusquedaProfundidad(grafo, inicio):
    stack = [inicio]
    visited = set()
    order = []
    while stack:
        node = stack.pop()
        if node not in visited:
            order.append(node)
            visited.add(node)
            neighbors = sorted(grafo.neighbors(node), reverse=True)
            stack.extend(neighbors)
    return order

def graficar_grafo(grafo, order=None, posY=None):
    pos = nx.planar_layout(grafo)
    fig, ax = plt.subplots(figsize=(4, 3))
    node_colors = [color_degradado(i, len(grafo)) for i in range(len(grafo))]
    nx.draw(grafo, pos, ax=ax, with_labels=True, node_color='lightblue', edge_color='gray', node_size=600, font_size=8)
    if order:
        for i in range(len(order)):
            nx.draw_networkx_nodes(grafo, pos, nodelist=[order[i]], node_color=[node_colors[i]], ax=ax)
        for i in range(len(order)-1):
            if (order[i], order[i + 1]) in grafo.edges or (order[i + 1], order[i]) in grafo.edges:
                nx.draw_networkx_edges(grafo, pos, edgelist=[(order[i], order[i + 1])], width=1, edge_color='r', style='dashed', ax=ax)
            
            #nx.draw_networkx_edges(grafo, pos, edgelist=[(order[i], order[i+1])], width=2, edge_color='r', style='dashed', ax=ax)
    canvas_fig = FigureCanvasTkAgg(fig, master=miFrame)
    canvas_fig.draw()
    canvas_fig.get_tk_widget().place(x=640, y=posY)

def iniciar_busqueda_ancho():
    if ListaVertices:
        order = BusquedaAncho(G, ListaVertices[0])
        ordenVisita.set(", ".join(order))
        graficar_grafo(G, order, 370)

def iniciar_busqueda_profundidad():
    if ListaVertices:
        order = BusquedaProfundidad(G, ListaVertices[0])
        ordenVisitaProfundidad.set(", ".join(order))
        graficar_grafo(G, order, 370)

# Elementos de la interfaz
Entry(miFrame, textvariable=verticeNuevo, bg="#9370DB").place(x=250, y=50, width=150)
ttk.Label(miFrame, text="Coloca la etiqueta para un vértice:", style="Rounded.TLabel").place(x=50, y=50)
ttk.Button(miFrame, text="Guardar Vértice", command=AgregarVertice, style="Rounded.TButton").place(x=420, y=40, width=150, height=40)
CampoVertices = Text(miFrame, width=16, height=6)
CampoVertices.place(x=250, y=100)
ttk.Label(miFrame, text="Vértices disponibles:", style="Rounded.TLabel").place(x=50, y=100)

Entry(miFrame, textvariable=verticeSalida, bg="#9370DB").place(x=250, y=220, width=150)
ttk.Label(miFrame, text="Vértice de salida:", style="Rounded.TLabel").place(x=50, y=220)
Entry(miFrame, textvariable=verticeLlegada, bg="#9370DB").place(x=250, y=250, width=150)
ttk.Label(miFrame, text="Vértice de llegada:", style="Rounded.TLabel").place(x=50, y=250)
ttk.Button(miFrame, text="Guardar Arista", command=AgregarArista, style="Rounded.TButton").place(x=420, y=225, width=150, height=40)

# Botones de búsqueda y etiquetas de resultado
ttk.Button(miFrame, text="Búsqueda a lo Ancho", command=iniciar_busqueda_ancho, style="Rounded.TButton").place(x=250, y=320, width=150, height=40)
ttk.Label(miFrame, textvariable=ordenVisita, style="Rounded.TLabel").place(x=420, y=320)

ttk.Button(miFrame, text="Búsqueda a lo Profundo", command=iniciar_busqueda_profundidad, style="Rounded.TButton").place(x=250, y=370, width=150, height=40)
ttk.Label(miFrame, textvariable=ordenVisitaProfundidad, style="Rounded.TLabel").place(x=420, y=370)

#------------------- LÍNEAS DIVISORIAS ------------------------
ttk.Separator(miFrame, orient='vertical').place(x=600, y=0, relheight=80)  # Línea vertical divisoria
# ttk.Separator(miFrame, orient='horizontal').place(x=0, y=250, relwidth=1)  # Línea horizontal divisoria


raiz.mainloop()
