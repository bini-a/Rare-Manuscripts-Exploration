from pathlib import Path
home_dir = Path(__file__).parents[1]
img_dir = Path(__file__).parents[0]
print(home_dir/"data\main_data.csv")
print(img_dir)
# loc = home_dir/r"data\img\topic.png"

# print(loc, str(loc))
import os
import re
loc = home_dir/r"data\img\topic.png"
# loc  = str(loc)
# # "data\img\\topic.png"
# print(Path(loc))
print(os.path.abspath(__file__))
print(Path().parent.absolute())
print( Path().parent.absolute()/"data/img/topic.png")