# uma dica para resolver os problemas é dividi-lo em várias funções menores que resolvem uma pequena parte do problema
# devemos escrever primeiro em palavras e depois em código
# para a função não bugar quando estiver vazia é importante utilizar o pass


import random

######### GENES #########

def gene_caixa_binaria():
    ''' Gera um gene válido para o problema das caixas binárias.
    
        Return:
            Um valor zero ou um.
    '''
    lista = [0,1]
    gene = random.choice(lista)
    return gene

# novo
def gene_cnb(valor_max_caixa):
    ''' Gera um gene válido para o problema das caixas não-binárias
    
    Args:
        valor_max_caixa: valor máximo que a caixa pode assumir, (sendo um número inteiro)
        
    Return:
        Um valor entre zero e 'valor_max_caixa'(inclusive).
    '''
    gene = random.randint(0, valor_max_caixa)
    return gene

# novo
def gene_letra(letras):
    '''Sorteia "aleatoriamente" uma letra.
    
    Args:
        letras: letras passíveis de serem sorteadas.
        
    Return:
        retorna uma das letras possíveis de serem sorteadas.
    '''
    letra = random.choice(letras)
    return letra


######### INDIVÍDUOS ########


def individuo_caixa_binaria(n):
    ''' Gera um indivíduo para o problema das caixas binárias.
        
        Args:
            n: número de genes do indivíduo.
        
        Return:
            Uma lista com n genes. Cada gene é um valor zero ou um.
    '''
    individuo = []
    for i in range(n):
        gene = gene_caixa_binaria()
        individuo.append(gene)
    return individuo


# novo
def individuo_cnb(n_genes, valor_max_caixa):
    '''Cria indivíduos para o problema das caixas não-binárias.
    
    Args:
        n_genes: número de genes do indivíduo.
        valor_max_caixa: maior número inteiro possível dentro de uma caixa
        
    Return: 
        Uma lista com n genes. Cada gene é um valor entre zero e valor_max_caixa
    '''
    individuo = []
    for i in range(n_genes):
        gene = gene_cnb(valor_max_caixa)
        individuo.append(gene)
    return individuo

# novo
def individuo_senha(tamanho_senha, letras):
    '''Cria uma possível resposta para o problema
    
    Args:
    tamanho_senha: número inteiro que representa o tamanho da senha a ser gerada.
    letras: letras que podem ser sorteadas para formarem essa senha
    
    Return:
    lista(possível resposta) com n letras conforme o tamanho definido antes.
    '''
    
    candidato = []
    
    for n in range(tamanho_senha):
        candidato.append(gene_letra(letras))
        
    return candidato


######## POPULAÇÃO ########



def populacao_caixa_binaria(tamanho, n):
    ''' Cria uma população no problema das caixas binárias.
    
    Args:
        tamanho: tamanho da população.
        n: número de genes de um indivíduo.
        
    Returns:
        Uma lista onde cada item é um indivíduo. Um indivíduo é uma lista com n genes.
        '''
    populacao = []
    for _ in range(tamanho):
        populacao.append(individuo_caixa_binaria(n))
    return populacao

# novo
def populacao_cnb(tamanho, n_genes, valor_max_caixa):
    '''Cria uma população para problema das caixas não-binárias.
    
    Args:
        tamanho: tamanho dessa população.
        n_genes: número de genes de cada um doss indivíduos dessa população.
        valor_max_caixa: maior número inteiro possível dentro de uma caixa
    
    Returns:
        Uma lista onde cada item é um indivíduo. Um indivíduo é uma lisca com n_genes genes.
    '''
    populacao = []
    for _ in range(tamanho):
        populacao.append(individuo_cnb(n_genes, valor_max_caixa))
    return populacao

# novo
def populacao_inicial_sennha(tamanho, tamanho_senha, letras):
    '''Cria "população inicial" no problema da senha, ou seja, várias possíveis soluções iniciais
    
    Args:
        tamanho: tamanho da população do problema.
        tamanho_senha: número inteiro que representa o tamanho da senha.
        letras: letras possíveis de serem sorteadas.
        
    Returns;
        Lista com todos os indivíduos da população no problema da senha.
    '''
    populacao = []
    for n in range(tamanho):
        populacao.append(individuo_senha(tamanho_senha, letras))
    return populacao


######## SELEÇÃO ########

        

def selecao_roleta_max(populacao, fitness):
    ''' Seleciona individuos de uma população usando o método da roleta.
    
    Nota: apenas funciona para problemas de maximização.
    
    Args:
        populacao: lista com todos os indivíduos da população.
        fitness: lista com o valor da função objetivo dos indivíduos da população.
        
    Returns:
        População dos indivíduos selecionados.
    '''
    populacao_selecionada = random.choices(populacao, weights=fitness, k=len(populacao))
    return populacao_selecionada

# novo
def selecao_torneio_min(populacao, fitness, tamanho_torneio = 3):
    '''Faz a seleção de uma população usando torneio entre as opções para ficar com a resposta que mais se aproxima da solução real
    
    Nota: da maneira em que aqui fui implementada essa função só funcionará em problemas de minimização
    
    Args:
        populacao: população do problema
        fun_objectivo: função objetivo
        tamanho_torneio: quantidade de individuos que competem entre si.

    Return:
        Individuos selecionados. Lista com os indivíduos selecionados com mesmo tamanho do argumento 'populacao'.
    '''
    selecionados = []
    
    # variável que associa cada indivíduo com seu valor de fitness
    par_populacao_fitness = list(zip(populacao, fitness))
    
    # len(populacao) torneios!
    for _ in range(len(populacao)):
        combatentes = random.sample(par_populacao_fitness, tamanho_torneio)
        
        # infinito
        minimo_fitness = float("inf")

        for par_individuo_fitness in combatentes:
            individuo = par_individuo_fitness[0]
            fit = par_individuo_fitness[1]

            # selecionando o individuo com o menos fitness
            if fit < minimo_fitness:
                selecionado = individuo
                minimo_fitness = fit

        selecionados.append(selecionado)
    return selecionados


