class Sample():
    def __init__(self):
        self.sample_id = None
        self.sample_name = None
        self.sample_type = None
        self.sample_data = None
    def set_sample_id(self, id):
        self.sample_id = str(id)
    def set_sample_name(self, name):
        self.sample_name = str(name)
    def set_sample_type(self, sample_type):
        self.sample_type = sample_type
    def set_sample_data(self, data):
        self.sample_data = data