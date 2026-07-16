alfa = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' #String com todas as letras(maiúsculas) do alfabeto

def todas_intersecoes(t):
    '''
    Esta função recebe um território e retorna um tuplo
    com todas as interseções do mesmo.
    '''
    intersecoes = ()
    for i in range(len(t)): # i corresponde às colunas do território
        for j in range(1 , len(t[0])+1): # j corresponde às linhas do território
            intersecoes += ((alfa[i] , j),)
    return intersecoes


def eh_territorio(arg): 
    """
    eh_territorio: universal → booleano
    Esta função recebe um argumento de qualquer tipo e devolve True se o argumento 
    corresponder a um território, caso contrário devolve False, sem gerar erros.
    """
    if not (isinstance(arg , tuple) and 0<len(arg)<=26):
        return False
    for i in arg:
        if not (isinstance(i , tuple) and 1<=len(i)<=99): 
            return False
        elif len(i) != len(arg[0]):
            return False        
        for j in i: 
            if not (type(j) == int and (j==0 or j==1)):
                return False
    return True 


def obtem_ultima_intersecao(t):
    '''
    obtem_ultima_intersecao: territorio → intersecao
    Esta função recebe um território e devolve a interseção do seu 
    extremo superior direito
    '''
    return (alfa[len(t)-1] , len(t[0]))


def eh_intersecao(arg):
    '''
    eh_intersecao: universal → booleano
    Esta função recebe um argumento de qualquer tipo e devolve True se o argumento 
    corresponder a uma interseção, caso contrário devolve False
    '''
    if not (isinstance(arg , tuple) and len(arg)==2 and isinstance(arg[0] , str)): 
        return False
    if not (len(arg[0])==1 and arg[0] in alfa and type(arg[1])==int  and 1<=arg[1]<=99):
        return False
    return True 



def eh_intersecao_valida(t , i): 
    '''
    eh_intersecao_valida: territorio x intersecao → booleano
    Esta função recebe um território e uma interseção,
    se a interseção pertencer ao território devolve True,
    caso contrário devolve False.
    '''
    if eh_intersecao(i) and i[0] in alfa[:len(t)] and 0<i[1]<=len(t[0]):                  
        return True 
    return False


def eh_intersecao_livre(t,i):
    '''
    eh_intersecao_livre: territorio × intersecao → booleano
    Esta função recebe um território e uma interseção do mesmo e
    devolve True se a interseção for livre (não ocupada por uma montanha),
    caso contrário devolve False
    '''
       #[índice do tuplo][índice do subtuplo]    
    if t[alfa.index(i[0])][i[1]-1] == 0: 
        return True                  
    return False



def obtem_intersecoes_adjacentes(t,i):
    '''
    obtem_intersecoes_adjacentes: territorio × intersecao → tuplo
    Esta função recebe um território e uma interseção do mesmo
    e devolve um tuplo formado pelas interseções válidas adjacentes 
    da interseção escolhida em ordem de leitura.
    '''
    novo_tuplo = () 
         
    if eh_intersecao_valida(t,(i[0] , i[1]-1)): # interseção de baixo
        novo_tuplo += ((i[0] , i[1]-1),)
        
    if eh_intersecao_valida(t,(alfa[alfa.index(i[0])-1] , i[1])): # interseção da esquerda
        novo_tuplo += ((alfa[alfa.index(i[0])-1] , i[1]),)

    if alfa.index(i[0])+1<=25 and eh_intersecao_valida(t,(alfa[alfa.index(i[0])+1] , i[1])): # interseção da direita
        novo_tuplo += ((alfa[alfa.index(i[0])+1] , i[1]),) 

    if eh_intersecao_valida(t,(i[0] , i[1]+1)): # interseção de cima
        novo_tuplo+= ((i[0] , i[1]+1),)
    return novo_tuplo



def ordena_intersecoes(tup): 
    '''
    ordena_intersecoes: tuplo → tuplo
    Esta função recebe um tuplo com interseções e devolve um tuplo com as 
    mesmas interseções ordenadas por ordem de leitura do território.
    (o tuplo pode ser vazio)
    '''
    return tuple(sorted(tup, key=lambda x: (x[1] , x[0])))


def territorio_para_str(t):
    '''
    territorio_para_str: territorio → cad
    Esta função recebe um território e devolve a cadeia de caracteres 
    que o representa(representação externa)
    Se o argumento for inválido, a função gera um erro
    '''
    if not eh_territorio(t):
        raise ValueError('territorio_para_str: argumento invalido')
    
    # 1ª linha
    string = '  '
    for i in range(len(t)):
        string += f' {alfa[i]}'
    string +='\n'
    
    # Linhas do meio    
    for i in range(len(t[0])-1 , -1 , -1): 
        if i+1>=10:   # caso o território tenha 10 ou mais linhas
            string += f'{str(i+1)}'

            for j in range(len(t)):
                if t[j][i] == 1:
                    string += f' X'
                else:
                    string += f' .'
            string +=  f' {str(i+1)}\n' 
        else:
            string += f' {str(i+1)}'
            for j in range(len(t)):
            
                if t[j][i] == 1:
                    string += f' X'
                else:
                    string += f' .'
            string += f'  {str(i+1)}\n'

    # Ultima linha
    string += '  '
    for i in range(len(t)):
        string += f' {alfa[i]}'
    return string



