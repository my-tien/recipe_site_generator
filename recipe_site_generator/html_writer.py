from importlib import resources
from pathlib import Path

import markdown
import yaml
import  jinja2
from recipe_site_generator.asciiart_md_extension import ASCIIArtExtension


def markdown_filter(text: str) -> str:
    return markdown.markdown(text, extensions=[ASCIIArtExtension()])


def write_html_recipe(recipe: Recipe, recipe_root: str, recipe_output_path: Path, overwrite: bool) -> None:
    template_path = resources.files("recipe_site_generator") / "html/templates"
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(template_path)))
    env.filters["markdown"] = markdown_filter

    template = env.get_template("recipe.jinja")

    image_path = f"../images/{recipe['name']}.jpg"
    html = template.render(
        title=recipe["head"]["title"],
        story=recipe["head"].get("story", ""),
        image=image_path,
        ingredients=recipe["head"]["ingredients"],
        tools=recipe["head"].get("tools", []),
        oven_instructions=recipe["head"].get("oven_instructions", ""),
        schedule=recipe["head"].get("schedule", ""),
        instructions=recipe["instructions"]
    )
    with open(recipe_output_path.with_suffix(".html"), "w") as f:
        f.write(html)


def write_html_index(target_folder: str | Path, abouts: list[str], recipes: list[list[Recipe]], _recipe_root: str) -> None:
    template_path = resources.files("recipe_site_generator") / "html/templates"
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(template_path)))
    env.filters["markdown"] = markdown_filter

    template = env.get_template("index.jinja")

    html = template.render(
        abouts=abouts,
        recipes=recipes
    )
    with open(f"{target_folder}/index.html", "w",encoding="utf8") as f:
        f.write(html)
