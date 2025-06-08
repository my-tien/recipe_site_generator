import os

# Root folder of the recipes. Recipe images then are expected to be at {recipe_root}/{image_url_path}
recipe_root: str = os.environ.get('RECIPE_ROOT', default='/srv/gemini')

# link for back button in a recipe
back_button: str = f'=> /bakery Close the book.\n'

# Function to handle the ingredient multiplier provided by the user
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
