class Body:
    def __init__(self):
        self.body = {
            'Head':{
                'Health':100
            },
            'Torso':{
                'Health':100
            },
            'Left Arm':{
                'Health':100
            },
            'Right Arm':{
                'Health':100
            },
            'Left Leg':{
                'Health':100
            },
            'Right Leg':{
                'Health':100
            }
        }

    def set_health(self, part, value):
        self.body[part] = value
    
    def get_health(self, part):
        return self.body[part]