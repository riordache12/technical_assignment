from deltares_model.hydrology_simulation import HydrologyModel


# AI-ASSIST:
class TestHydrologyModel:

    # ----------------------------
    # runoff_to_discharge tests
    # ----------------------------
    def test_runoff_to_discharge_zero_area(self):
        """If area is zero, discharge must be zero regardless of runoff."""
        assert HydrologyModel.runoff_to_discharge(10.0, 0.0) == 0.0

    def test_runoff_to_discharge_zero_runoff(self):
        """If runoff is zero, discharge must be zero."""
        assert HydrologyModel.runoff_to_discharge(0.0, 10.0) == 0.0

    def test_runoff_to_discharge_positive_values(self):
        """Check correct conversion for known values."""
        mm_per_day = 5.0
        area_km2 = 10.0
        expected = (mm_per_day / 1000.0) * (area_km2 * 1e6) / 86400.0
        result = HydrologyModel.runoff_to_discharge(mm_per_day, area_km2)
        assert expected == result

    # ----------------------------
    # flow_weighted_concentration tests
    # ----------------------------
    def test_flow_weighted_concentration_zero_flows(self):
        """If both flows are zero, return c2 by design."""
        assert HydrologyModel.flow_weighted_concentration(0.0, 5.0, 0.0, 2.0) == 2.0

    def test_flow_weighted_concentration_only_q1(self):
        """If q2=0, concentration should equal c1."""
        assert HydrologyModel.flow_weighted_concentration(10.0, 5.0, 0.0, 2.0) == 5.0

    def test_flow_weighted_concentration_only_q2(self):
        """If q1=0, concentration should equal c2."""
        assert HydrologyModel.flow_weighted_concentration(0.0, 5.0, 10.0, 2.0) == 2.0

    def test_flow_weighted_concentration_mixed_flows(self):
        """Check weighted average when both flows > 0."""
        q1, c1 = 10.0, 5.0
        q2, c2 = 20.0, 2.0
        expected = (q1 * c1 + q2 * c2) / (q1 + q2)
        result = HydrologyModel.flow_weighted_concentration(q1, c1, q2, c2)
        assert expected == result
