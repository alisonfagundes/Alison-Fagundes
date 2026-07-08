import random
import os

""" (DEFINIÇÃO DE CORES) """
# COR  = "\033[cor fundo\033[cor texto"
VERDE = "\033[42m\033[30m"  # fundo verde --> texto preto
AMARELO = "\033[43m\033[30m"  # fundo amarelo --> texto preto
CINZA = "\033[100m\033[97m"  # fundo cinza --> texto branco
RESET = "\033[0m"  # Deixa "normal" dnv
NEGRITO = "\033[1m"

PALAVRAS_FACIL = [
    "BOLO", "CASA", "GATO", "PATO", "SOPA", "LAGO", "FOGO", "MAPA",
    "PELE", "BOCA", "DEDO", "MESA", "NOME", "OLHO", "RATO", "SINO",
    "TETO", "URSO", "VALE", "AMOR", "COPO", "FLOR", "HORA", "ILHA",
    "JOGO", "MEDO", "VELA", "PANO", "CAMA", "FITA",
]

PALAVRAS_MEDIO = [
    "BRISA", "CALMA", "GLOBO", "HOTEL", "LIVRE", "MUNDO", "NINHO",
    "PEDRA", "RISCO", "SABOR", "BANCO", "CHUVA", "PRAIA",   
    "TIGRE", "VINHO", "PONTO", "AREIA", "FORCA", "TROCA",
]

PALAVRAS_DIFICIL = [
    "ABISMO", "ENIGMA", "GLORIA", "LOGICA","NOMADE", "ANCORA",
    "BENCAO", "GENERO", "MODULO","REPTIL", "SOLIDO", "BASICO",
    "CODIGO", "DECIMO",
]

# Limite de tentativas por nível
TENTATIVAS_FACIL = 6
TENTATIVAS_MEDIO = 5
TENTATIVAS_DIFICIL = 4

# FUNÇÕES AUXILIARES:
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

#pausa para poder ler o que está na tela
def pausar():
    input("\nPressione Enter para continuar...")

def escolher_palavra(nivel):
    if nivel == "1":
        return random.choice(PALAVRAS_FACIL)
    elif nivel == "2":
        return random.choice(PALAVRAS_MEDIO)
    else:
        return random.choice(PALAVRAS_DIFICIL)

def limite_de_tentativas(nivel):
    if nivel == "1":
        return TENTATIVAS_FACIL
    elif nivel == "2":
        return TENTATIVAS_MEDIO
    else:
        return TENTATIVAS_DIFICIL


def nome_do_nivel(nivel):
    nomes = {"1": "Fácil", "2": "Médio", "3": "Difícil"}
    return nomes[nivel]



#   LÓGICA DE AVALIAÇÃO

def avaliar(tentativa, palavra):
    resultado = []
    letras_restantes = list(palavra)  #Separa a palavra em letras "soltas"

    estado = ["ausente"] * len(tentativa) #Atribui o estado inicial de "ausente" para todas as letras da palavra

    for i in range(len(tentativa)): #"Converte" o número de caracteras da palavra tentada, no número de vezes que vai "rodar o código"

        if tentativa[i] == palavra[i]: #Compara os caracteres da msm posição, na palavra correta e na palavra escrita
            estado[i] = "certo" #Altera o estado do caractere na casa indicada de "ausente" para "certo" dentro da lista "estado"
            letras_restantes[i] = None  #Vai substituir o caractere da posição por "none", para que evitar que na próxima etapa ele seja contado novamente quando for comparado


    for i in range(len(tentativa)):
        if estado[i] == "certo": #Verifica se o caractere já está marcado como "certo"
            continue #termina essa repetição e começa a próxima
        if tentativa[i] in letras_restantes: #Se o caractere da posição estiver dentro da lista "letras_restantes"
            estado[i] = "presente"
            letras_restantes[letras_restantes.index(tentativa[i])] = None #Procura a posição em que está o caractere analisado e substitui por "none", para evitar erro na próxima análise

    for i in range(len(tentativa)):
        resultado.append((tentativa[i], estado[i])) #Junta o caractere com seu respectivo resultado após as análises

    return resultado



