# AGENTS.md — MemecoinsAI Operating Briefing

> This file is the standing context prompt for every agent session working on this
> repository. Read it fully before touching anything. It describes what the project
> IS, what it is NOT, the rules of engagement, and the prioritized backlog.
> Version: 2026-11-26 · maintained by 50cent (leader) and Lucki (executor).

---

## 1. MISSION

**MemecoinsAI** is an AI-driven platform for analyzing, tracking, and (eventually)
trading memecoins. The goal is to turn speculative social noise into actionable,
risk-managed intelligence: real-time market data + social sentiment velocity +
on-chain signals → signals → guarded execution.

Product pillars (from README, in priority order):
1. **Real-time Social Velocity Tracking** — momentum across X, Telegram, Reddit.
2. **Smart Money Wallet Analysis** — whale behavior and influence patterns.
3. **Rug-Pull Detection Suite** — contract analysis + liquidity monitoring.
4. **Multi-Chain Arbitrage** — cross-chain liquidity analysis and routing.
5. **Position Sizing Engine** — risk management based on the "Barbell Model".

The near-term deliverable is the **memetrading bot** described in
`memetrading_bot_plan/PROJECT_PLAN.md`: a sentiment-aware bot that identifies
trending tokens and enters/exits positions on Binance/MEXC with hard risk limits.

---

## 2. ROLES AND AUTHORITY (non-negotiable)

This repo operates the **Leader–Coder model** (see
`description/collaboration_protocol.md` and the LEADER-EXECUTOR-CHARTER in the
10000line-plan repo):

- **50cent (leader/researcher):** roadmap, research, task specs, priorities, code
  review, merge decisions, project acceptance. 50cent does NOT write production code.
- **Lucki (coder/executor):** implements, tests, verifies, deploys. Lucki does NOT
  re-plan; objections are raised once with evidence, then the leader's call stands.
- **Humans (Maloneam / Hristo Botev):** final authority on everything, especially
  anything involving real money (see §8).
- Coordination happens in the Matrix "Research" room; only @mentions trigger agents;
  error notices are never tasks. One message per milestone, no ack-pong.

---

## 3. REPOSITORY MAP (what actually exists, verified 2026-11-26)

```
MemecoinsAI/
├── README.md                     ← project vision, architecture, roadmap (5 phases)
├── AGENTS.md                     ← THIS FILE — the agent briefing
├── COMBINED_MEMECOIN_TRADING_REPORT_EXPANDED.md   ← 500 KB research report.
│     Do NOT read it whole into context. Grep/section-read it for what you need.
├── requirements.txt              ← ccxt, pandas, scikit-learn, sqlalchemy,
│     python-telegram-bot
├── exchange_connector.py         ← ExchangeConnector class: ccxt wrappers for
│     Binance + MEXC (spot, rate-limited), fetch_ticker, close()
├── market_data_stream.py         ← MarketDataStream class: polling ticker loop
│     (fetch_ticker_continuously, default 5 s interval)
├── order_executor.py             ← OrderExecutor class: market buy/sell via ccxt
├── sentiment_analysis.py         ← ⚠ PLACEHOLDER ONLY — see §4. Imports a
│     non-existent `helpers` module; it does not run.
├── description/
│   ├── project_overview.md       ← goals, target audience
│   └── collaboration_protocol.md ← roles, workflow cycle, branching, commit style
├── development/
│   ├── tech_specs.md             ← env/infra notes (loguru, Prometheus/Grafana,
│   │     CoinGecko / Galaxy Research / Dune as data sources, VPS deployment)
│   ├── setup_env.py              ← environment bootstrap script
│   └── plan/memetrading_bot_plan/← API spike scripts: binance_test.py,
│         kucoin_test.py, coinGecko_test.py / coinGecko_api_test.py
├── memetrading_bot_plan/
│   ├── PROJECT_PLAN.md           ← the bot plan: 4 core modules, 3 phases
│   ├── TODO_LUCKI.md             ← Phase-1 checklist (all items done)
│   └── current_plan              ← latest plan snapshot
├── research/
│   ├── memecoin_guide_summary.md ← research digest
│   └── notes.md                  ← empty stub
├── docs/readme.md                ← docs stub
└── sync_repo.sh / test_commit.txt ← leftovers; candidates for cleanup (§9 P0)
```

