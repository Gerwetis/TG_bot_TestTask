import os


def ensure_user_dir(tg_id, file_name):
    path = os.path.join("temp", str(tg_id))
    os.makedirs(path, exist_ok=True)
    path = os.path.join(path, file_name)
    return path


# более компактное решение
def allowed_file(filename, file_type, msg_type):
    return file_type == 'document' and filename.endswith(('.pdf', '.doc', 'xlsx')) or file_type == msg_type == 'photo'

# def allowed_file(filename, file_type):
#     if file_type == "document":
#         return filename.endswith((".pdf", ".doc", ".xlsx"))
#     if file_type == "photo":
#         return True
#     return False