#Função para mostrar as letras com cores
def mostrar_tentativa(resultado):
    linha = ""
    for letra, estado in resultado: #"Desempacota" cada par, colocando o caractere na variável "letra" e o status na "estado"
        if estado == "certo":
            linha += VERDE + " " + letra + " " + RESET
        elif estado == "presente":
            linha += AMARELO + " " + letra + " " + RESET
        else:
            linha += CINZA + " " + letra + " " + RESET
    print("  " + linha)



#FUNÇÃO "PRINCIPAL"
def jogar(palavra, max_tentativas): #Se o parâmetro "max_tentativas" receber "none" é pq o modo é sem limites de tentativas
    tentativas_feitas = [] #Guarda o histórico de palavras que foram tentadas

    while True: #Mantém o jogo rodando até receber um "return"
        limpar_tela()

        #Mostrar as tentativas anteriores
        print()
        for resultado in tentativas_feitas: #Para cada palavra tentada/conferida e salva dentro da variável "resultado" ele já vai mostrar formatada para o jogador
            mostrar_tentativa(resultado)

        #Mostrar linhas vazias
        if max_tentativas is None:
            linhas_vazias = 3
        else:
            linhas_vazias = max_tentativas - len(tentativas_feitas) #Subtrai a quantidade de chances pela quantidade de tentativas

        for _ in range(min(linhas_vazias, 6)): #Permite que mostre no máximo 6 linhas vazias
            print("  " + CINZA + "   " * len(palavra) + RESET) # "*len(palavra)" ---> indica a quantidade de colunas que terá nos espaços vazios

        print()


        #Informações das tentativas
        if max_tentativas is None:
            print(f"  Tentativas usadas: {len(tentativas_feitas)}  (sem limite)")
        else:
            restam = max_tentativas - len(tentativas_feitas)
            print(f"  Tentativas restantes: {restam}")


        #Verificação para ver se esgotou as tentativas
        if max_tentativas is not None and len(tentativas_feitas) >= max_tentativas: #Verifica se a quant. de tentativas importa e compara em relação ao número de tentativas feitas
            print(f"\n  Suas tentativas acabaram! A palavra era: {NEGRITO}{palavra}{RESET}")
            pausar() #ajudar a ler o código antes de apagar a tela
            return -1 #Retorna o código para sinaliazar que o jogador perdeu

        #Pede a tentativa
        print()
        entrada = input(f"  Digite uma palavra com {len(palavra)} letras: ").upper().strip()

        if len(entrada) != len(palavra): #Verifica se o que foi escrito tem o msm número de caracteres
            input(f"  A palavra precisa ter {len(palavra)} letras! Enter para tentar de novo...")
            continue #Volta para o início da rodada sem contar a tentativa

        if not entrada.isalpha():
            input("  Use apenas letras! Enter para tentar de novo...")
            continue

        #Avalia e guarda
        resultado = avaliar(entrada, palavra) #Chama a função "avaliar" para analisar o palpite do usuário
        tentativas_feitas.append(resultado) #Adiciona o resultado do palpite analisado na lista "tentativas_feitas", para que possa ser contabilizado e mostrado na roda seguinte

        #Verifica se o palpite é igual a palavra sorteada
        if entrada == palavra:
            limpar_tela()
            print()
            for r in tentativas_feitas: #Mostrar as tentativas que o usuário fez antes de acertar
                mostrar_tentativa(r)

            n = len(tentativas_feitas)
            print(f"\n  Você acertou em {n} tentativa(s)! A palavra era: {NEGRITO}{palavra}{RESET}")
            pausar()
            return n




#MENU DE NÍVEL
def menu_nivel():
    print("  Escolha o nível:\n")
    print("  1. Fácil    (palavras curtas, 6 tentativas)")
    print("  2. Médio    (palavras médias, 5 tentativas)")
    print("  3. Difícil  (palavras longas, 4 tentativas)")
    print()

    while True:
        nivel = input("  Opção (1-3): ").strip()
        if nivel in ["1", "2", "3"]:
            return nivel
        print("  Opção inválida, tente de novo.")


