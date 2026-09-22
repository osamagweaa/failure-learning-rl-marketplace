# osama-rl-plugins (Claude Code marketplace)

Contains one plugin: `failure-learning-rl`, an RL agent that learns from failures and retries until it succeeds.

## Install

From a local checkout:

```
/plugin marketplace add /path/to/failure-learning-rl-marketplace
/plugin install failure-learning-rl@osama-rl-plugins
```

From GitHub, after pushing this folder as a repo root:

```
/plugin marketplace add <github-user>/<repo>
/plugin install failure-learning-rl@osama-rl-plugins
```

Then run `/rl-demo`.
