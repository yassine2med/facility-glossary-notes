"""Glossary entries. Each one has a plain definition, its formula and a worked example that runs."""

from __future__ import annotations

from dataclasses import dataclass, field

from . import kpis


@dataclass(frozen=True)
class Term:
    key: str
    name: str
    definition: str
    formula: str
    unit: str
    func: object
    example: dict = field(default_factory=dict)
    note: str = ""

    def run_example(self) -> float:
        return self.func(**self.example)

    def args(self) -> list[str]:
        return list(self.func.__code__.co_varnames[: self.func.__code__.co_argcount])


TERMS: list[Term] = [
    Term("mtbf", "MTBF (mean time between failures)",
         "Average operating time between two failures of a repairable asset.",
         "operating_hours / failures", "hours", kpis.mtbf, {"operating_hours": 8000, "failures": 4},
         "A pump ran 8,000 hours and failed 4 times."),
    Term("mttr", "MTTR (mean time to repair)",
         "Average time it takes to fix an asset once it has failed, from start of repair to return to service.",
         "total_repair_hours / repairs", "hours", kpis.mttr, {"total_repair_hours": 30, "repairs": 4},
         "Four repairs took 30 hours in total."),
    Term("availability", "Availability",
         "How much of the time an asset is able to do its job, built from MTBF and MTTR.",
         "100 * mtbf / (mtbf + mttr)", "percent", kpis.availability, {"mtbf_hours": 2000, "mttr_hours": 7.5},
         "An asset with 2,000 hours between failures and 7.5 hours to repair on average."),
    Term("pm_compliance", "PM compliance",
         "Share of scheduled preventive maintenance that was finished on time. Late work does not count.",
         "100 * pm_completed_on_time / pm_scheduled", "percent", kpis.pm_compliance,
         {"pm_completed_on_time": 92, "pm_scheduled": 100}, "92 of 100 scheduled PM work orders closed on time."),
    Term("reactive_ratio", "Reactive ratio",
         "Share of maintenance labor spent on unplanned corrective work. High values mean the team is firefighting.",
         "100 * corrective_hours / total_maintenance_hours", "percent", kpis.reactive_ratio,
         {"corrective_hours": 310, "total_maintenance_hours": 1000}, "310 of 1,000 labor hours were corrective."),
    Term("backlog_weeks", "Backlog (in weeks)",
         "How many weeks of work are waiting, if the crew worked only on the backlog.",
         "open_work_hours / crew_hours_per_week", "weeks", kpis.backlog_weeks,
         {"open_work_hours": 480, "crew_hours_per_week": 160}, "480 open hours and a crew that has 160 hours a week."),
    Term("cost_per_sqft", "Cost per square foot",
         "Yearly cost of a service or of the whole building divided by its area. Used to compare buildings.",
         "annual_cost / square_feet", "currency per sq ft", kpis.cost_per_sqft,
         {"annual_cost": 420000, "square_feet": 60000}, "A 60,000 sq ft building with 420,000 of annual cost."),
    Term("fci", "FCI (facility condition index)",
         "Deferred maintenance as a fraction of what it would cost to replace the building. Lower is better.",
         "deferred_maintenance / replacement_value", "ratio", kpis.fci,
         {"deferred_maintenance": 2500000, "replacement_value": 40000000},
         "2.5 million of deferred work on a 40 million replacement value."),
    Term("eui", "EUI (energy use intensity)",
         "Energy used per square foot per year. It lets you compare buildings of different sizes.",
         "annual_kbtu / square_feet", "kBtu per sq ft per year", kpis.eui,
         {"annual_kbtu": 5400000, "square_feet": 60000}, "5.4 million kBtu a year in 60,000 sq ft."),
    Term("sla_met", "Service level met",
         "Share of service requests that were answered within the agreed response time.",
         "100 * requests_on_time / requests_total", "percent", kpis.sla_met,
         {"requests_on_time": 188, "requests_total": 200}, "188 of 200 requests answered on time."),
]

BY_KEY = {t.key: t for t in TERMS}


def find(word: str) -> Term | None:
    """Find a term by key or by part of its name, ignoring case and spaces/underscores."""
    w = word.lower().replace(" ", "_")
    if w in BY_KEY:
        return BY_KEY[w]
    hits = [t for t in TERMS if w in t.name.lower().replace(" ", "_")]
    return hits[0] if len(hits) == 1 else None


def fmt(value: float) -> str:
    return f"{value:,.2f}".rstrip("0").rstrip(".")


def to_markdown() -> str:
    """The whole glossary as a Markdown document, with each worked example calculated."""
    out = ["# Facility management glossary", "",
           "Ten maintenance and facility KPIs, each with a definition, its formula and a worked example. "
           "Every result below is calculated by the code in `src/fmglossary/kpis.py`.", ""]
    for t in TERMS:
        out += [f"## {t.name}", "", t.definition, "", f"Formula: `{t.formula}` ({t.unit})", "",
                f"Example: {t.note} Inputs: " + ", ".join(f"{k}={v:,}" if isinstance(v, int) else f"{k}={v}" for k, v in t.example.items())
                + f". Result: **{fmt(t.run_example())}** {t.unit}.", ""]
    return "\n".join(out)
