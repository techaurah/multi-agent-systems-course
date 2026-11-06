# Solution: Shared memory: the stale read and the version check

Upgrading only order-06 gives 11 of 12 correct bands. The exposed thin order that matters is order-04, and it stays wrong; order-07 and order-12 keep correct bands on version 1 fields, because for them the careful and quick readings agree on every field that carries points. Triage rule for verification effort: spend it where the two readings disagree, not where the order merely looks unusual. Thin is a routing label; disagreement is the evidence.
