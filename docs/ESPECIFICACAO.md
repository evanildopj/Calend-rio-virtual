# Especificação do calendário 2026–2027

Página única em HTML, sem dependências externas além da fonte do Google (Cormorant Garamond e Outfit). O arquivo `index.html` é a fonte da verdade: copiá-lo já recria a página idêntica.

## 1. Para recriar do zero

1. Copie `index.html` para qualquer pasta ou serviço de hospedagem estática (GitHub Pages, Netlify, pasta local).
2. Abra no navegador. Não há build, servidor nem banco de dados.
3. Para alterar a agenda da igreja, use `tools/agenda_igreja.py` com a senha na variável de ambiente `CAL_PW`. Ele exige o pacote `cryptography` (`pip install cryptography`).

Se a página precisar ser recriada sem o arquivo original, esta especificação descreve tudo o que ele faz: layout, dados, estilos e comportamento.

## 2. Estrutura da página (de cima para baixo)

1. **Cabeçalho** (`header.hero`): selo "Calendário anual · São Paulo · PUC-SP", título "2026 & 2027" e subtítulo.
2. **Barra de anos** (`.toolbar`): botões 2026, 2027 e "Ver os dois anos". O botão ativo fica preenchido em gradiente.
3. **Legenda** (`.legend`): bolinhas coloridas que explicam as marcações:
   - Feriado (rosa)
   - Recesso PUC (verde-água)
   - Data comemorativa / ponto facultativo (dourado)
   - Igreja (Livração) (azul, com ponto)
   - Hoje (contorno lilás pulsante)
   - Mês vigente (contorno dourado)
   - Início das estações (verde, com ✦)
   - Eclipse (laranja, com ◐)
4. **Bloco de senha** (`#lock`): campo "Agenda da igreja", botão "Mostrar", dica da senha e botão "Ocultar agenda da igreja".
5. **Blocos de ano** (`section.year-block`): título do ano e uma grade (`.grid`) de 12 cards, um por mês.
6. **Rodapé**: fontes, observação sobre horário e aviso sobre os recessos de 2027.

## 3. Anatomia de cada card de mês (`article.month`)

- **Título**: nome do mês em Cormorant Garamond, minúsculo.
- **Selo "MÊS VIGENTE"**: aparece só no mês atual, no canto superior direito.
- **Tabela** (`table.cal`): cabeçalho D S T Q Q S S, com domingo em rosa. Cada dia é um `td`.
- **Notas** (`.notes`): lista de marcações do mês, com o nome em negrito antes de " – ". Ao passar o mouse em um dia, a linha correspondente acende.
- **Interação**: passar o mouse em um dia ou em uma linha da legenda destaca o par (dia ↔ linha).

## 4. Grade responsiva

- Acima de 980 px: 3 colunas.
- De 641 a 980 px: 2 colunas.
- Até 640 px: 1 coluna.
- O corpo nunca tem rolagem lateral. O espaçamento lateral mínimo é de 16 px.

## 5. Dados

### 5.1 Feriados e recessos (`const events`)
Objeto por ano, com chave `"mês-dia"` (sem zero à esquerda, exemplo `"10-12"`). Cada valor é `{ type, label }`:
- `type`: `holiday`, `recesso`, `commemo` ou `holiday`.
- `label`: texto da nota. Vazio significa "continuação do dia anterior". Use `ref` para apontar a um dia que tem o texto.

### 5.2 Agenda da igreja (`const CHURCH_ENC`)
Criptografada. Não há compromissos em texto aberto no arquivo. O formato, depois de descriptografado, é:
```json
{"2026": {"10-12": ["12 – Ministro da Eucaristia · missa 10h"]}, "2027": {}}
```
- Chave: `mês-dia`.
- Valor: lista de rótulos no formato `DIA – Título (horário)`.
- Cifra: AES-GCM 256 bits. Chave derivada da senha com PBKDF2-SHA256, 250 mil iterações e sal aleatório.
- Ao abrir, a página pede a senha e guarda a chave derivada no `localStorage` do navegador (chave `agenda-igreja-chave`). O botão "Ocultar" apaga essa chave.

### 5.3 Estações e eclipses (`const ASTRO`)
Mesmo formato de lista, com tipo: `"estacao"` ou `"eclipse"`. Horário de Brasília (UTC-3). Estações e eclipses são públicos e ficam em texto aberto.

## 6. Estilo

Tokens em `:root`:

| Token | Valor | Uso |
|---|---|---|
| `--bg` | `#07070e` | fundo |
| `--paper` | `rgba(14,16,28,.78)` | cards |
| `--ink` | `#e8edf7` | texto |
| `--muted` | `#8b93ad` | textos secundários |
| `--line` | `rgba(120,240,255,.18)` | bordas |
| `--sunday` | `#ff4d8d` | domingos |
| `--holiday` | `#ff2d6a` | feriados |
| `--recesso` | `#14f1c4` | recessos |
| `--gold` | `#ffe36b` | mês vigente e datas comemorativas |
| `--cyan` | `#3cf0ff` | destaques |
| `--today` | `#b9a4ff` | hoje |
| `--church` | `#6cb8ff` | igreja |

Tipografia: Cormorant Garamond para títulos e Outfit para o texto.

Efeitos:
- **Hoje**: contorno dourado com brilho neon, pulsando a cada 2,6 s. Sem animação se o sistema pedir movimento reduzido.
- **Recesso e feriado**: fundo translúcido com contorno interno.
- **Igreja**: ponto azul na parte de baixo da célula.
- **Lua e estações**: ponto na parte de cima. Eclipse: contorno laranja.

## 7. Impressão

`@media print` remove o fundo, o botão e o selo "mês vigente", e força texto preto. Cada ano sai em página própria.

## 8. Comportamento (JavaScript)

- `renderYear(year, id)` monta os 12 meses de um ano. Para cada dia: aplica as classes de `events`, `church` e `ASTRO`, e monta o `data-note` (com `||` entre rótulos).
- `renderAll()` redesenha os dois anos. Chamado depois de descriptografar ou ocultar a agenda.
- Desbloqueio: `crypto.subtle` faz PBKDF2 e AES-GCM. Senha errada mostra "Senha incorreta. Tente de novo."
- Hover: `mouseover` e `mouseout` em cada card acendem a linha da legenda e o dia correspondente.

## 9. Manutenção

- **Mudar feriados ou recessos**: editar `events` em `index.html`.
- **Mudar a agenda da igreja**: `CAL_PW=... python3 tools/agenda_igreja.py decrypt > agenda.json`, editar, depois `CAL_PW=... python3 tools/agenda_igreja.py encrypt agenda.json`. Use `encrypt`, nunca `init`, para não invalidar a senha lembrada nos navegadores.
- **Trocar a senha**: `init` com a nova `CAL_PW`. Todos os navegadores precisarão digitar a senha de novo.
- **Publicar**: fazer commit e push na branch `main`. O GitHub Pages atualiza sozinho.
