
from ...interface import AbstractPriceBoard
from ...environment import Environment
from ...model.snapshot import SnapshotObject
from .utils import get_tick


class PriceBoard(AbstractPriceBoard):
	
	def get_last_price(self, order_book_id):
		
		return get_tick(order_book_id)