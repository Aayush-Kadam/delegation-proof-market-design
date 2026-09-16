import json
import numpy as np
from delegation_market.level3 import _holdout_pairs, _load_completed_pair, _pair_id, execute_holdout_resumable, run_seed


def test_level3_accounting_identities_small_run():
    r=run_seed("first_price",.4,100,.1,.1,17,step=.1,tail_share=.1)
    assert np.isclose(r["full_dl_revenue"],.4-r["full_revenue"])
    assert np.isclose(r["full_dl_ae"],1-r["full_high_win"])
    assert np.isclose(r["full_dl_welfare"],1-r["full_welfare"])
    assert np.isclose(r["full_surplus_total"],r["full_surplus_high"]+r["full_surplus_low"])
    assert 0 <= r["full_high_win"] <= 1


def test_discrete_reference_profile_is_equilibrium_on_registered_values():
    step=.01
    for vl in [.1,.2,.3,.4,.5,.6,.7,.8,.9]:
        bh,bl=vl,vl-step
        high_u=1-bh; high_tie=.5*(1-bl)
        assert high_u >= high_tie
        assert bl <= vl and bh <= 1


def test_holdout_pair_ids_are_deterministic_and_unique():
    grid={"seeds":{"start":2000,"count":2},"v_low":[.1,.3],"horizons":[50],"rate_factors":[[1.,1.]],"bid_step":.1,"tail_share":.1}
    pairs=_holdout_pairs(grid)
    assert len(pairs)==4 and len({p[0] for p in pairs})==4
    assert pairs[0][0]==_pair_id(.1,50,1.,1.,.1,.1,2000)


def test_resumable_holdout_persists_pairs_and_skips_completed(tmp_path):
    grid={"name":"L3_HOLDOUT","mechanisms":["first_price","second_price"],"seeds":{"start":2000,"count":2},"v_low":[.1],"horizons":[20],"rate_factors":[[1.,1.]],"bid_step":.1,"tail_share":.1}
    grid_path=tmp_path/"grid.json"; grid_path.write_text(json.dumps(grid),encoding="utf-8")
    first=execute_holdout_resumable(tmp_path,grid_path,"protocol","commit",workers=1,max_pairs=1)
    assert first["completed_pairs"]==1 and first["status"]=="shard_complete"
    parts=list((tmp_path/"results"/"level_03"/"holdout"/"pairs").glob("*.json")); assert len(parts)==1
    before=parts[0].read_bytes()
    final=execute_holdout_resumable(tmp_path,grid_path,"protocol","commit",workers=1)
    assert final["completed_pairs"]==2 and final["status"]=="complete"
    assert parts[0].read_bytes()==before
    frame=np.genfromtxt(tmp_path/"results"/"level_03"/"holdout"/"seed_results.csv",delimiter=",",names=True,dtype=None,encoding="utf-8")
    assert len(frame)==4
    assert _load_completed_pair(parts[0],json.loads(before)["pair_id"])
