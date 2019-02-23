class ReadFile(object):

    def __init__(self, filename):
        self.filename = filename
        self.res = []

    def read_content(self):
        for path in self.filename:
            with open(str(path), 'r', encoding='utf-8') as file:
                for line in file:
                    self.res.append(line.strip("\n"))
        return self.res
