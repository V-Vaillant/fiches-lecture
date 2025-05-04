import os
import re
import glob
from bs4 import BeautifulSoup

# Template HTML pour l'index
INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Index des fiches de lecture</title>
    <style>
        :root {
            --primary-color: #6a1b9a;
            --secondary-color: #9c27b0;
            --accent-color: #e1bee7;
            --background-color: #f8f9fa;
            --text-color: #333;
            --card-bg: #fff;
            --border-radius: 12px;
            --box-shadow: 0 3px 8px rgba(0,0,0,0.15);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.5;
            color: var(--text-color);
            background-color: var(--background-color);
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            margin-bottom: 30px;
            padding: 25px;
            background-color: var(--primary-color);
            color: white;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
        }
        
        h1 {
            font-size: 2.2rem;
            margin-bottom: 10px;
        }
        
        .subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .fiches-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }
        
        .fiche-card {
            background-color: var(--card-bg);
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            height: 100%;
            display: flex;
            flex-direction: column;
        }
        
        .fiche-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .fiche-header {
            padding: 15px;
            background-color: var(--secondary-color);
            color: white;
        }
        
        .fiche-title {
            font-size: 1.3rem;
            margin-bottom: 5px;
        }
        
        .fiche-author {
            font-size: 0.9rem;
            opacity: 0.9;
            font-style: italic;
        }
        
        .fiche-content {
            padding: 15px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        .fiche-description {
            margin-bottom: 15px;
            font-size: 0.95rem;
        }
        
        .fiche-link {
            display: inline-block;
            background-color: var(--primary-color);
            color: white;
            text-decoration: none;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9rem;
            align-self: flex-start;
            transition: background-color 0.3s ease;
        }
        
        .fiche-link:hover {
            background-color: var(--secondary-color);
        }
        
        @media (max-width: 768px) {
            .fiches-container {
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 20px;
            }
            
            h1 {
                font-size: 1.8rem;
            }
            
            .subtitle {
                font-size: 1rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Fiches de Lecture</h1>
            <div class="subtitle">Oeuvres littéraires analysées</div>
        </header>
        <div class="fiches-container">
            {fiches_html}
        </div>
        <div style="text-align: center; margin: 20px 0; color: #666;">
            <p>{count_fiches}</p>
            <p><small>Dernière mise à jour: {update_date}</small></p>
        </div>
    </div>
</body>
</html>"""

# Fichiers à exclure
EXCLUDE_FILES = ['index.html', 'README.html', '404.html']

# Trouver toutes les fiches HTML
html_files = glob.glob('*.html')
print(f"Fichiers HTML trouvés: {html_files}")
fiches = []

for filename in html_files:
    if filename in EXCLUDE_FILES:
        print(f"Fichier exclu: {filename}")
        continue
        
    print(f"Traitement de {filename}")
    # Extraire les informations de chaque fiche
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extraction du titre
            title = None
            if soup.find('h1'):
                title = soup.find('h1').text.strip()
                print(f"Titre trouvé via h1: {title}")
            elif soup.find('title'):
                title = soup.find('title').text.strip()
                print(f"Titre trouvé via balise title: {title}")
            else:
                title = filename.replace('.html', '').replace('-', ' ').title()
                print(f"Titre par défaut: {title}")
            
            # Extraction de l'auteur
            author = 'Auteur non spécifié'
            subtitle = soup.find(class_='subtitle')
            if subtitle:
                subtitle_text = subtitle.text.strip()
                print(f"Sous-titre trouvé: {subtitle_text}")
                
                # Essayer plusieurs patterns
                patterns = [
                    r"d[e']?\s+([\w\s\.\-]+)(\s+-|$)",  # "de Victor Hugo - Fiche"
                    r"par\s+([\w\s\.\-]+)(\s+|$)",      # "par Victor Hugo"
                    r"([\w\s\.\-]+)(\s+-\s+|$)"         # "Victor Hugo - Fiche"
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, subtitle_text)
                    if match and match.group(1):
                        author = match.group(1).strip()
                        print(f"Auteur extrait: {author}")
                        break
            
            # Extraction de la description
            description = "Fiche de lecture détaillée"
            
            # Essayer plusieurs emplacements
            selectors = [
                '#resume .highlight-box', 
                '#resume p:first-of-type',
                '.resume p:first-of-type',
                '.description',
                'meta[name="description"]',
                '#introduction p:first-of-type',
                'article p:first-of-type',
                'p:first-of-type'
            ]
            
            for selector in selectors:
                element = soup.select_one(selector)
                if element:
                    if element.name == 'meta':
                        description = element.get('content', '')
                    else:
                        description = element.text.strip()
                    
                    if description and len(description) > 20:
                        print(f"Description trouvée via {selector}")
                        break
            
            fiches.append({
                'filename': filename,
                'title': title,
                'author': author,
                'description': description
            })
            print(f"Fiche ajoutée: {filename} - {title}")
    except Exception as e:
        print(f"Erreur lors du traitement de {filename}: {str(e)}")

# Trier par titre
fiches.sort(key=lambda x: x['title'])

# Générer le HTML pour chaque fiche
fiches_html = ""
for fiche in fiches:
    description = fiche['description']
    if len(description) > 150:
        description = description[:150] + '...'
    
    fiches_html += f"""
    <div class="fiche-card">
        <div class="fiche-header">
            <h2 class="fiche-title">{fiche['title']}</h2>
            <div class="fiche-author">{fiche['author']}</div>
        </div>
        <div class="fiche-content">
            <p class="fiche-description">{description}</p>
            <a href="{fiche['filename']}" class="fiche-link">Consulter la fiche</a>
        </div>
    </div>
    """

# Texte indiquant le nombre de fiches
count_fiches = f"{len(fiches)} fiche{'s' if len(fiches) > 1 else ''} de lecture disponible{'s' if len(fiches) > 1 else ''}"

# Date de mise à jour
from datetime import datetime
update_date = datetime.now().strftime("%d/%m/%Y à %H:%M")

# Générer l'index final
index_html = INDEX_TEMPLATE.format(
    fiches_html=fiches_html,
    count_fiches=count_fiches,
    update_date=update_date
)

# Écrire le fichier index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print(f"Index généré avec {len(fiches)} fiches.")
