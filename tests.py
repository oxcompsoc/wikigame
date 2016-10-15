import wikigame

checks = [ "Republic of Iceland"
         , "Arno River"
         , "International nongovernmental organization"
         ]

for check in checks:
    print(check + " -> " + wikigame.get_redirect(check))
    print(wikigame.links_in_order(check, cache=False))

