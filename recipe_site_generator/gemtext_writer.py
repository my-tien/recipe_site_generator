import os
from pathlib import Path
import stat
import traceback
 
from recipe_site_generator.util import Recipe


GEMINI_TEMPLATE = '''#!/usr/bin/env python3

head=\'\'\'{head}\'\'\'

instructions = \'\'\'{instructions}\'\'\'

from recipe_site_generator.gemtext_recipe import print_recipe
print_recipe(head, instructions, image_url_path="{image}", additional_image_url_paths={additional_images})
'''

def write_gemini_recipe(recipe: Recipe, recipe_root: str, recipe_output_path: Path, overwrite: bool) -> None:
    image_path = Path("/") / recipe_root / "images" / f"{recipe['name']}.jpg"
    gemini_recipe = GEMINI_TEMPLATE.format(
        head=recipe["head_str"],
        instructions=recipe["instructions"],
        image=image_path,
        additional_images=recipe.get('additional_images')
    )
    with open(recipe_output_path, 'w', encoding='utf-8') as gemini_file:
        gemini_file.write(gemini_recipe)
    st = os.stat(recipe_output_path)
    os.chmod(recipe_output_path, st.st_mode | stat.S_IEXEC)


def write_gemini_link(recipe: Recipe, recipe_root) -> str:
    optional_date = f" ({recipe['head']['date']})" if recipe['head'].get('date') else ""
    link = Path("/") / recipe_root / recipe["path"]
    return f"=> {link} {recipe['head']['title']}{optional_date}"


def write_gemini_index(target_folder: str | Path, abouts: list[str], recipes: list[list[Recipe]], recipe_root: str):
    try:
        sections = []
        for idx, about in enumerate(abouts):
            if len(recipes[idx]) > 0:
                recipe_links = [write_gemini_link(recipe, recipe_root) for recipe in recipes[idx]]
                sections.append(f"{about}\n{'\n'.join(recipe_links)}")
            else:
                sections.append(about)
        with open(f"{target_folder}/index.gmi", "w", encoding="utf8") as index_file:
            index_str = "\n\n".join(sections)
            index_file.write(index_str)
    except:
        print(f"Failed to write index.gmi file: {traceback.print_exc()}")
