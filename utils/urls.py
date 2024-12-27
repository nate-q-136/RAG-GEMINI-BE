import requests


class UrlHandler:    
    @staticmethod
    def download_file(url:str, file_name:str):
        response = requests.get(url)
        with open(file_name, 'wb') as f:
            f.write(response.content)
        return file_name