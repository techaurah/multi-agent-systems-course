# Solution: Parallel fan-out: buying time with workers

Four workers give a makespan of 6 steps, no better than three workers. The deal is uneven: workers one and two receive two orders each (six steps each) while workers three and four receive one each (three steps), so the busiest worker still carries six steps and the makespan is set by the deal, not the pool. Tokens are unchanged at 1434. The general rule: a pool larger than the batch's natural deal granularity buys idle workers, and Lesson 25 watches the same effect flatten the scaling curve.
