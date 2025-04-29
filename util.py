def formatar_valor(valor):
    return f"{float(valor) / 100:.2f}"


def formatar_data(data):
    if len(data) != 6:
        return data
    dia = data[0:2]
    mes = data[2:4]
    ano = data[4:6]

    return f"{dia}/{mes}/20{ano}"
