from __future__ import annotations
from typing import Any, Dict, List, Optional
from datetime import datetime

from deltares_model.helpers import read_csv_as_dicts, parse_date
from deltares_model.config import SimulationConfig


class HydrologyModel:
    @staticmethod
    def runoff_to_discharge(mm_per_day: float, area_km2: float) -> float:
        if area_km2 == 0:
            return 0.0
        else:
            return (mm_per_day / 10 ** 3) * (area_km2 * 10 ** 6) / 86400

    @staticmethod
    def flow_weighted_concentration(q1: float, c1: float, q2: float, c2: float) -> float:
        if q1 + q2 > 0:
            return (q1 * c1 + q2 * c2) / (q1 + q2)
        # To me, this felt weird to be a 'nan' value. It's obvious that you cannot divide by 0, but there should
        # be at least the initial concentration
        else:
            return c2

class Reach:
    def __init__(self, name: str, area_km2: float, tracer_init_mgL: float, beta: float = 0.85):
        self.name = name
        self.area_km2 = area_km2
        self.tracer_init_mgL = tracer_init_mgL
        self.beta = beta

        # State variables
        self.q_prev: float = 0.0
        self.q: float = 0.0
        self.c: float = tracer_init_mgL

    def update(self, runoff_mm: float, tracer_upstream: float = 0.0, q_upstream: float = 0.0,
               c_upstream: Optional[float] = None) -> None:
        # Convert runoff to local discharge
        q_local = HydrologyModel.runoff_to_discharge(runoff_mm, self.area_km2)

        # Apply recession
        self.q = q_local + self.beta * self.q_prev + q_upstream


        self.c = HydrologyModel.flow_weighted_concentration(
            q1=q_upstream if q_upstream is not None else 0.0,
            c1=c_upstream if c_upstream is not None else tracer_upstream,
            q2=q_local,
            c2=self.tracer_init_mgL
        )

        # Update previous discharge
        self.q_prev = self.q

    def record_result(self, date: datetime) -> dict:
        """Return current state as a dict for results collection."""
        return {
            "date": date,
            "reach": self.name,
            "q_m3s": round(self.q, 3),
            "c_mgL": round(self.c, 3),
        }


class Simulation:
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.results: List[Dict[str, Any]] = []
        self.beta = self.config.beta


    def process_rows(self, forcing: List[Dict], reach_a: Reach, reach_b: Reach) -> List[Dict[str, Any]]:
        # Instantiate reaches
        results = []

        for row in forcing:
            d = parse_date(row.get("date", "1970-01-01"))
            p = float(row.get("precip_mm", 0.0))
            et = float(row.get("et_mm", 0.0))
            tracer_upstream = float(row.get("tracer_upstream_mgL", 0.0))

            runoff = max(p - et, 0.0)

            # Update Reach A
            reach_a.update(runoff_mm=runoff, tracer_upstream=tracer_upstream)
            results.append(reach_a.record_result(d))

            # Update Reach B with inflow from A
            reach_b.update(runoff_mm=runoff, q_upstream=reach_a.q, c_upstream=reach_a.c)
            results.append(reach_b.record_result(d))

        return results

    def run(self) -> List[Dict[str, Any]]:
        forcing = read_csv_as_dicts(self.config.forcing_path)
        reaches = read_csv_as_dicts(self.config.reaches_path)
        if len(reaches) < 2:
            raise ValueError("need at least 2 reaches A and B")

        reach_a = Reach("A",
                        area_km2=float(reaches[0]['area_km2']),
                        tracer_init_mgL=float(reaches[0]['tracer_init_mgL']),
                        beta=self.beta)
        reach_b = Reach("B",
                        area_km2=float(reaches[1]['area_km2']),
                        tracer_init_mgL=float(reaches[1]['tracer_init_mgL']),
                        beta=self.beta)
        return self.process_rows(forcing, reach_a, reach_b)
