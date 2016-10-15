# Wikipedia game

The aim of the [Wikipedia game][game] is to click the random article button and
then click on as few links as possible try to get to another designated
Wikipedia article. In this game our goal is to write bots to get to the page for
the [department][].

This repository contains some Python code to get started with the challenge,
along with an example that uses the 'Philosophy' strategy: if you keep clicking
the first link of an article you eventually get to [Philosophy][], and from
there we can get to the department page using a known path.

**Python 3** is required, so you may need to run `python3` instead of `python`
if you have both installed.

To get started, download a local copy of this repository (either via cloning,
forking, or downloading the zip file) and checking it works with `python3
philosophy.py`.

## Functions

```python
import wikigame
# Gets the title of a random article
rnd = wikigame.random_article()
# Gets a list of all the links on that page
links = wikigame.links_in_order(rnd)

print(rnd)
for link in links:
    print(" - " + link)
```

When I run this using `python3`:

```
Bhujabalapatnam
 - Village
 - India
 - States and territories of India
...
```

## Caching

To reduce the number of requests to Wikipedia, a set of links for each page are
also cached in a sub-folder called 'cache', so you will find that after running
a strategy a few times it will run reasonably quickly.

[game]: https://en.wikipedia.org/wiki/Wikipedia:Wiki_Game
[department]: https://en.wikipedia.org/wiki/Department_of_Computer_Science,_University_of_Oxford
[philosophy]: https://en.wikipedia.org/wiki/Philosophy
