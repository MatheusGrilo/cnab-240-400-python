import random
from datetime import datetime

data_atual = datetime.now()
data_formatada = data_atual.strftime("%d%m%y")
numero_aleatorio = "0" * 8 + "".join(str(random.randint(0, 9)) for _ in range(4))

titulo = ""
aviso_bancario = ""
sucesso = 0
erro = 0


def ler_arquivo_cnab400(caminho_arquivo):
    header_remessa = {}
    transacoes_remessa = []
    trailer_remessa = {}

    with open(caminho_arquivo, "r", encoding="latin1") as file:
        linhas = file.readlines()

        if not linhas:
            print("O arquivo selecionado está vazio")

        linha_header_remessa = linhas[0].strip()
        linhas_transacoes_remessa = linhas[1:-1]
        # linha_trailer_remessa = linhas[-1]

        # Header CNAB 400
        header_remessa = {
            "identificacao_do_registro": linha_header_remessa[0:1],  # 0
            "identificacao_do_arquivo_de_remessa": linha_header_remessa[1:2],  # 1
            "literal_remessa": linha_header_remessa[2:9],  # REMESSA
            "codigo_de_servico": linha_header_remessa[9:11],  # 01
            "literal_servico": linha_header_remessa[11:26],  # COBRANCA
            "codigo_da_empresa": linha_header_remessa[
                26:46
            ],  # Será fornecidor pelo banco
            "nome_da_empresa": linha_header_remessa[46:76],  # Razão Social
            "num_do_banco_na_camara_de_compensacao": linha_header_remessa[
                76:79
            ],  # Bradesco: 237,
            "nome_do_banco_por_extenso": linha_header_remessa[
                79:94
            ],  # Exemplo: Bradesco
            "data_da_gravacao_do_arquivo": linha_header_remessa[94:100],  # DDMMAA
            "branco_1": (
                True if linha_header_remessa[100:108] == 8 * " " else False
            ),  # Branco
            "identificacao_do_sistema": linha_header_remessa[
                108:110
            ],  # MX (para Bradesco)
            "num_sequencial_da_remessa": linha_header_remessa[110:117],  # Sequencial
            "branco_2": (
                True if linha_header_remessa[117:394] == 277 * " " else False
            ),  # Branco por 277 caracteres
            "num_sequencial_do_registro_de_um_em_um": linha_header_remessa[
                394:400
            ],  # exemplo: 000001,
        }

        # Transações CNAB 400
        for i, linha in enumerate(linhas_transacoes_remessa, start=2):
            identificacao_do_registro = linha[0:1]  # Identificação do Registro
            agencia_de_debito = linha[1:6]  # Agência de Débito (opcional)
            digito_da_agencia_de_debito = linha[
                6:7
            ]  # Dígito da Agência de Débito (opcional)
            razao_da_conta_corrente = linha[7:12]  # Razão da Conta-Corrente (opcional)
            conta_corrente = linha[12:19]  # Conta-Corrente (opcional)
            digito_da_conta_corrente = linha[
                19:20
            ]  # Dígito da Conta-Corrente (opcional)
            identificacao_da_empresa_beneficiaria_no_banco = linha[
                20:37
            ]  # Identificação da Empresa Beneficiária no Banco
            num_controle_do_participante = linha[37:62]  # Nº Controle do Participante
            cod_do_banco_a_ser_debitado = linha[
                62:65
            ]  # Código do Banco a ser debitado na Câmara de Compensação
            campo_de_multa = linha[65:66]  # Campo de Multa
            percentual_de_multa = linha[66:70]  # Percentual de Multa
            identificacao_do_titulo_no_banco = linha[
                70:81
            ]  # Identificação do Título no Banco
            digito_de_autoconferencia_do_num_bancario = linha[
                81:82
            ]  # Dígito de Autoconferência do nº bancário
            desconto_bonificacao_por_dia = linha[82:92]  # Desconto/Bonificação por dia
            condiacao_para_emissao_da_papeleta_de_cobranca = linha[
                92:93
            ]  # Condição para emissão da papeleta de cobrança
            ident_se_emite_boleto_para_debito_automatico = linha[
                93:94
            ]  # Ident. se emite boleto para débito automático
            identificacao_da_operacao_do_banco = linha[
                94:104
            ]  # Identificação da operação do banco
            indicador_rateio_credito = linha[
                104:105
            ]  # Indicador de rateio de crédito (opcional)
            enderecamento_p_aviso_do_deb_automatico_em_conta_corrente = linha[
                105:106
            ]  # Endereçamento p/ aviso do débito automático em conta corrente (opcional)
            quantidade_de_pagamentos = linha[106:108]  # Quantidade de pagamentos
            identifiacao_da_ocorrencia = linha[108:110]  # Identificação da ocorrência
            num_do_documento = linha[110:120]  # Número do documento
            data_do_vencimento_do_titulo = linha[
                120:126
            ]  # Data do vencimento do título
            valor_do_titulo = linha[126:139]  # Valor do título
            banco_encarregado_da_cobranca = linha[
                139:142
            ]  # Banco encarregado da cobrança
            agencia_depositaria = linha[142:147]  # Agência depositária
            especie_de_titulo = linha[147:149]  # Espécie de título
            # 01-Duplicata
            # 02-Nota Promissória
            # 03-Nota de Seguro
            # 05-Recibo
            # 10-Letras de Câmbio
            # 11-Nota de Débito
            # 12-Duplicata de Serv.
            # 31-Cartão de Crédito
            # 32-Boleto de Proposta
            # 33- Depósito e Aporte
            # 99-Outros
            identificacao = linha[149:150]  # Identificação
            data_da_emissao_do_titulo = linha[150:156]  # Data da emissão do título
            primeira_instrucao = linha[156:158]  # Primeira instrução
            segunda_instrucao = linha[158:160]  # Segunda instrução
            valor_a_ser_cobrado_por_dia_de_atraso = linha[
                160:173
            ]  # Valor a ser cobrado por dia de atraso
            data_limite_para_concessao_de_desconto = linha[
                173:179
            ]  # Data limite para concessão de desconto
            valor_do_desconto = linha[179:192]  # Valor do desconto
            valor_do_iof = linha[192:205]  # Valor do IOF
            valor_do_abatimento_a_ser_condedido_ou_cancelado = linha[
                205:218
            ]  # Valor do abatimento a ser concedido ou cancelado
            identificacao_do_tipo_de_inscricao_do_pagador = linha[
                218:220
            ]  # 01 - CPF - 02 - CNPJ
            num_inscricao_do_pagador = linha[220:234]  # CNPJ/CPF
            nome_do_pagador = linha[234:274]  # Nome do Pagador
            endereco_do_pagador = linha[274:314]  # Endereço do Pagador
            primeira_mensagem = linha[314:326]  # Primeira Mensagem
            cep = linha[326:331]  # CEP Pagador
            sufixo_do_cep = linha[331:334]  # Sufixo
            beneficiario_final_ou_segunda_mensagem = linha[
                334:394
            ]  # Beneficiário final ou segunda mensagem
            num_sequencial_do_registro = linha[394:400]  # Número sequencial do registro

            transacoes_remessa.append(
                {
                    "identificacao_do_registro": identificacao_do_registro,
                    "agencia_de_debito": agencia_de_debito,
                    "digito_da_agencia_de_debito": digito_da_agencia_de_debito,
                    "razao_da_conta_corrente": razao_da_conta_corrente,
                    "conta_corrente": conta_corrente,
                    "digito_da_conta_corrente": digito_da_conta_corrente,
                    "identificacao_da_empresa_beneficiaria_no_banco": identificacao_da_empresa_beneficiaria_no_banco,
                    "num_controle_do_participante": num_controle_do_participante,
                    "cod_do_banco_a_ser_debitado": cod_do_banco_a_ser_debitado,
                    "campo_de_multa": campo_de_multa,
                    "percentual_de_multa": percentual_de_multa,
                    "identificacao_do_titulo_no_banco": identificacao_do_titulo_no_banco,
                    "digito_de_autoconferencia_do_num_bancario": digito_de_autoconferencia_do_num_bancario,
                    "desconto_bonificacao_por_dia": desconto_bonificacao_por_dia,
                    "condiacao_para_emissao_da_papeleta_de_cobranca": condiacao_para_emissao_da_papeleta_de_cobranca,
                    "ident_se_emite_boleto_para_debito_automatico": ident_se_emite_boleto_para_debito_automatico,
                    "identificacao_da_operacao_do_banco": identificacao_da_operacao_do_banco,
                    "indicador_rateio_credito": indicador_rateio_credito,
                    "enderecamento_p_aviso_do_deb_automatico_em_conta_corrente": enderecamento_p_aviso_do_deb_automatico_em_conta_corrente,
                    "quantidade_de_pagamentos": quantidade_de_pagamentos,
                    "identifiacao_da_ocorrencia": identifiacao_da_ocorrencia,
                    "num_do_documento": num_do_documento,
                    "data_do_vencimento_do_titulo": data_do_vencimento_do_titulo,
                    "valor_do_titulo": valor_do_titulo,
                    "banco_encarregado_da_cobranca": banco_encarregado_da_cobranca,
                    "agencia_depositaria": agencia_depositaria,
                    "especie_de_titulo": especie_de_titulo,
                    "identificacao": identificacao,
                    "data_da_emissao_do_titulo": data_da_emissao_do_titulo,
                    "primeira_instrucao": primeira_instrucao,
                    "segunda_instrucao": segunda_instrucao,
                    "valor_a_ser_cobrado_por_dia_de_atraso": valor_a_ser_cobrado_por_dia_de_atraso,
                    "data_limite_para_concessao_de_desconto": data_limite_para_concessao_de_desconto,
                    "valor_do_desconto": valor_do_desconto,
                    "valor_do_iof": valor_do_iof,
                    "valor_do_abatimento_a_ser_condedido_ou_cancelado": valor_do_abatimento_a_ser_condedido_ou_cancelado,
                    "identificacao_do_tipo_de_inscricao_do_pagador": identificacao_do_tipo_de_inscricao_do_pagador,
                    "num_inscricao_do_pagador": num_inscricao_do_pagador,
                    "nome_do_pagador": nome_do_pagador,
                    "endereco_do_pagador": endereco_do_pagador,
                    "primeira_mensagem": primeira_mensagem,
                    "cep": cep,
                    "sufixo_do_cep": sufixo_do_cep,
                    "beneficiario_final_ou_segunda_mensagem": beneficiario_final_ou_segunda_mensagem,
                    "num_sequencial_do_registro": num_sequencial_do_registro,
                }
            )

        # Trailer CNAB 400
        trailer_remessa = {
            "identificacao_registro": linha[0:1],  # 9
            "branco": True if linha[1:394] == 393 * " " else False,  # Branco
            "num_sequencial_do_registro": linha[394:400],  # Exemplo: 000001
        }

        titulo = linha_header_remessa[110:117]
        aviso_bancario = str(int(linha_header_remessa[110:117]) + 100).zfill(5)
        file.close()

        return (
            header_remessa,
            transacoes_remessa,
            trailer_remessa,
            titulo,
            aviso_bancario,
        )


