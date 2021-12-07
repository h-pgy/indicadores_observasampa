from .portal_dados_abertos import RecursosPortalDadosAbertos, CsvResorceDownloader

def csv_name_callback(recurso):

    desc = recurso['description']

    mes = desc.split(':')[-1].strip()

    return f'servidores_ativos_{mes}'


class GetServidoresAtivos:
    ''' Retorna DataFrame com dados mais atualizados da lista de 
        servidores ativo da PMSP ou com o mes especificado.
        Salva esse .csv na pasta especificada em data_dir.
        Caso o .csv já esteja salvo, apenas abre o csv salvo ao invés 
        de fazer download.
        
        Caso seja especificado um recurso, ele baixa esse recurso ao invés do mais recente.
        '''

    url = 'http://dados.prefeitura.sp.gov.br/dataset/servidores-ativos-da-prefeitura'

    def __init__(self, data_dir='original_data/'):

        self.list_resources = RecursosPortalDadosAbertos()
        self.download_resource = CsvResorceDownloader(data_dir=data_dir, 
                                                    file_name_callbakc=csv_name_callback)
        self.data_dir = data_dir
        self.recursos = self.todos_os_recursos()

    
    def todos_os_recursos(self):
        '''Lista todos os recursos .csv disponiveis'''
        
        recs =  self.list_resources(self.url, data_format='csv')

        return recs
    
    def servidores_ativo_mais_atual(self):
        '''Retorna os metadados e o link para download do arquivo csv 
        com a lista de servidores ativos mais atualizada, de acordo com 
        o disponibilizado no Portal de Dados Abertos da PMSP'''

        return self.recursos[0]
        
    def get_ultimo_servidores_ativo(self):
        """Busca ultimos dados para servidores ativos.
        Mas primeiro checa se ja nao ha um csv salvo com essa informacao"""

        recurso = self.servidores_ativo_mais_atual()

        return self.download_resource(recurso)

    def __call__(self, rec = None):
        
        if rec is None:
            return self.get_ultimo_servidores_ativo

        return self.download_resource(rec)