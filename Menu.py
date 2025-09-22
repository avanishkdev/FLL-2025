from pybricks.tools import hub_menu

# Make a menu to choose a letter. You can also use numbers.
selected = hub_menu("H", "S", "L")

# Based on the selection, run a program.
if selected == "H":
    import Hello
elif selected == "S":
    import Sound
elif selected == "L":
    import Light
