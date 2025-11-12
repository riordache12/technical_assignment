from __future__ import annotations
from typing import Any, Dict, List

from csv_writer import CSVWriter
from helpers import read_csv_as_dicts, parse_date
from config import SimulationConfig


class HydrologyModel:
    @staticmethod
    def runoff_to_discharge(mm_per_day: float, area_km2: float) -> float:
        if area_km2 == 0:
            return 0.0
        else:
            return (mm_per_day / 10**3) * (area_km2 * 10**6) / 86400


    @staticmethod
    def flow_weighted_concentration(q1: float, c1: float, q2: float, c2: float) -> float:
        if q1 + q2 > 0:
            return (q1*c1 + q2*c2)/(q1 + q2)
        # To me, this felt weird to be a 'nan' value. It's obvious that you cannot divide by 0, but there should
        # be at least the initial concentration
        else:
            return c2


class Simulation:
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.results: List[Dict[str, Any]] = []

    def run(self) -> List[Dict[str, Any]]:
        beta = self.config.beta
        fpath = self.config.forcing_path
        rpath = self.config.reaches_path

        forcing = read_csv_as_dicts(fpath)
        reaches = read_csv_as_dicts(rpath)
        if len(reaches) < 2:
            raise ValueError("need at least 2 reaches A and B")

        q_a_prev, q_b_prev = 0.0, 0.0

        for row in forcing:
            d = parse_date(row.get("date", "1970-01-01"))

            p = float(row.get("precip_mm", 0.0))
            et = float(row.get("et_mm", 0.0))
            tracer_upstream = float(row.get("tracer_upstream_mgL", 0.0))

            runoff_a = max(p - et, 0.0)
            runoff_b = max(p - et, 0.0)

            q_a_local = HydrologyModel.runoff_to_discharge(runoff_a, float(reaches[0]["area_km2"]))
            q_b_local = HydrologyModel.runoff_to_discharge(runoff_b, float(reaches[1]["area_km2"]))

            tracer_a = float(reaches[0]["tracer_init_mgL"])
            tracer_b = float(reaches[1]["tracer_init_mgL"])

            q_a = q_a_local + beta * q_a_prev
            q_b = q_b_local + beta * q_b_prev + q_a

            concentration_a = HydrologyModel.flow_weighted_concentration(
                q1 = 0.0,
                c1 = tracer_upstream,
                q2 = q_a_local,
                c2 = tracer_a
            )
            concentration_b = HydrologyModel.flow_weighted_concentration(
                q1 = q_a,
                c1 = concentration_a,
                q2 = q_b_local,
                c2 = tracer_b
            )

            self.results.append({
                "date": d,
                "reach": "A",
                "q_m3s": round(q_a, 3),
                "c_mgL": round(concentration_a, 3),
            })
            self.results.append({
                "date": d,
                "reach": "B",
                "q_m3s": round(q_b, 3),
                "c_mgL": round(concentration_b, 3),
            })

            q_a_prev, q_b_prev = q_a, q_b

        return self.results


def main():
    config = SimulationConfig()  # uses defaults
    sim = Simulation(config)
    rows = sim.run()
    CSVWriter.write(config.output_path, rows)
    print(f"Wrote {len(rows)} rows to {config.output_path}")


if __name__ == "__main__":
    main()