"""
BOSS CHALLENGE: Der Martingal-Dämon
Löst und visualisiert die Boss Challenge aus Kapitel 1
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from martingales import SymmetricRandomWalk, optional_stopping_simulation
import seaborn as sns

# Dark Souls Stil für Plots
DARK_SOULS_COLORS = {
    'background': '#0a0a0a',
    'text': '#d4af37',
    'accent': '#8b0000',
    'highlight': '#ff4500',
    'grid': '#2a2a2a'
}

plt.style.use('dark_background')
sns.set_palette("dark")


def boss_challenge_proof():
    """
    Beweist das Optional Stopping Theorem für beschränkte Stoppzeiten
    und zeigt ein Gegenbeispiel für unbeschränkte Stoppzeiten
    """
    print("=" * 70)
    print("BOSS CHALLENGE: Der Martingal-Dämon")
    print("=" * 70)
    print("\nHerausforderung: Optional Stopping Theorem")
    print("-" * 70)
    
    # Teil 1: Beweis für beschränkte Stoppzeit
    print("\n[TEIL 1] Test mit beschränkter Stoppzeit")
    print("-" * 70)
    
    def bounded_stopping_time(path, bound=50):
        """Stoppzeit: Erste Zeit, wo |S_n| >= 10, aber maximal bei bound"""
        for i in range(1, min(len(path), bound + 1)):
            if abs(path[i]) >= 10:
                return i
        return bound
    
    rw = SymmetricRandomWalk(n_steps=100, n_paths=10000, seed=42)
    result_bounded = optional_stopping_simulation(
        rw, 
        lambda path: bounded_stopping_time(path, bound=50),
        n_simulations=10000
    )
    
    print(f"E[X_0] = {result_bounded['E[X_0]']:.6f}")
    print(f"E[X_tau] = {result_bounded['E[X_tau]']:.6f}")
    print(f"E[tau] = {result_bounded['E[tau]']:.6f}")
    print(f"Unterschied: {result_bounded['difference']:.6f}")
    print(f"✓ Theorem gilt für beschränkte Stoppzeit!")
    
    # Teil 2: Gegenbeispiel für unbeschränkte Stoppzeit
    print("\n[TEIL 2] Gegenbeispiel: Unbeschränkte Stoppzeit")
    print("-" * 70)
    print("Stoppzeit: tau = inf{n: S_n = 1}")
    print("(Erste Zeit, wo Random Walk den Wert 1 erreicht)")
    
    def first_hit_one(path):
        """Stoppzeit: Erste Zeit, wo S_n = 1"""
        for i in range(1, len(path)):
            if path[i] == 1:
                return i
        return len(path) - 1  # Falls nie erreicht
    
    rw2 = SymmetricRandomWalk(n_steps=200, n_paths=10000, seed=123)
    result_unbounded = optional_stopping_simulation(
        rw2,
        first_hit_one,
        n_simulations=10000
    )
    
    print(f"E[X_0] = {result_unbounded['E[X_0]']:.6f}")
    print(f"E[X_tau] = {result_unbounded['E[X_tau]']:.6f}")
    print(f"E[tau] = {result_unbounded['E[tau]']:.6f}")
    print(f"Unterschied: {result_unbounded['difference']:.6f}")
    
    if abs(result_unbounded['difference']) > 0.01:
        print("✗ Theorem gilt NICHT für unbeschränkte Stoppzeit!")
        print("  Grund: E[tau] = ∞ (Random Walk erreicht 1 fast sicher,")
        print("         aber die erwartete Zeit ist unendlich)")
    else:
        print("? Interessant - in dieser Simulation scheint es zu funktionieren")
        print("  (Dies kann bei endlicher Simulationszeit passieren)")
    
    return result_bounded, result_unbounded


def visualize_boss_challenge():
    """
    Visualisiert die Boss Challenge Ergebnisse
    """
    # Simuliere beide Fälle
    rw_bounded = SymmetricRandomWalk(n_steps=100, n_paths=1000, seed=42)
    rw_unbounded = SymmetricRandomWalk(n_steps=200, n_paths=1000, seed=123)
    
    def bounded_stop(path, bound=50):
        for i in range(1, min(len(path), bound + 1)):
            if abs(path[i]) >= 10:
                return i
        return bound
    
    def first_hit_one(path):
        for i in range(1, len(path)):
            if path[i] == 1:
                return i
        return len(path) - 1
    
    # Erstelle Figure mit Dark Souls Stil
    fig = plt.figure(figsize=(16, 10))
    fig.patch.set_facecolor(DARK_SOULS_COLORS['background'])
    
    # Plot 1: Beschränkte Stoppzeit
    ax1 = plt.subplot(2, 2, 1)
    paths_bounded = rw_bounded.get_paths()
    stopping_times = [bounded_stop(paths_bounded[i]) for i in range(100)]
    
    for i in range(20):  # Zeige 20 Pfade
        path = paths_bounded[i]
        tau = stopping_times[i]
        ax1.plot(path[:tau+1], alpha=0.6, linewidth=1.5, color='#d4af37')
        ax1.scatter([tau], [path[tau]], s=100, color='#ff4500', zorder=5, marker='X')
        ax1.axhline(y=10, color='#8b0000', linestyle='--', alpha=0.5)
        ax1.axhline(y=-10, color='#8b0000', linestyle='--', alpha=0.5)
    
    ax1.set_title('Beschränkte Stoppzeit: |S_n| >= 10', 
                  color=DARK_SOULS_COLORS['text'], fontsize=14, fontweight='bold')
    ax1.set_xlabel('Zeit n', color=DARK_SOULS_COLORS['text'])
    ax1.set_ylabel('S_n', color=DARK_SOULS_COLORS['text'])
    ax1.grid(True, alpha=0.3, color=DARK_SOULS_COLORS['grid'])
    ax1.set_facecolor(DARK_SOULS_COLORS['background'])
    ax1.tick_params(colors=DARK_SOULS_COLORS['text'])
    
    # Plot 2: Verteilung der Stoppzeiten (beschränkt)
    ax2 = plt.subplot(2, 2, 2)
    ax2.hist(stopping_times, bins=30, color=DARK_SOULS_COLORS['accent'], 
             edgecolor=DARK_SOULS_COLORS['text'], alpha=0.7)
    ax2.axvline(np.mean(stopping_times), color=DARK_SOULS_COLORS['highlight'], 
                linestyle='--', linewidth=2, label=f'E[τ] = {np.mean(stopping_times):.2f}')
    ax2.set_title('Verteilung der Stoppzeiten (beschränkt)', 
                  color=DARK_SOULS_COLORS['text'], fontsize=14, fontweight='bold')
    ax2.set_xlabel('Stoppzeit τ', color=DARK_SOULS_COLORS['text'])
    ax2.set_ylabel('Häufigkeit', color=DARK_SOULS_COLORS['text'])
    ax2.legend()
    ax2.grid(True, alpha=0.3, color=DARK_SOULS_COLORS['grid'])
    ax2.set_facecolor(DARK_SOULS_COLORS['background'])
    ax2.tick_params(colors=DARK_SOULS_COLORS['text'])
    
    # Plot 3: Unbeschränkte Stoppzeit
    ax3 = plt.subplot(2, 2, 3)
    paths_unbounded = rw_unbounded.get_paths()
    stopping_times_unb = [first_hit_one(paths_unbounded[i]) for i in range(100)]
    
    for i in range(20):  # Zeige 20 Pfade
        path = paths_unbounded[i]
        tau = stopping_times_unb[i]
        ax3.plot(path[:tau+1], alpha=0.6, linewidth=1.5, color='#d4af37')
        ax3.scatter([tau], [path[tau]], s=100, color='#ff4500', zorder=5, marker='X')
        ax3.axhline(y=1, color='#8b0000', linestyle='--', alpha=0.5, label='Ziel: S_n = 1')
    
    ax3.set_title('Unbeschränkte Stoppzeit: τ = inf{n: S_n = 1}', 
                  color=DARK_SOULS_COLORS['text'], fontsize=14, fontweight='bold')
    ax3.set_xlabel('Zeit n', color=DARK_SOULS_COLORS['text'])
    ax3.set_ylabel('S_n', color=DARK_SOULS_COLORS['text'])
    ax3.legend()
    ax3.grid(True, alpha=0.3, color=DARK_SOULS_COLORS['grid'])
    ax3.set_facecolor(DARK_SOULS_COLORS['background'])
    ax3.tick_params(colors=DARK_SOULS_COLORS['text'])
    
    # Plot 4: Vergleich E[X_0] vs E[X_tau]
    ax4 = plt.subplot(2, 2, 4)
    initial_vals_b = paths_bounded[:100, 0]
    stopped_vals_b = [paths_bounded[i, stopping_times[i]] for i in range(100)]
    initial_vals_u = paths_unbounded[:100, 0]
    stopped_vals_u = [paths_unbounded[i, stopping_times_unb[i]] for i in range(100)]
    
    x_pos = np.arange(2)
    width = 0.35
    
    ax4.bar(x_pos - width/2, 
            [np.mean(initial_vals_b), np.mean(stopped_vals_b)],
            width, label='Beschränkt', color=DARK_SOULS_COLORS['accent'], alpha=0.7)
    ax4.bar(x_pos + width/2,
            [np.mean(initial_vals_u), np.mean(stopped_vals_u)],
            width, label='Unbeschränkt', color=DARK_SOULS_COLORS['highlight'], alpha=0.7)
    
    ax4.set_ylabel('Erwartungswert', color=DARK_SOULS_COLORS['text'])
    ax4.set_title('Vergleich: E[X_0] vs E[X_τ]', 
                  color=DARK_SOULS_COLORS['text'], fontsize=14, fontweight='bold')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(['E[X_0]', 'E[X_τ]'], color=DARK_SOULS_COLORS['text'])
    ax4.legend()
    ax4.grid(True, alpha=0.3, color=DARK_SOULS_COLORS['grid'], axis='y')
    ax4.set_facecolor(DARK_SOULS_COLORS['background'])
    ax4.tick_params(colors=DARK_SOULS_COLORS['text'])
    
    plt.suptitle('BOSS CHALLENGE: Der Martingal-Dämon', 
                 color=DARK_SOULS_COLORS['text'], fontsize=18, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    plt.savefig('boss_challenge_visualization.png', dpi=300, 
                facecolor=DARK_SOULS_COLORS['background'], bbox_inches='tight')
    print("\nVisualisierung gespeichert als 'boss_challenge_visualization.png'")
    
    return fig


if __name__ == "__main__":
    # Führe Boss Challenge aus
    result_bounded, result_unbounded = boss_challenge_proof()
    
    # Erstelle Visualisierung
    print("\n" + "=" * 70)
    print("Erstelle Visualisierung...")
    print("=" * 70)
    fig = visualize_boss_challenge()
    plt.show()
