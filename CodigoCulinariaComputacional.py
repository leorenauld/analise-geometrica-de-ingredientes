import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def getIngredientes():
    data = df.head(N)
    m = np.array(data['NER'])
    lista = [[],[]]
    for i in m:
        ingredientes = i.split(', ')
        for j in ingredientes:
            j = j.replace('[', '')
            j = j.replace(']', '')
            j = j.replace('"', '')
            if (lista[0].count(j) == 0):
                lista[0].append(j)
                lista[1].append(0)
    return(lista)

def mqAlternados(A, k, iteracoes):
    m,n=np.shape(A)
    B = np.random.random((m, k))
    for i in range(iteracoes):
        C=np.linalg.lstsq(B,A, rcond=None)[0]
        B=np.linalg.lstsq(A.transpose(),C.transpose(), rcond=None)[0]       
    erro=A-B.dot(C)
    return B,C,np.linalg.norm(erro)

def ingredienteProximo(ingrediente):
    B, C, erro = mqAlternados(dados, 4, 1)
    temp = []
    for j in ingredientes[0]:
        j = j.replace('[', '')
        j = j.replace(']', '')
        j = j.replace('"', '')
        temp.append(j)
    index = temp.index(ingrediente)
    ingredientePronto = [C[0][index], C[1][index], C[2][index], C[3][index]]
    d = np.linalg.norm(np.array(ingredientePronto) - np.array([C[0][0], C[1][0], C[2][0], C[3][0]]))
    melhorIndex = 0
    for i in range(len(C[0])):
        sub = np.linalg.norm(np.array(ingredientePronto) - np.array([C[0][i], C[1][i], C[2][i], C[3][i]]))
        print(sub)
        if (sub < d and temp[i] != ingrediente):
            d = sub
            melhorIndex = i
    print(d)
    print(temp[melhorIndex])

def receitaProximo(receita):
    B, C, erro = mqAlternados(dados, 4, 1)
    temp = []
    for j in titulos:
        j = j.replace('[', '')
        j = j.replace(']', '')
        j = j.replace('"', '')
        temp.append(j)
    index = temp.index(receita)
    receitaPronta = [B.transpose()[0][index], B.transpose()[1][index], B.transpose()[2][index], B.transpose()[3][index]]
    d = np.linalg.norm(np.array(receitaPronta) - np.array([B.transpose()[0][0], B.transpose()[1][0], B.transpose()[2][0], B.transpose()[3][0]]))
    melhorIndex = 0
    for i in range(len(B)):
        sub = np.linalg.norm(np.array(receitaPronta) - np.array([B.transpose()[0][i], B.transpose()[1][i], B.transpose()[2][i], B.transpose()[3][i]]))
        if (sub < d and temp[i] != receita):
            d = sub
            melhorIndex = i
    print(d)
    print(temp[melhorIndex])
    print(links[melhorIndex])

def graficoReceitas():
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot3D(B.transpose()[0],B.transpose()[1],B.transpose()[2], linestyle='None')
    ax.set_title('Agrupamento de receitas')
    for i in range(len(titulos)):
        ax.text(B.transpose()[0][i], B.transpose()[1][i], B.transpose()[2][i], titulos[i])
    plt.show()

def graficoIngredientes():
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot3D(C[0],C[1], C[2], linestyle='None')
    ax.set_title('Agrupamento de ingredientes')
    for i in range(len(ingredientes[0])):
        ax.text(C[0][i], C[1][i] ,C[2][i], ingredientes[0][i])
    plt.show()

def graficoErro(A):
    posto = A.shape[0]
    print(posto)
    erros = []
    postos = []
    for i in range(1, posto):
        print(i)
        B, C, erro = mqAlternados(A, i, 1)
        erros.append(erro)
        postos.append(i)
    print(erros)
    plt.plot(erros, postos)
    plt.show()

print('Carregando dataset...')    
df = pd.read_csv("D:/Desktop/cocada file/recipes_data.csv", engine='python')

N = 1000
print('Dataset carregado...')
ingredientes = getIngredientes()
print('Ingredientes gerados...')
dados = receitasPorIngrediente()
dados = np.array(dados)
print('Matriz de receitas geradas...')
print(dados)
print('Programa pronto.')
B, C, erro = mqAlternados(dados, 3, 1)

data = df.head(N)
titulos = np.array(data['title'])
links = np.array(data['link'])
