"""
Martingales in diskreter Zeit - Python Implementation
Implementiert verschiedene Martingal-Typen und ihre Eigenschaften
"""

import numpy as np
from typing import Callable, Optional
import matplotlib.pyplot as plt
from scipy import stats


class Martingale:
    """
    Basisklasse für Martingale in diskreter Zeit
    """
    
    def __init__(self, n_steps: int, n_paths: int = 1000, seed: Optional[int] = None):
        """
        Parameters:
        -----------
        n_steps : int
            Anzahl der Zeitschritte
        n_paths : int
            Anzahl der simulierten Pfade
        seed : int, optional
            Random seed für Reproduzierbarkeit
        """
        self.n_steps = n_steps
        self.n_paths = n_paths
        self.rng = np.random.default_rng(seed)
        self.paths = None
        
    def simulate(self):
        """Simuliert die Martingal-Pfade"""
        raise NotImplementedError("Subklassen müssen diese Methode implementieren")
    
    def get_paths(self):
        """Gibt die simulierten Pfade zurück"""
        if self.paths is None:
            self.simulate()
        return self.paths
    
    def mean(self, step: int) -> float:
        """Berechnet den Erwartungswert zum Zeitpunkt step"""
        if self.paths is None:
            self.simulate()
        return np.mean(self.paths[:, step])
    
    def variance(self, step: int) -> float:
        """Berechnet die Varianz zum Zeitpunkt step"""
        if self.paths is None:
            self.simulate()
        return np.var(self.paths[:, step])


class SymmetricRandomWalk(Martingale):
    """
    Symmetrischer Random Walk: S_n = X_1 + ... + X_n
    wobei X_i unabhängig sind mit P(X_i = 1) = P(X_i = -1) = 1/2
    """
    
    def simulate(self):
        """Simuliert symmetrischen Random Walk"""
        # Inkremente: +1 oder -1 mit Wahrscheinlichkeit 1/2
        increments = self.rng.choice([-1, 1], size=(self.n_paths, self.n_steps))
        
        # Random Walk: kumulative Summe
        self.paths = np.zeros((self.n_paths, self.n_steps + 1))
        self.paths[:, 1:] = np.cumsum(increments, axis=1)
        
        return self.paths


class GeneralRandomWalk(Martingale):
    """
    Allgemeiner Random Walk mit beliebigen Inkrementen
    """
    
    def __init__(self, n_steps: int, increment_dist: Callable, 
                 n_paths: int = 1000, seed: Optional[int] = None):
        """
        Parameters:
        -----------
        increment_dist : Callable
            Funktion, die Inkremente generiert (z.B. lambda: rng.normal(0, 1))
        """
        super().__init__(n_steps, n_paths, seed)
        self.increment_dist = increment_dist
    
    def simulate(self):
        """Simuliert allgemeinen Random Walk"""
        increments = np.array([[self.increment_dist() 
                               for _ in range(self.n_steps)] 
                              for _ in range(self.n_paths)])
        
        self.paths = np.zeros((self.n_paths, self.n_steps + 1))
        self.paths[:, 1:] = np.cumsum(increments, axis=1)
        
        return self.paths


class MartingaleTransform(Martingale):
    """
    Martingal-Transform: (H · M)_n = sum_{k=1}^n H_k (M_k - M_{k-1})
    wobei H vorhersehbar ist (H_k ist F_{k-1}-messbar)
    """
    
    def __init__(self, base_martingale: Martingale, 
                 strategy: Callable, n_paths: int = 1000):
        """
        Parameters:
        -----------
        base_martingale : Martingale
            Basis-Martingal M
        strategy : Callable
            Strategie-Funktion H_k = strategy(k, M_0, ..., M_{k-1})
        """
        self.base_martingale = base_martingale
        self.strategy = strategy
        super().__init__(base_martingale.n_steps, n_paths, 
                        base_martingale.rng.bit_generator.state['state']['state'])
    
    def simulate(self):
        """Simuliert Martingal-Transform"""
        # Simuliere Basis-Martingal
        base_paths = self.base_martingale.get_paths()
        
        # Berechne Inkremente
        increments = np.diff(base_paths, axis=1)
        
        # Berechne Strategie (vorhersehbar)
        self.paths = np.zeros((self.n_paths, self.n_steps + 1))
        
        for k in range(1, self.n_steps + 1):
            # Strategie hängt nur von vergangenen Werten ab
            H_k = np.array([self.strategy(k, base_paths[i, :k]) 
                           for i in range(self.n_paths)])
            self.paths[:, k] = self.paths[:, k-1] + H_k * increments[:, k-1]
        
        return self.paths


