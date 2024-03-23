import os
import requests
from bs4 import BeautifulSoup

folder_path = './games'  # Replace with the path to your folder containing the HTML pages
output_folder = './game_icons'  # Replace with the path to the folder where you want to save the game icons

def generate_game_icon_links():
    game_files = get_game_files()
    game_icons = {}
    for file in game_files:
        game_name = os.path.splitext(file)[0]
        game_icon = fetch_game_icon(game_name)
        if game_icon:
            game_icons[game_name] = game_icon
    return game_icons

def get_game_files():
    # Filter HTML files in the folder
    game_files = [file for file in os.listdir(folder_path) if file.endswith('.html')]
    return game_files

def fetch_game_icon(game_name):
    # Perform a web search using the game name
    search_query = f'{game_name} game icon'
    search_url = f'https://www.google.com/search?q={search_query}&tbm=isch'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        image_elements = soup.find_all('img')
        if image_elements:
            game_icon = image_elements[0]['src']
            return game_icon
    return None

def download_game_icons(game_icons):
    for game_name, game_icon in game_icons.items():
        image_url = game_icon
        response = requests.get(image_url)
        if response.status_code == 200:
            # Prepare the output file path
            output_path = os.path.join(output_folder, f'{game_name}_icon.jpg')
            with open(output_path, 'wb') as f:
                f.write(response.content)
                print(f"Downloaded icon for {game_name} successfully.")
        else:
            print(f"Failed to download icon for {game_name}.")

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

game_icon_links = generate_game_icon_links()

# Download the game icons
download_game_icons(game_icon_links)