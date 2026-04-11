import customtkinter as ctk
from tkinter import messagebox, ttk
import pandas as pd
import os

# Configurações de Design
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AuroraPortApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AURORA - Gestão Portuária de Grãos")
        self.geometry("1000x700")
        
        self.db_path = "dados_porto.xlsx"
        self.colunas = [
            "SAÍDA DO PÁTIO", "CHEGADA ETC", "TT VIAGEM", "ENTR. CLASSIFIC", 
            "SAÍDA CLASSIFICAÇÃO", "TT CLASSIFIC", "ENTR. BALANÇA", "SAÍDA BALANÇA", 
            "TT BALANÇA", "ENTRADA TOMBADOR", "SAÍDA TOMBADOR", "TT TOMBADOR"
        ]
        
        if not os.path.exists(self.db_path):
            pd.DataFrame(columns=self.colunas).to_excel(self.db_path, index=False)

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.show_login_screen()

    def clear_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # --- TELA 1: LOGIN ---
    def show_login_screen(self):
        self.clear_screen()
        frame = ctk.CTkFrame(self.container, width=400, height=500, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="AURORA", font=("Inter", 40, "bold"), text_color="#3a7ebf").pack(pady=(40, 5))
        ctk.CTkLabel(frame, text="Logística de Grãos", font=("Inter", 14)).pack(pady=(0, 30))

        self.user_entry = ctk.CTkEntry(frame, placeholder_text="Usuário", width=250, height=40)
        self.user_entry.pack(pady=10)

        self.pass_entry = ctk.CTkEntry(frame, placeholder_text="Senha", show="*", width=250, height=40)
        self.pass_entry.pack(pady=10)

        ctk.CTkButton(frame, text="ENTRAR", command=self.login, width=250, height=45, font=("Inter", 16, "bold")).pack(pady=40)

    def login(self):
        # Login simplificado para teste
        if self.user_entry.get() != "" and self.pass_entry.get() != "":
            self.show_input_screen()
        else:
            messagebox.showwarning("Aviso", "Preencha usuário e senha.")

    # --- TELA 2: LANÇAMENTOS ---
    def show_input_screen(self):
        self.clear_screen()
        
        menu_frame = ctk.CTkFrame(self.container, height=60, corner_radius=0)
        menu_frame.pack(fill="x")
        ctk.CTkLabel(menu_frame, text="NOVO LANÇAMENTO", font=("Inter", 18, "bold")).pack(side="left", padx=20)
        ctk.CTkButton(menu_frame, text="VER REGISTROS", command=self.show_table_screen, width=140).pack(side="right", padx=20)

        scroll_frame = ctk.CTkScrollableFrame(self.container, width=800, height=500)
        scroll_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.entries = {}
        for col in self.colunas:
            f = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            f.pack(fill="x", pady=8)
            ctk.CTkLabel(f, text=col, width=250, anchor="w", font=("Inter", 13, "bold")).pack(side="left", padx=10)
            entry = ctk.CTkEntry(f, placeholder_text="Digite aqui...", width=350)
            entry.pack(side="right", padx=10, expand=True)
            self.entries[col] = entry

        ctk.CTkButton(self.container, text="CONFIRMAR LANÇAMENTO", command=self.save_data, 
                      fg_color="#28a745", hover_color="#218838", height=50, font=("Inter", 16, "bold")).pack(pady=20)

    def save_data(self):
        data = {col: self.entries[col].get() for col in self.colunas}
        try:
            df_old = pd.read_excel(self.db_path)
            df_new = pd.concat([df_old, pd.DataFrame([data])], ignore_index=True)
            df_new.to_excel(self.db_path, index=False)
            messagebox.showinfo("Sucesso", "Lançado com sucesso!")
            for entry in self.entries.values():
                entry.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    # --- TELA 3: VISUALIZAÇÃO ---
    def show_table_screen(self):
        self.clear_screen()
        
        menu_frame = ctk.CTkFrame(self.container, height=60, corner_radius=0)
        menu_frame.pack(fill="x")
        ctk.CTkButton(menu_frame, text="VOLTAR", command=self.show_input_screen).pack(side="left", padx=20)
        
        tree_frame = ctk.CTkFrame(self.container)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Configuração da Tabela Visual
        tree = ttk.Treeview(tree_frame, columns=self.colunas, show='headings')
        for col in self.colunas:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        df = pd.read_excel(self.db_path)
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(side="left", fill="both", expand=True)

if __name__ == "__main__":
    app = AuroraPortApp()
    app.mainloop()