class SquareIntegrableMartingale(Martingale):
    """
    Quadratintegrierbares Martingal mit quadratischer Variation
    """
    
    def __init__(self, base_martingale: Martingale):
        self.base_martingale = base_martingale
        super().__init__(base_martingale.n_steps, base_martingale.n_paths,
                        base_martingale.rng.bit_generator.state['state']['state'])
        self.quadratic_variation = None
        self.predictable_quadratic = None
    
    def simulate(self):
        """Simuliert das quadratintegrierbare Martingal"""
        self.paths = self.base_martingale.get_paths()
        return self.paths
    
    def compute_quadratic_variation(self):
        """Berechnet die quadratische Variation [M]_n"""
        if self.paths is None:
            self.simulate()
        
        increments = np.diff(self.paths, axis=1)
        self.quadratic_variation = np.cumsum(increments**2, axis=1)
        return self.quadratic_variation
    
    def compute_predictable_quadratic(self):
        """Berechnet den vorhersehbaren quadratischen Prozess <M>_n"""
        if self.paths is None:
            self.simulate()
        
        increments = np.diff(self.paths, axis=1)
        # Erwartungswert der quadrierten Inkremente (bedingt auf F_{k-1})
        # Für symmetrischen Random Walk: E[(M_k - M_{k-1})^2 | F_{k-1}] = 1
        expected_squared = np.ones_like(increments)
        self.predictable_quadratic = np.cumsum(expected_squared, axis=1)
        return self.predictable_quadratic


def conditional_expectation_simple(X, Y, y_value):
    """
    Berechnet E[X | Y = y] für diskrete Zufallsvariablen
    (Einfache Version für Demonstration)
    """
    mask = (Y == y_value)
    if np.sum(mask) == 0:
        return np.nan
    return np.mean(X[mask])


def optional_stopping_simulation(martingale: Martingale, stopping_time_func: Callable,
                                 n_simulations: int = 10000):
    """
    Simuliert das Optional Stopping Theorem
    
    Parameters:
    -----------
    martingale : Martingale
        Das zu testende Martingal
    stopping_time_func : Callable
        Funktion, die Stoppzeit berechnet: tau = stopping_time_func(path)
    n_simulations : int
        Anzahl der Simulationen
    """
    paths = martingale.get_paths()
    initial_values = []
    stopped_values = []
    stopping_times = []
    
    for i in range(min(n_simulations, martingale.n_paths)):
        path = paths[i, :]
        tau = stopping_time_func(path)
        
        if tau < len(path):
            initial_values.append(path[0])
            stopped_values.append(path[tau])
            stopping_times.append(tau)
    
    initial_values = np.array(initial_values)
    stopped_values = np.array(stopped_values)
    stopping_times = np.array(stopping_times)
    
    return {
        'E[X_0]': np.mean(initial_values),
        'E[X_tau]': np.mean(stopped_values),
        'E[tau]': np.mean(stopping_times),
        'difference': np.mean(stopped_values) - np.mean(initial_values),
        'stopping_times': stopping_times,
        'initial_values': initial_values,
        'stopped_values': stopped_values
    }


if __name__ == "__main__":
    # Beispiel: Symmetrischer Random Walk
    print("Simuliere symmetrischen Random Walk...")
    rw = SymmetricRandomWalk(n_steps=100, n_paths=1000, seed=42)
    paths = rw.simulate()
    
    print(f"Erwartungswert bei t=0: {rw.mean(0):.4f}")
    print(f"Erwartungswert bei t=50: {rw.mean(50):.4f}")
    print(f"Erwartungswert bei t=100: {rw.mean(100):.4f}")
    print(f"Varianz bei t=100: {rw.variance(100):.4f}")
