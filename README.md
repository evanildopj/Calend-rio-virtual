# Calendário virtual 2026–2027

Feriados nacionais e de São Paulo, recessos acadêmico-administrativos da PUC-SP e datas comemorativas, publicados pelo GitHub Pages a partir do `index.html`.

A agenda pessoal da paróquia fica criptografada dentro da página (AES-GCM, chave derivada da senha com PBKDF2). Quem abre o link sem a senha vê só o calendário público. O script `tools/agenda_igreja.py` grava ou lê essa agenda; a senha vem da variável de ambiente `CAL_PW` e nunca é salva no repositório.
