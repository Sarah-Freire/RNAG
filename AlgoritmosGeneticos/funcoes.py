def funcao_objetivo_caixa_binaria(individuo):
    ''' Computa a função objetivo no problema das caixas binárias.
    
        Args:
            individuo: lista contendo os genes das caixas binárias
    
        Return:
        Um valor representando a soma dos genes do individuo
    '''
    return sum(individuo) 