def obtem_cadeia(t,i):
    '''
    obtem_cadeia: territorio × intersecao → tuplo
    Esta função recebe um território e uma interseção (livre ou não) do mesmo e devolve 
    um tuplo formado por essa interseção e por todas as interseções conectadas a ela,
    ordenadas por ordem de leitura.
    Se algum dos argumentos for inválido, a função gera um erro.
    '''
    if not (eh_territorio(t) and eh_intersecao_valida(t,i)):
        raise ValueError('obtem_cadeia: argumentos invalidos')
    
    cadeia = ((i),)
    valor = True
    while valor:      
        valor = False  
        if t[alfa.index(i[0])][i[1]-1] == 1: # se a interseção escolhida tiver uma montanha
            for j in cadeia: 
                for k in obtem_intersecoes_adjacentes(t,j): 
                    if not eh_intersecao_livre(t,k) and k not in cadeia:
                        cadeia += (k,)
                        valor = True
        else:
            for j in cadeia:
                for k in obtem_intersecoes_adjacentes(t,j):
                    if eh_intersecao_livre(t,k) and k not in cadeia:
                        cadeia += (k,) 
                        valor = True
    return ordena_intersecoes(cadeia)



def obtem_vale(t,i):
    '''
    obtem_vale: territorio × intersecao → tuplo
    Esta função recebe um território e uma interseção do mesmo
    ocupada por uma montanha, e devolve o tuplo com todas as interseções 
    correspondentes ao vale da montanha fornecida como argumento, 
    ordenado por oredem de leitura (o tuplo devolvido pode ser vazio).
    Se algum dos argumentos for inválido, a função gera um erro. 
    '''
    if not (eh_territorio(t) and eh_intersecao_valida(t,i) and not eh_intersecao_livre(t,i)): 
        raise ValueError('obtem_vale: argumentos invalidos')
    vale=()
    for j in obtem_cadeia(t,i):
        for k in obtem_intersecoes_adjacentes(t,j):
            if eh_intersecao_livre(t,k) and not k in vale :
                vale += (k,)
    return ordena_intersecoes(vale)


def verifica_conexao(t,i1,i2):
    '''
    verifica_conexao: territorio × intersecao ×-intersecao → booleano
    Esta função recebe um territ+orio e duas interseções do mesmo
    e devolve True se ambas as interseções estiverem conectadas,
    caso contrário devolve False.
    Se algum dos argumentos dados for inválido, a função gera um erro.
    '''
    if not (eh_territorio(t) and eh_intersecao(i1) and eh_intersecao(i2)):
        raise ValueError('verifica_conexao: argumentos invalidos')
    elif not (eh_intersecao_valida(t,i1) and eh_intersecao_valida(t,i2)):
        raise ValueError('verifica_conexao: argumentos invalidos')
    
    if i2 in obtem_cadeia(t,i1):
        return True
    return False


def calcula_numero_montanhas(t): 
    '''
    calcula_numero_montanhas: territorio → int
    Esta função recebe um território e devolve o número 
    de interseções ocupadas por montanhas no território.
    Se o argumento dado for inválido, a função gera um erro. 
    '''
    if not eh_territorio(t): 
        raise ValueError('calcula_numero_montanhas: argumento invalido')
    montanhas = 0
    for i in t:
        for j in i:
            if j == 1:
                montanhas += 1
    return montanhas



def calcula_numero_cadeias_montanhas(t):
    '''
    calcula_numero_cadeias_montanhas: territorio → int
    Esta função recebe um território e devolve o 
    número de cadeias de montanhas contidas no mesmo.
    Se o argumento dado for inválido, a função gera um erro
    '''
    if not eh_territorio(t):
        raise ValueError('calcula_numero_cadeias_montanhas: argumento invalido')
    n_cadeias = 0
    intersecoes_cadeia = () 
    
    for y in todas_intersecoes(t):
        if not eh_intersecao_livre(t,y) and y not in intersecoes_cadeia:
            if obtem_cadeia(t,y) not in intersecoes_cadeia: 
                n_cadeias += 1
                intersecoes_cadeia += obtem_cadeia(t,y)
    return n_cadeias



def calcula_tamanho_vales(t):
    '''
    calcula_tamanho_vales: territorio → int
    Esta função recebe um território e devolve o número total
    de interseções diferentes correspondentes a todos os vales
    do território
    Se o argumento dado for inválido, a função gera um erro.
    '''
    if not eh_territorio(t):
        raise ValueError('calcula_tamanho_vales: argumento invalido')
    
    intersecoes_vales = ()
    intersecoes_cadeia= () #tuplo que terá as interseções pertencentes a cada cadeia de montanhas
    for y in todas_intersecoes(t):
        if not eh_intersecao_livre(t,y) and not y in intersecoes_cadeia:
            intersecoes_cadeia += obtem_cadeia(t,y)
            for k in obtem_vale(t,y):
                if k not in intersecoes_vales:
                    intersecoes_vales += (k,)
    return len(intersecoes_vales)




