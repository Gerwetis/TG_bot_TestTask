import os

def ensure_user_dir(tg_id):
    path = os.path.join("temp", str(tg_id))
    os.makedirs(path, exist_ok=True)
    return path

def allowed_file(filename, file_type):
    if file_type == "document":
        return filename.endswith((".pdf", ".doc", ".xlsx"))
    if file_type == "photo":
        return True 
    return False
