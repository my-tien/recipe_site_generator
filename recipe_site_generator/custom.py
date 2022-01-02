import os


spacebeans_root: str = '/srv/gemini'
back_button: str = f'=> /bakery Close the book.\n'

def handle_multiplier(factor: str) -> float:
	amount: float = 1
	if len(os.environ['QUERY_STRING']) > 0:
		try:
			amount = float(os.environ['QUERY_STRING'])
			if amount == 0:
				print('Saddened, the chef takes off her apron again.')
			elif amount < 0:
				print('The chef politely explains to you that negative amounts require the ingredient antimatter which is currently out of stock.')
				amount = 1
		except ValueError:
			amount = 1
			print(f'Torn between slight indignation and embarrasment the chef concedes that she does not know how to multiply the ingredients by the factor “{os.environ["QUERY_STRING"]}”.')
	return amount
