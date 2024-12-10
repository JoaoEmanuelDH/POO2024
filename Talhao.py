import csv

class Talhao:
    def __init__(self, id_talhao, area, fazenda):
        self.id_talhao = id_talhao
        self.area = area
        self.fazenda = fazenda

    @staticmethod
    def set_talhao(lista, id_talhao, area, fazenda):
        for talhao in lista:
            if talhao.id_talhao == id_talhao:
                return "ID já cadastrado. Por favor, escolha outro ID."
        talhao = Talhao(id_talhao, area, fazenda)
        lista.append(talhao)
        return f"Talhão {id_talhao} cadastrado com sucesso!"

    @staticmethod
    def salvar_talhoes_em_csv(lista, nome_arquivo):
        registros_existentes = set()

        try:
            with open(nome_arquivo, mode='r', newline='') as arquivo_csv:
                leitor = csv.reader(arquivo_csv)
                next(leitor, None)  # Pula o cabeçalho
                for linha in leitor:
                    registros_existentes.add((int(linha[0]), float(linha[1]), str(linha[2])))
        except FileNotFoundError:
            pass

        with open(nome_arquivo, mode='a', newline='') as arquivo_csv:
            writer = csv.writer(arquivo_csv)
            if not registros_existentes:
                writer.writerow(['ID', 'Área (hectares)', 'Fazenda'])  # Cabeçalho
            for talhao in lista:
                if (talhao.id_talhao, talhao.area, talhao.fazenda) not in registros_existentes:
                    writer.writerow([talhao.id_talhao, talhao.area, talhao.fazenda])

    @staticmethod
    def carregar_talhoes_do_csv(nome_arquivo):
        talhoes = []
        try:
            with open(nome_arquivo, mode='r', newline='') as arquivo_csv:
                leitor = csv.reader(arquivo_csv)
                next(leitor, None)  # Pula o cabeçalho
                for linha in leitor:
                    id_talhao = int(linha[0])
                    area = float(linha[1])
                    fazenda = str(linha[2])
                    talhao = Talhao(id_talhao, area, fazenda)
                    talhoes.append(talhao)
        except FileNotFoundError:
            pass
        return talhoes