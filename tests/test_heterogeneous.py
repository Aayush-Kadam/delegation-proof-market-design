import json
from pathlib import Path

from delegation_market.agents import HedgeAgent
from delegation_market.heterogeneous import make_agents, job_id, tasks
from delegation_market.level5 import FTPLAgent, RegretMatchingAgent


def test_ordered_profiles_swap_actual_agent_types():
    expected = {"hedge": HedgeAgent, "ftpl": FTPLAgent, "regret_matching": RegretMatchingAgent}
    profiles = [("hedge", "ftpl"), ("ftpl", "hedge"), ("hedge", "regret_matching"),
                ("regret_matching", "hedge"), ("ftpl", "regret_matching"),
                ("regret_matching", "ftpl")]
    for high, low in profiles:
        agents, _ = make_agents(high, low, .5, 100, 1, 1, .01, 7)
        assert type(agents[0]) is expected[high]
        assert type(agents[1]) is expected[low]
        assert agents[0].rng is not agents[1].rng


def test_primary_ids_and_exact_compute():
    cfg = json.loads((Path(__file__).parents[1] / "configs/heterogeneous/main.json").read_text())
    all_tasks = tasks(cfg)
    ids = [job_id(x) for x in all_tasks]
    assert len(all_tasks) == 9000
    assert len(ids) == len(set(ids))
    assert sum(x[4] for x in all_tasks) == 288_000_000


def test_pilot_ids_and_roles():
    cfg = json.loads((Path(__file__).parents[1] / "configs/heterogeneous/pilot.json").read_text())
    all_tasks = tasks(cfg)
    assert len(all_tasks) == 600
    assert len({job_id(x) for x in all_tasks}) == 600
    assert {(x[0], x[1]) for x in all_tasks} == {tuple(x) for x in cfg["profiles"]}
