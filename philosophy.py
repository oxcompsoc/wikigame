# By clicking the first link of a Wikipedia article you will, in most cases, get
# to the article on philosophy. I then found a fixed route from philosophy to
# frogs, so we do that route at the end

import wikigame

# Ensure that we don't get stuck in a loop
seen = set()
current = wikigame.random_article()

while current.lower() != "philosophy":
    print(current)
    seen.add(current)
    links = wikigame.links_in_order(current)
    # Remove any links not already seen
    links = [link for link in links if not link in seen]
    # Go to the first link in the article
    if len(links) > 0:
        current = links[0]
    else:
        # You could come up with a better strategy here
        print("Dead end!")
        exit()

# A known route from Philosophy to Frog
print("Philosophy")
print("Medicine")
print("Herbalism")
print("Chickens")
print("List of domesticated animals")
print("Australian green tree frog")
print("Hylidae")
print("Frog")
