import time
import fdb
import configparser
import script
import PySimpleGUI as sg
from random import randrange as r

cfg = configparser.ConfigParser()
cfg.read('cfg.ini')

dados_conexao = fdb.connect(host='localhost', database=cfg['DEFAULT']['NomeBanco'], user='sysdba', port=3050, password='masterkey')
cur = dados_conexao.cursor()

comandos = script.scripts
def start():
    tamanho = 0
    event, values = window.read()
    while True:
        if event == 'Iniciar':
            if event == 'Cancel' or event == sg.WIN_CLOSED:
                break
            for comando in comandos:
                tamanho += 1
                print('Arquivo: ' + comando + ' iniciado em ' + time.strftime("%d/%m/%y %H:%M:%S"))
                cur.execute(comandos[comando])
                result = cur.fetchall()
                arquivo = open(cfg['DEFAULT']['DiretorioArquivos'] + comando + '_' + cfg['DEFAULT']['CodEntidade'] + '.txt', "w", newline='', encoding='ANSI')

                for inf in result:
                    arquivo.write(str(inf[0]).replace('#sec#',str(r(0, 5)) + str(r(0, 9)))+'\n')
                print('Arquivo: ' + comando + ' finalizado em ' + time.strftime("%d/%m/%y %H:%M:%S") +'\n')
                progress_bar.UpdateBar(tamanho + 1)
                window['status'].update(str(tamanho) + '/' + str(len(comandos)))

            sg.SystemTray.notify('Arquivos gerados com sucesso.', cfg['DEFAULT']['NomeEntidade'].replace("'", ''))

        dados_conexao.close()
        cur.close()
        time.sleep(2)
        break

layout = [[sg.Text('Gerando Arquivos')],
          [sg.Text('0/'+str(len(comandos)), key='status')],
          [sg.Output(size=(80,20))],
          [sg.ProgressBar(len(comandos), orientation='h', size=(53, 20), key='progressbar')],
          [sg.OK('Iniciar'), sg.Cancel()]]

window = sg.Window('Arquivos - ' + cfg['DEFAULT']['CodEntidade'] + ' - ' + cfg['DEFAULT']['NomeEntidade'].replace("'", '') , layout)
progress_bar = window['progressbar']

start()

# pyinstaller --name export_unifica_frotas --onefile --noconsole main.py