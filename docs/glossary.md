# Facility management glossary

Ten maintenance and facility KPIs, each with a definition, its formula and a worked example. Every result below is calculated by the code in `src/fmglossary/kpis.py`.

## MTBF (mean time between failures)

Average operating time between two failures of a repairable asset.

Formula: `operating_hours / failures` (hours)

Example: A pump ran 8,000 hours and failed 4 times. Inputs: operating_hours=8,000, failures=4. Result: **2,000** hours.

## MTTR (mean time to repair)

Average time it takes to fix an asset once it has failed, from start of repair to return to service.

Formula: `total_repair_hours / repairs` (hours)

Example: Four repairs took 30 hours in total. Inputs: total_repair_hours=30, repairs=4. Result: **7.5** hours.

## Availability

How much of the time an asset is able to do its job, built from MTBF and MTTR.

Formula: `100 * mtbf / (mtbf + mttr)` (percent)

Example: An asset with 2,000 hours between failures and 7.5 hours to repair on average. Inputs: mtbf_hours=2,000, mttr_hours=7.5. Result: **99.63** percent.

## PM compliance

Share of scheduled preventive maintenance that was finished on time. Late work does not count.

Formula: `100 * pm_completed_on_time / pm_scheduled` (percent)

Example: 92 of 100 scheduled PM work orders closed on time. Inputs: pm_completed_on_time=92, pm_scheduled=100. Result: **92** percent.

## Reactive ratio

Share of maintenance labor spent on unplanned corrective work. High values mean the team is firefighting.

Formula: `100 * corrective_hours / total_maintenance_hours` (percent)

Example: 310 of 1,000 labor hours were corrective. Inputs: corrective_hours=310, total_maintenance_hours=1,000. Result: **31** percent.

## Backlog (in weeks)

How many weeks of work are waiting, if the crew worked only on the backlog.

Formula: `open_work_hours / crew_hours_per_week` (weeks)

Example: 480 open hours and a crew that has 160 hours a week. Inputs: open_work_hours=480, crew_hours_per_week=160. Result: **3** weeks.

## Cost per square foot

Yearly cost of a service or of the whole building divided by its area. Used to compare buildings.

Formula: `annual_cost / square_feet` (currency per sq ft)

Example: A 60,000 sq ft building with 420,000 of annual cost. Inputs: annual_cost=420,000, square_feet=60,000. Result: **7** currency per sq ft.

## FCI (facility condition index)

Deferred maintenance as a fraction of what it would cost to replace the building. Lower is better.

Formula: `deferred_maintenance / replacement_value` (ratio)

Example: 2.5 million of deferred work on a 40 million replacement value. Inputs: deferred_maintenance=2,500,000, replacement_value=40,000,000. Result: **0.06** ratio.

## EUI (energy use intensity)

Energy used per square foot per year. It lets you compare buildings of different sizes.

Formula: `annual_kbtu / square_feet` (kBtu per sq ft per year)

Example: 5.4 million kBtu a year in 60,000 sq ft. Inputs: annual_kbtu=5,400,000, square_feet=60,000. Result: **90** kBtu per sq ft per year.

## Service level met

Share of service requests that were answered within the agreed response time.

Formula: `100 * requests_on_time / requests_total` (percent)

Example: 188 of 200 requests answered on time. Inputs: requests_on_time=188, requests_total=200. Result: **94** percent.

