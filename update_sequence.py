import configparser
cfg = configparser.ConfigParser()
cfg.read('cfg.ini')
import fdb

query = {
        'SEQ_SCF_IDMOTORISTACATCNH':f""" select 'set generator SEQ_SCF_IDMOTORISTACATCNH to ' || (select max(idmotoristacatcnh)+1 from SCF_MOTORISTACATCNH) from RDB$DATABASE """,
        'SEQ_SCF_IDORDEMABASTECIMENTO':f""" select 'set generator SEQ_SCF_IDORDEMABASTECIMENTO to ' || (select max(idordemabastecimento)+1 from SCF_ORDEMABASTECIMENTO) from RDB$DATABASE """,
        'SEQ_SCF_IDVEICULOABASTECIMENTO':f""" select 'set generator SEQ_SCF_IDVEICULOABASTECIMENTO to ' || (select max(idveiculoabastecimento)+1 from SCF_VEICULOABASTECIMENTO) from RDB$DATABASE """,
        'SEQ_SCF_IDVEICULOcontrolesimam':f""" select 'set generator SEQ_SCF_IDVEICULOcontrolesimam to ' || (select max(idveiculocontrolesimam)+1 from SCF_VEICULOCONTROLESIMAM) from RDB$DATABASE """,
        'SEQ_SCF_idmotoristasituacaocnhSEQ_SCF_idmotoristasituacaocnh':f""" select 'set generator SEQ_SCF_idmotoristasituacaocnh to ' || (select max(idmotoristasituacaocnh)+1 from SCF_MOTORISTASITUACAOCNH) from RDB$DATABASE """,
        'SEQ_SCF_IDCONSUMOCOMBUSTIVEL':f""" select 'set generator SEQ_SCF_IDCONSUMOCOMBUSTIVEL to ' || (select max(idconsumocombustivel)+1 from SCF_CONSUMOCOMBUSTIVEL) from RDB$DATABASE """,
        'SEQ_SCF_idnfconsumo':f""" select 'set generator SEQ_SCF_idnfconsumo to ' || (select max(idnfconsumo)+1 from SCF_NFCONSUMO) from RDB$DATABASE """,
        'SEQ_SCF_IDVEICULOACUMULADOR':f""" select 'set generator SEQ_SCF_IDVEICULOACUMULADOR to ' || (select max(idveiculoacumulador)+1 from SCF_VEICULOACUMULADOR) from RDB$DATABASE """,
        'SEQ_SCF_IDVEICULOORDEMSERVICO':f""" select 'set generator SEQ_SCF_IDVEICULOORDEMSERVICO to ' || (select max(idVEICULOORDEMSERVICO)+1 from SCF_VEICULOORDEMSERVICO) from RDB$DATABASE """,
        'SEQ_SCF_IDVEICULOORDEMSERVICOP':f""" select 'set generator SEQ_SCF_IDVEICULOORDEMSERVICOP to ' || (select max(idVEICULOORDEMSERVICOPRODUTO)+1 from SCF_VEICULOORDEMSERVICOPRODUTO) from RDB$DATABASE """,
        'SEQ_SCF_IDVEICULOUTILIZACAO':f""" select 'set generator SEQ_SCF_IDVEICULOUTILIZACAO to ' || (select max(idVEICULOutilizacao)+1 from SCF_VEICULOUTILIZACAO) from RDB$DATABASE """
        }
class Update_sequence:

    def sequences(self, host=cfg['DEFAULT']['Host'], database=cfg['DEFAULT']['NomeBancoSequence'], user=cfg['DEFAULT']['User'], port=cfg['DEFAULT']['Port'], password=cfg['DEFAULT']['Password']):
        result = []
        global query
        for seq, sql in query.items():
            try:
                dados_conexao = fdb.connect(host=host, database=database, user=user, port=int(port), password=password)
            except BaseException as e:
                return e, False
            cur = dados_conexao.cursor()

            cur.execute(sql)
            result.append(cur.fetchone())

        return result, cur

    def atualiza_sequence(self, host, database, user, port, password):
        sequencia, cur = self.sequences(host=host, database=database, user=user, port=int(port), password=password)
        if not cur:
            return cur, sequencia
        else:
            for linha in sequencia:
                if linha[0]:
                    cur.execute(linha[0])
            return True, sequencia

