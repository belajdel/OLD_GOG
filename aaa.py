import os
import json
import re

directory = "games"
output_directory = "output"  # Specify the directory where HTML files will be saved

def sanitize_filename(filename):
    # Remove special characters and spaces, replace with underscores
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'[-\s]+', '_', filename)
    return filename

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for filename in os.listdir(directory):
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)

        with open(filepath, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            game_title = json_data['MSG']['title']
            download_links = [link['links'][0]['link'] for link in json_data['MSG']['links']['GAME']]
            goodies = [{'name': goodie['name'], 'link': goodie['links'][0]['link']} for goodie in json_data['MSG']['links']['GOODIES']]

            html_content = f'''
            <html>
            <head>
                <title>{game_title}</title>
                <link rel="stylesheet" href="style.css">
            </head>
            <body>
                <h1>{game_title}</h1>
                <h2>Download Links:</h2>
                <ul>
                    {''.join(f"<li><a href='{link}'>{link}</a></li>" for link in download_links)}
                </ul>
                <h2>Goodies:</h2>
                <ul>
                    {''.join(f"<li><a href='{goodie['link']}'>{goodie['name']}</a></li>" for goodie in goodies)}
                </ul>
            </body>
            </html>
            '''
            sanitized_title = sanitize_filename(game_title)

            output_filename = os.path.join(output_directory, f"{sanitized_title}.html")
            with open(output_filename, 'w',encoding='utf-8') as output_file:
                output_file.write(html_content)