class Business2:

    def __init__(self, data):
        self._data = data

    @property
    def name(self):
        return self._data['Name']

    @property
    def phone(self):
        return self._data.get("Phone Number", '')

    @property
    def address(self):
        return self._data.get("Address", '')

    @property
    def province(self):
        return self._data.get("Province", '')

    @property
    def zip_code(self):
        return self._data.get("Zip Code", '')

    @property
    def city(self):
        return self._data.get("City", '')

    @property
    def continent(self):
        return self._data.get("Continent", '')

    @property
    def rating(self):
        return self._data.get("Review Score", '')

    @property
    def reviews(self):
        return self._data.get("Number of Reviews", 0)

    @property
    def web_url_root(self):
        return self._data.get("Web Domain", '')

    @property
    def website(self):
        return self._data.get("Web URL", '')

    @property
    def latitude(self):
        return self._data.get("Latitude", 0.0)

    @property
    def longitude(self):
        return self._data.get("Longitude", 0.0)

    @property
    def categories(self):
        categories = self._data.get("Categories", '')
        if categories:
            return [cat.strip() for cat in categories.split(',')]
        return []

    @property
    def extra_info(self):
        extra_info = self._data.get("Extra Info", '')
        if extra_info:
            return [info.strip() for info in extra_info.split(',')]
        return []

    @property
    def short_description(self):
        return self._data.get("Short Description", '')

    @property
    def long_description(self):
        return self._data.get("Long Description", '')

    @property
    def hours(self):
        return self._data.get("Schedule", '')

    @property
    def number_of_images(self):
        try:
            return int(self._data.get("Number of Images", 0))
        except ValueError:
            return 0

    @property
    def image_1(self):
        return self._data.get("Image 1", '')

    @property
    def image_2(self):
        return self._data.get("Image 2", '')

    @property
    def image_3(self):
        return self._data.get("Image 3", '')

    @property
    def image_4(self):
        return self._data.get("Image 4", '')

    @property
    def keyword(self):
        return self._data.get("Keyword", '')

    @property
    def main_keyword(self):
        return self._data.get("Main Keyword", '')

    @property
    def country(self):
        return self._data.get("Country", '')

    @property
    def place_id(self):
        return self._data.get("Place ID", '')

    @property
    def related_url(self):
        return self._data.get("Related URL", '')

    @property
    def reviews_link(self):
        return self._data.get("Reviews URL", '')