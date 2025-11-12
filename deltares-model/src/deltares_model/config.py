from dataclasses import dataclass


@dataclass
class SimulationConfig:
    beta: float = 0.85
    forcing_path: str = "data/forcing.csv"
    reaches_path: str = "data/reaches.csv"
    output_path: str = "results.csv"