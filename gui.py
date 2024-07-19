#Cadastro de EPI's
#Aluno: Pablo Ramon Galdino Barros RU: 4623803
import shutil
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from database import add_epi, get_epis, add_entrega, get_entregas, remove_epi
from reports import gerar_relatorio_entregas, gerar_relatorio_epis
from tkinter import font as tkfont
import datetime
import os

class EpiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Equipamentos de Segurança")
        self.root.geometry("1900x720")
        self.default_font = tkfont.Font(family="Roboto-Medium", size=11)
        self.root.option_add("*Font", self.default_font)

        self.search_query = ""
        self.sort_column = None
        self.sort_order = None

        self.create_widgets()
        self.refresh_epi_list()

    def create_widgets(self):
        self.tabs = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tab3 = ttk.Frame(self.tabs)
        self.tabs.add(self.tab1, text='Cadastrar EPI')
        self.tabs.add(self.tab2, text='Lista de EPIs')
        self.tabs.add(self.tab3, text='Entrega e Histórico de Entregas')
        self.tabs.pack(expand=1, fill="both")

        self.create_add_epi_widgets()
        self.create_manage_epi_widgets()
        self.create_entrega_widgets()

    def create_add_epi_widgets(self):
        self.add_frame = ttk.LabelFrame(self.tab1, text="Adicionar Novo EPI")
        self.add_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(self.add_frame, text="Nome:").grid(row=0, column=0, padx=10, pady=5)
        self.nome_entry = ttk.Entry(self.add_frame)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.add_frame, text="Descrição:").grid(row=1, column=0, padx=10, pady=5)
        self.descricao_entry = ttk.Entry(self.add_frame)
        self.descricao_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.add_frame, text="Marca:").grid(row=2, column=0, padx=10, pady=5)
        self.marca_entry = ttk.Entry(self.add_frame)
        self.marca_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self.add_frame, text="C.A.:").grid(row=3, column=0, padx=10, pady=5)
        self.ca_entry = ttk.Entry(self.add_frame)
        self.ca_entry.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(self.add_frame, text="Validade:").grid(row=4, column=0, padx=10, pady=5)
        self.validade_entry = DateEntry(self.add_frame, date_pattern='dd/MM/yyyy')
        self.validade_entry.grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(self.add_frame, text="Quantidade:").grid(row=5, column=0, padx=10, pady=5)
        self.quantidade_a_cadastrar_entry = ttk.Entry(self.add_frame)
        self.quantidade_a_cadastrar_entry.grid(row=5, column=1, padx=10, pady=5)

        ttk.Label(self.add_frame, text="Imagem:").grid(row=6, column=0, padx=10, pady=5)
        self.image_path_entry = ttk.Entry(self.add_frame, state='readonly')
        self.image_path_entry.grid(row=6, column=1, padx=10, pady=5)

        self.upload_button = ttk.Button(self.add_frame, text="Upload Imagem", command=self.upload_image)
        self.upload_button.grid(row=6, column=2, padx=10, pady=5)

        self.add_button = ttk.Button(self.add_frame, text="Adicionar EPI", command=self.add_epi)
        self.add_button.grid(row=7, column=0, columnspan=3, pady=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.image_path_entry.config(state='normal')
            self.image_path_entry.delete(0, tk.END)
            self.image_path_entry.insert(0, file_path)
            self.image_path_entry.config(state='readonly')

    def view_image(self):
        selecionar_item = self.epi_table.selection()
        if selecionar_item:
            image_path = self.epi_table.item(selecionar_item, 'values')[7]
            if image_path and os.path.exists(image_path):
                self.show_image(image_path)
            else:
                messagebox.showerror("Erro", "Imagem não encontrada ou não cadastrada.")
        else:
            messagebox.showerror("Erro", "Selecione um dos EPI's cadastrados para visualizar a imagem.")

    def show_image(self, image_path):
        window = tk.Toplevel(self.root)
        window.title = "Vizualizar imagem"

        image = Image.open(image_path)
        image.thumbnail((600, 600))
        photo = ImageTk.PhotoImage(image)

        label = ttk.Label(window, image=photo)
        label.image = photo #Mantém uma referência para evitar coleta de lixo
        label.pack(padx=10, pady=10)

        close_button = ttk.Button(window, text="Fechar", command=window.destroy)
        close_button.pack(pady=10)

    def add_epi(self):
        nome = self.nome_entry.get().strip().upper()
        descricao = self.descricao_entry.get().strip().upper()
        marca = self.marca_entry.get().strip().upper()
        ca = self.ca_entry.get()
        validade = self.validade_entry.get()
        quantidade_a_cadastrar = self.quantidade_a_cadastrar_entry.get().strip().upper()
        image_path = self.image_path_entry.get()

        if nome and descricao and marca and ca and validade and quantidade_a_cadastrar:
            try:
                quantidade_a_cadastrar = int(quantidade_a_cadastrar)
                if image_path:
                    if not os.path.exists('Imagens'):
                        os.makedirs('Imagens')
                    image_dest = os.path.join('Imagens', os.path.basename(image_path))
                    shutil.copy(image_path, image_dest)
                else:
                    image_dest = ''
                add_epi(nome, descricao, marca, ca, validade, quantidade_a_cadastrar, image_path)
                messagebox.showinfo("Sucesso", "EPI adicionado com sucesso!")
                self.clear_add_epi_fields()
                self.refresh_epi_list()
            except ValueError:
                messagebox.showerror("Erro", "Quantidade à cadastrar deve ser um número.")
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showerror("Erro", "Preencha todos os campos!")

    def clear_add_epi_fields(self):
        self.nome_entry.delete(0, tk.END)
        self.descricao_entry.delete(0, tk.END)
        self.marca_entry.delete(0, tk.END)
        self.ca_entry.delete(0, tk.END)
        self.validade_entry.set_date(datetime.datetime.now())
        self.quantidade_a_cadastrar_entry.delete(0, tk.END)
        self.image_path_entry.delete(0, tk.END)

    def refresh_epi_list(self):
        for widget in self.tab2.winfo_children():
            widget.destroy()

        search_frame = ttk.Frame(self.tab2)
        search_frame.pack(pady=10)

        search_label = ttk.Label(search_frame, text="Buscar")
        search_label.pack(side="left", padx=5)

        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5)

        search_button = ttk.Button(search_frame, text="Buscar", command=self.search_epi)
        search_button.pack(side="left", padx=5)

        epis = get_epis()
        if self.search_query:
            epis = [epi for epi in epis if self.search_query.upper() in epi[1].upper() or self.search_query.upper() in epi[2].upper()]

        if self.sort_column is not None:
            epis.sort(key=lambda x: x[self.sort_column], reverse=self.sort_order == "desc")

        columns = ("ID", "Nome", "Descrição", "Marca", "C.A.", "Validade", "Estoque", "Imagem")
        self.epi_table = ttk.Treeview(self.tab2, columns=columns, show="headings")
        self.epi_table.tag_configure('vencido', background='red')
        #self.epi_table.tag_configure('valido', background='green')#Exibe verde / dentro da validade
        for col in columns:
            self.epi_table.heading(col, text=col, command=lambda c=col: self.sort_by(c))
        self.epi_table.pack(fill="both", expand=True)

        for epi in epis:
            validade = datetime.datetime.strptime(epi[5], '%d/%m/%Y')
            tag = 'valido' if validade >= datetime.datetime.now() else 'vencido'
            self.epi_table.insert('', 'end', values=(epi[0], epi[1], epi[2], epi[3], epi[4], epi[5], epi[6], epi[7]),
                                  tags=(tag,))

        self.relatorio_button = ttk.Button(self.tab2, text="Gerar Relatório EPIs", command=self.gerar_relatorio_epis)
        self.relatorio_button.pack(pady=10)

        self.remover_button = ttk.Button(self.tab2, text="Remover EPI Selecionado", command=self.remover_epi)
        self.remover_button.pack(pady=10)

        self.view_image_button = ttk.Button(self.tab2, text="Visualizar Imagem", command=self.view_image)
        self.view_image_button.pack(pady=10)

    def search_epi(self):
        self.search_query = self.search_entry.get().strip().upper()
        self.refresh_epi_list()

    def sort_by(self, column):
        column_index = ["ID", "Nome", "Descrição", "Marca", "C.A.", "Validade", "Estoque", "Imagem"].index(column)
        if self.sort_column == column_index:
            self.sort_order = "asc" if self.sort_order == "desc" else "desc"
        else:
            self.sort_column = column_index
            self.sort_order = "asc"
        self.refresh_epi_list()



    def remover_epi(self):
        selected_item = self.epi_table.selection()
        if selected_item:
            epi_id = self.epi_table.item(selected_item, 'values')[0]
            response = messagebox.askyesno("Confirmação", "Tem certeza que quer remover o EPI selecionado?")
            if response:
                try:
                    remove_epi(epi_id)
                    messagebox.showinfo("Sucesso", "EPI removido com sucesso!")
                    self.refresh_epi_list()
                except Exception as e:
                    messagebox.showerror("Erro", str(e))
        else:
            messagebox.showerror("Erro", "Selecione um EPI para remover!")


    def create_manage_epi_widgets(self):
        self.manage_frame = ttk.LabelFrame(self.tab2, text="Lista de EPI's")
        self.manage_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(self.manage_frame, text="ID:").grid(row=0, column=0, padx=10, pady=5)
        self.manage_id_entry = ttk.Entry(self.manage_frame)
        self.manage_id_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.manage_frame, text="Unidade:").grid(row=1, column=0, padx=10, pady=5)
        self.manage_unidade_entry = ttk.Entry(self.manage_frame)
        self.manage_unidade_entry.grid(row=1, column=1, padx=10, pady=5)

        self.update_button = ttk.Button(self.manage_frame, text="Adicionar Unidade", command=self.update_epi)
        self.update_button.grid(row=2, column=0, columnspan=2, pady=10)

    def update_epi(self):
        id = self.manage_id_entry.get()
        unidade = self.manage_unidade_entry.get()

        if id and unidade:
            try:
                conn = sqlite3.connect('epi_database.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE epi SET unidade = unidade + ? WHERE id = ?", (unidade, id))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Unidade adicionado com sucesso!")
                self.refresh_epi_list()
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showerror("Erro", "Preencha todos os campos!")

    def create_entrega_widgets(self):
        self.entrega_frame = ttk.LabelFrame(self.tab3, text="Registrar Entrega de EPI")
        self.entrega_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(self.entrega_frame, text="EPI ID:").grid(row=0, column=0, padx=10, pady=5)
        self.entrega_epi_id_entry = ttk.Entry(self.entrega_frame)
        self.entrega_epi_id_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.entrega_frame, text="Data da Entrega:").grid(row=1, column=0, padx=10, pady=5)
        self.entrega_data_entry = DateEntry(self.entrega_frame, date_pattern='dd/MM/yyyy')
        self.entrega_data_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.entrega_frame, text="Setor:").grid(row=2, column=0, padx=10, pady=5)
        self.entrega_setor_entry = ttk.Entry(self.entrega_frame)
        self.entrega_setor_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self.entrega_frame, text="Quantidade:").grid(row=3, column=0, padx=10, pady=5)
        self.entrega_quantidade_entry = ttk.Entry(self.entrega_frame)
        self.entrega_quantidade_entry.grid(row=3, column=1, padx=10, pady=5)

        self.entrega_button = ttk.Button(self.entrega_frame, text="Registrar Entrega", command=self.registrar_entrega)
        self.entrega_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.relatorio_button = ttk.Button(self.tab3, text="Gerar Relatório", command=self.gerar_relatorio_entregas)
        self.relatorio_button.pack(pady=10)

        self.refresh_entrega_list()

    def registrar_entrega(self):
        epi_id = self.entrega_epi_id_entry.get()
        data_entrega = self.entrega_data_entry.get()
        setor = self.entrega_setor_entry.get()
        quantidade = self.entrega_quantidade_entry.get()

        if epi_id and data_entrega and setor and quantidade:
            try:
                add_entrega(epi_id, data_entrega, setor, quantidade)
                messagebox.showinfo("Sucesso", "Entrega registrada com sucesso!")
                self.clear_registrar_entrega_fields()
                self.refresh_entrega_list()
                self.refresh_epi_list()
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showerror("Erro", "Preencha todos os campos!")

    def clear_registrar_entrega_fields(self):
        self.entrega_epi_id_entry.delete(0, tk.END)
        self.entrega_data_entry.delete(0, tk.END)
        self.entrega_setor_entry.delete(0, tk.END)
        self.entrega_quantidade_entry.delete(0, tk.END)

    def refresh_entrega_list(self):
        for widget in self.tab3.winfo_children():
            if isinstance(widget, ttk.Treeview):
                widget.destroy()

        entregas = get_entregas()
        columns = ("ID", "EPI ID", "EPI Nome", "Descrição", "Data Entrega", "Setor", "Quantidade")
        self.entrega_table = ttk.Treeview(self.tab3, columns=columns, show="headings")
        for col in columns:
            self.entrega_table.heading(col, text=col)
        self.entrega_table.pack(fill="both", expand=True)

        for entrega in entregas:
            self.entrega_table.insert('', 'end', values=entrega)


    def gerar_relatorio_entregas(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
            if file_path:
                entregas = get_entregas()
                gerar_relatorio_entregas(entregas, file_path)
                messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def gerar_relatorio_epis(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
            if file_path:
                epis = get_epis()
                gerar_relatorio_epis(epis, file_path)
                messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

def run():
    root = tk.Tk()
    app = EpiApp(root)
    root.mainloop()

if __name__ == "__main__":
    run()
