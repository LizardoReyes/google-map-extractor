class Competitor:
    def __init__(self, data):
        self._data = data

    @property
    def name(self):
        return self._data['name']

    @property
    def link(self):
        return self._data['link']

    @property
    def reviews(self):
        return self._data['reviews']

    @property
    def rating(self):
        return self._data['rating']

    @property
    def main_category(self):
        return self._data['main_category']

class Owner:
    def __init__(self, data):
        self._data = data

    @property
    def id(self):
        return self._data['id']

    @property
    def name(self):
        return self._data['name']

    @property
    def link(self):
        return self._data['link']

class Keyword:
    def __init__(self, data):
        self._data = data

    @property
    def keyword(self):
        return self._data['keyword']

    @property
    def count(self):
        return self._data['count']

class AskedBy:

    def __init__(self, data):
        self._data = data

    @property
    def name(self):
        return self._data['name']

    @property
    def link(self):
        return self._data['link']

class AnsweredBy:

    def __init__(self, data):
        self._data = data

    @property
    def name(self):
        return self._data['name']

    @property
    def link(self):
        return self._data['link']

class FeaturedQuestion:

    def __init__(self, data):
        self._data = data

    @property
    def question(self):
        return self._data['question']

    @property
    def answer(self):
        return self._data['answer']

    @property
    def question_date(self):
        return self._data['question_date']

    @property
    def asked_by(self):
        data_asked = self._data.get('asked_by')
        return AskedBy(data_asked) if data_asked else None

    @property
    def answer_ago(self):
        return self._data['answer_ago']

    @property
    def answered_by(self):
        data_answered = self._data.get('answered_by')
        return AnsweredBy(data_answered) if data_answered else None

class Coordinate:

    def __init__(self, data):
        self._data = data

    @property
    def latitude(self):
        return self._data['latitude']

    @property
    def longitude(self):
        return self._data['longitude']

class DetailedAddress:

    def __init__(self, data):
        self._data = data

    @property
    def ward(self):
        return self._data['ward']

    @property
    def street(self):
        return self._data['street_address']

    @property
    def city(self):
        return self._data['city']

    @property
    def postal_code(self):
        return self._data['postal_code']

    @property
    def state(self):
        return self._data['state']

    @property
    def country_code(self):
        return self._data['country_code']

class Option:

    def __init__(self, data):
        self._data = data

    @property
    def name(self):
        return self._data['name']

    @property
    def enabled(self):
        return self._data['enabled']

class About:

    def __init__(self, data):
        self._data = data

    @property
    def id(self):
        return self._data['id']

    @property
    def name(self):
        return self._data['name']

    @property
    def options(self):
        return [Option(c) for c in self._data.get('options', [])]

class Image:

    def __init__(self, data):
        self._data = data

    @property
    def about(self):
        return self._data['about']

    @property
    def link(self):
        return self._data['link']

class MostPopularTime:

    def __init__(self, data):
        self._data = data

    @property
    def hour_of_day(self):
        return self._data['hour_of_day']

    @property
    def average_popularity(self):
        return self._data['average_popularity']

    @property
    def time_label(self):
        return self._data['time_label']

class Hour:

    def __init__(self, data):
        self._data = data

    @property
    def day(self):
        return self._data['day']

    @property
    def times(self):
        return self._data.get("times", [])

class PopularTime:
    def __init__(self, data):
        self.data = data

    @property
    def hour_of_day(self):
        return self.data.get("hour_of_day")

    @property
    def time_label(self):
        return self.data.get("time_label")

    @property
    def popularity_percentage(self):
        return self.data.get("popularity_percentage")

    @property
    def popularity_description(self):
        return self.data.get("popularity_description")

class Menu:
    def __init__(self, data):
        self._data = data

    @property
    def link(self):
        return self._data['link']

    @property
    def source(self):
        return self._data['source']

class Reservation:

    def __init__(self, data):
        self._data = data

    @property
    def link(self):
        return self._data['link']

    @property
    def source(self):
        return self._data['source']

class OrderOnlineLinks:

    def __init__(self, data):
        self._data = data

    @property
    def link(self):
        return self._data['link']

    @property
    def source(self):
        return self._data['source']

class ExperienceDetail:

    def __init__(self, data):
        self._data = data

    @property
    def name(self):
        return self._data['name']

    @property
    def value(self):
        return self._data['value']

class ReviewPhoto:

    def __init__(self, data):
        self._data = data

    @property
    def id(self):
        return self._data['id']

    @property
    def url(self):
        return self._data['url']

    @property
    def caption(self):
        return self._data['caption']

    @property
    def width(self):
        return self._data['width']

    @property
    def height(self):
        return self._data['height']

