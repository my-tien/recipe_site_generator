import os
from typing import Callable, Iterable, Optional

from recipe_site_generator import custom
from recipe_site_generator.ingredient import Ingredient
from tabulate import tabulate
import yaml


def print_ingredient_list(ingredients: list, amount: float) -> None:
	print(tabulate([Ingredient.create(ing, amount).h() for ing in ingredients], tablefmt='simple', floatfmt='.3g'))


def print_recipe(head: str, instructions: str, image_url_path: Optional[str] = None, additional_image_url_paths: Optional[dict[str, str]] = None, multiply_handler: Callable[[str], float] = custom.handle_multiplier) -> None:
	if 'amount' in os.environ['QUERY_STRING']:
		print('10 Please enter an amount factor:\r\n')
		exit(0)
	
	print('20 text/gemini\r\n')

	recipe: dict = yaml.safe_load(head)

	print(custom.back_button)

	print(f'# {recipe["title"]}\n')
	if 'story' in recipe:
		print(recipe['story'] + '\n')

	if image_url_path is not None and os.path.exists(f'{custom.spacebeans_root}/{image_url_path}'):
		print(f'=> {image_url_path} An image of {recipe["title"]}\n')

	for title, image_url_path in (additional_image_url_paths or {}).items():
		print(f'=> {image_url_path} {title}\n')

	amount = multiply_handler(os.environ['QUERY_STRING'])

	print(f'## Zutaten (Menge: ×{amount:.4g})\n')
	print(f'=> {os.environ["GEMINI_URL"]}/?amount Specify the amount you want to make.')

	if isinstance(recipe['ingredients'], dict):
		for section, ingredients in recipe['ingredients'].items():
			print(f'\n### {section}\n')
			print(f'```{section}-Zutaten-Tabelle')
			print_ingredient_list(ingredients, amount)
			print('```')
	else:
		print(f'```')
		print_ingredient_list(recipe['ingredients'], amount)
		print('```')
	if 'tools' in recipe:
		print('\n## Utensilien\n')
		for tool in recipe['tools']:
			print(f'* {tool}')
	if 'oven_instructions' in recipe:
		print(f'\n## Ofeneinstellung:\n\n⏲ {recipe["oven_instructions"]}')

	print(f'\n## Anweisungen')
	print(instructions)
	print(custom.back_button)
