class Customer:
    def __init__(self, first_name, last_name, birth_date, phone_num, id_num):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.phone_num = phone_num
        self.id_num = id_num


    def get_first_name(self):
        return self.first_name


    def get_last_name(self):
        return self.last_name


    def get_birth_date(self):
        return self.birth_date


    def get_phone_num(self):
        return self.phone_num


    def get_id_num(self):
        return self.id_num


    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.birth_date} {self.phone_num} {self.id_num}'
    
    