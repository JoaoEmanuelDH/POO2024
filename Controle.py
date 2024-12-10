import csv

class Controle:
    def __init__(self, nome, antes, depois, data, id_talhao, eficiencia):
        self.nome = nome
        self.antes = antes
        self.depois = depois
        self.data = data
        self.id_talhao = id_talhao
        self.eficiencia = eficiencia

    @staticmethod
    def set_controle(lista, lista_talhoes, nome, antes, depois, data, id_talhao):
        talhao_existe = False
        for talhao in lista_talhoes:
            if talhao.id_talhao == id_talhao:
                talhao_existe = True
                break
        
        if not talhao_existe:
            return f"Erro: Talhão com ID {id_talhao} não está cadastrado."

        eficiencia = (1 - (depois / antes)) * 100
        controle = Controle(nome, antes, depois, data, id_talhao, eficiencia)
        lista.append(controle)
        return f"Controle {nome} cadastrado com sucesso!"

    @staticmethod
    def salvar_controles_em_csv(lista, nome_arquivo):
        registros_existentes = set()

        try:
            with open(nome_arquivo, mode='r', newline='') as arquivo_csv:
                leitor = csv.reader(arquivo_csv)
                next(leitor, None)
                for linha in leitor:
                    registros_existentes.add((str(linha[0]), int(linha[1]), int(linha[2]), str(linha[3]), int(linha[4]), float(linha[5])))

        except FileNotFoundError:
            pass

        with open(nome_arquivo, mode='a', newline='') as arquivo_csv:
            writer = csv.writer(arquivo_csv)
            if not registros_existentes:
                writer.writerow(['Nome', 'Antes', 'Depois', 'Data', 'ID (do talhão)', 'Eficiência (%)'])
            for controle in lista:
                if (controle.nome, controle.antes, controle.depois, controle.data, controle.id_talhao, controle.eficiencia) not in registros_existentes:
                    writer.writerow([controle.nome, controle.antes, controle.depois, controle.data, controle.id_talhao, controle.eficiencia])

    @staticmethod
    def carregar_controles_do_csv(nome_arquivo, lista_talhoes):
        controles = []
        try:
            with open(nome_arquivo, mode='r', newline='') as arquivo_csv:
                leitor = csv.reader(arquivo_csv)
                next(leitor, None)
                for linha in leitor:
                    nome = str(linha[0])
                    antes = int(linha[1])
                    depois = int(linha[2])
                    data = str(linha[3])
                    id_talhao = int(linha[4])
                    eficiencia = float(linha[5])
                    controle = Controle(nome, antes, depois, data, id_talhao, eficiencia)
                    controles.append(controle)
        except FileNotFoundError:
            pass
        return controles