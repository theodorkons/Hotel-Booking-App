from pickle import FALSE


class Room:
	def __init__(self, room_number, name, beds, facilities):
		self.room_number = room_number
		self.name = name
		self.beds = beds
		self.booked = False
		self.facilities = facilities

	def set_price(self, price):
		self.price = price
	
	def check_out(self):
		self.booked = False
	
	def book(self):
		self.booked = True
	
	def is_available(self):
		return self.booked

	def get_room_number(self):
		return self.room_number

	def __str__(self):
		return f'{self.name}, {self.beds}, {self.facilities}'
	
