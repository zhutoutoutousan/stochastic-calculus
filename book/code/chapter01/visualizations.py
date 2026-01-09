"""
Visualisierungen für Kapitel 1: Martingales in diskreter Zeit
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from martingales import (
    SymmetricRandomWalk, 
    GeneralRandomWalk, 
    MartingaleTransform,
    SquareIntegrableMartingale,
    optional_stopping_simulation
)

# Stil für Plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def visualize_random_walk():
    """Visualisiert symmetrischen Random Walk"""
    rw = SymmetricRandomWalk(n_steps=100, n_paths=10, seed=42)
    paths = rw.get_paths()
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Einzelne Pfade
    ax1 = axes[0, 0]
    for i in range(10):
        ax1.plot(paths[i], alpha=0.7, linewidth=1.5)
    ax1.set_title('Symmetrischer Random Walk - 10 Pfade')
    ax1.set_xlabel('Zeit n')
    ax1.set_ylabel('S_n')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color='black', linestyle='--', linewidth=1)
    
    # Plot 2: Erwartungswert über Zeit
    ax2 = axes[0, 1]
    means = [rw.mean(i) for i in range(101)]
    ax2.plot(means, linewidth=2, color='red', label='E[S_n]')
    ax2.axhline(y=0, color='black', linestyle='--', linewidth=1)
    ax2.set_title('Erwartungswert E[S_n]')
    ax2.set_xlabel('Zeit n')
    ax2.set_ylabel('E[S_n]')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Varianz über Zeit
    ax3 = axes[1, 0]
    variances = [rw.variance(i) for i in range(101)]
    theoretical_var = np.arange(101)  # Var(S_n) = n für symmetrischen RW
    ax3.plot(variances, linewidth=2, color='blue', label='Empirische Varianz')
    ax3.plot(theoretical_var, linewidth=2, color='red', linestyle='--', 
             label='Theoretische Varianz: n')
    ax3.set_title('Varianz Var(S_n)')
    ax3.set_xlabel('Zeit n')
    ax3.set_ylabel('Var(S_n)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Verteilung bei verschiedenen Zeitpunkten
    ax4 = axes[1, 1]
    time_points = [10, 50, 100]
    for t in time_points:
        ax4.hist(paths[:, t], bins=30, alpha=0.6, label=f't = {t}')
    ax4.set_title('Verteilung von S_n zu verschiedenen Zeitpunkten')
    ax4.set_xlabel('Wert von S_n')
    ax4.set_ylabel('Häufigkeit')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle('Symmetrischer Random Walk - Analyse', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('random_walk_analysis.png', dpi=300, bbox_inches='tight')
    print("Visualisierung gespeichert als 'random_walk_analysis.png'")
    return fig


def visualize_martingale_transform():
    """Visualisiert Martingal-Transform"""
    base_rw = SymmetricRandomWalk(n_steps=100, n_paths=5, seed=42)
    
    # Strategie: H_k = 1 (konstante Strategie)
    def constant_strategy(k, history):
        return 1.0
    
    # Strategie: H_k = S_{k-1} (proportional zur aktuellen Position)
    def proportional_strategy(k, history):
        if len(history) == 0:
            return 0
        return history[-1]
    
    transform1 = MartingaleTransform(base_rw, constant_strategy, n_paths=5)
    transform2 = MartingaleTransform(base_rw, proportional_strategy, n_paths=5)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    base_paths = base_rw.get_paths()
    transform1_paths = transform1.get_paths()
    transform2_paths = transform2.get_paths()
    
    # Plot 1: Basis-Martingal
    ax1 = axes[0, 0]
    for i in range(5):
        ax1.plot(base_paths[i], alpha=0.7, linewidth=1.5)
    ax1.set_title('Basis-Martingal: Symmetrischer Random Walk')
    ax1.set_xlabel('Zeit n')
    ax1.set_ylabel('S_n')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Martingal-Transform mit konstanter Strategie
    ax2 = axes[0, 1]
    for i in range(5):
        ax2.plot(transform1_paths[i], alpha=0.7, linewidth=1.5, color='green')
    ax2.set_title('Martingal-Transform: H_k = 1 (konstant)')
    ax2.set_xlabel('Zeit n')
    ax2.set_ylabel('(H · M)_n')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Martingal-Transform mit proportionaler Strategie
    ax3 = axes[1, 0]
    for i in range(5):
        ax3.plot(transform2_paths[i], alpha=0.7, linewidth=1.5, color='orange')
    ax3.set_title('Martingal-Transform: H_k = S_{k-1} (proportional)')
    ax3.set_xlabel('Zeit n')
    ax3.set_ylabel('(H · M)_n')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Vergleich der Erwartungswerte
    ax4 = axes[1, 1]
    time_points = np.arange(0, 101, 10)
    base_means = [base_rw.mean(t) for t in time_points]
    transform1_means = [transform1.mean(t) for t in time_points]
    transform2_means = [transform2.mean(t) for t in time_points]
    
    ax4.plot(time_points, base_means, 'o-', label='Basis-Martingal', linewidth=2)
    ax4.plot(time_points, transform1_means, 's-', label='Transform (H=1)', linewidth=2)
    ax4.plot(time_points, transform2_means, '^-', label='Transform (H=S)', linewidth=2)
    ax4.axhline(y=0, color='black', linestyle='--', linewidth=1)
    ax4.set_title('Erwartungswerte über Zeit')
    ax4.set_xlabel('Zeit n')
    ax4.set_ylabel('E[X_n]')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle('Martingal-Transform - Visualisierung', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('martingale_transform.png', dpi=300, bbox_inches='tight')
    print("Visualisierung gespeichert als 'martingale_transform.png'")
    return fig


def visualize_quadratic_variation():
    """Visualisiert quadratische Variation"""
    rw = SymmetricRandomWalk(n_steps=100, n_paths=1000, seed=42)
    sq_mart = SquareIntegrableMartingale(rw)
    
    paths = sq_mart.get_paths()
    quad_var = sq_mart.compute_quadratic_variation()
    pred_quad = sq_mart.compute_predictable_quadratic()
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Einzelne Pfade mit quadratischer Variation
    ax1 = axes[0, 0]
    for i in range(5):
        ax1.plot(paths[i], alpha=0.6, linewidth=1.5, label=f'Pfad {i+1}')
    ax1.set_title('Martingal-Pfade')
    ax1.set_xlabel('Zeit n')
    ax1.set_ylabel('M_n')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Quadratische Variation
    ax2 = axes[0, 1]
    time_points = np.arange(1, 101)
    mean_quad_var = np.mean(quad_var, axis=0)
    theoretical = time_points  # [M]_n = n für symmetrischen RW
    
    ax2.plot(time_points, mean_quad_var, linewidth=2, label='Empirisch: E[[M]_n]')
    ax2.plot(time_points, theoretical, '--', linewidth=2, label='Theoretisch: n')
    ax2.set_title('Quadratische Variation [M]_n')
    ax2.set_xlabel('Zeit n')
    ax2.set_ylabel('[M]_n')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Vorhersehbarer quadratischer Prozess
    ax3 = axes[1, 0]
    mean_pred_quad = np.mean(pred_quad, axis=0)
    ax3.plot(time_points, mean_pred_quad, linewidth=2, label='<M>_n')
    ax3.plot(time_points, theoretical, '--', linewidth=2, label='Theoretisch: n')
    ax3.set_title('Vorhersehbarer quadratischer Prozess <M>_n')
    ax3.set_xlabel('Zeit n')
    ax3.set_ylabel('<M>_n')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Verteilung der quadratischen Variation
    ax4 = axes[1, 1]
    final_quad_var = quad_var[:, -1]
    ax4.hist(final_quad_var, bins=50, alpha=0.7, edgecolor='black')
    ax4.axvline(np.mean(final_quad_var), color='red', linestyle='--', 
                linewidth=2, label=f'Mittelwert: {np.mean(final_quad_var):.2f}')
    ax4.axvline(100, color='green', linestyle='--', linewidth=2, 
                label='Theoretisch: 100')
    ax4.set_title('Verteilung von [M]_100')
    ax4.set_xlabel('[M]_100')
    ax4.set_ylabel('Häufigkeit')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle('Quadratische Variation - Analyse', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('quadratic_variation.png', dpi=300, bbox_inches='tight')
    print("Visualisierung gespeichert als 'quadratic_variation.png'")
    return fig


def visualize_optional_stopping():
    """Visualisiert Optional Stopping Theorem"""
    rw = SymmetricRandomWalk(n_steps=100, n_paths=1000, seed=42)
    
    # Verschiedene Stoppzeiten
    def stop_at_10(path):
        for i in range(1, len(path)):
            if abs(path[i]) >= 10:
                return i
        return len(path) - 1
    
    def stop_at_20(path):
        for i in range(1, len(path)):
            if abs(path[i]) >= 20:
                return i
        return len(path) - 1
    
    result1 = optional_stopping_simulation(rw, stop_at_10, n_simulations=1000)
    result2 = optional_stopping_simulation(rw, stop_at_20, n_simulations=1000)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Verteilung der Stoppzeiten
    ax1 = axes[0, 0]
    ax1.hist(result1['stopping_times'], bins=30, alpha=0.7, label='|S_n| >= 10')
    ax1.hist(result2['stopping_times'], bins=30, alpha=0.7, label='|S_n| >= 20')
    ax1.set_title('Verteilung der Stoppzeiten')
    ax1.set_xlabel('Stoppzeit τ')
    ax1.set_ylabel('Häufigkeit')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Vergleich E[X_0] vs E[X_tau]
    ax2 = axes[0, 1]
    categories = ['E[X_0]', 'E[X_τ] (|S|>=10)', 'E[X_τ] (|S|>=20)']
    values = [
        result1['E[X_0]'],
        result1['E[X_tau]'],
        result2['E[X_tau]']
    ]
    colors = ['blue', 'green', 'orange']
    bars = ax2.bar(categories, values, color=colors, alpha=0.7, edgecolor='black')
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax2.set_title('Optional Stopping Theorem Test')
    ax2.set_ylabel('Erwartungswert')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Füge Werte auf Balken hinzu
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.4f}', ha='center', va='bottom')
    
    # Plot 3: Pfade mit Stoppzeiten markiert
    ax3 = axes[1, 0]
    paths = rw.get_paths()
    for i in range(10):
        path = paths[i]
        tau = stop_at_10(path)
        ax3.plot(path[:tau+1], alpha=0.6, linewidth=1.5)
        ax3.scatter([tau], [path[tau]], s=100, color='red', zorder=5, marker='X')
    ax3.axhline(y=10, color='red', linestyle='--', alpha=0.5)
    ax3.axhline(y=-10, color='red', linestyle='--', alpha=0.5)
    ax3.set_title('Pfade mit Stoppzeiten (|S_n| >= 10)')
    ax3.set_xlabel('Zeit n')
    ax3.set_ylabel('S_n')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Unterschied E[X_tau] - E[X_0]
    ax4 = axes[1, 1]
    differences = [
        result1['difference'],
        result2['difference']
    ]
    labels = ['|S_n| >= 10', '|S_n| >= 20']
    colors = ['green', 'orange']
    bars = ax4.bar(labels, differences, color=colors, alpha=0.7, edgecolor='black')
    ax4.axhline(y=0, color='black', linestyle='-', linewidth=2)
    ax4.set_title('Unterschied: E[X_τ] - E[X_0]')
    ax4.set_ylabel('Unterschied')
    ax4.grid(True, alpha=0.3, axis='y')
    
    for bar, diff in zip(bars, differences):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{diff:.6f}', ha='center', 
                va='bottom' if height >= 0 else 'top')
    
    plt.suptitle('Optional Stopping Theorem - Visualisierung', 
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('optional_stopping.png', dpi=300, bbox_inches='tight')
    print("Visualisierung gespeichert als 'optional_stopping.png'")
    return fig


if __name__ == "__main__":
    print("Erstelle Visualisierungen für Kapitel 1...")
    print("=" * 70)
    
    print("\n1. Random Walk Visualisierung...")
    visualize_random_walk()
    
    print("\n2. Martingal-Transform Visualisierung...")
    visualize_martingale_transform()
    
    print("\n3. Quadratische Variation Visualisierung...")
    visualize_quadratic_variation()
    
    print("\n4. Optional Stopping Theorem Visualisierung...")
    visualize_optional_stopping()
    
    print("\n" + "=" * 70)
    print("Alle Visualisierungen erstellt!")
    print("=" * 70)
