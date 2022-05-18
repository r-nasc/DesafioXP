### O seguinte código compara as formas de tributação de duas bases de fundos de 
### investimento (CVM e Anbima) e gera um arquivo .xlsx com os resultados.
### O código foi testado em Python 3.7 e depende das bibliotecas pandas e openpyxl


import re
import pandas as pd


pwd = '' # Manter vazio para pasta local ou indicar caminho. ex: 'C:\\DesafioXP\\'
path_cvm = pwd + 'fundos_cvm.xlsx'
path_anbima = pwd + 'fundos_anbima.xlsx'
path_output = pwd + 'output.xlsx'


### Lê arquivos .xlsx e retorna dataframes
df_cvm = pd.read_excel(path_cvm, na_filter = False)
df_anbima = pd.read_excel(path_anbima, na_filter = False)


### Manipula colunas 'id_fundo' para que possam ser comparadas
def id_from_string(s):
    return re.sub('\\D', '', s).lstrip('0')

df_cvm['id_fundo'] = df_cvm.apply(lambda row : id_from_string(row['id_fundo']), axis = 1)
df_anbima['id_fundo'] = df_anbima['id_fundo'].astype(str)


### Dropa colunas não utilizadas, marca coluna 'id_fundo' como primary key e renomeia colunas restantes
df_cvm = df_cvm[['id_fundo', 'TRIB_LPRAZO']].set_index('id_fundo')
df_cvm.rename(columns={'TRIB_LPRAZO': 'tributacao_cvm'}, inplace=True)

df_anbima = df_anbima[['id_fundo', 'tributacao_alvo']].set_index('id_fundo')
df_anbima.rename(columns={'tributacao_alvo': 'tributacao_anbima'}, inplace=True)


### Cria dataframe contendo apenas fundos presentes em ambas as bases e compara tributações
dict_cvm = {
	'': 'Indefinido',
    'S': 'Longo Prazo',
    'N/A': 'Não Aplicável'    
}

def get_result(a, b):
    if a in dict_cvm and dict_cvm[a]==b:
        return 'igual'
    return 'diferente'

def_result = df_cvm.join(df_anbima, how='inner')
def_result['resultado'] = def_result.apply(lambda row : get_result(row['tributacao_cvm'], row['tributacao_anbima']), axis = 1)


### Salva resultados em uma planilha excel
def_result.to_excel(path_output)