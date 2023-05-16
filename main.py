import flet as ft
import time
import fdb
import configparser
import script
from random import randrange as r
from time import sleep

cfg = configparser.ConfigParser()
cfg.read('cfg.ini')

comandos = script.scripts

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_center()
    page.title = "Export Unifica Frotas"
    progressBar = ft.ProgressBar(width=700, color=ft.colors.DEEP_ORANGE)

    def start(host='localhost', database=cfg['DEFAULT']['NomeBanco'], user='sysdba', port=3050, password='masterkey'):
        try:
            dados_conexao = fdb.connect(host=host, database=database, user=user, port=port, password=password)
        except BaseException as e:
            return e

        cur = dados_conexao.cursor()
        page.add(list_arquivos)
        list_arquivos.clean()
        page.add(progressBar)
        com_dados = 0
        sem_dados = 0
        step = 0
        while True:

            for comando in comandos:
                step+=1
                list_arquivos.update()
                list_arquivos.controls.append(ft.Text(f'{step}° Arquivo: ' + comando + ' iniciado em ' + time.strftime("%d/%m/%y %H:%M:%S"), size=10, color=ft.colors.GREEN))
                cur.execute(comandos[comando])
                result = cur.fetchall()
                arquivo = open(
                    cfg['DEFAULT']['DiretorioArquivos'] + comando + '_' + cfg['DEFAULT']['CodEntidade'] + '.txt', "w",
                    newline='', encoding='ANSI')

                for inf in result:
                    arquivo.write(str(inf[0]).replace('#sec#', str(r(0, 5)) + str(r(0, 9))) + '\n')
                if len(result) < 1:
                    list_arquivos.controls.append(ft.Text('-- Finalizado em ' + time.strftime("%d/%m/%y %H:%M:%S"), size=10, color=ft.colors.ORANGE))
                    sem_dados+=1
                else:
                    list_arquivos.controls.append(ft.Text('-- Finalizado em ' + time.strftime("%d/%m/%y %H:%M:%S"), size=10))
                    com_dados+=1
                for i in range(0, len(comandos)+1):
                    progressBar.value = step / len(comandos)
                    txt_header.value=(f'{step} arquivos Gerados [Com dado: {com_dados}/ Vazio: {sem_dados}]')
                    page.update()
                sleep(0.3)
                page.update()

            dados_conexao.close()
            cur.close()
            time.sleep(2)
            break
    def btn_click(e):
        if not txt_database.value:
            txt_database.error_text = "Informe o caminho do Banco"
            page.update()
        else:
            page.update()
            txt_header.value = 'Arquivos Gerados'
            database = txt_database.value
            host= txt_host.value
            user= txt_user.value
            port= txt_port.value
            password= txt_password.value

            log = start(host=host, port=port, user=user, password=password, database=database)
            if log != None:
                txt_header.value = log
                list_arquivos.controls.clear()
                progressBar.value=0
                progressBar.update()
                if not progressBar:
                    progressBar.update()

            page.update()

    txt_entidade = ft.TextField(label="Entidade", text_size=12, value=cfg['DEFAULT']['CodEntidade'], width=100, height=30)
    txt_host = ft.TextField(label="Host", text_size=12, value='localhost', width=100, height=30)
    txt_user = ft.TextField(label="User", text_size=12, value='sysdba', width=100, height=30)
    txt_password = ft.TextField(label="Password", text_size=12, value='masterkey', width=130, height=30,password=True, can_reveal_password=True)
    txt_database = ft.TextField(label="Caminho do Banco", value=cfg['DEFAULT']['NomeBanco'], text_size=12, height=40)
    txt_port = ft.TextField(label="Porta", text_size=12, value=3050, width=100, height=30)
    txt_header = ft.Text('Arquivos Gerados')
    page.add(ft.Row([txt_entidade, txt_host, txt_port, txt_user, txt_password]))
    page.add(txt_database)
    page.add(ft.Row([ft.ElevatedButton("Gerar Arquivos", on_click=btn_click, icon=ft.icons.ADD_BOX)]))
    page.add(txt_header)
    list_arquivos = ft.ListView(expand=1, spacing=2, padding=20, auto_scroll=True)


if __name__ == "__main__":
    ft.app(port=3636, target=main, view=ft.WEB_BROWSER)


# pyinstaller --name redirect_port --onefile --noconsole main.py