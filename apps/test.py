from pathlib import Path
home_dir = Path(__file__).parents[1]
img_dir = Path(__file__).parents[0]
print(home_dir/"data\main_data.csv")
print(img_dir)
print(home_dir/r"data\img\topic.png")