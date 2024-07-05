
from pathlib import Path

path = Path("C:/Users/TeJiang/Documents/Tencent Files/1471157779/FileRecv")
figure_path = path / "大合影-.jpg"
file_list = list(path.rglob("*.*"))
for i, file in enumerate(file_list):
    print(file)