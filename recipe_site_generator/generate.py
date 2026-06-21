import argparse
from pathlib import Path
import shutil
import traceback

from recipe_site_generator.gemtext_writer import write_gemini_index, write_gemini_recipe
from recipe_site_generator.html_writer import write_html_index, write_html_recipe
from recipe_site_generator.util import collect_recipes, Recipe


def main():
    parser = argparse.ArgumentParser(
        prog="recipe_site_generator",
        description="Generate gemini or HTML recipe pages from input markdown files (default: gemini).")
    parser.add_argument("INPUT_RECIPE_FOLDER",
        type=Path,
        default=Path.cwd(),
        help="Input root folder of markdown recipe files.")
    parser.add_argument("INPUT_IMAGE_FOLDER",
        type=Path,
        default=Path.cwd(),
        help="Input root folder of recipe images."
    )
    parser.add_argument("--out",
        type=Path,
        default=None,
        metavar="OUTPUT_FOLDER",
        help="Output folder for recipe files. By default subfolder 'gemini' or 'html' in the input folder."
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
    input_recipe_folder: Path = args.INPUT_RECIPE_FOLDER
    input_image_folder: Path = args.INPUT_IMAGE_FOLDER
    output_folder: Path = args.out
    overwrite: bool = args.overwrite

    write_recipe = write_gemini_recipe
    write_index = write_gemini_index
    if args.html:
        write_recipe = write_html_recipe
        write_index = write_html_index    

    if not input_recipe_folder.exists():
        raise ValueError(f"The provided input folder doesn't exist: {input_recipe_folder}")
    if not input_image_folder.exists():
        raise ValueError(f"The provided input folder doesn't exist: {input_image_folder}")

    if not output_folder:
        subfolder = "html" if args.html else "gemini"
        output_folder = input_recipe_folder / subfolder

    recipe_root = output_folder.absolute().name
    recipe_folders = collect_recipes(input_recipe_folder)

    abouts: list[str] = []
    recipes: list[list[Recipes]] = []

    for recipe_folder in recipe_folders:
        this_about = recipe_folder.get("about", "")
        this_recipes: list[Recipe] = []
        for recipe in recipe_folder["recipes"]:
            try:
                recipe_output_path = output_folder / Path(recipe["path"])
                if recipe_output_path.exists():
                    if overwrite:
                        print(f"Overwriting existing file {recipe_output_path}")
                    else:
                        raise FileExistsError(f"File already exists: {recipe_output_path}")
                recipe_output_path.parent.mkdir(exist_ok=True, parents=True)

                write_recipe(recipe, recipe_root, recipe_output_path, overwrite)
                print(f"{recipe['name']} done.")
            except:
                print(f"Failed to generate output for {recipe['name']}: {traceback.print_exc()}")

            this_recipes.append(recipe)

        abouts.append(this_about)
        recipes.append(this_recipes)
    
    write_index(output_folder, abouts, recipes, recipe_root)

    input_image_folder = str(input_image_folder)
    output_image_folder = str(output_folder / "images")
    if input_image_folder != output_image_folder:
        shutil.copytree(input_image_folder, output_image_folder, dirs_exist_ok=overwrite)


if __name__ == '__main__':
    main()
