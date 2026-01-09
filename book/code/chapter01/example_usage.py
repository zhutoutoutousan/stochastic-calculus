"""
Beispiel-Verwendung der Martingal-Implementierungen
"""

import numpy as np
import matplotlib.pyplot as plt
from martingales import (
    SymmetricRandomWalk,
    MartingaleTransform,
    SquareIntegrableMartingale,
    optional_stopping_simulation
)

def main():
    print("=" * 70)
    print("Beispiel: Martingales in diskreter Zeit")
    print("=" * 70)
    
    # Beispiel 1: Symmetrischer Random Walk
    print("\n[Beispiel 1] Symmetrischer Random Walk")
    print("-" * 70)
    rw = SymmetricRandomWalk(n_steps=100, n_paths=1000, seed=42)
    paths = rw.simulate()
    
    print(f"Anzahl Pfade: {rw.n_paths}")
    print(f"Anzahl Zeitschritte: {rw.n_steps}")
    print(f"E[S_0] = {rw.mean(0):.6f}")
    print(f"E[S_50] = {rw.mean(50):.6f}")
    print(f"E[S_100] = {rw.mean(100):.6f}")
    print(f"Var(S_100) = {rw.variance(100):.6f}")
    print(f"Theoretische Varianz: 100")
    
    # Beispiel 2: Martingal-Transform
    print("\n[Beispiel 2] Martingal-Transform")
    print("-" * 70)
    
    def constant_strategy(k, history):
        """Konstante Strategie: H_k = 1"""
        return 1.0
    
    transform = MartingaleTransform(rw, constant_strategy, n_paths=1000)
    transform_paths = transform.simulate()
    
    print(f"E[(H·M)_0] = {transform.mean(0):.6f}")
    print(f"E[(H·M)_100] = {transform.mean(100):.6f}")
    
    # Beispiel 3: Quadratische Variation
    print("\n[Beispiel 3] Quadratische Variation")
    print("-" * 70)
    
    sq_mart = SquareIntegrableMartingale(rw)
    quad_var = sq_mart.compute_quadratic_variation()
    
    mean_quad_var_100 = np.mean(quad_var[:, -1])
    print(f"E[[M]_100] = {mean_quad_var_100:.6f}")
    print(f"Theoretisch: 100")
    
    # Beispiel 4: Optional Stopping Theorem
    print("\n[Beispiel 4] Optional Stopping Theorem")
    print("-" * 70)
    
    def stop_at_10(path):
        """Stoppzeit: Erste Zeit, wo |S_n| >= 10"""
        for i in range(1, len(path)):
            if abs(path[i]) >= 10:
                return i
        return len(path) - 1
    
    result = optional_stopping_simulation(
        rw, 
        stop_at_10, 
        n_simulations=1000
    )
    
    print(f"E[X_0] = {result['E[X_0]']:.6f}")
    print(f"E[X_tau] = {result['E[X_tau]']:.6f}")
    print(f"E[tau] = {result['E[tau]']:.6f}")
    print(f"Unterschied: {result['difference']:.6f}")
    
    if abs(result['difference']) < 0.1:
        print("✓ Optional Stopping Theorem bestätigt!")
    else:
        print("✗ Optional Stopping Theorem verletzt!")
    
    # Einfache Visualisierung
    print("\n[Visualisierung] Erstelle Plot...")
    print("-" * 70)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot 1: Random Walk Pfade
    ax1 = axes[0, 0]
    for i in range(10):
        ax1.plot(paths[i], alpha=0.6, linewidth=1)
    ax1.set_title('Symmetrischer Random Walk')
    ax1.set_xlabel('Zeit n')
    ax1.set_ylabel('S_n')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Erwartungswert
    ax2 = axes[0, 1]
    means = [rw.mean(i) for i in range(0, 101, 10)]
    time_points = np.arange(0, 101, 10)
    ax2.plot(time_points, means, 'o-', linewidth=2, color='red')
    ax2.axhline(y=0, color='black', linestyle='--')
    ax2.set_title('Erwartungswert E[S_n]')
    ax2.set_xlabel('Zeit n')
    ax2.set_ylabel('E[S_n]')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Martingal-Transform
    ax3 = axes[1, 0]
    for i in range(10):
        ax3.plot(transform_paths[i], alpha=0.6, linewidth=1, color='green')
    ax3.set_title('Martingal-Transform (H=1)')
    ax3.set_xlabel('Zeit n')
    ax3.set_ylabel('(H·M)_n')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Quadratische Variation
    ax4 = axes[1, 1]
    mean_quad_var = np.mean(quad_var, axis=0)
    time_points = np.arange(1, 101)
    ax4.plot(time_points, mean_quad_var, linewidth=2, label='Empirisch')
    ax4.plot(time_points, time_points, 'r--', linewidth=2, label='Theoretisch: n')
    ax4.set_title('Quadratische Variation')
    ax4.set_xlabel('Zeit n')
    ax4.set_ylabel('[M]_n')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle('Martingales - Beispiele', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('example_output.png', dpi=300, bbox_inches='tight')
    print("Plot gespeichert als 'example_output.png'")
    
    print("\n" + "=" * 70)
    print("Fertig!")
    print("=" * 70)


if __name__ == "__main__":
    main()
