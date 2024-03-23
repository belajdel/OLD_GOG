import os
import requests
from bs4 import BeautifulSoup

def fetch_game_icon(game_id):
    game_url = f"https://www.gogdb.org/product/{game_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(game_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        product_logo = soup.find(id='product-logo')
        if product_logo:
            game_icon = product_logo['src']
            return game_icon
    return None

def add_game_icon_to_html(file_path, game_icon):
    with open(file_path, 'r+', encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        head_tag = soup.find('head')
        if head_tag:
            icon_id = os.path.basename(file_path).replace('.html', '')
            p_tag = soup.new_tag('p', id=icon_id, hidden='', style='display: none;')
            p_tag.string = game_icon
            head_tag.append(p_tag)
            f.seek(0)
            f.write(str(soup))
            f.truncate()

def get_game_icon_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        game_id_element = soup.find('p', {'hidden': True})
        if game_id_element:
            game_id = game_id_element.text.strip()
            game_icon = fetch_game_icon(game_id)
            if game_icon:
                add_game_icon_to_html(file_path, game_icon)
                return game_icon
    return None

if __name__ == '__main__':
    directory = './games'
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            file_path = os.path.join(directory, filename)
            game_icon = get_game_icon_from_html(file_path)
            if game_icon:
                b=True
            else:
                print(f"Failed to fetch the game icon for {filename}.")