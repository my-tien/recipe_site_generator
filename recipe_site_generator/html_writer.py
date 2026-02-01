import argparse
from importlib import resources
from pathlib import Path
import shutil

import markdown
import yaml
import  jinja2
from recipe_site_generator.util import split_yaml_md
from recipe_site_generator.asciiart_md_extension import ASCIIArtExtension


def markdown_filter(text: str):
    return markdown.markdown(text, extensions=[ASCIIArtExtension()])


def write_html_page(input_md_path: Path, target_html_path: Path, image_path: str | None):
    with open(input_md_path, 'r', encoding='utf-8') as md_file:
        head, instructions = split_yaml_md(md_file.read())

    recipe: dict[str, str] = yaml.safe_load(head)

    template_path = resources.files("recipe_site_generator") / "html/templates"
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(template_path)))
    env.filters["markdown"] = markdown_filter

    template = env.get_template("recipe.jinja")

    html = template.render(
        title=recipe["title"],
        story=recipe.get("story", ""),
        image=image_path,
        ingredients=recipe["ingredients"],
        tools=recipe.get("tools", []),
        oven_instructions=recipe.get("oven_instructions", ""),
        schedule=recipe.get("schedule", ""),
        instructions=instructions
    )
    with open(target_html_path, "w") as f:
        f.write(html)


def write_html_index(target_path: str | Path, abouts: list[str]):
    template_path = resources.files("recipe_site_generator") / "html/templates"
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(template_path)))
    env.filters["markdown"] = markdown_filter

    template = env.get_template("recipe.jinja")

    html = template.render(
    )
    with open(target_html_path, "w") as f:
        f.write(html)


def main():
    parser = argparse.ArgumentParser("""Generate HTML recipe pages from input markdown files.""", allow_abbrev=False)
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
        help="Output folder for HTML recipe files. By default a html subfolder in the input folder."
    )
    parser.add_argument("--overwrite",
        action="store_true",
        help="Whether to overwrite the output folder if it already exists."
    )

    args = parser.parse_args()
    input_recipe_folder: Path = args.recipe_folder
    input_image_folder: Path = args.image_folder
    output_folder: Path = args.out
    overwrite: bool = args.overwrite

    if not input_recipe_folder.exists():
        raise ValueError(f"The provided input folder doesn't exist: {input_recipe_folder}")
    if not input_image_folder.exists():
        raise ValueError(f"The provided input folder doesn't exist: {input_image_folder}")

    if not output_folder:
        output_folder = input_recipe_folder / "html"

    for dirpath, _, filenames in input_recipe_folder.walk():
        recipe_dir = output_folder/dirpath.name
        for filename in filenames:
            try:
                if not filename.lower().endswith(".md") or filename.lower() == "readme.md":
                    continue

                recipe_input_path = dirpath / filename
                image_input_path = input_image_folder / Path(filename).with_suffix('.jpg')
                has_image = image_input_path.exists()
                recipe_output_path = recipe_dir / Path(filename).with_suffix(".html")
                relative_image_path = f"images/{image_input_path.with_suffix('.jpg').name}"
                image_output_path = recipe_dir / relative_image_path

                if recipe_output_path.exists():
                    if overwrite:
                        print(f"Overwriting existing file {recipe_output_path}")
                    else:
                        raise FileExistsError(f"File already exists: {recipe_output_path}")

                if has_image and image_output_path.exists():
                    if overwrite:
                        print(f"Overwriting existing file {recipe_output_path}")
                    else:
                        raise FileExistsError(f"File alreadey exists: {image_output_path}")

                (recipe_dir / "images").mkdir(exist_ok=True, parents=True)
                write_html_page(
                    recipe_input_path,
                    recipe_output_path,
                    relative_image_path if has_image else None
                )
                shutil.copy(image_input_path, image_output_path)
                print(f"{filename} done.")
            except:
                print(f"Failed to generate output for {filename}.")


if __name__ == '__main__':
    main()
