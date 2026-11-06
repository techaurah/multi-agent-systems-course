"""The measurement harness: run a system over orders and
summarize, so every comparison in the course uses the same
arithmetic.

Cost per success is the headline metric: total tokens spent
divided by orders completed successfully. A system that is
cheap per attempt and wrong is not cheap.
"""


def summarize(results):
    n = len(results)
    successes = sum(1 for r in results if r["success"])
    tokens = sum(r["tokens"] for r in results)
    return {
        "orders": n,
        "successes": successes,
        "success_rate": round(successes / n, 4) if n else 0.0,
        "mean_messages": round(sum(r["messages"] for r in results) / n, 2)
        if n else 0.0,
        "mean_tokens": round(tokens / n, 1) if n else 0.0,
        "mean_steps": round(sum(r["steps"] for r in results) / n, 2)
        if n else 0.0,
        "escapes": sum(len(r["escapes"]) for r in results),
        "tokens_per_success": round(tokens / successes, 1)
        if successes else None,
        "failed_orders": [r["order_id"] for r in results
                          if not r["success"]],
    }


def by_family(results, orders):
    fams = {}
    fam_of = {o["id"]: o["family"] for o in orders}
    for r in results:
        fams.setdefault(fam_of[r["order_id"]], []).append(r)
    return {fam: summarize(rs) for fam, rs in sorted(fams.items())}