**Tracked file count is ~30.** Everything else on disk (venv, nested copies) is
ignored via `.gitignore`.

---

## 4. HONEST CURRENT STATE (verified, not aspirational)

What WORKS / exists as real code:
- `exchange_connector.py`, `market_data_stream.py`, `order_executor.py` — coherent
  ccxt-based classes for **Binance + MEXC spot**, consistent logging pattern,
  type hints, docstrings. Never executed as part of a test suite — no tests exist.
- API spike scripts under `development/plan/` (Binance, KuCoin, CoinGecko probes).

What is FAKE or BROKEN (do not trust the checkboxes):
- `sentiment_analysis.py` is a placeholder that **imports a `helpers` module that
  does not exist** → it crashes on import. PROJECT_PLAN.md marks "Integrate
  Twitter/Telegram API for sentiment analysis" as **[x] done — it is NOT done.**
- `PROJECT_PLAN.md` Phase 1 checkboxes are accurate; Phase 2's first checkbox is not.
- README promises a `tests/` directory — **it does not exist**.
- `requirements.txt` lists `python-telegram-bot` and `sqlalchemy` — **no code uses
  either yet**.
- The repo previously contained a nested duplicate of itself committed as a broken
  gitlink (`MemecoinsAI` submodule entry). Removed from the index on 2026-11-26;
  the on-disk copy is now gitignored. Do not re-add it.
- `test_commit.txt` and root `sync_repo.sh` are debris from sync experiments.

Phase status (real): **Phase 1 done. Phase 2 barely started. Phase 3 not started.**

---

## 5. TARGET ARCHITECTURE (from PROJECT_PLAN.md — build toward this)

1. **Data Ingestion Layer** — market data (Binance, MEXC, later Gate.io via
   WebSockets), social sentiment feeds (X, Telegram), on-chain data (Phase 2+).
2. **Signal Generation Engine** — trend analysis (RSI, MACD, volume profile),
   NLP sentiment scoring, hot-token detection (volume spikes + social velocity).
3. **Execution Engine** — order management with slippage control, portfolio/PnL
   tracking, risk management (stop-loss, max drawdown, volatility position sizing).
4. **Alerting & Monitoring** — Telegram trade/health alerts, simple dashboard.

Stack: Python primary; `ccxt` for exchanges; `pandas` for data; `scikit-learn` for
simple sentiment; `sqlalchemy` for trade history (SQLite first, PostgreSQL later);
`python-telegram-bot` for alerts.

Design rules extracted from the existing code — keep them:
- One class per concern, constructor initializes exchanges with
  `{'enableRateLimit': True, 'options': {'defaultType': 'spot'}}`.
- `logging.basicConfig` module-level logger; log every external call; return
  `None` + log on error rather than crashing the stream.
- Type hints and Google-style docstrings on all public methods.

---

## 6. ENVIRONMENT

- Python 3.x + venv (a working venv exists on nikipc; Windows side uses
  `Documents\GitHub\MemecoinsAI`). `development/setup_env.py` bootstraps deps.
- Install: `python -m venv venv && source venv/bin/activate && pip install -r
  requirements.txt` (on Windows: `venv\Scripts\activate`).
- No API keys are in the repo and none may be added: secrets live in `.env`
  (gitignored) or the OS credential store. Public endpoints (CoinGecko, public
  tickers) need no keys and should be the default for development/testing.

---

## 7. CONVENTIONS

- **Branching** (from collaboration_protocol.md): `main` = reviewed code;
  `research/*` = 50cent's docs; `feature/*` and `fix/*` = Lucki's work. Small
  docs/config changes may go straight to main.
- **Commits**: Conventional Commits — `feat:` `fix:` `docs:` `refactor:` `test:`
  `chore:`. (Auto-sync commits are prefixed `auto-sync:` — that is the cross-PC
  file watcher, not a convention violation; see §10.)
- **Review**: code changes get reviewed by 50cent (diff-based) before being called
  done. Lucki's report must include the commit hash + test evidence.
- **Tests**: new logic lands with a test under `tests/` (create it). The spike
  scripts in `development/plan/` are throwaway probes, not tests.
- **Style**: match the existing modules (logging, type hints, docstrings, ccxt
  patterns). No new frameworks without a task spec.

---

## 8. TRADING SAFETY (hard rules — human-level policy)

