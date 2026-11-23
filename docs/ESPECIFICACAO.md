# Especificação do calendário 2026–2027

Página única em HTML, sem dependências externas além das fontes do Google (Cormorant Garamond e Outfit). O arquivo `index.html` é a fonte da verdade: copiá-lo recria a página idêntica.

## 1. Para recriar do zero

1. Copie `index.html` para qualquer pasta ou serviço de hospedagem estática (GitHub Pages, Netlify, pasta local).
2. Abra no navegador. Não há build, servidor nem banco de dados.

## 2. Estrutura da página (de cima para baixo)

1. **Cabeçalho** (`header.hero`): selo, título "2026 & 2027" e subtítulo.
2. **Barra de anos** (`.toolbar`): botões 2026, 2027 e "Ver os dois anos".
3. **Legenda** (`.legend`): Feriado, Recesso PUC, Pós-Graduação (PG), Data comemorativa, Início das estações, Eclipse, Hoje e Mês vigente.
4. **Blocos de ano** (`section.year-block`): título do ano e uma grade (`.grid`) de 12 cards.
5. **Rodapé**: fontes, observação sobre horário e sobre a compensação dos recessos de 2027.

## 3. Card de mês (`article.month`)

- Título em minúsculas, selo "MÊS VIGENTE" no mês atual.
- Tabela (`table.cal`) com cabeçalho D S T Q Q S S. Domingo em rosa.
- Notas (`.notes`) com o nome em negrito antes de " – ". Passar o mouse em um dia ou numa linha da legenda acende o par.

## 4. Grade responsiva

- Acima de 980 px: 3 colunas. De 641 a 980 px: 2. Até 640 px: 1.
- Sem rolagem lateral. Margem mínima de 16 px.

## 5. Dados

### 5.1 Feriados, recessos, PG e comemorações (`const events`)
Objeto por ano, com chave `"mês-dia"` (sem zero à esquerda, exemplo `"10-12"`). Cada dia pode ter:
- `type`: `holiday`, `recesso` ou `commemo`. Opcional.
- `label`: texto da nota. Vazio significa "continuação do dia anterior"; use `ref` para apontar ao dia que tem o texto.
- `pg`: lista de textos de Pós-Graduação. O dia recebe a cor de PG e cada texto vira uma linha "PG ·" nas notas.

### 5.2 Estações e eclipses (`const ASTRO`)
Lista por dia com tipo `"estacao"` ou `"eclipse"`. Horário de Brasília (UTC-3).

## 6. Estilo

Tema claro. Tokens principais:

| Uso | Valor |
|---|---|
| Fundo da página | `#e7e5de` |
| Cards | `#ffffff` com borda `#e3e6ee` |
| Texto | `#1c2230` |
| Feriado | fundo `#fbe4eb`, texto `#9b1b44` |
| Recesso | fundo `#dcf4ec`, texto `#0f6b57` |
| Comemorativo | fundo `#fbf1cc`, texto `#7a5a00` |
| PG | fundo `#e4ecfa`, texto `#2d4f8c` |
| Mês vigente | borda `#c99a2e` |
| Hoje | contorno dourado pulsando a cada 2,6 s (sem animação se o sistema pedir movimento reduzido) |

As cores ficam na seção "Tema claro" do CSS, no fim da `<style>`.

## 7. Impressão

`@media print` remove o fundo, os botões e o selo "mês vigente", e força texto preto. Cada ano sai em página própria.

## 8. Comportamento (JavaScript)

- `renderYear(year, id)` monta os 12 meses de um ano, aplica as classes de `events` e `ASTRO` e monta o `data-note` (com `||` entre rótulos).
- Hover: `mouseover` e `mouseout` em cada card acendem a linha da legenda e o dia correspondente.

## 9. Manutenção

- **Mudar feriados, recessos ou PG**: editar `events` em `index.html`.
- **Publicar**: commit e push na branch `main`. O GitHub Pages atualiza sozinho.
