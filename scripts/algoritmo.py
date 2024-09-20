import os
from collections import defaultdict
import sys

sys.setrecursionlimit(1000000)  

def ler_grade_do_arquivo(caminho_arquivo):
    grade = []
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                grade.append(list(linha.rstrip('\n')))
    except FileNotFoundError:
        print(f"O arquivo '{caminho_arquivo}' não foi encontrado.")
        exit()
    return grade

def construir_lista_adjacencia(grade):
    lista_adjacencia = defaultdict(list)
    total_linhas = len(grade)

    direcoes_movimento = {
        '|': [(1, 0)],
        '/': [(1, -1)],
        '\\': [(1, 1)],
        'V': [(1, -1), (1, 0), (1, 1)],
        'W': [(1, -1), (1, 0), (1, 1), (-1, 0)],
    }

    for linha in range(total_linhas):
        total_colunas = len(grade[linha])
        for coluna in range(total_colunas):
            caractere = grade[linha][coluna]
            if caractere == ' ':
                continue
            posicao_atual = (linha, coluna)
            movimentos_possiveis = []
            if caractere in direcoes_movimento:
                movimentos_possiveis = direcoes_movimento[caractere]
            elif caractere.isdigit():
                movimentos_possiveis = [(1, 0)] 
            elif caractere == '#':
                continue  
            else:
                continue

            for mov_linha, mov_coluna in movimentos_possiveis:
                nova_linha, nova_coluna = linha + mov_linha, coluna + mov_coluna
                if 0 <= nova_linha < total_linhas and 0 <= nova_coluna < len(grade[nova_linha]):
                    caractere_vizinho = grade[nova_linha][nova_coluna]
                    if caractere_vizinho != ' ':
                        lista_adjacencia[posicao_atual].append((nova_linha, nova_coluna))
    return lista_adjacencia

def encontrar_nos_raiz(lista_adjacencia):
    posicoes_filhas = set()
    for vizinhos in lista_adjacencia.values():
        posicoes_filhas.update(vizinhos)
    posicoes_raiz = set(lista_adjacencia.keys()) - posicoes_filhas
    return list(posicoes_raiz)

def dfs_iterativa(grade, no_inicial):
    pilha = [(no_inicial, 0)]  
    pontuacao_maxima = 0
    nos_visitados = set()  

    while pilha:
        no_atual, soma_atual = pilha.pop()

        if no_atual in nos_visitados:
            continue  
        nos_visitados.add(no_atual) 

        linha, coluna = no_atual
        caractere = grade[linha][coluna]
        soma_atual += int(caractere) if caractere.isdigit() else 0

        if no_atual not in lista_adjacencia or not lista_adjacencia[no_atual]: 
            if soma_atual > pontuacao_maxima:
                pontuacao_maxima = soma_atual
        else:
            for vizinho in lista_adjacencia[no_atual]:
                pilha.append((vizinho, soma_atual))

    return pontuacao_maxima

def processar_casos_no_diretorio(diretorio):
    arquivos_caso = [f for f in os.listdir(diretorio) if f.endswith('.txt')]  
    global lista_adjacencia
    
    if not arquivos_caso:
        print("Nenhum arquivo de caso foi encontrado na pasta.")
        return
    
    for arquivo_caso in arquivos_caso:
        caminho_arquivo = os.path.join(diretorio, arquivo_caso)
        print(f"\nProcessando arquivo: {arquivo_caso}")
        
        grade = ler_grade_do_arquivo(caminho_arquivo)
        lista_adjacencia = construir_lista_adjacencia(grade)
        raizes = encontrar_nos_raiz(lista_adjacencia)
        pontuacao_maxima = 0

        for raiz in raizes:
            pontuacao = dfs_iterativa(grade, raiz)
            if pontuacao > pontuacao_maxima:
                pontuacao_maxima = pontuacao

        print(f"A pontuação máxima para o arquivo {arquivo_caso} é: {pontuacao_maxima}")

def main():
    diretorio = 'casos'
    if not os.path.exists(diretorio):
        print(f"A pasta '{diretorio}' não foi encontrada.")
        return
    processar_casos_no_diretorio(diretorio)

if __name__ == "__main__":
    main()
