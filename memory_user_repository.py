class UserRepository:
    def __init__(self):
        self.user_id = 0
        self.data = dict()

    def create(self,data):
        user_id = self.user_id
        self.user_id += 1
        self.set(user_id,data)
        return user_id

    def get(self,user_id):
        return self.data[user_id]

    def set(self,user_id,data):
        self.data[user_id] = data

