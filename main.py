import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from cnab400 import ler_arquivo_cnab400
from util import formatar_data, formatar_valor

status_opcoes = {
    "Pago": "06",
    "Aceito": "02",
    "Rejeitado": "03",
    "Estornado": "40",
    # "Venc. alterado": "14",
}


def editar_status(event):
    item_selecionado = tabela.focus()
    if not item_selecionado:
        return

    col = tabela.identify_column(event.x)
    if col != "#4":  # "#4" é a coluna STATUS
        return

    bbox = tabela.bbox(item_selecionado, column=col)
    if not bbox:
        return

    x, y, width, height = bbox

    valor_atual = tabela.set(item_selecionado, "status")

    combo_editar = ttk.Combobox(
        frame_tabela, values=list(status_opcoes.keys()), state="readonly"
    )
    combo_editar.place(x=x, y=y, width=width, height=height)
    combo_editar.set(valor_atual)

    def salvar_novo_status(event=None):
        novo_status = combo_editar.get()
        tabela.set(item_selecionado, "status", novo_status)
        combo_editar.destroy()

    combo_editar.bind("<<ComboboxSelected>>", salvar_novo_status)
    combo_editar.focus()


def selecionar_arquivo():
    arquivo = filedialog.askopenfilename(title="Selecionar Arquivo")
    if arquivo:
        label_arquivo_selecionado.config(text=arquivo.split("/")[-1])
        try:
            header, transacoes, trailer, titulo, aviso_bancario = ler_arquivo_cnab400(
                arquivo
            )
            dados_para_tabela = []
            for t in transacoes:
                dados_para_tabela.append(
                    {
                        "pagador": t["nome_do_pagador"],
                        "valor": formatar_valor(t["valor_do_titulo"]),
                        "valor_desconto": formatar_valor(t["valor_do_desconto"]),
                        "status": "Pago",
                        "data_vencimento": formatar_data(
                            t["data_do_vencimento_do_titulo"]
                        ),
                    }
                )

            popular_tabela(dados_para_tabela)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler o arquivo: {str(e)}")


def nome_do_arquivo(arquivo):
    return arquivo


def gerar_arquivo():
    messagebox.showinfo("Gerar Arquivo", "Arquivo gerado com sucesso!")


# Exemplo de dados (simulando o dictionary)


def popular_tabela(dados):
    for linha in tabela.get_children():
        tabela.delete(linha)

    for item in dados:
        tabela.insert(
            "",
            tk.END,
            values=(
                item["pagador"],
                item["valor"],
                item["valor_desconto"],
                item["status"],
                item["data_vencimento"],
            ),
        )


app = tk.Tk()
app.title("CNAB")
app.geometry("600x400")
app.resizable(False, False)

# Frame Seleção
frame_topo = tk.Frame(app, bd=1, relief="solid")
frame_topo.place(x=5, y=5, width=590, height=60)

# Selecionar tipo
label_tipo = tk.Label(frame_topo, text="Selecionar tipo:")
label_tipo.place(x=10, y=5)

tipo_cnab = tk.StringVar(value="400")  # Valor padrão

radio_cnab240 = tk.Radiobutton(
    frame_topo, text="CNAB 240", variable=tipo_cnab, value="240", state="disabled"
)
radio_cnab240.place(x=10, y=25)

radio_cnab400 = tk.Radiobutton(
    frame_topo, text="CNAB 400", variable=tipo_cnab, value="400"
)
radio_cnab400.place(x=100, y=25)

# Selecionar arquivo
label_arquivo = tk.Label(frame_topo, text="Selecionar arquivo:")
label_arquivo.place(x=300, y=5)

botao_selecionar = tk.Button(frame_topo, text="Selecionar", command=selecionar_arquivo)
botao_selecionar.place(x=300, y=25)


label_arquivo_selecionado_text = "Nenhum arquivo selecionado"
label_arquivo_selecionado = tk.Label(frame_topo, text=label_arquivo_selecionado_text)
label_arquivo_selecionado.place(x=375, y=25)

# Frame Tabela com Scroll
frame_tabela = tk.Frame(app, bd=1, relief="solid")
frame_tabela.place(x=5, y=70, width=590, height=250)

colunas = ("pagador", "valor", "valor_desconto", "status", "vencimento")

tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

# Definindo os títulos das colunas
tabela.heading("pagador", text="Pagador")
tabela.heading("valor", text="Valor")
tabela.heading("valor_desconto", text="Desconto")
tabela.heading("status", text="Status")
tabela.heading("vencimento", text="Vencimento")

# Ajustando tamanho de colunas
tabela.column("pagador", width=200)
tabela.column("valor", width=80)
tabela.column("valor_desconto", width=80)
tabela.column("status", width=80)
tabela.column("vencimento", width=80)

# Scrollbar vertical
scrollbar = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=tabela.yview)
tabela.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tabela.pack(fill=tk.BOTH, expand=True)

tabela.bind("<Double-1>", editar_status)


# Botão Gerar Arquivo
botao_gerar = tk.Button(app, text="Gerar Arquivo", command=gerar_arquivo)
botao_gerar.place(x=200, y=330, width=200, height=40)

app.mainloop()