class FeaturedReviews:

    def __init__(self, data):
        self._data = data

    @property
    def review_id(self):
        return self._data.get('review_id')

    @property
    def review_link(self):
        return self._data.get('review_link')

    @property
    def name(self):
        return self._data['name']

    @property
    def reviewer_id(self):
        return self._data.get('reviewer_id')

    @property
    def reviewer_profile(self):
        return self._data.get('reviewer_profile')

    @property
    def rating(self):
        return self._data.get('rating')

    @property
    def review_text(self):
        return self._data.get('review_text')

    @property
    def published_at(self):
        return self._data.get('published_at')

    @property
    def published_at_date(self):
        return self._data.get('published_at_date')

    @property
    def response_from_owner_text(self):
        return self._data.get('response_from_owner_text')

    @property
    def response_from_owner_ago(self):
        return self._data.get('response_from_owner_ago')

    @property
    def response_from_owner_date(self):
        return self._data.get('response_from_owner_date')

    @property
    def total_number_of_reviews_by_reviewer(self):
        return self._data.get('total_number_of_reviews_by_reviewer')

    @property
    def total_number_of_photos_by_reviewer(self):
        return self._data.get('total_number_of_photos_by_reviewer')

    @property
    def is_local_guide(self):
        return self._data.get('is_local_guide')

    @property
    def review_translated_text(self):
        return self._data.get('review_translated_text')

    @property
    def response_from_owner_translated_text(self):
        return self._data.get('response_from_owner_translated_text')

    @property
    def experience_details(self):
        return [ExperienceDetail(c) for c in self._data.get('experience_details', [])]

    @property
    def review_photos(self):
        return [ReviewPhoto(c) for c in self._data.get('review_photos', [])]

class Business:

    def __init__(self, data):
        self._data = data

    @property
    def place_id(self):
        return self._data['place_id']

    @property
    def name(self):
        return self._data['name']

    @property
    def description(self):
        return self._data['description']

    @property
    def is_spending_on_ads(self):
        return self._data['is_spending_on_ads']

    @property
    def reviews(self):
        return self._data['reviews']

    @property
    def rating(self):
        return self._data['rating']

    @property
    def competitors(self):
        return [Competitor(c) for c in self._data.get('competitors', [])]

    @property
    def website(self):
        return self._data['website']

    @property
    def phone(self):
        return self._data['phone']

    @property
    def can_claim(self):
        return self._data['can_claim']

    @property
    def owner(self):
        data_owner = self._data.get('owner')
        return Owner(data_owner) if data_owner else None

    @property
    def featured_image(self):
        return self._data['featured_image']

    @property
    def main_category(self):
        return self._data['main_category']

    @property
    def categories(self):
        return self._data.get('categories', [])

    @property
    def workday_timing(self):
        return self._data['workday_timing']

    @property
    def is_temporarily_closed(self):
        return self._data['is_temporarily_closed']

    @property
    def is_permanently_closed(self):
        return self._data['is_permanently_closed']

    @property
    def closed_on(self):
        return self._data['closed_on']

    @property
    def address(self):
        return self._data['address']

    @property
    def review_keywords(self):
        return [Keyword(c) for c in self._data.get('review_keywords', [])]

    @property
    def link(self):
        return self._data['link']

    @property
    def status(self):
        return self._data['status']

    @property
    def price_range(self):
        return self._data['price_range']

    # business.reviews_per_rating["1"]
    # business.reviews_per_rating["2"]
    # business.reviews_per_rating["3"]
    # business.reviews_per_rating["4"]
    # business.reviews_per_rating["5"]
    @property
    def reviews_per_rating(self):
        return self._data.get('reviews_per_rating', {})

    @property
    def featured_question(self):
        data_featured = self._data.get('featured_question')
        return FeaturedQuestion(data_featured) if data_featured else None

    @property
    def reviews_link(self):
        return self._data.get('reviews_link')

    @property
    def coordinates(self):
        data_coordinates = self._data.get('coordinates')
        return Coordinate(data_coordinates) if data_coordinates else None

    @property
    def plus_code(self):
        return self._data['plus_code']

    @property
    def detailed_address(self):
        data_address = self._data.get('detailed_address')
        return DetailedAddress(data_address) if data_address else None

    @property
    def time_zone(self) -> str:
        return self._data['time_zone']

    @property
    def cid(self):
        return self._data['cid']

    @property
    def data_id(self) -> str:
        return self._data['data_id']

    @property
    def about(self):
        return [About(a) for a in self._data.get('about', [])]

    @property
    def images(self):
        return [Image(a) for a in self._data.get('images', [])]

    @property
    def hours(self):
        return [Hour(a) for a in self._data.get('hours', [])]

    @property
    def most_popular_times(self):
        return [MostPopularTime(a) for a in self._data.get('most_popular_times', [])]

    @property
    def popular_times(self):
        raw = self._data.get('popular_times', {})
        return {
            day: [PopularTime(slot) for slot in slots]
            for day, slots in raw.items()
        }

    @property
    def menu(self):
        data_menu = self._data.get('menu')
        return Menu(data_menu) if data_menu else None

    @property
    def reservations(self):
        return [Reservation(a) for a in self._data.get('reservations', [])]

    @property
    def order_online_links(self):
        return [OrderOnlineLinks(a) for a in self._data.get('order_online_links', [])]

    @property
    def featured_reviews(self):
        return  [FeaturedReviews(a) for a in self._data.get('featured_reviews', [])]

    # No se como podria ser la estructura, ya que no hay datos.
    @property
    def detailed_reviews(self):
        return self._data.get('detailed_reviews', {})

    @property
    def query(self):
        return self._data.get('query')