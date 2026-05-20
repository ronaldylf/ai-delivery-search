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

- [uv](https://docs.astral.sh/uv/)
- Python 3.13+

## Como executar

Instale as dependências (cria o ambiente virtual na primeira vez):

```bash
uv sync
```

Execute o projeto:

```bash
uv run python main.py
```

A saída mostra a rota encontrada, o número de trechos e a distância total em metros.