######## CRUZAMENTO ########


def cruzamento_ponto_simples(pai, mae):
    '''Operador de cruzamento de ponto simples.
    
    Args:
        pai: uma lista representando um indivíduo
        mae: uma lista representando um indivíduo
    
    Returns:
        Duas listas, sendo que cada uma representa um filho dos pais que foram os argumentos.
        '''
    ponto_de_corte = random.randint(1, len(mae)-1)
    
    filho1 = pai[:ponto_de_corte] + mae[ponto_de_corte:]
    filho2 = mae[:ponto_de_corte] + pai[ponto_de_corte:]
    
    return filho1,filho2


######## MUTAÇÃO ########


def mutacao_cb(individuo):
    ''' Realiza a mutação de um gene no problema das caixas binárias.
    
    Args:
        individuo: uma lista representando um individuo no problema das caixas binárias.
        
    Return:
        Um indivíduo com um gene mutado.
    '''
    gene_a_ser_mutado = random.randint(0, len(individuo)- 1)
    individuo[gene_a_ser_mutado] = gene_caixa_binaria()
    return individuo

# novo
def mutacao_cnb(individuo, valor_max_caixa):
    '''Realiza a mutação de um gene no problema das caixas não-binárias
    
    Args:
        individuo:uma lista representando um individuo no problema das caixas não-binárias
        valor_max_caixa: maior número inteiro possível dentro de uma caixa.
        
    Return:
        Um indivíduo com um gene mutado.
    '''
    gene_a_ser_mutado = random.randint(0, len(individuo)-1)
    individuo[gene_a_ser_mutado] = gene_cnb(valor_max_caixa)
    return individuo

# novo
def mutacao_senha(individuo, letras):
    '''Realiza a mutação de um gene no problema da senha.
    
    Args: 
        individuo: uma lista representando um indivíduo no problema da senha
        letras: letras possíveis de serem sorteadas.
        
    Return:
        Um individuo (senha) com um gene mutado.
    '''
    gene = random.randint(0, len(individuo)-1)
    individuo[gene] = gene_letra(letras)
    return individuo



######## FUNÇÃO OBJETIVO- indivíduos ########


def funcao_objetivo_caixa_binaria(individuo):
    ''' Computa a função objetivo no problema das caixas binárias.
    
        Args:
            individuo: lista contendo os genes das caixas binárias
    
        Return:
        Um valor representando a soma dos genes do individuo
    '''
    return sum(individuo) + 1

# novo
def funcao_objetivo_cnb(individuo):
    '''Roda a função objetivo no problema das caixas não-binárias.
    
    Args:
        individuo: lista contendo os genes das caixas não-binárias.
        
    Return:
        Um valor representando a soma dos genes do individuo.
    '''
    return sum(individuo)

# novo
def funcao_objetivo_senha(individuo, senha_verdadeira):
    '''Computa a função objetivo de um individuo no problema da senha
    
    Args:
        individuo: lista contendo as letras da senha.
        senha_verdadeira: a senha que você está tentando descobrir.
        
    Returns:
        A "distância" entre a senha proposta e a senha verdadeira. Essa distância é medida letra por letra. Quanto mais distante uma letra for da letra que ela deveria ser, maior é essa distância. 
    '''
    diferenca = 0
    
    for letra_candidato, letra_oficial in zip(individuo, senha_verdadeira):
        diferenca = deferenca + abs(ord(letra_candidato) - ord(letra_oficial))
        
    return diferenca




######## FUNÇÃO OBJETIVO- população #########


def funcao_objetivo_pop_cb(populacao):
    ''' Calcula a função objetivo para todos os membros de uma população
    
    Args: 
        populacao: lista com todos os indivíduos da população.
    
    Return:
        lista de valores representando a fitness de cada individuo da população.
    '''
    fitness = []
    for individuo in populacao:
        fobj = funcao_objetivo_caixa_binaria(individuo)
        fitness.append(fobj)
    return fitness

# novo
def funcao_objetivo_pop_cnb(populacao):
    '''Calcula a função objetivo para todos os membros de uma população
    
    Args:
        população: lista com todos os indivíduos da população
        
    Return:
        Lista de valores representando o fitness de cada indivíduo da população.
    '''
    fitness = []
    for individuo in populacao:
        fobj = funcao_objetivo_cnb(individuo)
        fitness.append(fobj)
    return fitness

# novo
def funcao_objetivo_pop_senha(populacao, senha_verdadeira):
    '''Calcula a função objetivo de uma população no problema da senha.
    
    Args:
        populacao: lista com todos os indivíduos da população
        senha_verdadeira: a senha que você quer encontrar
        
    Returns:
        Lista contendo os valores da métrica de distância entre senhas.
    '''
    resultado = []
    
    for individuo in populacao:
        resultado.append(funcao_objetivo_senha(individuo, senha_verdadeira))
        
    return resultado

