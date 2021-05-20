import PySimpleGUI as sg
import pandas as pd
import chardet
import webbrowser

#Este programa foi desenvolvido por: Rafael Gardel com o objetivo de permitir que você una arquivos .CSV com facilidade
#Acesse o projeto acessando o meu repositório no github: https://github.com/rafaelgard/Junta_CSV
#
#
#
class une_csv:
    def __init__(self, caminhos, nome_arquivo_final, encoding, separador):
        self.caminhos = caminhos
        self.nome_arquivo_final = nome_arquivo_final
        self.encoding = encoding
        self.separador = separador

    def janela_1(self):
        #Layout
        sg.theme('DarkGrey14')

        layout = [
            [
                [sg.Text('JUNTA CSV', size=(170, 1), text_color='green', justification='center', font=("Helvetica", 20))],
                [sg.Text('ARQUIVOS  ', size=(10, 1)), sg.Input(key='ARQUIVOS_IMPORTADOS', size=(50, 1)), sg.FilesBrowse('SELECIONAR', size=(20, 1))],
                [sg.Text('NOME FINAL', size=(10, 1)), sg.Input(key='ARQUIVO_GERADO', size=(50, 1)), sg.Button('UNIR ARQUIVOS', size=(20, 1))],
                [sg.Text('SEPARADOR', size=(10, 1)), sg.DropDown(list(['PONTO E VÍRGULA', 'VÍRGULA', 'ESPAÇO']), key='SEPARADOR', size=(20, 1)), sg.Text(size=(23, 1)), sg.Button('SOBRE', size=(20, 1))],
                [sg.Text('', size=(60, 1)), sg.Button('FECHAR', size=(10, 1))]
            ]
        ]
        return sg.Window('JUNTA CSV', layout=layout, size=(650, 190), finalize=True)

    def janela_2(self):
        #Layout
        sg.theme('DarkGrey14')

        layout = [
            [
                [sg.Text('JUNTA CSV', size=(170, 1), text_color='green', justification='center', font=("Helvetica", 20))],
                [sg.Text('ESTE PROGRAMA FOI DESENVOLVIDO POR: RAFAEL GARDEL COM O OBJETIVO DE PERMITIR QUE VOCÊ UNA ARQUIVOS .CSV COM FACILIDADE.', size=(50, 3)), sg.Text(size=(4, 2)), sg.Button('ACESSAR PROJETO', size=(20, 2))],
                [sg.Text('PARA CONHECER O PROJETO CLIQUE NO BOTÃO AO LADO', size=(50,2))],
                [sg.Text(size=(56, 1)), sg.Button('VOLTAR', size=(20, 1))]
            ]
        ]
        return sg.Window('SOBRE', layout=layout, size=(650, 190), finalize=True)


    def importa_dados(self, caminhos, nome_arquivo_final, separador):
        '''Importa os dados preenchidos na janela'''

        '''Verifica se os caminhos foram importados corretamente'''
        validacao = self.importa_caminhos(caminhos)

        '''Identifica se os caminhos dos arquivos foram importados com sucesso'''
        if validacao == True:
            validacao = self.importa_separador(separador)

        '''Identifica se o separador foi preenchido corretamente'''
        if validacao == True:
            validacao = self.nome_arquivo_final = nome_arquivo_final
            return True

    def importa_separador(self, separador):

        '''Identifica os separadores preennchidos'''
        if separador =='PONTO E VÍRGULA':
            self.separador = ';'
            return True

        elif separador == 'VÍRGULA':
            self.separador = ','
            return True

        elif separador == 'ESPAÇO':
            self.separador = ' '
            return True

    def importa_caminhos(self, caminhos):
        '''Adiciona ; para demarcar o final do arquivo'''
        self.caminhos = caminhos + ';'
        lista_de_caminhos = []
        caminho_certo = ''

        '''Detecta na string contendo os caminhos, cada caminho individualmente e atualiza a variável'''
        for i, caracter in enumerate(self.caminhos):
            if caracter == ';':
                '''Verifica se o arquivo está em formato .csv'''
                if caminho_certo[len(caminho_certo)-3:] != 'csv':
                    sg.popup('OS ARQUIVOS DEVEM ESTAR EM FORMATO .CSV')
                    return False

                try:
                    '''Tenta abrir o arquivo'''
                    arquivo = open(caminho_certo, 'r')
                    arquivo.close()

                except FileNotFoundError:
                    '''Caso não consiga abrir o arquivo significa que o arquivo não está no caminho apontado'''
                    sg.popup('Arquivo não encontrado!')
                    return False

                '''Caso o arquivo seja em formato .csv e seja encontrado, salva na lista de caminhos '''
                lista_de_caminhos.append(caminho_certo)
                caminho_certo = ''

            else:
                caminho_certo = caminho_certo + caracter

        '''Atualiza a variável contendo os caminhos dos arquivos'''
        self.caminhos = lista_de_caminhos
        return True

    def une_arquivos(self):
        '''Inicialmente obriga o separador a ser ; e o encoding a ser UTF-8 '''

        '''Cria um dataframe vazio'''
        df = pd.DataFrame()

        '''Percorre a lista de arquivos que serão unidos'''
        for i, arquivo in enumerate(self.caminhos):
            '''Identifica o encoding do arquivo'''
            self.encoding = self.detecta_encoding(arquivo)

            '''Tenta unir os arquivos'''
            try:
                '''Caso seja o primeiro arquivo da lista'''
                if i == 0:
                   # Importa o dataframe inicial
                   df = pd.read_csv(arquivo, sep=self.separador, encoding=self.encoding)

                else:
                    '''Caso não seja o primeiro arquivo da lista'''
                    arquivo_novo = pd.read_csv(arquivo, sep=self.separador, encoding=self.encoding)

                    '''Faz um append para acrescentar o banco recém importado ao banco principal'''
                    df = df.append(arquivo_novo)

                    '''Atribui um dataframe vazio ao ultimo arquivo importado para liberar memória ram'''
                    arquivo_novo = pd.DataFrame()

                '''Remove colunas indesejadas'''
                colunas = df.columns
                for coluna in colunas:
                    if coluna == 'Unnamed: 0':
                        df = df.drop(coluna, axis=1)

                    if coluna == 'Unnamed: 1':
                        df = df.drop(coluna, axis=1)

                    if coluna == 'Unnamed: 2':
                        df = df.drop(coluna, axis=1)

                    if coluna == 'Unnamed: 3':
                        df = df.drop(coluna, axis=1)

            except:
                sg.popup('O SEPARADOR ESCOLHIDO ESTÁ ERRADO!')
                sg.popup('VERIFIQUE O SEPARADOR!')
                return False

        '''Salva o arquivo'''
        validacao = self.salva_arquivo(df)

        '''Caso o arquivo tenha sido salvo com sucesso'''
        if validacao == True:
            return True

        else:
            '''Caso o arquivo não tenha sido salvo com sucesso'''
            return False

    def salva_arquivo(self, dataframe):
        '''Salva o dataframe atulizado em formato .csv'''

        try:
            '''Salva o dataframe'''
            dataframe.to_csv(self.nome_arquivo_final+'.csv', sep=self.separador, encoding=self.encoding)

            '''Atribui um dataframe vazio ao ultimo dataframe para liberar memória ram'''
            dataframe = pd.DataFrame()
            return True

        except:
            sg.popup('O SEPARADOR ESCOLHIDO ESTÁ ERRADO!')
            sg.popup('VERIFIQUE O SEPARADOR!')
            return False

    def detecta_encoding(self, caminho):
        '''Detecta o encoding do arquivo'''
        rawdata = open(caminho, 'rb').read()
        result = chardet.detect(rawdata)
        charenc = result['encoding']
        return charenc

