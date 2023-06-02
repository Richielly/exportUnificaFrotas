import configparser

class Util:

    def update_cfg(self, ini='cfg.ini',secao='DEFAULT', chave='CodEntidade', new=0):
        cfg = configparser.ConfigParser()
        cfg.read(ini)
        # Modifica um valor existente
        cfg.set(secao, chave, new)
        # Salva as alterações no arquivo de configuração
        with open(ini, 'w') as configfile:
            cfg.write(configfile)