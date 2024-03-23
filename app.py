import os
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    game_files = get_game_files()
    games = parse_games(game_files)
    return render_template('index.html', games=games)

def get_game_files():
    folder_path = './games'  
 
    game_files = [file for file in os.listdir(folder_path) if file.endswith('.html')]
    return game_files

def parse_games(game_files):
    games = []
    for file in game_files:
        game_name = os.path.splitext(file)[0]
        game_link = parse_game_link(file)
        games.append({'name': game_name, 'link': game_link})
    return games

def parse_game_link(file):
    folder_path = './games' 
    file_path = os.path.join(folder_path, file)
    with open(file_path, 'r',encoding='utf-8') as f:
        content = f.read()
        game_link = extract_download_link(content)
    return game_link

def extract_download_link(content):
    soup = BeautifulSoup(content, 'html.parser')
    download_link_element = soup.find('a', href=True)
    if download_link_element:
        download_link = download_link_element['href']
        return download_link
    return None

if __name__ == '__main__':
    app.run()