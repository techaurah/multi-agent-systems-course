# Solution: The coordination ledger: messages, tokens, and steps

Order-01 takes 5 messages and 5 steps, spending 333 tokens: task, fields, score, draft, verdict, and no redraft loop, because the naive draft on a clean order breaks no policy. The two missing messages against order-05's seven are exactly the price of the trap: a violating draft costs one extra draft and one extra verdict on top of the review itself. Review is a fixed cost on every order and a variable cost on the orders that need it, which is the arithmetic Lesson 09's router exploits.
