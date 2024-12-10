import csv

class Praga:
    def __init__(self, nome, qnt, data, id_talhao, densidade):
        self.nome = nome
        self.qnt = qnt
        self.data = data
        self.id_talhao = id_talhao
        self.densidade = densidade

    @staticmethod
    def set_praga(lista, lista_talhoes, nome, qnt, data, id_talhao):
        talhao_existe = False
        area_talhao = 0
        for talhao in lista_talhoes:
            if talhao.id_talhao == id_talhao:
                talhao_existe = True
                area_talhao = talhao.area
                break
        
        if not talhao_existe:
            return f"Erro: Talhão com ID {id_talhao} não está cadastrado."

        densidade = qnt / (area_talhao * 10000)
        praga = Praga(nome, qnt, data, id_talhao, densidade)
        lista.append(praga)
        return f"Praga {nome} cadastrada com sucesso!"

    @staticmethod
    def salvar_pragas_em_csv(lista, nome_arquivo):
        registros_existentes = set()

        try:
            with open(nome_arquivo, mode='r', newline='') as arquivo_csv:
                leitor = csv.reader(arquivo_csv)
                next(leitor, None)
                for linha in leitor:
                    registros_existentes.add((str(linha[0]), int(linha[1]), str(linha[2]), int(linha[3]), float(linha[4])))

        except FileNotFoundError:
            pass

        with open(nome_arquivo, mode='a', newline='') as arquivo_csv:
            writer = csv.writer(arquivo_csv)
            if not registros_existentes:
                writer.writerow(['Nome', 'Quantidade', 'Data', 'ID (do talhão)', 'Densidade (pragas/m²)'])
            for praga in lista:
                if (praga.nome, praga.qnt, praga.data, praga.id_talhao, praga.densidade) not in registros_existentes:
                    writer.writerow([praga.nome, praga.qnt, praga.data, praga.id_talhao, praga.densidade])

    @staticmethod
    def carregar_pragas_do_csv(nome_arquivo, lista_talhoes):
        pragas = []
        try:
            with open(nome_arquivo, mode='r', newline='') as arquivo_csv:
                leitor = csv.reader(arquivo_csv)
                next(leitor, None)
                for linha in leitor:
                    nome = str(linha[0])
                    qnt = int(linha[1])
                    data = str(linha[2])
                    id_talhao = int(linha[3])
                    densidade = float(linha[4])
                    praga = Praga(nome, qnt, data, id_talhao, densidade)
                    pragas.append(praga)
        except FileNotFoundError:
            pass
        return pragas