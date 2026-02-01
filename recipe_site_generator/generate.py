import argparse
from pathlib import Path
import shutil
import traceback
from typing import Callable

from gemtext_writer import write_gemini_index, write_gemini_link, write_gemini_page
from html_writer import write_html_index, write_html_link, write_html_page
from recipe_site_generator.util import collect_recipes, Recipe


def main():
    parser = argparse.ArgumentParser("""Generate gemtext recipe pages from input markdown files.""")
    parser.add_argument("recipe_folder",
        type=Path,
        default=Path.cwd(),
        help="Input root folder of markdown recipe files.")
    parser.add_argument("image_folder",
        type=Path,
        default=Path.cwd(),
        help="Input root folder of recipe images."
    )
    parser.add_argument("--out",
        type=Path,
        default=None,
        help="Output folder for gemini recipe files. By default a gemini subfolder in the input folder."
    )
    parser.add_argument("--overwrite",
        action="store_true",
        help="Whether to overwrite the output folder if it already exists."
    )
    parser.add_argument("--html",
        action="store_true",
        default=None,
        help="Generate HTML instead of gemini files"
    )

    args = parser.parse_args()
    input_recipe_folder: Path = args.recipe_folder
    input_image_folder: Path = args.image_folder
    output_folder: Path = args.out
    overwrite: bool = args.overwrite

    write_page = write_gemini_page
    write_link: Callable[[Recipe], str] = write_gemini_link
    write_index = write_gemini_index
    if args.html:
        write_page = write_html_page
        write_link = write_html_link
        write_index = write_html_index    

    if not input_recipe_folder.exists():
        raise ValueError(f"The provided input folder doesn't exist: {input_recipe_folder}")
    if not input_image_folder.exists():
        raise ValueError(f"The provided input folder doesn't exist: {input_image_folder}")

    if not output_folder:
        output_folder = input_recipe_folder / "gemini"

    recipe_root = output_folder.absolute().name
    recipe_folders = collect_recipes(input_recipe_folder, recipe_root)

    abouts: list[str] = []
    for recipe_folder in recipe_folders:
        this_about = recipe_folder.get("about", "")
        about_links: list[str] = []
        for recipe in recipe_folder["recipes"]:
            try:
                write_page(recipe, recipe_root, output_folder, overwrite)
                print(f"{recipe['name']} done.")
            except:
                print(f"Failed to generate output for {recipe['name']}: {traceback.print_exc()}")

            about_links.append(write_link(recipe))

        if len(about_links) > 0:
            this_about = f"{this_about}\n{'\n'.join(about_links)}"
        abouts.append(this_about)
    
    write_index(output_folder / "index.gmi", abouts)

    (output_folder / "images").mkdir(exist_ok=True, parents=True)
    shutil.copytree(str(input_image_folder), str(output_folder / "images"), dirs_exist_ok=overwrite)


if __name__ == '__main__':
    main()
