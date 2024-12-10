import tkinter as tk
from Controle import Controle
from Pragas import Praga
from Talhao import Talhao


class InterfaceGrafica:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestão de Talhões, Pragas e Controles")
        self.master.attributes('-fullscreen', True)  # Tela cheia
        self.master.configure(bg='#228B22')  # Fundo verde
        self.lista_talhoes = Talhao.carregar_talhoes_do_csv("talhoes.csv")
        self.lista_pragas = Praga.carregar_pragas_do_csv("pragas.csv", self.lista_talhoes)
        self.lista_controles = Controle.carregar_controles_do_csv("controles.csv", self.lista_talhoes)

        self.mensagem_label = tk.Label(self.master, text="", font=("Arial", 12), fg="yellow", bg="#228B22")
        self.mensagem_label.pack(pady=10)

        self.label = tk.Label(self.master, text="Escolha uma opção:", font=("Arial", 14), fg="yellow", bg="#228B22")
        self.label.pack(pady=20)

        self.botoes = {
            "Cadastrar talhão": self.cadastrar_talhao,
            "Cadastrar praga": self.cadastrar_praga,
            "Cadastrar controle": self.cadastrar_controle,
            "Consultar talhões": self.consultar_talhoes,
            "Consultar pragas": self.consultar_pragas,
            "Consultar controles": self.consultar_controles,
            "Excluir talhão": self.excluir_talhao,
            "Excluir praga": self.excluir_praga,
            "Excluir controle": self.excluir_controle,
            "Sair": self.sair
        }

        for texto, comando in self.botoes.items():
            btn = tk.Button(self.master, text=texto, command=comando, font=("Arial", 12), fg="black", bg="yellow")
            btn.pack(fill='both', pady=5)

    def mostrar_entrada(self, label_text, campos, entrada_func):
        top = tk.Toplevel(self.master)
        top.title(label_text)

        # Definir o tamanho da janela secundária como metade da tela
        width = self.master.winfo_screenwidth() // 2
        height = self.master.winfo_screenheight() // 2
        top.geometry(f"{width}x{height}+{self.master.winfo_x()}+{self.master.winfo_y()}")

        entradas = {}
        for campo, descricao in campos.items():
            label = tk.Label(top, text=descricao, fg="green", bg="yellow")
            label.pack(pady=5)
            entry = tk.Entry(top, font=("Arial", 12))
            entry.pack(pady=5)
            entradas[campo] = entry

        def on_submit():
            valores = {campo: entrada.get() for campo, entrada in entradas.items()}
            mensagem = entrada_func(valores)
            self.exibir_mensagem(mensagem)
            top.destroy()

        submit_btn = tk.Button(top, text="Enviar", command=on_submit, font=("Arial", 12), fg="black", bg="yellow")
        submit_btn.pack(pady=5)

    def exibir_mensagem(self, mensagem):
        self.mensagem_label.config(text=mensagem)

    def cadastrar_talhao(self):
        def salvar_talhao(valores):
            try:
                id_talhao = int(valores['id_talhao'])
                area = float(valores['area'])
                fazenda = valores['fazenda']
                return Talhao.set_talhao(self.lista_talhoes, id_talhao, area, fazenda)
            except ValueError:
                return "Entrada inválida!"

        campos = {
            'id_talhao': "Digite o ID do Talhão:",
            'area': "Informe a área (hectares):",
            'fazenda': "Informe a fazenda:"
        }

        self.mostrar_entrada("Cadastrar Talhão", campos, salvar_talhao)

    def cadastrar_praga(self):
        def salvar_praga(valores):
            nome = valores['nome']
            qnt = int(valores['qnt'])
            data = valores['data']
            id_talhao = int(valores['id_talhao'])
            return Praga.set_praga(self.lista_pragas, self.lista_talhoes, nome, qnt, data, id_talhao)

        campos = {
            'nome': "Digite o nome da Praga:",
            'qnt': "Informe a quantidade de pragas:",
            'data': "Informe a data (dd/mm/aaaa):",
            'id_talhao': "Digite o ID do Talhão:"
        }

        self.mostrar_entrada("Cadastrar Praga", campos, salvar_praga)

    def cadastrar_controle(self):
        def salvar_controle(valores):
            nome = valores['nome']
            antes = int(valores['antes'])
            depois = int(valores['depois'])
            data = valores['data']
            id_talhao = int(valores['id_talhao'])
            return Controle.set_controle(self.lista_controles, self.lista_talhoes, nome, antes, depois, data, id_talhao)

        campos = {
            'nome': "Digite o nome do Controle:",
            'antes': "Informe a quantidade de pragas antes do controle:",
            'depois': "Informe a quantidade de pragas depois do controle:",
            'data': "Informe a data (dd/mm/aaaa):",
            'id_talhao': "Digite o ID do Talhão:"
        }

        self.mostrar_entrada("Cadastrar Controle", campos, salvar_controle)

    def consultar_talhoes(self):
        talhoes_info = "\n".join([f"ID: {talhao.id_talhao}, Área: {talhao.area} hectares, Fazenda: {talhao.fazenda}" for talhao in self.lista_talhoes])
        self.exibir_mensagem(talhoes_info if talhoes_info else "Nenhum talhão cadastrado.")

    def consultar_pragas(self):
        pragas_info = "\n".join([f"Nome: {praga.nome}, Quantidade: {praga.qnt}, Data: {praga.data}, ID Talhão: {praga.id_talhao}, Densidade: {praga.densidade:.2f} pragas/m²" for praga in self.lista_pragas])
        self.exibir_mensagem(pragas_info if pragas_info else "Nenhuma praga cadastrada.")

    def consultar_controles(self):
        controles_info = "\n".join([f"Nome: {controle.nome}, Antes: {controle.antes}, Depois: {controle.depois}, Data: {controle.data}, ID Talhão: {controle.id_talhao}, Eficiência: {controle.eficiencia:.2f}%" for controle in self.lista_controles])
        self.exibir_mensagem(controles_info if controles_info else "Nenhum controle cadastrado.")

    def excluir_talhao(self):
        def excluir(valores):
            try:
                id_talhao = int(valores['id_talhao'])
                talhao_a_excluir = next((talhao for talhao in self.lista_talhoes if talhao.id_talhao == id_talhao), None)
                if talhao_a_excluir:
                    self.lista_talhoes.remove(talhao_a_excluir)
                    Talhao.salvar_talhoes_em_csv(self.lista_talhoes, "talhoes.csv")
                    return f"Talhão com ID {id_talhao} excluído com sucesso!"
                else:
                    return f"Talhão com ID {id_talhao} não encontrado!"
            except ValueError:
                return "ID inválido!"

        campos = {
            'id_talhao': "Digite o ID do Talhão para excluir:"
        }

        self.mostrar_entrada("Excluir Talhão", campos, excluir)

    def excluir_praga(self):
        def excluir(valores):
            try:
                nome = valores['nome']
                praga_a_excluir = next((praga for praga in self.lista_pragas if praga.nome == nome), None)
                if praga_a_excluir:
                    self.lista_pragas.remove(praga_a_excluir)
                    Praga.salvar_pragas_em_csv(self.lista_pragas, "pragas.csv")
                    return f"Praga {nome} excluída com sucesso!"
                else:
                    return f"Praga {nome} não encontrada!"
            except ValueError:
                return "Nome inválido!"

        campos = {
            'nome': "Digite o nome da Praga para excluir:"
        }

        self.mostrar_entrada("Excluir Praga", campos, excluir)

    def excluir_controle(self):
        def excluir(valores):
            try:
                nome = valores['nome']
                controle_a_excluir = next((controle for controle in self.lista_controles if controle.nome == nome), None)
                if controle_a_excluir:
                    self.lista_controles.remove(controle_a_excluir)
                    Controle.salvar_controles_em_csv(self.lista_controles, "controles.csv")
                    return f"Controle {nome} excluído com sucesso!"
                else:
                    return f"Controle {nome} não encontrado!"
            except ValueError:
                return "Nome inválido!"

        campos = {
            'nome': "Digite o nome do Controle para excluir:"
        }

        self.mostrar_entrada("Excluir Controle", campos, excluir)

    def sair(self):
        self.master.quit()
