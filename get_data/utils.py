import os
import json

def solve_dir(data_dir):
    '''Resolve o diretório de forma independente do OS,
    retornando seu caminho absoluto.
    Se o diretório não existe, cria ele.'''

    data_dir = os.path.abspath(os.path.join(os.getcwd(), data_dir))

    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    return data_dir

class JsonLoader:
    """
    Abre arquivos JSON.
    """

    def __init__(self, data_dir = 'original_data'):
            
        self.data_dir = solve_dir(data_dir)

    def solve_extension(self, fname):
        
        if fname.endswith('.json'):
            return fname
        
        else:
            return fname+'.json'


    def json_file_path(self, fname, data_dir=None):

        data_dir = data_dir or self.data_dir

        fname = self.solve_extension(fname)

        fpath = os.path.abspath(os.path.join(data_dir, fname))

        return fpath

    def load_json(self, fname, data_dir=None):

        fpath = self.json_file_path(fname, data_dir)

        with open(fpath, 'r') as f:
            return json.load(f)

    def __call__(self, fname):
        """
        Carrega os dados de arquivo JSON salvo 
        no diretorio especificado em self.data_dir.
        """
        
        return self.load_json(fname)



class JsonSaver:
    """
    Salva dados em JSON em um diretório.
    Caso o diretório não exista, o cria de forma segura.
    """
    
    
    def __init__(self, data_dir = 'original_data'):
        
        self.data_dir = solve_dir(data_dir)

    def solve_extension(self, fname):
        
        if fname.endswith('.json'):
            return fname
        
        else:
            return fname+'.json'


    def json_file_path(self, fname, data_dir=None):

        data_dir = data_dir or self.data_dir

        fname = self.solve_extension(fname)

        fpath = os.path.abspath(os.path.join(data_dir, fname))

        return fpath

    def save_json(self, data, fname, data_dir = None):

        fpath = self.json_file_path(fname, data_dir)

        with open(fpath, 'w') as f:
            json.dump(data, f)
            
    def __call__(self, data, fname):
        """
        Salva os dados do param 'data' em um arquivo json com nome fname,
        no diretorio especificado em self.data_dir.
        """
        
        self.save_json(data, fname)

def remover_acentos(texto):
    '''Remove acentos e alguns caracteres especiais
    de uma string'''
    
    texto = str(texto)
    texto = texto.lower()
    
    acentos = {
        'á' : 'a',
        'â' : 'a',
        'à' : 'a',
        'ã' : 'a',
        'é' : 'e',
        'ê' : 'e',
        'è' : 'e',
        'í' : 'i', 
        'î' : 'i',
        'ì' : 'i',
        'ó' : 'o',
        'ô' : 'o',
        'ò' : 'o',
        'õ' : 'o',
        'ú' : 'u',
        'û' : 'u',
        'ù' : 'u',
        'ü' : 'u',
        'ç' : 'c',
        'ñ' : 'n'
    }
    
    for acento, letra in acentos.items():
        texto = texto.replace(acento, letra)
        
    texto = texto.replace("'", ' ')
    texto = texto.replace('*', '')
    texto = texto.replace('#', '')
    texto = texto.replace('ª', '')

    texto = texto.replace('  ', ' ')

    texto = texto.strip()
    
    return texto