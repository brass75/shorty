# Shorty - The Spiderweb URL Shortener

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Actions status](https://github.com/brass75/shorty/workflows/CI/badge.svg)](https://github.com/brass75/shorty/actions)
[![Mastodon Follow](https://img.shields.io/mastodon/follow/109552736199041636?domain=https%3A%2F%2Ftwit.social&style=flat)](https://twit.social/@brass75)

My friend, [Joe Kaufeld](https://fosstodon.org/@itsthejoker) decided he wanted to
understand how web frameworks actually work. So he wrote one. I decided I would be a 
good guinea pig for it and that it would be a fun project for me to play with - and
give me a reason to take [UV](https://docs.astral.sh/uv/) out for a spin - for me to
use [Spiderweb](https://itsthejoker.github.io/spiderweb/#/) to write a URL shortener.
So I did. And that's what this is.

You should be aware that I am not, at my core, a web developer. I know the basics and 
that's about it. I'm not a DB person, I know the basics and that's about it. My
initial goal was to write something that would shorten a URL and give that shortened
URL back and that when you clicked on that link it would take you where you want to 
go. So I did and that's what this is.

For now, I decided, since this is a weekend project, to keep it simple. Just get 
something that works. The data store is a JSON file. There is no good handling of
hash collisions. But it works. And it only took me a couple of hours of tinkering
to get it there.

Right now it:
- Allows you to add a URL.
- Redirects properly to a known shortened URL.
- Uses persistent storage (in the form of a JSON file.)
- Gives an error on hash collision.
- Redirects back to the add route page for an unknown short code.
- Add methods to see what URLs are stored.
- Add a method for a custom short URL.

Future plans:
- Handle hash collision.
- Use an actual DB as a data store.

## If you want to run this locally

All you need to do is:

```shell
git clone git@github.com:brass75/shorty.git
cd shorty
uv run src/app.py
```

NOTE: This is my first time playing with `uv` as I noted above. You might need to run:

```shell
uv python install 3.12
```

before the `uv run` line (and you definitely need to install `uv` but I've linked to 
them above so you can pick how you want to do it from there) to install the correct
version of Python for the venv, but I'm not 100% sure.
