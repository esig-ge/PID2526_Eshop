PROJET PID 2526

Osman Anthony Abel Mégane

Commande pour installer les requirements : pip install -r requirements.txt
Lancer le script d'ajout des prodiuts : python populate_eshop.py

Mise en place de la clé api :

Ouvrir powershell

    $>setx API_KEY_OLLAMA "clé-api-ici"

puis dans le fichier python souhaitez : 

        import os
        api_key = os.getenv("API_KEY")
        if not api_key:
            raise ValueError("API_KEY not set in environment")
