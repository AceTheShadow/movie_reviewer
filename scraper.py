from bs4 import BeautifulSoup
import requests
from llm import GeminiLLM
from models import MovieModel


class MovieScraper:
    URL = "https://www.imdb.com/find"
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'}
    SENTENCES_LIMIT = 4

    def __init__(self, movie_name):
        """
        Accepts number of movie_name. Will display films released in last n movie_name.
        :param movie_name:
        """
        self.movie_name = movie_name

    def _build_payload(self):
        return {
            's': 'tt',
            'q': self.movie_name,
        }

    def _get_html_document(self):
        # request for HTML document of given url
        response = requests.get(self.URL, params=(self._build_payload()), headers=self.HEADERS)

        # response will be provided in JSON format
        return response.text

    async def parse_html_document(self):
        soup = BeautifulSoup((self._get_html_document()), 'html5lib')
        elements = soup.find_all(name='li', class_='ipc-metadata-list-summary-item')
        result = []
        for element in elements[:3]:
            title = element.find(class_='ipc-title__text ipc-title__text--reduced').text
            year_container = soup.find("div", class_="hhUutV")
            year = year_container.find('span').text
            rating = element.find(class_='ipc-rating-star--rating')
            question_to_llm = f'Compose review for the {year} film {title}. Limit it to max of {self.SENTENCES_LIMIT} sentences'
            llm = GeminiLLM(question_to_llm)
            movie = MovieModel(
                title=title,
                year=year,
                rating= rating.text if rating else None,
                review=await llm.generate()
            )
            result.append(movie)

        return result
