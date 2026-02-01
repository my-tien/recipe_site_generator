import os
from pathlib import Path
import stat
import traceback
import yaml
 
from recipe_site_generator.util import Recipe


GEMINI_TEMPLATE = '''#!/usr/bin/env python3

head=\'\'\'{head}\'\'\'

instructions = \'\'\'{instructions}\'\'\'

from recipe_site_generator.gemtext_recipe import print_recipe
print_recipe(head, instructions, image_url_path="{image}", additional_image_url_paths={additional_images})
'''

def write_gemini_page(recipe: Recipe, recipe_root: str, output_folder: Path, overwrite: bool):
    recipe_output_path = output_folder / Path(recipe["path"]).relative_to(recipe_root)
    if recipe_output_path.exists():
        if overwrite:
            print(f"Overwriting existing file {recipe_output_path}")
        else:
            raise FileExistsError(f"File already exists: {recipe_output_path}")
    recipe_output_path.parent.mkdir(exist_ok=True, parents=True)

    gemini_recipe = GEMINI_TEMPLATE.format(
        head=recipe["head"],
        instructions=recipe["instructions"],
        image=Path("/") / recipe_root / "images" / f"{recipe['name']}.jpg",
        additional_images=recipe.get('additional_images')
    )
    with open(recipe_output_path, 'w', encoding='utf-8') as gemini_file:
        gemini_file.write(gemini_recipe)
    st = os.stat(recipe_output_path)
    os.chmod(recipe_output_path, st.st_mode | stat.S_IEXEC)


def write_gemini_link(recipe: Recipe) -> str:
    recipe_head = yaml.safe_load(recipe["head"])
    optional_date = f" ({recipe_head['date']})" if recipe_head.get('date') else ""
    return f"=> /{recipe["path"]} {recipe['name']}{optional_date}"


def write_gemini_index(target_path: str | Path, abouts: list[str]):
    try:
        with open(target_path, "w", encoding="utf8") as index_file:
            about = "\n\n".join(abouts)
            index_file.write(about)
    except:
        print(f"Failed to write index.gmi file: {traceback.print_exc()}")
