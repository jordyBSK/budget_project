# Mode d’emploi du projet pour gérer son budget
## 1.1. Télécharger le project (29.03.2024)

Tout doit être installé en local.

Dans un terminal de commande Windows, copiez les lignes ci-dessous et collez-les dans le terminal :

```bash
git clone https://git@github.com:jordyBSK/budget-database.git ou telecharger le fichier zip sur git hub
cd APP_BUDGET_164
pip install -r requirements.txt
python -m pip install --upgrade pip
exit
```

## 1.2. Ouvrir le projet avec PyCharm
Vous pouvez maintenant ouvrir PyCharm et aller dans le menu « File » -> « Open Project »


## 1.3 Scripts (BD) Import et test
Démarrer le serveur MySQL (Laragon (heidi.sql), UwAmp, XAMPP, MAMP, etc.)

### Importer la base de données :

Dans PyCharm, importer la base de données à partir du fichier DUMP.

Ouvrir le fichier APP_BUDGET_164/database/1_ImportationDumpSql.py.

Cliquer avec le bouton droit sur l’onglet de ce fichier et choisir “run” (CTRL-MAJ-F10).

En cas d’erreurs, ouvrir le fichier .env à la racine du projet et vérifier les informations de connexion à la base de données.

### Tester la connexion à la base de données :

Ouvrir le fichier APP_BUDGET_164/database/2_test_connection_bd.py.

Cliquer avec le bouton droit sur l’onglet de ce fichier et choisir “run” (CTRL-MAJ-F10).

### Démarrer le microframework FLASK

Dans le répertoire racine du projet, ouvrir le fichier run_mon_app.py

Cliquer avec le bouton droit sur l’onglet de ce fichier et choisir “run” (CTRL-MAJ-F10)




