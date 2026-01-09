"""
Skript zum Generieren aller Bilder für LaTeX
Führt alle Visualisierungen aus und speichert sie im richtigen Format
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend für Server
import matplotlib.pyplot as plt
import sys
import os

# Füge aktuelles Verzeichnis zum Pfad hinzu
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from visualizations import (
    visualize_random_walk,
    visualize_martingale_transform,
    visualize_quadratic_variation,
    visualize_optional_stopping
)
from boss_challenge import visualize_boss_challenge

def main():
    print("=" * 70)
    print("Generiere alle Bilder für LaTeX")
    print("=" * 70)
    
    # Stelle sicher, dass wir im richtigen Verzeichnis sind
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("\n1. Generiere Random Walk Visualisierung...")
    try:
        fig = visualize_random_walk()
        plt.close(fig)
        print("   ✓ random_walk_analysis.png erstellt")
    except Exception as e:
        print(f"   ✗ Fehler: {e}")
    
    print("\n2. Generiere Martingal-Transform Visualisierung...")
    try:
        fig = visualize_martingale_transform()
        plt.close(fig)
        print("   ✓ martingale_transform.png erstellt")
    except Exception as e:
        print(f"   ✗ Fehler: {e}")
    
    print("\n3. Generiere Quadratische Variation Visualisierung...")
    try:
        fig = visualize_quadratic_variation()
        plt.close(fig)
        print("   ✓ quadratic_variation.png erstellt")
    except Exception as e:
        print(f"   ✗ Fehler: {e}")
    
    print("\n4. Generiere Optional Stopping Visualisierung...")
    try:
        fig = visualize_optional_stopping()
        plt.close(fig)
        print("   ✓ optional_stopping.png erstellt")
    except Exception as e:
        print(f"   ✗ Fehler: {e}")
    
    print("\n5. Generiere Boss Challenge Visualisierung...")
    try:
        fig = visualize_boss_challenge()
        plt.close(fig)
        print("   ✓ boss_challenge_visualization.png erstellt")
    except Exception as e:
        print(f"   ✗ Fehler: {e}")
    
    print("\n" + "=" * 70)
    print("Alle Bilder wurden generiert!")
    print("=" * 70)
    print("\nHinweis: Die Bilder befinden sich im Verzeichnis:")
    print(f"  {os.path.abspath('.')}")
    print("\nFür LaTeX: Die Bilder werden automatisch eingebunden,")
    print("wenn sie im code/chapter01/ Verzeichnis sind.")

if __name__ == "__main__":
    main()