#MENU DE TENTATIVAS
def menu_tentativas(nivel):
    limite = limite_de_tentativas(nivel)
    print(f"\n  Modo de tentativas:\n")
    print(f"  1. Com limite  ({limite} tentativas)")
    print(f"  2. Sem limite  (conta as tentativas, mas não elimina)")
    print()

    while True:
        op = input("  Opção (1 ou 2): ").strip()
        if op == "1":
            return limite
        elif op == "2":
            return None
        print("  Opção inválida.")




#MODO SOLO
def modo_solo():
    limpar_tela()
    print("\n  === MODO SOLO ===\n")

    nivel = menu_nivel() #Função de escolher o nível
    max_tent = menu_tentativas(nivel) #Função de conf. tentativas
    palavra = escolher_palavra(nivel) #Função de sortear palavras

    jogar(palavra, max_tent) #Função para iniciar o jogo




#MODO MULTIPLAYER
def modo_multiplayer():
    limpar_tela()
    print("\n  === MODO MULTIPLAYER ===\n")

    #Cadastro de jogadores
    while True:
        try:
            quantidade = int(input("  Quantos jogadores? (2 a 6): "))
            if 2 <= quantidade <= 6:
                break
            print("  Entre 2 e 6 jogadores.")
        except ValueError: #Não deixa o erro aparecer para o usuário
            print("  Digite um número.")

    nomes = []
    for i in range(quantidade): #O loop se repete uma quantidade de vezes numericamente igual ao número de jogadores
        nome = input(f"  Nome do jogador {i + 1}: ").strip()
        if nome == "":
            nome = f"Jogador {i + 1}"
        nomes.append(nome) #Junta o nome do ciclo à lista com todos os nomes

    nivel = menu_nivel() #Função de escolher o nível
    max_tent = menu_tentativas(nivel) #Função de escolher o número de tentativas

    #Sorteia uma palavra diferente para cada jogador
    if nivel == "1":
        pool = PALAVRAS_FACIL #A variável "pool" passa a carregar a lista de palavras fáceis
    elif nivel == "2":
        pool = PALAVRAS_MEDIO #A variável "pool" passa a carregar a lista de palavras médias
    else:
        pool = PALAVRAS_DIFICIL #A variável "pool" passa a carregar a lista de palavras difíceis

    random.shuffle(pool) #Embaralhamento das palavras
    palavras = []
    for i in range(quantidade): #Analisa a quantidade de jogadores e repete esse loop a quantidade que tiver
        palavras.append(pool[i % len(pool)]) #Garante que sempre vai existir palavras para todos os jogadores, msm que repetidas

    #Guardar resultados
    resultados = []  #lista de (nome, tentativas_usadas, venceu)

    for i in range(quantidade):
        limpar_tela()
        print(f"\n  Vez de {NEGRITO}{nomes[i]}{RESET}")
        input("  Olhem para o lado! Pressione Enter quando estiver pronto...")

        tentativas_usadas = jogar(palavras[i], max_tent)
        venceu = tentativas_usadas != -1
        resultados.append((nomes[i], tentativas_usadas, venceu))

    # Placar final
    limpar_tela()
    print("\n  === PLACAR FINAL ===\n")



    vencedores = []
    perdedores = []

#Separar quem ganhou de quem perdeu
    for jogador in resultados:
        nome = jogador[0]
        tentativas = jogador[1]
        venceu = jogador[2]

        if venceu == True:
            vencedores.append(jogador)
        else:
            perdedores.append(jogador)

#Ordenar os vencedores
    def pegar_tentativas(jogador):
        return jogador[1]

    vencedores.sort(key=pegar_tentativas)
    todos_jogadores = vencedores + perdedores

    medalhas = ["1o", "2o", "3o", "4o", "5o", "6o"]
    posicao_da_medalha = 0

    for jogador in todos_jogadores:
        nome = jogador[0]
        tent = jogador[1]
        venceu = jogador[2]

        med = medalhas[posicao_da_medalha]

        if venceu == True:
            print(f"  {med}. {nome}  —  {tent} tentativa(s)")
        else:
            print(f"  {med}. {nome}  —  não acertou")

        posicao_da_medalha += 1

    pausar()



