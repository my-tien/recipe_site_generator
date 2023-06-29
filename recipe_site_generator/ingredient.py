from __future__ import annotations
from typing import Optional


def _assert(expression: bool, msg: str) -> None:
	if not expression:
		raise ValueError(msg)


class Ingredient:
	def __init__(self, name: str, amount: Optional[int]=None, unit: Optional[str]=None):
		_assert(unit is None or amount is not None, f'Missing amount for set unit: {unit} {name}')
		self.amount: Optional[int] = amount
		self.unit: Optional[str] = unit
		self.name: str = name

	@staticmethod
	def create(l: list, factor: float) -> Ingredient:
		assertion_msg = 'Accepted lists: [name: str], [amount: Number, name: str], [amount: Number, unit: str, name: str]'
		if len(l) == 1:
			_assert(isinstance(l[0], str), assertion_msg)
			return Ingredient(name=l[0])
		elif len(l) == 2:
			_assert(isinstance(l[0], (int, float)) and isinstance(l[1], str), assertion_msg)
			return Ingredient(name=l[1], amount=l[0]*factor)
		elif len(l) == 3:
			_assert(isinstance(l[0], (int, float)) and isinstance(l[1], str) and isinstance(l[2], str), assertion_msg)
			return Ingredient(name=l[2], amount=l[0]*factor, unit=l[1])

	def h(self) -> tuple:
		if self.unit == 'g':
			if self.amount < 0.1:
				return self.amount*1000, 'mg', self.name
			elif self.amount < 1000:
				return self.amount, 'g', self.name
			else:
				return self.amount/1000, 'kg', self.name
		elif self.unit == 'ml':
			if self.amount < 1000:
				return self.amount, 'ml', self.name
			else:
				return self.amount/1000, 'L', self.name
		elif self.unit == 'TL':
			if divmod(self.amount, 0.5)[1] == 0:
				return self.amount, 'TL', self.name
			else:
				return Ingredient(name=self.name, amount=self.amount*5, unit='ml').h()
		elif self.unit == 'EL':
			if divmod(self.amount, 0.5)[1] == 0:
				return self.amount, 'EL', self.name
			else:
				return Ingredient(name=self.name, amount=self.amount*15, unit='ml').h()
		elif isinstance(self.unit, str):
			return self.amount, self.unit, self.name
		elif self.unit is None:
			return (self.name,) if self.amount is None else (self.amount, '', self.name)
		else:
			raise ValueError(f'Don’t know how to print unit {self.unit}')
