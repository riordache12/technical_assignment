import argparse
from deltares_model.hydrology_simulation import Simulation, SimulationConfig
from deltares_model.csv_writer import CSVWriter

def main():
    parser = argparse.ArgumentParser(
        prog="mycli",
        description="My CLI tool that does something useful"
    )
    parser.add_argument("--name", help="Your name")
    args = parser.parse_args()

    config = SimulationConfig()  # uses defaults
    sim = Simulation(config)
    rows = sim.run()
    CSVWriter.write(config.output_path, rows)
    print(f"Wrote {len(rows)} rows to {config.output_path}")

