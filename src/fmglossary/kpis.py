"""Facility and maintenance KPI formulas. Plain functions, no dependencies."""

from __future__ import annotations


def _need_positive(name: str, value: float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than 0")


def mtbf(operating_hours: float, failures: int) -> float:
    """Mean time between failures: operating hours divided by the number of failures."""
    _need_positive("failures", failures)
    return operating_hours / failures


def mttr(total_repair_hours: float, repairs: int) -> float:
    """Mean time to repair: total repair hours divided by the number of repairs."""
    _need_positive("repairs", repairs)
    return total_repair_hours / repairs


def availability(mtbf_hours: float, mttr_hours: float) -> float:
    """Share of time an asset is able to work, as a percentage: MTBF / (MTBF + MTTR)."""
    _need_positive("mtbf_hours + mttr_hours", mtbf_hours + mttr_hours)
    return 100 * mtbf_hours / (mtbf_hours + mttr_hours)


def pm_compliance(pm_completed_on_time: int, pm_scheduled: int) -> float:
    """Preventive maintenance compliance: percentage of scheduled PM done on time."""
    _need_positive("pm_scheduled", pm_scheduled)
    return 100 * pm_completed_on_time / pm_scheduled


def reactive_ratio(corrective_hours: float, total_maintenance_hours: float) -> float:
    """Percentage of maintenance labor spent on unplanned (corrective) work."""
    _need_positive("total_maintenance_hours", total_maintenance_hours)
    return 100 * corrective_hours / total_maintenance_hours


def backlog_weeks(open_work_hours: float, crew_hours_per_week: float) -> float:
    """Weeks of work waiting if the crew did nothing else: open hours / weekly crew hours."""
    _need_positive("crew_hours_per_week", crew_hours_per_week)
    return open_work_hours / crew_hours_per_week


def cost_per_sqft(annual_cost: float, square_feet: float) -> float:
    """Annual cost (maintenance, cleaning, utilities and so on) per square foot."""
    _need_positive("square_feet", square_feet)
    return annual_cost / square_feet


def fci(deferred_maintenance: float, replacement_value: float) -> float:
    """Facility condition index: deferred maintenance divided by current replacement value."""
    _need_positive("replacement_value", replacement_value)
    return deferred_maintenance / replacement_value


def eui(annual_kbtu: float, square_feet: float) -> float:
    """Energy use intensity: kBtu used per square foot per year."""
    _need_positive("square_feet", square_feet)
    return annual_kbtu / square_feet


def sla_met(requests_on_time: int, requests_total: int) -> float:
    """Percentage of service requests answered within the agreed response time."""
    _need_positive("requests_total", requests_total)
    return 100 * requests_on_time / requests_total
