# investment-analysis/ — investment decision tools

**Provenance:** these 6 Python modules were created 2026-02-11 as part of the
"investment analysis system" (see `archive/2026-02-strategy-batch/investment_system_summary.md`).
They were misfiled under `projects/poultry-farm/operations/` — a place they have nothing to do
with. Moved here 2026-10-12.

## Files
| File | Role |
|---|---|
| `main.py` | Entry point — ties the modules together (Investment Decision Tool) |
| `investment_analyzer.py` | User profile + scoring + comparison engine |
| `risk_calculator.py` | Volatility, beta, Sharpe, VaR, correlation, max drawdown |
| `portfolio_diversifier.py` | Portfolio metrics, diversification, allocation suggestions |
| `scalable_investment_analysis.py` | Parallel/bulk analysis, storage, filtering |
| `scale_deployment_config.py` | Deployment config (Docker/Kubernetes specs) |

## Status: unused / unverified
No record of these being run against real data. They predate the live trading systems
(`trading_sim/`) and overlap with the opportunity scanner's territory. Treat as a starting
point only — do not rely on outputs until they are exercised and validated.
