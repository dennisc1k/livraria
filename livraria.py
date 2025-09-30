import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Lista para armazenar os livros
catalogo = []

# Função para adicionar livro
def adicionar_livro():
    titulo = entrada_titulo.get()
    autor = entrada_autor.get()
    ano = entrada_ano.get()

    if titulo and autor and ano:
        livro = {"Título": titulo, "Autor": autor, "Ano": ano}
        catalogo.append(livro)
        atualizar_treeview(catalogo)
        entrada_titulo.delete(0, tk.END)
        entrada_autor.delete(0, tk.END)
        entrada_ano.delete(0, tk.END)
    else:
        messagebox.showwarning("Campos vazios", "Preencha todos os campos.")

# Função para atualizar a Treeview
def atualizar_treeview(lista):
    for item in tree.get_children():
        tree.delete(item)
    for livro in lista:
        tree.insert("", tk.END, values=(livro["Título"], livro["Autor"], livro["Ano"]))

# Função de pesquisa
def pesquisar():
    termo = entrada_pesquisa.get().lower()
    resultados = [livro for livro in catalogo if termo in livro["Título"].lower() or termo in livro["Autor"].lower()]
    atualizar_treeview(resultados)

# Funções de ordenação
def ordenar_por_titulo():
    catalogo.sort(key=lambda x: x["Título"])
    atualizar_treeview(catalogo)

def ordenar_por_autor():
    catalogo.sort(key=lambda x: x["Autor"])
    atualizar_treeview(catalogo)

# Função para remover livro
def remover_livro():
    selecionado = tree.selection()
    if selecionado:
        valores = tree.item(selecionado)["values"]
        for livro in catalogo:
            if livro["Título"] == valores[0] and livro["Autor"] == valores[1] and livro["Ano"] == valores[2]:
                catalogo.remove(livro)
                break
        atualizar_treeview(catalogo)
    else:
        messagebox.showerror("Erro", "Selecione um livro para remover.")

# Criar janela principal
janela = tk.Tk()
janela.title("Sistema de livraria")

# Labels e Entradas
tk.Label(janela, text="Título:").grid(row=0, column=0, sticky="w")
entrada_titulo = tk.Entry(janela)
entrada_titulo.grid(row=0, column=1)

tk.Label(janela, text="Autor:").grid(row=1, column=0, sticky="w")
entrada_autor = tk.Entry(janela)
entrada_autor.grid(row=1, column=1)

tk.Label(janela, text="Ano:").grid(row=2, column=0, sticky="w")
entrada_ano = tk.Entry(janela)
entrada_ano.grid(row=2, column=1)

# Botão Adicionar
btn_adicionar = tk.Button(janela, text="Adicionar livro", command=adicionar_livro)
btn_adicionar.grid(row=3, column=0, columnspan=2, pady=5)

# Treeview
tree = ttk.Treeview(janela, columns=("Título", "Autor", "Ano"), show="headings")
tree.heading("Título", text="Título")
tree.heading("Autor", text="Autor")
tree.heading("Ano", text="Ano")
tree.grid(row=4, column=0, columnspan=2, pady=10)

# Campo de pesquisa
tk.Label(janela, text="Pesquisar:").grid(row=5, column=0, sticky="w")
entrada_pesquisa = tk.Entry(janela)
entrada_pesquisa.grid(row=5, column=1)

btn_pesquisar = tk.Button(janela, text="Pesquisar", command=pesquisar)
btn_pesquisar.grid(row=6, column=0, columnspan=2, pady=5)

# Botões de ordenação
btn_ordenar_autor = tk.Button(janela, text="Classificar por autor", command=ordenar_por_autor)
btn_ordenar_autor.grid(row=7, column=0)

btn_ordenar_titulo = tk.Button(janela, text="Classificar por título", command=ordenar_por_titulo)
btn_ordenar_titulo.grid(row=7, column=1)

# Botão de remoção
btn_remover = tk.Button(janela, text="Remover livro", command=remover_livro)
btn_remover.grid(row=8, column=0, columnspan=2, pady=5)

# Executar aplicativo
janela.mainloop()
