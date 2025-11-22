# CWM for Games
A pipeline that uses LLM to generate Code World Models (CWMs) of perfect or imperfect information games.

## Running the current code
1. Clone the repository (or pull the latest changes) and implement dependencies.
2. Set parameters and run main.py.
3. Check results and logs to see codes/errors.

> OpenSpiel is **not** required yet; plan to add it once a solver (e.g., CFR) is integrated.

## TODO
- Add a trajectory → test generator so game tests can be produced automatically; right now they are hand-written with descriptive errors.
- Implement functions that call CFR or other game-theory algorithms to search for equilibria.
- Fix code generation for `kuhn_poker`, which currently fails because the LLM cannot infer the reward function.
