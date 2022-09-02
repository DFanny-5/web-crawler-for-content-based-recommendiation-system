class movie_entry:
    def __init__(self, page_url):
        self.page_url = page_url
        self.id = None
        self.title = None
        self.genre = None
        self.cast = None
        self.director = None
        self.time_duration = None
        self.added_date = None
        self.added_month = None
        self.added_year = None
        self.parent_control = None
        self.available_language = None

    def get_title(self):
        return self.title
