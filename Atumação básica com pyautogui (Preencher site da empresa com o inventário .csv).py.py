import pyautogui
import time
import pandas # Manipulação e análise de dados em tabelas
import os  # Interação com arquivos e pastas do sistema
import glob # Busca de arquivos usando padrões (*.csv, *.xlsx)

#Pensando etapas.

#passo 1:Entrar no sistema da empresa
link = "https://dlp.hashtagtreinamentos.com/python/intensivao/login"
pyautogui.PAUSE = 1
pyautogui.press('win')
pyautogui.write('chrome')
pyautogui.press('enter')
pyautogui.write(link)
pyautogui.press('enter')
#passo 2: Fazer login
time.sleep(1)
pyautogui.click('logar.png')
time.sleep(1)

#passo 3: Acessar os dados 
tabela = pandas.read_csv('produtos.csv')
print(tabela)   

#passo 4: Cadastrar 1 produto
#Categorias: "codigo,marca,tipo,categoria,preco_unitario,custo,obs"
for linha in tabela.index:
    pyautogui.click(x=674, y=288)

    pyautogui.write(str(tabela.loc[linha, 'codigo']))   

    pyautogui.press('tab')  

    pyautogui.write(str(tabela.loc[linha, 'marca']))

    pyautogui.press('tab')
    pyautogui.write(str(tabela.loc[linha, 'tipo']))

    pyautogui.press('tab')

    pyautogui.write(str(tabela.loc[linha, 'categoria']))

    pyautogui.press('tab')
    pyautogui.write(str(tabela.loc[linha, 'preco_unitario']))

    pyautogui.press('tab')
    pyautogui.write(str(tabela.loc[linha, 'custo']))   

    pyautogui.press('tab')
    obs_value = str(tabela.loc[linha, 'obs'])
    Televisao = tabela.loc[linha, 'tipo']       
    
    # Verifica se a célula não é "nan", "NaN" ou vazia ""
    if obs_value != 'nan' and obs_value != '':
        pyautogui.press('tab')
        pyautogui.write(obs_value)   

    pyautogui.press('tab')
    pyautogui.press('enter')   


    