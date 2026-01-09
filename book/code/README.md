# Python Code für Stochastische Calculus

Dieses Verzeichnis enthält Python-Implementierungen und Visualisierungen für das Buch "Stochastische Calculus".

## Installation

1. Installieren Sie die benötigten Pakete:
```bash
pip install -r requirements.txt
```

## Struktur

```
code/
├── requirements.txt          # Python-Abhängigkeiten
├── chapter01/                # Code für Kapitel 1
│   ├── martingales.py        # Martingal-Klassen und Funktionen
│   ├── boss_challenge.py     # Boss Challenge Lösung
│   ├── visualizations.py     # Visualisierungsfunktionen
│   └── Chapter01_Notebook.ipynb  # Jupyter Notebook
└── README.md                 # Diese Datei
```

## Verwendung

### Jupyter Notebook

Öffnen Sie das Jupyter Notebook für interaktive Visualisierungen:

```bash
jupyter notebook chapter01/Chapter01_Notebook.ipynb
```

### Python-Skripte

#### Martingales simulieren

```python
from chapter01.martingales import SymmetricRandomWalk

# Erstelle symmetrischen Random Walk
rw = SymmetricRandomWalk(n_steps=100, n_paths=1000, seed=42)
paths = rw.simulate()

# Berechne Statistiken
print(f"E[S_0] = {rw.mean(0)}")
print(f"E[S_100] = {rw.mean(100)}")
print(f"Var(S_100) = {rw.variance(100)}")
```

#### Boss Challenge lösen

```python
from chapter01.boss_challenge import boss_challenge_proof, visualize_boss_challenge

# Führe Boss Challenge aus
result_bounded, result_unbounded = boss_challenge_proof()

# Erstelle Visualisierung
fig = visualize_boss_challenge()
```

#### Visualisierungen erstellen

```python
from chapter01.visualizations import (
    visualize_random_walk,
    visualize_martingale_transform,
    visualize_quadratic_variation,
    visualize_optional_stopping
)

# Erstelle alle Visualisierungen
visualize_random_walk()
visualize_martingale_transform()
visualize_quadratic_variation()
visualize_optional_stopping()
```

## Features

- **Martingal-Simulationen**: Verschiedene Martingal-Typen (Random Walk, Martingal-Transform, etc.)
- **Boss Challenge Lösungen**: Implementierung der mathematischen Herausforderungen
- **Visualisierungen**: Umfangreiche Plots für alle Konzepte
- **Statistische Analyse**: Berechnung von Erwartungswerten, Varianzen, etc.
- **Optional Stopping Theorem**: Simulation und Test des Theorems

## Nächste Schritte

- Weitere Kapitel hinzufügen
- Erweiterte Visualisierungen
- Interaktive Widgets für Parameter-Exploration
