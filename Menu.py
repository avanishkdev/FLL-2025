from pybricks.tools import hub_menu

# Make a menu to choose a letter. You can also use numbers.
selected = hub_menu("A", "C" )

# Based on the selection, run a program.
if selected == "C":
    import Mission_3
elif selected == "A":
    import Mission_1

