# ⚡Snapshot Proposer Stats

A simple script to return the number of proposals each author has posted from the last 100 proposals from a given space if they weren't flagged as spam.

## Requirements

python >=3.10.13

[optional] [rye](https://github.com/mitsuhiko/rye) >= 0.16.0

Your [Snapshot API key](https://docs.snapshot.org/tools/api/api-keys) also needs to be added to a `.env` file. Simply:

```console
$ cp .env.example .env
```

then add your API key to the `SNAPSHOT_API` variable in the `.env` file you just created.

## Usage

with [rye](https://github.com/mitsuhiko/rye):

```console
$ rye sync
...
$ rye run stats
Enter the space name: hop.eth
{ '0xDeAdBeEF': 1}
```

without rye installed:

```console
$ pip install -r ./requirements-dev.lock
...
$ python ./src/proposers/__init__.py -m hop_proposers_stats
Enter the space name: hop.eth
{ '0xDeAdBeEF': 1}
```