'''Inicializa a classe'''
une_csv = une_csv(0, 0, 0, 0)

'''Inicializa o programa abrindo a janela 1'''
janela_1, janela_2 = une_csv.janela_1(), None

'''Lê os eventos'''
while True:
    window, event, values = sg.read_all_windows()

    '''====================EVENTOS DA JANELA INICIAL===================='''
    if window == janela_1:

        '''Inicializa os campos como nulos'''
        #values['ARQUIVOS_IMPORTADOS'] = None
        #values['ARQUIVO_GERADO'] = None

        '''Se fechar a janela 1 ou clicar em fechar, fecha o programa'''
        if (event == sg.WINDOW_CLOSED or event == 'FECHAR') == True:
            break

        if event == 'UNIR ARQUIVOS':
            try:
                '''Se todos os campos foram preenchidos'''
                if (values['ARQUIVOS_IMPORTADOS'] != ''
                    and values['ARQUIVO_GERADO'] != ''
                    and values['SEPARADOR'] != '') \
                        == True:

                    '''Importação dos dados'''
                    validacao = une_csv.importa_dados(values['ARQUIVOS_IMPORTADOS'],
                                                      values['ARQUIVO_GERADO'],
                                                      values['SEPARADOR'])

                    '''Verifica se os arquivos foram importados som sucesso'''
                    if validacao == True:
                        sg.popup('ARQUIVOS IMPORTADOS COM SUCESSO!')

                        sg.popup('UNINDO ARQUIVOS...')
                        validacao = une_csv.une_arquivos()

                        '''Verifica se conseguiu unir os arquivos corretamente'''
                        if validacao == True:
                            sg.popup('ARQUIVO SALVO COM SUCESSO!')

                        else:
                            sg.popup('ERRO AO UNIR ARQUIVOS!')
                            sg.popup(
                            'Verifique se todos os arquivos tem as mesmas colunas e estão em formato .csv')

                    else:
                        '''Caso não tenha sido importado com sucesso, fecha o programa'''
                        sg.popup('Erro ao importar arquivos')

                else:
                    sg.popup('PREENCHA TODOS OS DADOS!')

            except FileNotFoundError:
                pass

        '''====================EVENTOS DA JANELA SOBRE===================='''
        if event == 'SOBRE':
            '''Esconde a janela inicial'''
            janela_1.hide()

            '''Abre a janela sobre'''
            janela_2 = une_csv.janela_2()

    if window == janela_2:
        '''Se fechar a janela 1 ou clicar em fechar, fecha o programa'''
        if event == sg.WINDOW_CLOSED == True:
            break

        if event == 'VOLTAR':
            '''Esconde a janela inicial'''
            janela_2.hide()
            janela_1.un_hide()

        if event == 'ACESSAR PROJETO':
            '''Abre o site do projeto'''
            url = 'https://github.com/rafaelgard/Junta_CSV'
            webbrowser.open_new_tab(url)