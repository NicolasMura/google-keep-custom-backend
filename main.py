import os

import gkeepapi
import keyring
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# -----------------
# Configuration
# -----------------
load_dotenv()
EMAIL = os.getenv("KEEP_EMAIL", "")
API_KEY = os.getenv("X_API_KEY", "")  # pour sécuriser l’API
print(f"Using email: {EMAIL}")
print(f"Using API Key: {API_KEY}")

# -----------------
# Google Keep setup
# -----------------


def get_keep():
    # Auth via gpsoauth
    # To save the master_token (à faire en ligne de commande sur la machine cible, ou en local avec iTerm):
    # keyring.set_password('google-keep-token', EMAIL, MASTER_TOKEN)
    # Ne fonctionnera pas sur Render !!!
    master_token = keyring.get_password("google-keep-token", EMAIL)

    if master_token is None:
        master_token = os.getenv("KEEP_MASTER_TOKEN", "")

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

    return keep


# -----------------
# FastAPI app
# -----------------
app = FastAPI(title="Google Keep API", version="1.0")

# Schéma du body attendu


class AddItemRequest(BaseModel):
    note_title: str
    item_text: str


@app.post("/add-item-to-shopping-list")
def add_item(
    request: AddItemRequest,
    x_api_key: str = Header(None)
):
    print(f"Adding item '{request.item_text}' to note '{request.note_title}'")
    print(f"Received API Key: {x_api_key}")
    print(f"Stored API Key: {API_KEY}")

    # Vérification API key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Connexion à Keep
    keep = get_keep()

    # recherche de la note à modifier (doit être une liste de cases à cocher)
    notes = keep.find(query=request.note_title)
    # note: gkeepapi._node.TopLevelNode | None = next(notes, None)
    note = next(notes, None)

    if not note:
        raise HTTPException(
            status_code=404, detail=f"La note '{request.note_title}' est introuvable")

    # Vérifier que c’est une checklist
    if not hasattr(note, "add"):
        raise HTTPException(
            status_code=400, detail=f"La note '{request.note_title}' n'est pas une checklist")

    print(f"Note trouvée : {note.title}")

    # Ajouter une case à cocher
    # note_text = note.text
    # print(f"Items avant ajout (text):")
    # print(f"{note_text}")
    note.add(text=request.item_text, checked=False)  # type: ignore
    # print(f"Items après ajout (text):")
    # print(f"{note.text}")

    # Synchroniser
    keep.sync()
    print("Nouvel item ajouté et synchronisé ✅")

    return {"status": "ok", "note": note.title, "added_item": request.item_text}

# ✅ Endpoint de santé


@app.get("/")
async def root():
    return {"status": "running"}


@app.get("/health")
async def healthcheck():
    return JSONResponse(content={"ok": True})
