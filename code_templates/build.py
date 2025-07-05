from Background import Background_template
from Main import Main_template
from Player import Player_template
import json

with open("runnable_code/img/topology.json", 'r') as f:
    topology = json.load(f)

game_fp = "runnable_code"

# Write game code from code templates to game folder
bg_template = Background_template()
bg_template.write_class_to_file(filename=f"{game_fp}/background.py")

player_template = Player_template()
player_template.write_class_to_file(
    filename=f"{game_fp}/player.py", topology=topology
)

main_template = Main_template()
main_template.write_class_to_file(filename=f"{game_fp}/main.py", win_width=800, win_height=600)

