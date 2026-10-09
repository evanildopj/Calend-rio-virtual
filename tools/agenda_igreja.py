"""Criptografa / descriptografa a agenda da igreja embutida no index.html.

A agenda fica no index.html como um bloco AES-GCM (chave derivada da senha
com PBKDF2-SHA256). Sem a senha, a página mostra só feriados e recessos.

Uso (a senha vem sempre da variável de ambiente CAL_PW, nunca do repositório):
  python tools/agenda_igreja.py decrypt               -> imprime o JSON atual
  python tools/agenda_igreja.py encrypt agenda.json   -> grava o JSON no index.html
  python tools/agenda_igreja.py init agenda.json      -> igual a encrypt, com sal novo
                                                         (invalida a senha lembrada nos navegadores)

Formato do JSON: {"2026": {"10-12": ["12 – Ministro da Eucaristia · missa 10h"]}, "2027": {}}
"""
import base64, json, os, re, secrets, sys
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

INDEX = Path(__file__).resolve().parent.parent / "index.html"
PATTERN = re.compile(r"const CHURCH_ENC = (\{.*?\}|null);")
ITER = 250_000

b64e = lambda b: base64.b64encode(b).decode()
b64d = base64.b64decode


def password():
    pw = os.environ.get("CAL_PW")
    if not pw:
        sys.exit("Defina a senha na variável de ambiente CAL_PW.")
    return pw.encode()


def key(salt, iterations):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iterations)
    return kdf.derive(password())


def current(html):
    m = PATTERN.search(html)
    if not m:
        sys.exit("Linha 'const CHURCH_ENC = ...;' não encontrada no index.html.")
    return None if m.group(1) == "null" else json.loads(m.group(1))


def decrypt():
    enc = current(INDEX.read_text(encoding="utf-8"))
    if not enc:
        return {"2026": {}, "2027": {}}
    k = key(b64d(enc["salt"]), enc["iter"])
    data = AESGCM(k).decrypt(b64d(enc["iv"]), b64d(enc["data"]), None)
    return json.loads(data)


def encrypt(path, new_salt=False):
    html = INDEX.read_text(encoding="utf-8")
    enc = current(html)
    salt = secrets.token_bytes(16) if (new_salt or not enc) else b64d(enc["salt"])
    iterations = ITER if (new_salt or not enc) else enc["iter"]
    agenda = json.loads(Path(path).read_text(encoding="utf-8"))
    iv = secrets.token_bytes(12)
    data = AESGCM(key(salt, iterations)).encrypt(
        iv, json.dumps(agenda, ensure_ascii=False).encode(), None)
    blob = json.dumps({"salt": b64e(salt), "iter": iterations, "iv": b64e(iv), "data": b64e(data)})
    INDEX.write_text(PATTERN.sub(lambda _: f"const CHURCH_ENC = {blob};", html), encoding="utf-8")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "decrypt":
        print(json.dumps(decrypt(), ensure_ascii=False, indent=2))
    elif cmd in ("encrypt", "init") and len(sys.argv) == 3:
        encrypt(sys.argv[2], new_salt=(cmd == "init"))
        print("index.html atualizado.")
    else:
        sys.exit(__doc__)
