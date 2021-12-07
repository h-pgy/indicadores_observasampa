from requests import Session
from bs4 import BeautifulSoup
import os
from io import StringIO
import pandas as pd
from .utils import solve_dir

class RecursosPortalDadosAbertos:
    '''Lista os recursos disponíveis no Portal de Dados Abertos 
    para uma dada Url no site.
    Filtra os recursos por extensão (p. ex., csv) e 
    disponibiliza os links para download.
    '''
    
    def __init__(self):
        
        self.session = Session()
        
    def get_page(self, url):
        
        with self.session.get(url) as r:
            assert r.status_code == 200
            html = r.text
        
        return html
    
    def generate_soup(self, html):
        
        sopa = BeautifulSoup(html, features='lxml')
        return sopa
        

    def list_resources(self, sopa):
        
        resources = sopa.find_all('li', 
                                  {'class' : 'resource-item'})
        
        return resources
    
    def resource_data_format(self, resource):
        
        data_format = resource.find('a', 
                               {'class' : 'heading'}
                              ).find('span')
        
        if data_format: 
            data_format = data_format.get('data-format')
            return data_format.lower().strip()
        
        
    def resource_description(self, resource):
        
        desc = resource.find('p', 
                             {'class' : 'description'})
        
        if desc: return desc.text.strip()
                
            
    def link_downlaod_resource(self, resource):
        
        link = resource.find('a',
                             {'class' : 'resource-url-analytics'})
        
        if link: return link.get('href')
        
    
    def parse_resource(self, resource):
        
        
        return dict(
            data_format = self.resource_data_format(resource),
            description = self.resource_description(resource),
            link = self.link_downlaod_resource(resource)
         )
    
    def get_parsed_resources(self, sopa, data_format = None):
        
        resources = self.list_resources(sopa)
        
        parsed_data = []
        
        for resource in resources:
            
            parsed_resource = self.parse_resource(resource)
            parsed_data.append(parsed_resource)
    
        if data_format:
            
            parsed_data = [resource for resource in parsed_data 
                          if resource['data_format'] == data_format]
        
        return parsed_data
    
    def __call__(self, url, data_format=None):
        
        html = self.get_page(url)
        sopa = self.generate_soup(html)
        
        return self.get_parsed_resources(sopa, data_format)

class CsvResorceDownloader:
    '''Faz o download do recurso do Portal de Dados Abertos.
    Caso o recurso já esteja salvo no diretorio, apenas abre ele
    em formato de pandas dataframe'''

    def __init__(self, data_dir, file_name_callbakc):
        '''name_callback must be a callback function
        to be aplied on the resource object to build the filename. Must return a string'''

        self.file_name_callbakc = file_name_callbakc #nome do arquivo a ser salvo
        self.session = Session()
        self.data_dir = data_dir

    def build_file_name(self, recurso, extension, name_callback = None):
        '''Buils the file name. name_callback must be a callback function
        to be aplied on the resource object to build the filename. Must return a string'''

        if name_callback is None:
            name_callback = self.file_name_callbakc

        file_name = f'{name_callback(recurso)}.{extension}'

        return file_name

    def solve_file_path(self, recurso, data_dir, extension):

        data_dir = solve_dir(data_dir)

        file_name = self.build_file_name(recurso, extension)

        return os.path.join(data_dir, file_name)

    def save_file(self, data, recurso, extension, data_dir=None):

        if data_dir is None:
            data_dir = self.data_dir

        file_path = self.solve_file_path(recurso, data_dir, extension)

        with open(file_path, 'w') as f:
            f.write(data)

    def read_csv_io(self, csv_data):

        file_like = StringIO(csv_data)
        df = pd.read_csv(file_like, encoding='latin-1', sep=';')

        return df


    def download_csv_resource(self, recurso, data_dir=None, save=True):

        link = recurso['link']
        with self.session.get(link) as r:
            assert r.status_code == 200
            csv = r.text

        if save:
            self.save_file(csv, recurso, extension='csv', data_dir=data_dir)

        df = self.read_csv_io(csv)

        return df
    
    def find_saved_resource(self, recurso, extension, data_dir=None):

        if data_dir is None:
            data_dir = self.data_dir

        file_name = self.build_file_name(recurso, extension)

        files = os.listdir(data_dir)

        found = [file for file in files if file == file_name]

        if found:
            file_path = os.path.join(data_dir, file_name)
            return file_path

    def load_saved_csv_resource(self, resource_file):

        return pd.read_csv(resource_file, encoding='latin-1', sep=';')

    def get_csv_resource(self, recurso, data_dir=None):

        saved_file = self.find_saved_resource(recurso,
             extension='csv', data_dir=data_dir)

        if saved_file:
            print(f'Carregando arquivo ja salvo: {saved_file}')
            return self.load_saved_csv_resource(saved_file)

        print(f'Baixando recurso {recurso}')
        return self.download_csv_resource(recurso, data_dir = data_dir)

    def __call__(self, recurso):

        return self.get_csv_resource(recurso)