# put python doc here
"""
This script demonstrates how to use the gkeepapi library to interact with Google Keep.
It authenticates the user using a master token stored in a keyring and creates a new note.
See https://github.com/kiwiz/gkeepapi?tab=readme-ov-file for more details.
"""

import gkeepapi
import keyring

EMAIL = "contact@nicolasmura.fr"

# To save the master_token (à faire en ligne de commande sur la machine cible, ou en local avec iTerm):
# keyring.set_password('google-keep-token', EMAIL, MASTER_TOKEN)
# (Pour info : le master_token est dans "Google Gmail PRO (master_token)" sur EnPass)
master_token = keyring.get_password("google-keep-token", EMAIL)

if master_token is None:
    raise ValueError(
        "Master token not found in keyring for email: {}".format(EMAIL))

keep = gkeepapi.Keep()

try:
    keep.authenticate(EMAIL, master_token)
except Exception as exc:
    raise ValueError(
        "Failed to authenticate with Google Keep. Check your master token."
    ) from exc

print("Connexion réussie à Google Keep ✅")

# TESTS
# note: gkeepapi._node.TopLevelNode = keep.createNote('Todo', 'Eat breakfast')  # type: ignore
# note.pinned = True
# note.color = gkeepapi._node.ColorValue.Red

# keep.sync()

# # print(note.title)
# print(note.text)
# END TESTS

# Retrouver une note existante
# titre de la note à modifier (doit être une liste de cases à cocher)
NOTE_TITLE = "Test gkeepapi"
# NOTE_TITLE = "Gourmandises"

notes = keep.find(query=NOTE_TITLE)
# note: gkeepapi._node.TopLevelNode | None = next(notes, None)
note = next(notes, None)

if not note:
    raise Exception(f"Note '{NOTE_TITLE}' introuvable")

# Vérifier que c’est une checklist
if not hasattr(note, "add"):
    raise Exception(f"La note '{NOTE_TITLE}' n'est pas une checklist")

print(f"Note trouvée : {note.title}")

# Ajouter une case à cocher
note_text = note.text
print(f"Items avant ajout (text):")
print(f"{note_text}")
note.add(text='Acheter du lait', checked=False)  # type: ignore
print(f"Items après ajout (text):")
print(f"{note.text}")

# Synchroniser
keep.sync()
print("Nouvel item ajouté et synchronisé ✅")