def gravar_arquivo_cnab400(header_remessa, transacoes_remessa, transacao_status="06"):
    sucesso = 0
    erro = 0
    with open("retorno_" + titulo + ".ret", "w", encoding="latin1") as file:
        header_retorno = ""
        trailer_retorno = ""
        # transacoes_retorno = []

        quantidade_total_de_titulos = 0
        valor_total_de_titulos = 0

        quantidade_registros_02 = 0
        quantidade_registros_06 = 0
        quantidade_registros_09_e_10 = 0
        quantidade_registros_12 = 0
        quantidade_registros_13 = 0
        quantidade_registros_14 = 0
        quantidade_registros_19 = 0

        # valor_registros_02 = 0
        valor_registros_06 = 0
        # valor_registros_09_e_10 = 0
        # valor_registros_12 = 0
        # valor_registros_13 = 0
        # valor_registros_14 = 0
        # valor_registros_19 = 0

        # print(len(header_remessa["nome_do_banco_por_extenso"]))

        # Header de retorno CNAB 400
        header_retorno = (
            "0"  # 1 - Identificação do Registro
            + "2"  # 1 - Identificação do Arquivo-Retorno
            + "RETORNO"  # 7 - Retorno
            + "01"  # 2 - Código de Serviço
            + "COBRANCA"
            + 7 * " "  # 15 - Literal Serviço (COBRANCA + 7 ESPAÇOS)
            + header_remessa[
                "codigo_da_empresa"
            ]  # 20 - Código da Empresa (padrão = 20 zeros)
            + header_remessa["nome_da_empresa"]  # 30 - Nome do Banco
            + header_remessa[
                "num_do_banco_na_camara_de_compensacao"
            ]  # 3 - Num do Banco
            + header_remessa[
                "nome_do_banco_por_extenso"
            ]  # 15 - Nome do banco por extenso
            + header_remessa[
                "data_da_gravacao_do_arquivo"
            ]  # 6 - Data da gravação do arquivo
            + "01600000"  # 8 - Densidade da Gravação (?)
            + aviso_bancario  # 5 - Nº Aviso
            + " " * 266  # 266 - Branco
            + data_formatada  # 6 - Data de Geração do Arquivo
            + " " * 9  # 9 - Branco
            + "000001"  # 6 - Nº Sequencial do Registro
        )

        trailer_retorno = (
            "9"  # 1 - Identificação do Registro
            + "2"  # 1 - Identificação do Retorno
            + "01"  # 2 - Identificação Tipo de Registro
            + header_remessa[
                "num_do_banco_na_camara_de_compensacao"
            ]  # 3 - Código do banco
            + " " * 10  # 10 - Branco
            + str(quantidade_total_de_titulos).zfill(
                8
            )  # 8 - Quantidade de Títulos em Cobrança
            + str(valor_total_de_titulos).zfill(14)  # 14 - Valor Total em Cobrança
            + aviso_bancario.zfill(8)  # 8 - Nº Aviso Bancário
            + " " * 10  # 10 - Branco
            + str(quantidade_registros_02).zfill(
                5
            )  # 5 - Quantidade de Registros Ocorrência 02 - Confirmação de Entradas
            + "0" * 12  # 12 - Valor dos Registros 02 - Confirmação de Entradas
            + "0" * 12  # 12 - Valor dos Registros 06 - Liquidação
            + str(quantidade_registros_06).zfill(
                5
            )  # 5 - Quantidade de Registros Ocorrência 06 - Liquidação
            + "0" * 12  # 12 - Valor dos Registros 06 - Liquidação
            + str(quantidade_registros_09_e_10).zfill(
                5
            )  # 5 - Quantidade de Registros Ocorrência 09 e 10 - Títulos baixados
            + "0" * 12  # 12 - Valor dos Registros 09 e 10 - Títulos baixados
            + str(quantidade_registros_13).zfill(
                5
            )  # 5 - Quantidade de Registros Ocorrência 13 - Títulos em Abatimento Cancelado
            + "0" * 12  # 12 - Valor dos Registros 13 - Títulos em Abatimento Cancelado
            + str(quantidade_registros_14).zfill(
                5
            )  # 5 - Quantidade de Registros Ocorrência 14 - Vencimento Alterado
            + "0" * 12  # 12 - Valor dos Registros 14 - Vencimento Alterado
            + str(quantidade_registros_12).zfill(
                5
            )  # 5 - Quantidade de Registros Ocorrência 12 - Abatimento Concedido
            + "0" * 12  # 12 - Valor dos Registros 12 - Abatimento Concedido
            + str(quantidade_registros_19).zfill(
                5
            )  # 5 - Quantidade de Registros Ocorrência 19 - Confirmação da Instrução Protesto
            + "0"
            * 12  # 12 - Valor dos Registros 19 - Confirmação da Instrução Protesto
            + " " * 174  # 174 - Branco
            + "0" * 15  # 15 - Valor Total dos Rateios
            + "0" * 8  # 8 - Quantidade Total de Rateios Efetuados
            + " " * 9  # 9 - Branco
            + titulo[1:7]  # 6 - Nº Sequencial do Registro
        )

        # Escreve o header no arquivo de retorno
        if len(header_retorno) == 400:
            file.write(header_retorno + "\n")
            print("Header escrito")
        else:
            print("Header não contém 400 caracteres")

        # Escreve as transações no arquivo de retorno
        numero_sequencial_do_registro = 2

        for i, transacoes in enumerate(transacoes_remessa):
            # print(transacoes_remessa[i]["especie_de_titulo"])
            # print(len(transacoes_remessa[i]["especie_de_titulo"]))
            transacao_a_ser_escrita = ""
            # Start writing the transaction
            transacao_a_ser_escrita = (
                "1"  #  1 - Identificação do Registro
                + transacoes_remessa[i][
                    "identificacao_do_tipo_de_inscricao_do_pagador"
                ]  # 2 - 01 - CPF / 02 - CNPJ
                + transacoes_remessa[i][
                    "num_inscricao_do_pagador"
                ]  # 14 - CPF/CNPJ do Pagador
                + "000"  # 3 - Zeros
                + transacoes_remessa[i][
                    "identificacao_da_empresa_beneficiaria_no_banco"
                ]  # 17 - (Identificação da Empresa Beneficiário no Banco) [Zero - Carteira - Agência - Conta-corrente - Vide Obs.] (pag. 39)
                + transacoes_remessa[i][
                    "num_controle_do_participante"
                ]  # 25 - (Nº Controle do Participante) Uso da empresa
                + "0" * 8  # 8 - Zeros
                + transacoes_remessa[i]["identificacao_do_titulo_no_banco"]
                + " "  # 12 - (Identificação do Título no Banco) Número do Banco (pag. 39)
                + "0" * 10  # 10 - Zeros
                + "0" * 12  # 12 - Zeros
                + "0"  # 1 - Indicador de Rateio Crédito ("R" obs pag. 39)
                + "00"  # 2 - (Pagamento Parcial) 00 -Não informado ou parcelamento recusado / outro valor - Parcelamento aceito
                + "9"  # 1 - Carteira
                + transacao_status  # 2 - Identificação da Ocorrência (pag. 40)
                # [02 - Aguardando / 06 - PAGO]
                + data_formatada  # 6 - Data Ocorrência no Banco (DDMMAA)
                + transacoes_remessa[i]["num_do_documento"]  # 10 - Nº do Documento
                + str(transacoes_remessa[i]["identificacao_do_titulo_no_banco"]).zfill(
                    20
                )  # 20 - (Identificação do Título no Banco pag. 40) #TODO
                + transacoes_remessa[i][
                    "data_do_vencimento_do_titulo"
                ]  # 6 - Data do Vencimento do Título (DDMMAA)
                + transacoes_remessa[i]["valor_do_titulo"]  # 13 - Valor do Título (R$)
                + header_remessa[
                    "num_do_banco_na_camara_de_compensacao"
                ]  # 3 - Banco Encarregado da Cobrança (pag. 40)
                + transacoes_remessa[i][
                    "agencia_depositaria"
                ]  # 5 - Agência Depositária (pag. 40)
                + "  "  # 2 - BRANCO - Espécie do Título (pag. 40)
                + "0"
                * 13  # 13 - Valor Despesa pag. 40 (02 - Entradas Confirmadas / 28 - Débitos de Tarifas)
                + "0"
                * 13  # 13 - Valor Outras Despesas pag. 40 (Outras despesas / Custas de protesto)
                + "0" * 13  # 13 - juros Operação em Atraso (será informado com zeros)
                + "0" * 13  # 13 - Valor do IOF Devido (pag. 41)
                + "0" * 13  # 13 - Valor Abatimento Concedido sob o título (pag. 41)
                + "0" * 13  # 13 - Valor de Desconto Concedido (pag. 41)
                + transacoes_remessa[i]["valor_do_titulo"]  # 13 - Valor Pago (pag. 41)
                + "0" * 13  # 13 - Juros de Mora
                + "0" * 13  # 13 - Outros Créditos (será informado com zeros)
                + " " * 2  # 2 - Brancos
                + " "  # "A"  # 1 - A - Aceito / D - Desprezado (pag. 41) Motivo do código da Ocorrência
                + " " * 6  # data_formatada  # 6 - Data do Crédito
                + " " * 3  # "?" * 3  # 3 - Oridem Pagamento (pag. 41)
                + " " * 10  # 10 - Brancos
                + " "
                * 4  # "0237"  # 4 - Código do Banco (Quando cheque bradesco informe 0237)
                + "0"  # "?"
                * 10  # 10 - Motivo das Rejeições para cod ocorrência 109/110 (pag. 42)
                + " " * 40  # 40 - Brancos
                + "  "  # "??"  # 2 - Número do Cartório
                + " " * 10  # "?" * 10  # 10 - Número do Protocolo
                + " " * 14  # 14 - Brancos
                + str(numero_sequencial_do_registro).zfill(
                    6
                )  # 6 - Número Sequencial de Registro
            )

            # End writing the transaction

            # Write the transaction to the file
            if len(transacao_a_ser_escrita) == 400:
                file.write(transacao_a_ser_escrita + "\n")
                sucesso += 1
                numero_sequencial_do_registro += 1
            else:
                print(
                    f"Transação {i + 1} não contém 400 caracteres, contém {len(transacao_a_ser_escrita)} caracteres"
                )
                erro += 1

        if sucesso == 0:
            print("Nenhuma transação escrita")
        else:
            print(
                f"{sucesso} transaç{"ões" if sucesso > 1 else "ão"} escrita{"s" if sucesso > 1 else ""} com sucesso"
            )

        if erro > 0:
            print(f"{erro} erro{"s" if erro > 1 else ""} ao escrever as transações")

        # Escreve o trailer no arquivo de retorno
        if len(trailer_retorno) == 400:
            file.write(trailer_retorno + "\n")
            print("Trailer escrito")
        else:
            print("Trailer não contém 400 caracteres")

        file.close()
