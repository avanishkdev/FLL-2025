from pybricks.tools import hub_menu

# Make a menu to choose a letter. You can also use numbers.
selected = hub_menu("3", "1")

# Based on the selection, run a program.
if selected == "3":
    import Mission_3
elif selected == "1":
    import Mission_1
