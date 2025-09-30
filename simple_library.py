import tkinter as tk
from tkinter import messagebox

class Livro:
    def __init__(self, titulo: str, autor: str, book_id: int):
        self.titulo = titulo
        self.autor = autor
        self.book_id = book_id
        self.disponivel = True

    def __str__(self):
        status = "Disponível" if self.disponivel else "Emprestado"
        return f"ID: {self.book_id} | {self.titulo} por {self.autor} - {status}"

class Usuario:
    def __init__(self, nome: str, matricula: str):
        self.nome = nome
        self.matricula = matricula
        self.livros_emprestados = []

    def __str__(self):
        return f"{self.nome} (Matrícula: {self.matricula})"

class SimpleLibraryApp:
    def __init__(self, master):
        self.master = master
        master.title("Sistema de Biblioteca Simplificado (Sem ISBN)")

        self.livros = {}
        self.usuarios = {}
        self.next_book_id = 1

        # Frame para Livros
        self.book_frame = tk.LabelFrame(master, text="Livros")
        self.book_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(self.book_frame, text="Título:").grid(row=0, column=0, sticky="w")
        self.book_title_entry = tk.Entry(self.book_frame)
        self.book_title_entry.grid(row=0, column=1, sticky="ew")

        tk.Label(self.book_frame, text="Autor:").grid(row=1, column=0, sticky="w")
        self.book_author_entry = tk.Entry(self.book_frame)
        self.book_author_entry.grid(row=1, column=1, sticky="ew")

        tk.Button(self.book_frame, text="Adicionar Livro", command=self.add_book).grid(row=2, column=0, columnspan=2, pady=5)

        # Frame para Usuários
        self.user_frame = tk.LabelFrame(master, text="Usuários")
        self.user_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(self.user_frame, text="Nome:").grid(row=0, column=0, sticky="w")
        self.user_name_entry = tk.Entry(self.user_frame)
        self.user_name_entry.grid(row=0, column=1, sticky="ew")

        tk.Label(self.user_frame, text="Matrícula:").grid(row=1, column=0, sticky="w")
        self.user_id_entry = tk.Entry(self.user_frame)
        self.user_id_entry.grid(row=1, column=1, sticky="ew")

        tk.Button(self.user_frame, text="Adicionar Usuário", command=self.add_user).grid(row=2, column=0, columnspan=2, pady=5)

        # Frame para Empréstimos/Devoluções
        self.loan_frame = tk.LabelFrame(master, text="Empréstimo / Devolução")
        self.loan_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(self.loan_frame, text="ID do Livro:").grid(row=0, column=0, sticky="w")
        self.loan_book_id_entry = tk.Entry(self.loan_frame)
        self.loan_book_id_entry.grid(row=0, column=1, sticky="ew")

        tk.Label(self.loan_frame, text="Matrícula do Usuário:").grid(row=1, column=0, sticky="w")
        self.loan_user_id_entry = tk.Entry(self.loan_frame)
        self.loan_user_id_entry.grid(row=1, column=1, sticky="ew")

        tk.Button(self.loan_frame, text="Emprestar Livro", command=self.lend_book).grid(row=2, column=0, pady=5)
        tk.Button(self.loan_frame, text="Devolver Livro", command=self.return_book).grid(row=2, column=1, pady=5)

        # Listagem de Livros
        self.book_list_label = tk.Label(master, text="Livros Cadastrados:")
        self.book_list_label.pack(padx=10, pady=2, anchor="w")
        self.book_listbox = tk.Listbox(master, height=5)
        self.book_listbox.pack(padx=10, fill="both", expand=True)

        # Listagem de Usuários
        self.user_list_label = tk.Label(master, text="Usuários Cadastrados:")
        self.user_list_label.pack(padx=10, pady=2, anchor="w")
        self.user_listbox = tk.Listbox(master, height=5)
        self.user_listbox.pack(padx=10, fill="both", expand=True)

        self.update_lists()

    def add_book(self):
        title = self.book_title_entry.get()
        author = self.book_author_entry.get()

        if not all([title, author]):
            messagebox.showerror("Erro", "Título e Autor do livro são obrigatórios!")
            return

        new_book = Livro(title, author, self.next_book_id)
        self.livros[self.next_book_id] = new_book
        self.next_book_id += 1
        messagebox.showinfo("Sucesso", f"Livro \'{title}\' adicionado com sucesso com ID {new_book.book_id}!")
        self.clear_book_entries()
        self.update_lists()

    def clear_book_entries(self):
        self.book_title_entry.delete(0, tk.END)
        self.book_author_entry.delete(0, tk.END)

    def add_user(self):
        name = self.user_name_entry.get()
        matricula = self.user_id_entry.get()

        if not all([name, matricula]):
            messagebox.showerror("Erro", "Todos os campos do usuário são obrigatórios!")
            return

        if matricula in self.usuarios:
            messagebox.showerror("Erro", "Usuário com esta matrícula já cadastrado.")
            return

        new_user = Usuario(name, matricula)
        self.usuarios[matricula] = new_user
        messagebox.showinfo("Sucesso", f"Usuário \'{name}\' adicionado com sucesso!")
        self.clear_user_entries()
        self.update_lists()

    def clear_user_entries(self):
        self.user_name_entry.delete(0, tk.END)
        self.user_id_entry.delete(0, tk.END)

    def lend_book(self):
        try:
            book_id = int(self.loan_book_id_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "ID do Livro deve ser um número.")
            return
        matricula = self.loan_user_id_entry.get()

        book = self.livros.get(book_id)
        user = self.usuarios.get(matricula)

        if not book:
            messagebox.showerror("Erro", "Livro não encontrado.")
            return
        if not user:
            messagebox.showerror("Erro", "Usuário não encontrado.")
            return

        if book.disponivel:
            book.disponivel = False
            user.livros_emprestados.append(book)
            messagebox.showinfo("Sucesso", f"Livro \'{book.titulo}\' emprestado para \'{user.nome}\'")
        else:
            messagebox.showwarning("Aviso", f"Livro \'{book.titulo}\' não está disponível.")
        self.clear_loan_entries()
        self.update_lists()

    def return_book(self):
        try:
            book_id = int(self.loan_book_id_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "ID do Livro deve ser um número.")
            return
        matricula = self.loan_user_id_entry.get()

        book = self.livros.get(book_id)
        user = self.usuarios.get(matricula)

        if not book:
            messagebox.showerror("Erro", "Livro não encontrado.")
            return
        if not user:
            messagebox.showerror("Erro", "Usuário não encontrado.")
            return

        if book in user.livros_emprestados:
            book.disponivel = True
            user.livros_emprestados.remove(book)
            messagebox.showinfo("Sucesso", f"Livro \'{book.titulo}\' devolvido por \'{user.nome}\'")
        else:
            messagebox.showwarning("Aviso", f"Livro \'{book.titulo}\' não foi emprestado para \'{user.nome}\' ou já está disponível.")
        self.clear_loan_entries()
        self.update_lists()

    def clear_loan_entries(self):
        self.loan_book_id_entry.delete(0, tk.END)
        self.loan_user_id_entry.delete(0, tk.END)

    def update_lists(self):
        self.book_listbox.delete(0, tk.END)
        for book in self.livros.values():
            self.book_listbox.insert(tk.END, str(book))

        self.user_listbox.delete(0, tk.END)
        for user in self.usuarios.values():
            self.user_listbox.insert(tk.END, str(user))

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleLibraryApp(root)
    root.mainloop()
