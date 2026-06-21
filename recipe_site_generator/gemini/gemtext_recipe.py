import os
from pathlib import Path
from typing import Optional

from recipe_site_generator.gemini.ingredient import Ingredient
from tabulate import tabulate
import yaml


RECIPE_FILESYSTEM_ROOT: str = os.environ.get('RECIPE_ROOT', default='/srv/gemini')


def handle_multiplier(multiplier_query_string: str) -> float:
	amount: float = 1
	if len(multiplier_query_string) > 0:
		try:
			amount = float(multiplier_query_string)
			if amount == 0:
				print('Saddened, the chef takes off her apron again.')
			elif amount < 0:
				print('The chef politely explains to you that negative amounts require the ingredient antimatter which is currently out of stock.')
				amount = 1
		except ValueError:
			amount = 1
			print(f'Torn between slight indignation and embarrasment the chef concedes that she does not know how to multiply the ingredients by the factor “{multiplier_query_string}”.')
	return amount


def get_ingredient_list(ingredients: list, amount: float) -> str:
	return tabulate([Ingredient.create(ing, amount).h() for ing in ingredients], tablefmt='simple', floatfmt='.3g')


def print_recipe(
		head: str,
		instructions: str,
		recipe_root: str,
		image_name: Optional[str] = None,
		additional_image_names: Optional[dict[str, str]] = None
) -> str:
	recipe: dict = yaml.safe_load(head)
	back_button = f'=> /{recipe_root} Close the book.\n'
	image_url_path = None
	filesystem_image_path = None
	if image_name is not None:
		image_url_path = f'{recipe_root}/images/{image_name}'
		filesystem_image_path = Path(RECIPE_FILESYSTEM_ROOT)/"images"/image_name 

	gemtext: list[str] = []
	if 'amount' in os.environ['QUERY_STRING']:
		return "10 Please enter an amount factor:\r\n"
	
	gemtext.append("20 text/gemini\r\n")

	gemtext.append(back_button)

	gemtext.append(f"# {recipe["title"]}\n")
	if 'story' in recipe:
		gemtext.append(recipe['story'] + '\n')

	if filesystem_image_path is not None and filesystem_image_path.exists():
		gemtext.append(f'=> {image_url_path} An image of {recipe["title"]}\n')

	for title, additional_img_name in (additional_image_names or {}).items():
		if  (Path(RECIPE_FILESYSTEM_ROOT)/"images"/additional_img_name).exists():
			gemtext.append(f'=> {recipe_root}/images/{additional_img_name} {title}\n')

	amount = handle_multiplier(os.environ['QUERY_STRING'])

	gemtext.append(f'## Zutaten (Menge: ×{amount:.4g})\n')
	gemtext.append(f'=> {os.environ["GEMINI_URL"]}/?amount Specify the amount you want to make.')

	if isinstance(recipe['ingredients'], dict):
		for section, ingredients in recipe['ingredients'].items():
			gemtext.append(f'\n### {section}\n')
			gemtext.append(f'```{section}-Zutaten-Tabelle')
			get_ingredient_list(ingredients, amount)
			print('```')
	else:
		gemtext.append(f'```')
		get_ingredient_list(recipe['ingredients'], amount)
		gemtext.append('```')
	if 'tools' in recipe:
		gemtext.append('\n## Utensilien\n')
		for tool in recipe['tools']:
			gemtext.append(f'* {tool}')
	if 'oven_instructions' in recipe:
		gemtext.append(f'\n## Ofeneinstellung:\n\n⏲ {recipe["oven_instructions"]}')

	gemtext.append(f'\n## Anweisungen')
	gemtext.append(instructions)
	gemtext.append(back_button)

	return "".join(gemtext)
