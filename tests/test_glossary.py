from pathlib import Path

import pytest

from fmglossary import kpis
from fmglossary.__main__ import main
from fmglossary.glossary import TERMS, find, fmt, to_markdown

DOC = Path(__file__).resolve().parent.parent / "docs" / "glossary.md"


def test_ten_terms_with_unique_keys():
    keys = [t.key for t in TERMS]
    assert len(keys) == 10 and len(set(keys)) == 10


def test_every_example_runs_and_matches_signature():
    for t in TERMS:
        assert set(t.example) == set(t.args())
        assert isinstance(t.run_example(), float)


def test_mtbf_and_mttr():
    assert kpis.mtbf(8000, 4) == 2000
    assert kpis.mttr(30, 4) == 7.5


def test_availability():
    assert round(kpis.availability(2000, 7.5), 2) == 99.63
    assert kpis.availability(100, 0) == 100


def test_percent_kpis():
    assert kpis.pm_compliance(92, 100) == 92
    assert kpis.reactive_ratio(310, 1000) == 31
    assert kpis.sla_met(188, 200) == 94


def test_backlog_cost_eui_fci():
    assert kpis.backlog_weeks(480, 160) == 3
    assert kpis.cost_per_sqft(420000, 60000) == 7
    assert kpis.eui(5400000, 60000) == 90
    assert kpis.fci(2500000, 40000000) == 0.0625


@pytest.mark.parametrize("call", [lambda: kpis.mtbf(10, 0), lambda: kpis.mttr(5, 0), lambda: kpis.pm_compliance(1, 0),
                                  lambda: kpis.cost_per_sqft(1, 0), lambda: kpis.availability(0, 0)])
def test_zero_division_becomes_clear_error(call):
    with pytest.raises(ValueError):
        call()


def test_find_by_key_and_name():
    assert find("mtbf").key == "mtbf"
    assert find("PM compliance").key == "pm_compliance"
    assert find("facility condition").key == "fci"
    assert find("nothing") is None


def test_fmt():
    assert fmt(7.0) == "7" and fmt(99.6266) == "99.63" and fmt(2000.0) == "2,000"


def test_published_markdown_is_current():
    assert DOC.read_text(encoding="utf-8") == to_markdown() + "\n"


def test_cli_list_define_example(capsys):
    assert main(["list"]) == 0
    assert main(["define", "mtbf"]) == 0
    assert main(["example", "pm_compliance"]) == 0
    out = capsys.readouterr().out
    assert "Result: 92 percent" in out and "Inputs: operating_hours, failures" in out


def test_cli_calc(capsys):
    assert main(["calc", "mttr", "total_repair_hours=30", "repairs=4"]) == 0
    assert capsys.readouterr().out.strip() == "7.5 hours"


def test_cli_calc_errors(capsys):
    assert main(["calc", "mttr", "repairs=0", "total_repair_hours=3"]) == 2
    assert main(["calc", "mttr", "repairs=2"]) == 2
    assert main(["calc", "mttr", "bogus=2", "repairs=1"]) == 2
    assert main(["calc", "mttr", "repairs=x", "total_repair_hours=3"]) == 2
    assert main(["define", "nope"]) == 2


def test_cli_export(tmp_path):
    out = tmp_path / "g.md"
    assert main(["export", "-o", str(out)]) == 0
    assert out.read_text(encoding="utf-8").startswith("# Facility management glossary")