#MODO TORNEIO
def modo_torneio():
    limpar_tela()
    print("\n  === MODO TORNEIO ===\n")
    print("  Você vai jogar os 3 níveis em sequência, sem limite de tentativas.")
    print("  O objetivo é acertar tudo usando o menor número total de tentativas.\n")
    pausar()

    nome = input("\n  Seu nome: ").strip()
    if nome == "":
        nome = "Jogador"

    niveis = ["1", "2", "3"]
    total_tentativas = 0
    tentativas_por_nivel = {} #Dicionário

    for nivel in niveis:
        palavra = escolher_palavra(nivel) #Função de sortear uma palavra
        nome_nivel = nome_do_nivel(nivel) #Dicionário com os níveis

        limpar_tela()
        print(f"\n  TORNEIO — Nível {nome_nivel}")
        print(f"  Palavra com {len(palavra)} letras  |  sem limite de tentativas\n")
        pausar()

        tentativas_usadas = jogar(palavra, None)  #"None"= sem limite
        total_tentativas += tentativas_usadas
        tentativas_por_nivel[nome_nivel] = tentativas_usadas

        #Mostrar progresso
        limpar_tela()
        print(f"\n  Progresso de {nome}:\n")
        for n, t in tentativas_por_nivel.items(): #O ".itens()" permite que o for pegue duas coisas ao msm tempo e atribua as variáveis "n" e "t"
            print(f"  {n}: {t} tentativa(s)") #"n" é referente ao nome do nível e "t" ao número de tentativas
        pausar()

    # Resultado final
    limpar_tela()
    print(f"\n  === RESULTADO DO TORNEIO — {nome} ===\n")
    for n, t in tentativas_por_nivel.items():
        print(f"  {n}: {t} tentativa(s)") #O ".itens()" permite que o for pegue duas coisas ao msm tempo e atribua as variáveis "n" e "t"
    print(f"\n  Total: {total_tentativas} tentativas")

    if total_tentativas <= 10:
        print("  Desempenho: LENDÁRIO!")
    elif total_tentativas <= 15:
        print("  Desempenho: EXCELENTE!")
    elif total_tentativas <= 22:
        print("  Desempenho: BOM!")
    elif total_tentativas <= 30:
        print("  Desempenho: REGULAR")
    else:
        print("  Desempenho: INICIANTE (continue praticando!)")

    pausar()



#TELA DE AJUDA
def tela_ajuda():
    limpar_tela()
    print(f"""
  === COMO JOGAR ===

  Adivinhe a palavra secreta!
  Após cada tentativa, cada letra recebe uma cor:

    {VERDE} A {RESET}  Letra CERTA no lugar CERTO
    {AMARELO} B {RESET}  Letra CERTA no lugar ERRADO
    {CINZA} C {RESET}  Letra AUSENTE na palavra

  NÍVEIS:
    Fácil    — palavras curtas,  6 tentativas
    Médio    — palavras médias,  5 tentativas
    Difícil  — palavras longas,  4 tentativas

  TORNEIO:
    Você joga os 3 níveis em sequência.
    Sem limite de tentativas — o objetivo é
    acertar tudo com o menor total possível.

  MULTIPLAYER:
    Cada jogador recebe uma palavra diferente.
    Vence quem acertar em menos tentativas.
""")
    pausar()




#MENU PRINCIPAL
def menu_principal():
    while True:
        limpar_tela()
        print(f"""
  ================================
       W O R D L E  TERMINAL
  ================================

  1. Solo
  2. Multiplayer
  3. Torneio
  4. Como jogar
  0. Sair
""")
        opcao = input("  Escolha uma opção: ").strip()

        if opcao == "1":
            modo_solo()
        elif opcao == "2":
            modo_multiplayer()
        elif opcao == "3":
            modo_torneio()
        elif opcao == "4":
            tela_ajuda()
        elif opcao == "0":
            limpar_tela()
            print("\n  Até a próxima!\n")
            break
        else:
            input("  Opção inválida. Enter para tentar de novo...")



#COMEÇAR O PROGRAMA
menu_principal()