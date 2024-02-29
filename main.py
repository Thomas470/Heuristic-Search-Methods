from queue import Queue

#Definindo o espaço vazio
Espaco_Vazio = None

#Definindo o estado objetivo
Estado_Objetivo = [1, 2, 3, 
                   4, 5, Espaco_Vazio, 
                   6, 7, 8]

#Função que define Distancia de Manhattan
def HeuristicaManhattan(estado_atual):
    distancia_valores = 0
    for x, valor in enumerate(estado_atual):
        if valor != Espaco_Vazio:#se valor diferente de Espaco_Vazio
            valor_estado_objetivo_posicao_linha = (valor-1) / 3#pega o numero de posições e subtrai 1 e divide por 3 e 
            #retorna a posição na linha em que esta posicionado
            valor_estado_objetivo_posicao_coluna = (valor-1) % 3#verifica o valor do estado objetivo 
            #e coluna que esta posicionado
            posicao_estado_atual_linha = x / 3#verifica a posição do estado atual e linha onde es ta
            posicao_estado_atual_coluna = x % 3#verifica a posição do estado atual e coluna onde esta
            distancia_valores += (valor_estado_objetivo_posicao_linha - posicao_estado_atual_linha) + (valor_estado_objetivo_posicao_coluna - posicao_estado_atual_coluna)
            #Aqui utilizando a função abs para pegar o valor absoluto da distancia entre o estado atual até o estado objetivo
    return distancia_valores
    #Retorna valor absoluto da distancia

#gera sucessores
def gera_sucessores1(estado):
    sucessores = []
    Indice_Espaco_Vazio = estado.index(Espaco_Vazio)
    
    #Para movimentar o Indice Espaco_Vazio para cima
    if Indice_Espaco_Vazio > 2:
        novo_estado = estado[:]
        novo_estado[Indice_Espaco_Vazio], novo_estado[Indice_Espaco_Vazio - 3] = novo_estado[Indice_Espaco_Vazio - 3], novo_estado[Indice_Espaco_Vazio]
        sucessores.append((novo_estado, HeuristicaManhattan(novo_estado)))

    #Para movimentar o Indice Espaco_Vazio para baixo
    if Indice_Espaco_Vazio < 6:
        novo_estado = estado[:]
        novo_estado[Indice_Espaco_Vazio], novo_estado[Indice_Espaco_Vazio + 3] = novo_estado[Indice_Espaco_Vazio + 3], novo_estado[Indice_Espaco_Vazio]
        sucessores.append((novo_estado, HeuristicaManhattan(novo_estado)))

    #Para movimentar o Indice Espaco_Vazio para o lado da esquerda
    if Indice_Espaco_Vazio % 3 != 0:
        novo_estado = estado[:]
        novo_estado[Indice_Espaco_Vazio], novo_estado[Indice_Espaco_Vazio - 1] = novo_estado[Indice_Espaco_Vazio - 1], novo_estado[Indice_Espaco_Vazio]
        sucessores.append((novo_estado, HeuristicaManhattan(novo_estado)))

    #Para movimentar o Indice Espaco_Vazio para o lado da direita
    if (Indice_Espaco_Vazio + 1) % 3 != 0:
        novo_estado = estado[:]
        novo_estado[Indice_Espaco_Vazio], novo_estado[Indice_Espaco_Vazio + 1] = novo_estado[Indice_Espaco_Vazio + 1], novo_estado[Indice_Espaco_Vazio]
        sucessores.append((novo_estado, HeuristicaManhattan(novo_estado)))
    return sorted(sucessores, key=lambda x: x[1])

#Função de Busca Gulosa que utiliza Heuristica de Manhattan e é chamada de bgl   
def bgl(estado_inicial):
    visitados = set()#coleção de estados visitados
    fila = Queue()#Cria uma fila
    fila.put((HeuristicaManhattan(estado_inicial), estado_inicial, []))
    #Aqui adiciona o estado inicial e caminho na fila odenados por Manhattan
    while not fila.empty():
        #Se a fila não estiver vazia
        _, estado, caminho = fila.get()
        if estado == Estado_Objetivo:#vai verificar se o estado atual é igual ao estado objetivo e se for
            return caminho#retorna o caminho para o mesmo
        if tuple(estado) not in visitados:#Caso não seja igual o estado objetivo
            visitados.add(tuple(estado))#adiciona como visitado
            for sucessor, h in gera_sucessores1(estado):#vai gerar os sucessores
                if tuple(sucessor) not in visitados:#e vai verificar se não é visitado
                    fila.put((h, sucessor, caminho + [sucessor]))#se não adiciona na fila
    return None

#Função de busca A* mas que esta nomeada como A.
def A(estado_inicial):
    visitados = set()#coleção de estados visitados
    fila = Queue()#Cria uma fila
    fila.put((HeuristicaManhattan(estado_inicial), estado_inicial, []))
    #Aqui adiciona o estado inicial e caminho na fila odenados por Manhattan
    while not fila.empty():
        #Se a fila não estiver vazia
        _, estado, caminho = fila.get()#_ variavel não é usada
        if estado == Estado_Objetivo:#vai verificar se o estado atual é igual ao estado objetivo e se for
            return caminho#retorna o caminho para o mesmo
        if tuple(estado) not in visitados:#Caso não seja igual o estado objetivo
            visitados.add(tuple(estado))#adiciona como visitado
            for sucessor, h in gera_sucessores1(estado):#vai gerar os sucessores
                if tuple(sucessor) not in visitados:#e vai verificar se não é visitado
                    fila.put((h + len(caminho), sucessor, caminho + [sucessor]))#se não adiciona o caminho na fila
    return None

#Para o usuario digitar o estado inicial-+
estado_inicial = []
print("Digite o estado inicial do quebra-cabeça, linha por linha, utilizando o número 1-8 para as peças e o caractere '-' para o espaço Espaco_Vazio.")

#Para printar o caminho em formato de matriz
for i in range(3):
    linha = input(f"Linha {i + 1}: ").strip().split()
    estado_inicial.extend(linha)

#definir estado inicial e simbolo para o espaço vazio
estado_inicial = [int(x) if x != '-' else None for x in estado_inicial]

caminho = bgl(estado_inicial)#Chama a função de busca gulosa

#Para Verificar se tem solução
#se não tiver solução não foi emcontrada
if caminho is None:
    print("Não foi encontrada uma solução.")
    #senão 
else:
    #Printa o estado inicial e o caminho até o estado objetivo
    print("Estado inicial:")
    for i in range(0, 9, 3):#0 é inicio da iteração 9 é final e 3 o intervalo das iterações
        print(estado_inicial[i:i+3])
    print("Caminho até o estado objetivo:")
    for estado in caminho:
        for i in range(0, 9, 3):
            print(estado[i:i+3])
        print()
