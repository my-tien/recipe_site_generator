from pathlib import Path
from typing import Any, TypedDict, Union
import yaml


def split_yaml_md(text: str) -> tuple[str, str]:
    idx1 = idx2 = None
    idx = 0
    try:
        for line in text.split('\n'):
            if line == '---':
                if idx1 is None:
                    idx1 = idx
                else:
                    idx2 = idx
                    break
            idx += len(line) + 1

        yaml = ''
        if idx2 is not None:
            yaml = text[idx1+4:idx2]
        md = text[idx2+4:]
    except TypeError as e:
        raise ValueError(f"Invalid recipe markdown file:\n{text}") from e
    return yaml, md


class Recipe(TypedDict):
    name: str
    path: str
    head: dict
    head_str: str
    instructions: str

class RecipeFolder(TypedDict):
    name: str
    about: str
    recipes: list[Recipe]


def collect_recipes(input_path: Union[str, Path]) -> list[RecipeFolder]:
    recipe_folders: list[RecipeFolder] = []
    for dirpath, _, filenames in Path(input_path).walk():
        folder_name = dirpath.name if dirpath.name != Path(input_path).name else ""
        folder_about = ""
        recipes: list[Recipe] = []
        for filename in filenames:

            if filename == "about.md":
                with open(dirpath / filename, "r", encoding="utf8") as about_file:
                    folder_about = about_file.read()

            elif filename.endswith(".md"):
                recipe_name = Path(filename).stem
                recipe_path = str(Path(dirpath.name) / recipe_name)
                with open(dirpath / filename, "r", encoding="utf8") as recipe_file:
                    yaml_part, md_part = split_yaml_md(recipe_file.read())
                head_str = yaml_part
                head = yaml.safe_load(head_str)
                instructions = md_part
                recipe = Recipe(name=recipe_name, path=recipe_path, head_str=head_str, head=head, instructions=instructions)
                recipes.append(recipe)
        recipe_folder = RecipeFolder(name=folder_name, about=folder_about, recipes=recipes)
        recipe_folders.append(recipe_folder)
    return sorted(recipe_folders, key=lambda recipe_folder: recipe_folder["name"])
