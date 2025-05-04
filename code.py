import sys
import time
from collections import defaultdict

def carregar_automato(caminho):
    estados = set()
    alfabeto = set()
    estado_inicial = ''
    estados_finais = set()
    transicoes = defaultdict(set)
    tipo = 'AFD'

    with open(caminho, 'r') as f:
        linhas = [linha.strip() for linha in f if linha.strip()]

    for linha in linhas:
        if linha.startswith("estados:"):
            estados = set(linha.split(":")[1].split(","))
        elif linha.startswith("alfabeto:"):
            alfabeto = set(linha.split(":")[1].split(","))
        elif linha.startswith("inicial:"):
            estado_inicial = linha.split(":")[1].strip()
        elif linha.startswith("finais:"):
            estados_finais = set(linha.split(":")[1].split(","))
        elif linha.startswith("transicoes:"):
            continue
        else:
            origem, simbolo, destino = [x.strip() for x in linha.split(",")]
            transicoes[(origem, simbolo)].add(destino)
            if simbolo in ('ε', 'lambda'):
                tipo = 'AFN-λ'
            elif len(transicoes[(origem, simbolo)]) > 1:
                tipo = 'AFN' if tipo != 'AFN-λ' else 'AFN-λ'

    return estados, alfabeto, estado_inicial, estados_finais, transicoes, tipo

def epsilon_closure(transicoes, estado):
    stack = [estado]
    closure = set([estado])
    while stack:
        atual = stack.pop()
        for destino in transicoes.get((atual, 'ε'), set()) | transicoes.get((atual, 'lambda'), set()):
            if destino not in closure:
                closure.add(destino)
                stack.append(destino)
    return closure

def simular_afd(palavra, inicial, finais, transicoes):
    estado = inicial
    for simbolo in palavra:
        if (estado, simbolo) not in transicoes:
            return "rejeita"
        estado = next(iter(transicoes[(estado, simbolo)]))
    return "aceita" if estado in finais else "rejeita"

def simular_afn(palavra, inicial, finais, transicoes):
    estados_atuais = set([inicial])
    for simbolo in palavra:
        proximos = set()
        for estado in estados_atuais:
            proximos.update(transicoes.get((estado, simbolo), set()))
        estados_atuais = proximos
        if not estados_atuais:
            break
    return "aceita" if estados_atuais & finais else "rejeita"

def simular_afn_lambda(palavra, inicial, finais, transicoes):
    estados_atuais = epsilon_closure(transicoes, inicial)
    for simbolo in palavra:
        proximos = set()
        for estado in estados_atuais:
            for destino in transicoes.get((estado, simbolo), set()):
                proximos.update(epsilon_closure(transicoes, destino))
        estados_atuais = proximos
        if not estados_atuais:
            break
    return "aceita" if estados_atuais & finais else "rejeita"

def main():
    if len(sys.argv) != 4:
        print("Uso: ferramenta <arquivo_do_automato>.aut <arquivo_de_testes>.in <arquivo_de_saida>.out")
        return

    automato_path, entradas_path, saida_path = sys.argv[1], sys.argv[2], sys.argv[3]
    estados, alfabeto, inicial, finais, transicoes, tipo = carregar_automato(automato_path)

    with open(entradas_path, 'r') as f:
        entradas = [linha.strip().split(";") for linha in f if linha.strip()]

    resultados = []
    for palavra, esperado in entradas:
        inicio = time.time()

        if tipo == 'AFD':
            obtido = simular_afd(palavra, inicial, finais, transicoes)
        elif tipo == 'AFN':
            obtido = simular_afn(palavra, inicial, finais, transicoes)
        elif tipo == 'AFN-λ':
            obtido = simular_afn_lambda(palavra, inicial, finais, transicoes)
        else:
            obtido = "erro"

        fim = time.time()
        duracao = "{:.6f}".format(fim - inicio)

        resultados.append(f"{palavra};{esperado};{obtido};{duracao}")

    with open(saida_path, 'w') as f:
        f.write("\n".join(resultados))

if __name__ == "__main__":
    main()