1. **No live trading with real funds** until ALL of: risk-management module exists
   (stop-loss, take-profit, max drawdown), a backtest report exists, and a human
   explicitly approves live use in the Matrix room. Until then: public market data
   and paper trading only.
2. Exchange API keys with withdrawal or trade permissions never go in the repo,
   in commits, in logs, or in Matrix.
3. `order_executor.py` currently places **real market orders** when given keys —
   treat it as a loaded gun. Any task touching it must add dry-run mode first
   (P1 in the backlog).
4. Slippage limits, order-size caps, and symbol allowlists must exist before any
   live account is connected.

---

## 9. PRIORITIZED BACKLOG (as of 2026-11-26 — 50cent owns ordering)

**P0 — repo truthfulness & hygiene**
- [ ] Fix or delete `sentiment_analysis.py` (it crashes on import). Either create
      the `helpers` module (collect_social_data / compute_velocity / generate_alerts)
      or strip the placeholder.
- [ ] Delete debris: `test_commit.txt`, root `sync_repo.sh` (superseded by the
      systemd/scheduled-task watchers).
- [ ] Correct the false `[x]` in PROJECT_PLAN.md Phase 2 (sentiment integration).
- [ ] Create `tests/` and add smoke tests for the three ccxt modules (public
      endpoints, no keys).

**P1 — make the core real**
- [ ] `dry_run` mode in `order_executor.py` (paper fills at ticker price).
- [ ] Persistence: `sqlalchemy` trade-history + market-data store (SQLite first).
- [ ] Real sentiment MVP: CoinGecko + public sources → `helpers.py` with
      `collect_social_data`, `compute_velocity`, `generate_alerts` (the interface
      `sentiment_analysis.py` already expects).
- [ ] Config layer: single `config.py`/`.env.example` for symbols, intervals,
      exchange list (currently hardcoded Binance+MEXC in three places — dedupe
      into one exchange-registry module).

**P2 — strategy & risk**
- [ ] Momentum+sentiment strategy with backtest harness (pandas).
- [ ] Risk module: stop-loss, take-profit, max drawdown, volatility position sizing.
- [ ] Telegram alerting (python-telegram-bot) for signals and system health.

**P3 — detection & UI**
- [ ] Hot-token auto-discovery (volume spike + social velocity scanners).
- [ ] Rug-pull checks (liquidity lock, contract flags) — research first.
- [ ] Minimal dashboard (terminal or web) for positions/PnL.

---

## 10. CROSS-PC SYNC — how the repo moves between the two machines

- Both clones (nikipc `~/MemecoinsAI` and Windows `Documents\GitHub\MemecoinsAI`)
  are watched by an **auto-sync loop every 10 s**: it commits any change as
  `auto-sync: <timestamp>`, rebases on origin, and pushes.
- Implications: (a) never edit the same file on both PCs simultaneously;
  (b) don't run destructive git commands (`reset --hard`, force push) — the
  watcher will fight you; (c) if a rebase conflicts, sync PAUSES on that side
  (log: `pull --rebase failed`) until a human/agent resolves it deliberately;
  (d) `git status` may show changes you didn't make — that's the peer's work
  arriving; pull-review, don't revert.
- Feature branches are still the norm for real code work; the watcher keeps
  whatever branch is checked out in sync with its remote.

---

## 11. DEFINITION OF DONE (every task)

1. Acceptance criteria from the task ticket verified with **fresh command output**.
2. Tests added/updated and passing (`pytest tests/` once it exists).
3. No secrets, no debris files, no placeholder left claiming to be real.
4. Committed (Conventional Commit) + pushed; commit hash in the report.
5. 50cent's `ACCEPTED` in the Matrix thread. Anything else is not done.

---

## 12. KEY DOCUMENTS — read order for a new session

1. This file (AGENTS.md).
2. `memetrading_bot_plan/PROJECT_PLAN.md` — the bot blueprint.
3. `description/collaboration_protocol.md` — roles/branches/commits.
4. `memetrading_bot_plan/TODO_LUCKI.md` — current task list.
5. `development/tech_specs.md` — infra intentions.
6. `COMBINED_MEMECOIN_TRADING_REPORT_EXPANDED.md` — 500 KB research; **grep it,
   don't swallow it**.

If anything in this file contradicts what you find on disk, the disk wins —
report the contradiction to @50cent and update this file in the same commit.
