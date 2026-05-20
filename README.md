# AI Delivery Search

Busca de rotas aéreas para entrega de medicamentos por drones em uma cidade com restrições de voo, usando o algoritmo **A\*** no NetworkX.

## O problema

Uma empresa de logística urbana usa drones para levar medicamentos de um **hospital central** até **postos de saúde** ou bairros mais afastados. A cidade não é um mapa livre: existem **zonas de exclusão aérea** (ex.: áreas militares), **prédios altos** e outros obstáculos que impedem voar em linha reta entre dois pontos.

O desafio é encontrar a **menor rota aérea permitida** entre origem e destino, respeitando onde o drone pode voar e quanto “custa” cada trecho.

### Modelagem em grafo

| Elemento | Significado no projeto |
|----------|------------------------|
| **Nós (vértices)** | Waypoints da cidade (hospital, praças, terminais, posto de destino), cada um com coordenadas `(x, y)` em metros |
| **Arestas** | Trechos aéreos diretos permitidos entre dois waypoints; não existem se a distância for maior que o alcance do drone ou se o segmento cruzar um obstáculo |
| **Peso `g(n)`** | Distância em metros do trecho (proxy do consumo de bateria) |
| **Heurística `h(n)`** | Distância euclidiana (linha reta) do nó atual até o destino — admissível, pois o drone voa no plano e a reta é o menor caminho possível |

### Limitações assumidas (simplificações do modelo)

- Não há vento em tempo real.
- O consumo de bateria não muda com o peso da carga ao longo do trajeto.
- Obstáculos são estáticos (zonas circulares e prédios retangulares).

## A solução

O projeto monta um **grafo não direcionado** com NetworkX a partir dos waypoints e obstáculos, e calcula a rota com **`astar_path`**, usando heurística euclidiana entre posições dos nós.

Fluxo resumido:

1. **Cenário** (`delivery_search/scenarios/smart_city.py`): define waypoints, zonas proibidas, prédios e o par origem → destino (hospital → posto periférico).
2. **Grafo** (`CityGraphBuilder`): conecta dois waypoints só se o voo direto for seguro e estiver dentro do alcance máximo.
3. **Busca** (`DroneRouteFinder`): executa A* com peso nas arestas e heurística euclidiana até o destino.
4. **Saída** (`main.py`): imprime a rota, a distância total e os trechos percorridos.

### Estrutura do código

```
delivery_search/
  domain/       # Point (coordenada) e Waypoint (nó do grafo)
  obstacles/    # NoFlyZone, Building — bloqueiam segmentos aéreos
  graph/        # Montagem do grafo urbano
  search/       # A* e resultado da rota
  scenarios/    # Cenário demo da cidade inteligente
main.py         # Ponto de entrada
```

- **`Point`**: apenas geometria `(x, y)` — distâncias, heurística e testes de colisão.
- **`Waypoint`**: lugar da cidade com `id`, nome e tipo (hospital, posto, hub) — vira nó no grafo.

## Pré-requisitos

- **Python 3.13+** (obrigatório em qualquer fluxo)
- **[uv](https://docs.astral.sh/uv/)** (opcional — recomendado, mas não obrigatório)

O repositório **não inclui** a pasta `.venv`. Depois de clonar, cada pessoa cria o ambiente virtual na própria máquina.

## Como executar

A saída mostra a rota encontrada, o número de trechos e a distância total em metros.

Escolha **uma** das opções abaixo.

### Opção A — com uv

#### Instalar o uv

**macOS / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Reabra o terminal (ou siga as instruções que o instalador mostrar) e confira:

```bash
uv --version
```

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Alternativa (se já tiver pip):**

```bash
pip install uv
```

Documentação completa: [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

#### Rodar o projeto

Na pasta do repositório:

```bash
uv sync
uv run python main.py
```

- `uv sync` — cria o `.venv` e instala dependências de `pyproject.toml` / `uv.lock`
- `uv run` — executa no ambiente do projeto **sem** precisar `source .venv/bin/activate`

### Opção B — sem uv (pip + venv)

Para quem **não quiser** instalar o uv, use só o Python padrão:

```bash
python3 -m venv .venv
```

Ative o ambiente virtual:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Instale as dependências e execute:

```bash
pip install -r requirements.txt
python main.py
```

Com o `.venv` ativo, nas próximas vezes basta `python main.py`.

### Atualizar `requirements.txt`

Se alguém alterar dependências no `pyproject.toml` (fluxo com uv), regenere o arquivo para quem usa pip:

```bash
uv export --format requirements-txt --no-hashes -o requirements.txt
```
