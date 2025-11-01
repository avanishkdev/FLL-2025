from pybricks.tools import hub_menu

# Make a menu to choose a letter. You can also use numbers.
selected = hub_menu("A", "B" , "C" , "D" , "E", "F" , "G", "H")

# Based on the selection, run a program.
if selected == "A":
    import Missioms_8_5_9_and_10
elif selected == "B":
    import mission_9_pull
elif selected == "C":
    import mission_10_pull
elif selected == "D":
    import mission_6
elif selected == "E":
    import mission_7
elif selected == "F":
    import Mission1_2
elif selected == "G":
    import Mission1_3_13
elif selected == "H":
    import Mission_12
