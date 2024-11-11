import requests
from bs4 import BeautifulSoup
import random
import string
import time
import os
from pathlib import Path
from typing import Dict, List, Optional
import logging
from dataclasses import dataclass
from urllib.parse import urljoin, parse_qs, urlparse


@dataclass
class ScraperConfig:
    """Configuration settings for the scraper"""
    base_save_path: Path
    request_timeout: int = 10
    download_delay: int = 5
    page_delay: int = 2
    chunk_size: int = 8192
    filename_length: int = 6


class CharacterClassifier:
    """Handles character recognition and classification"""

    # Character mappings by series
    CHARACTER_MAPPINGS = {
        "one_piece": {
            "luffy": ["monkey d luffy", "luffy", "strawhat"],
            "zoro": ["roronoa zoro", "zoro"],
            "nami": ["nami"],
            "sanji": ["vinsmoke sanji", "sanji", "black leg"],
            "robin": ["nico robin", "robin"],
            # Add more One Piece characters as needed
        },
        "dota2": {
            "lina": ["lina", "lina inverse"],
            "crystal_maiden": ["crystal maiden", "rylai"],
            "invoker": ["invoker", "kael"],
            "windrunner": ["windranger", "windrunner", "lyralei"],
            # Add more Dota 2 characters as needed
        },
        # Add more series as needed
    }

    @classmethod
    def identify_character(cls, tags: str) -> tuple[Optional[str], Optional[str]]:
        """
        Identify the series and character from image tags
        Returns: (series_name, character_name) or (None, None) if not found
        """
        tags_lower = tags.lower()

        for series, characters in cls.CHARACTER_MAPPINGS.items():
            for char_key, aliases in characters.items():
                if any(alias in tags_lower for alias in aliases):
                    return series, char_key

        return None, None


class HentaiScraper:
    def __init__(self, config: ScraperConfig):
        """Initialize the scraper with configuration settings."""
        self.config = config
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging for the scraper."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def setup(self):
        """Perform initial setup operations."""
        self.logger.info("Starting setup...")
        # Create base directory and series subdirectories
        os.makedirs(self.config.base_save_path, exist_ok=True)
        for series in CharacterClassifier.CHARACTER_MAPPINGS.keys():
            series_path = self.config.base_save_path / series
            os.makedirs(series_path, exist_ok=True)
            # Create character subdirectories
            for char_key in CharacterClassifier.CHARACTER_MAPPINGS[series].keys():
                char_path = series_path / char_key
                os.makedirs(char_path, exist_ok=True)
        self.logger.info("Setup completed successfully")

    def _generate_filename(self, url: str, tags: str) -> str:
        """Generate a filename based on character and random string."""
        series, character = CharacterClassifier.identify_character(tags)
        prefix = f"{character}_" if character else ""
        random_suffix = ''.join(random.choices(
            string.ascii_uppercase + string.digits,
            k=self.config.filename_length
        ))
        return f"{prefix}{random_suffix}.jpg"

    def _get_save_path(self, tags: str) -> Optional[Path]:
        """Determine the save path based on character classification."""
        series, character = CharacterClassifier.identify_character(tags)
        if series and character:
            return self.config.base_save_path / series / character
        return self.config.base_save_path / "unclassified"

    def _download_file(self, url: str, save_path: Path, filename: str) -> bool:
        """Download a single file from the given URL."""
        try:
            full_save_path = save_path / filename
            with requests.get(url, stream=True, timeout=self.config.request_timeout) as response:
                response.raise_for_status()
                save_path.mkdir(parents=True, exist_ok=True)

                with open(full_save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=self.config.chunk_size):
                        f.write(chunk)

            self.logger.info(f"Successfully downloaded file to {full_save_path}")
            return True

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to download from {url}: {str(e)}")
            return False

    def _extract_file_urls(self, page_url: str, domain_filter: str, path_filter: str) -> List[tuple[str, str]]:
        """Extract file URLs and their associated tags from a given page."""
        try:
            response = requests.get(page_url, timeout=self.config.request_timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')

            file_info = []
            for img in soup.find_all('img', src=True):
                if domain_filter in img['src'] and path_filter in img['src']:
                    # Extract tags from the image or its parent elements
                    tags = img.get('title', '') or img.get('alt', '')
                    if tags:
                        file_info.append((img['src'], tags))

            return file_info

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to extract from {page_url}: {str(e)}")
            return []

    def download_batch(self, urls_dict: Dict[str, str], max_pages: int = 380):
        """Download files from multiple URLs with character classification."""
        page_increment = 48

        for search_term, base_url in urls_dict.items():
            self.logger.info(f"Starting downloads for search term: {search_term}")

            for page_num in range(max_pages):
                page_offset = page_num * page_increment
                current_url = f"{base_url}&pid={page_offset}" if page_num > 0 else base_url

                self.logger.info(f"Processing page {page_num + 1}/{max_pages}")
                self.logger.debug(f"URL: {current_url}")

                # Extract and process file URLs with tags
                for file_url, tags in self._extract_file_urls(current_url, "gelbooru.com", "sample"):
                    save_path = self._get_save_path(tags)
                    if save_path:
                        filename = self._generate_filename(file_url, tags)
                        if self._download_file(file_url, save_path, filename):
                            time.sleep(self.config.download_delay)

                time.sleep(self.config.page_delay)

def main():
    config = ScraperConfig(
        base_save_path=Path("/Volumes/ExternalHD/workspace/python/Monke D. Luffy/")
    )

    scraper = HentaiScraper(config)
    scraper.setup()

    urls = {'uta': 'https://gelbooru.com/index.php?page=post&s=list&tags=uta_%28one_piece%29',
                'rebecca': 'https://gelbooru.com/index.php?page=post&s=list&tags=rebecca_%28one_piece%29+',
                'carrot': "https://gelbooru.com/index.php?page=post&s=list&tags=carrot_%28one_piece%29+",
                'bonney': "https://gelbooru.com/index.php?page=post&s=list&tags=jewelry_bonney+",
                'baby_5': "https://gelbooru.com/index.php?page=post&s=list&tags=baby_5+",
                'robin': "https://gelbooru.com/index.php?page=post&s=list&tags=nico_robin+",
                'nami': "https://gelbooru.com/index.php?page=post&s=list&tags=nami_%28one_piece%29",
                'nami': "https://gelbooru.com/index.php?page=post&s=list&tags=nami_(one_piece)+",
                'boa_hancock': "https://gelbooru.com/index.php?page=post&s=list&tags=boa_hancock+",
                'robin': "https://gelbooru.com/index.php?page=post&s=list&tags=nico_robin_(cosplay)",
                'robin': "https://gelbooru.com/index.php?page=post&s=list&tags=nico_robin_(alabasta)",
                'vivi': "https://gelbooru.com/index.php?page=post&s=list&tags=nefertari_vivi+",
                'vinsmoke_reiju': "https://gelbooru.com/index.php?page=post&s=list&tags=vinsmoke_reiju+",
                'charlotte_linlin': "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_linlin+",
                'kuina': "https://gelbooru.com/index.php?page=post&s=view&id=10840090&tags=kuina+",
                'kuina': "https://gelbooru.com/index.php?page=post&s=view&id=10840088&tags=kuina+",
                'kuina': "https://gelbooru.com/index.php?page=post&s=view&id=10840087&tags=kuina+",
                'charlotte_smoothie': "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_smoothie+",
                'shirahoshi': "https://gelbooru.com/index.php?page=post&s=list&tags=shirahoshi",
                'kouzuki_hiyori': "https://gelbooru.com/index.php?page=post&s=list&tags=kouzuki_hiyori",
                'catarina_devon': "https://gelbooru.com/index.php?page=post&s=list&tags=catarina_devon",
                'perona': "https://gelbooru.com/index.php?page=post&s=list&tags=perona",
                'charlotte_flampe': "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_flampe",
                'kouzuki_toki': "https://gelbooru.com/index.php?page=post&s=list&tags=kouzuki_toki",
                'alvida': "https://gelbooru.com/index.php?page=post&s=list&tags=alvida_(one_piece)",
                'kikunojo': "https://gelbooru.com/index.php?page=post&s=list&tags=kikunojo_(one_piece)",
                'vegapunk_lilith': "https://gelbooru.com/index.php?page=post&s=list&tags=vegapunk_lilith",
                'kaya': "https://gelbooru.com/index.php?page=post&s=list&tags=kaya_(one_piece)",
                'lily': "https://gelbooru.com/index.php?page=post&s=view&id=4939575&tags=lily_(one_piece)",
                'monet': "https://gelbooru.com/index.php?page=post&s=list&tags=monet_(one_piece)",
                'wanda': "https://gelbooru.com/index.php?page=post&s=list&tags=wanda_(one_piece)",
                'rebecca': "https://gelbooru.com/index.php?page=post&s=list&tags=rebecca_(one_piece)",
                'nico_olvia': "https://gelbooru.com/index.php?page=post&s=list&tags=nico_olvia",
                'nojiko': "https://gelbooru.com/index.php?page=post&s=list&tags=nojiko",
                'charlotte_pudding': "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_pudding",
                'charlotte_prim': "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_prim",
                'charlotte_poire': "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_poire",
                'charlotte_anana': "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_anana",
                'charlotte_amande': "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_amande",
                'charlotte_meukle': "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_meukle",
                'carrot': "https://gelbooru.com/index.php?page=post&s=list&tags=carrot_(one_piece)",
                'bellett': "https://gelbooru.com/index.php?page=post&s=list&tags=bellett",
                'bellemere': "https://gelbooru.com/index.php?page=post&s=list&tags=bellemere",
                'baby_5': "https://gelbooru.com/index.php?page=post&s=list&tags=baby_5",
                'vegapunk_atlas': "https://gelbooru.com/index.php?page=post&s=list&tags=vegapunk_atlas",
                'vegapunk_york': "https://gelbooru.com/index.php?page=post&s=list&tags=vegapunk_york",
                'gion': "https://gelbooru.com/index.php?page=post&s=list&tags=gion_(one_piece)",
                'stussy': "https://gelbooru.com/index.php?page=post&s=list&tags=stussy_(one_piece)",
                'uta': "https://gelbooru.com/index.php?page=post&s=list&tags=uta_(one_piece)",
                'isuka': "https://gelbooru.com/index.php?page=post&s=view&id=8003494&tags=isuka_(one_piece)",
                'isuka': "https://gelbooru.com/index.php?page=post&s=view&id=7661332&tags=isuka_(one_piece)",
                'tashigi': "https://gelbooru.com/index.php?page=post&s=list&tags=tashigi",
                'hina': "https://gelbooru.com/index.php?page=post&s=list&tags=hina_(one_piece)",
                'kujaku': "https://gelbooru.com/index.php?page=post&s=list&tags=kujaku_(one_piece)",
                'hibari': "https://gelbooru.com/index.php?page=post&s=list&tags=hibari_(one_piece)+",
                'doll': "https://gelbooru.com/index.php?page=post&s=list&tags=doll_(one_piece)",
                'one_piece': "https://gelbooru.com/index.php?page=post&s=list&tags=one_piece",
                'marci': "https://gelbooru.com/index.php?page=post&s=list&tags=marci_(dota)",
                'dark_willow': "https://gelbooru.com/index.php?page=post&s=list&tags=dark_willow",
                'mirana': "https://gelbooru.com/index.php?page=post&s=list&tags=mirana_(dota)+",
                'crystal_maiden': "https://gelbooru.com/index.php?page=post&s=list&tags=crystal_maiden+",
                'dota_2': "https://gelbooru.com/index.php?page=post&s=list&tags=dota_2+",
                'dota_2': "https://gelbooru.com/index.php?page=post&s=list&tags=dota_(series)+",
                'broodmother': "https://gelbooru.com/index.php?page=post&s=list&tags=broodmother_(dota)+",
                'dawnbreaker': "https://gelbooru.com/index.php?page=post&s=list&tags=dawnbreaker_(dota)+",
                'dawnbreaker': "https://gelbooru.com/index.php?page=post&s=list&tags=dawnbreaker_(dota_2)+",
                'death_prophet': "https://gelbooru.com/index.php?page=post&s=list&tags=death_prophet_(dota)+",
                'enchantress': "https://gelbooru.com/index.php?page=post&s=list&tags=enchantress_(dota)+",
                'enchantress': "https://gelbooru.com/index.php?page=post&s=list&tags=enchantress_(dota_2)+",
                'legion_commander': "https://gelbooru.com/index.php?page=post&s=list&tags=legion_commander_(dota)+",
                'luna': "https://gelbooru.com/index.php?page=post&s=list&tags=luna_(dota)",
                'dota_2_girls': "https://gelbooru.com/index.php?page=post&s=view&id=2447831",
                'marci': "https://gelbooru.com/index.php?page=post&s=list&tags=marci_(dota)+",
                'naga_siren': "https://gelbooru.com/index.php?page=post&s=list&tags=naga_siren_(dota)+",
                'phantom_assassin': "https://gelbooru.com/index.php?page=post&s=list&tags=phantom_assassin_(dota)+",
                'queen_of_pain': "https://gelbooru.com/index.php?page=post&s=list&tags=queen_of_pain_(dota)+",
                'snapfire': "https://gelbooru.com/index.php?page=post&s=list&tags=snapfire",
                'spectre': "https://gelbooru.com/index.php?page=post&s=list&tags=spectre_(dota)",
                'templar_assassin': "https://gelbooru.com/index.php?page=post&s=list&tags=templar_assassin_(dota)+",
                'vengeful_spirit': "https://gelbooru.com/index.php?page=post&s=list&tags=vengeful_spirit_(dota_2)+",
                'windranger': "https://gelbooru.com/index.php?page=post&s=list&tags=windranger_(dota)+",
                'winter_wyrven': "https://gelbooru.com/index.php?page=post&s=list&tags=winter_wyrven+",
            }

    scraper.download_batch(urls)


if __name__ == "__main__":
    main()

#
# # gelbooru.com
#
# class HentaiScraper():
#     def __init__(self):
#         # self._nami_url = "https://gelbooru.com/index.php?page=post&s=list&tags=nami_%28one_piece%29"
#         # self._robin_url = "https://gelbooru.com/index.php?page=post&s=list&tags=nico_robin+"
#         # self._baby5_url = "https://gelbooru.com/index.php?page=post&s=list&tags=baby_5+"
#         # 'nami': "https://gelbooru.com/index.php?page=post&s=list&tags=nami_%28one_piece%29",
#         # 'robin': "https://gelbooru.com/index.php?page=post&s=list&tags=nico_robin+",
#         # 'baby_5': "https://gelbooru.com/index.php?page=post&s=list&tags=baby_5+",
#         # 'bonney': "https://gelbooru.com/index.php?page=post&s=list&tags=jewelry_bonney+",
#         # 'carrot': "https://gelbooru.com/index.php?page=post&s=list&tags=carrot_%28one_piece%29+"
#         self._one_piece_urls = {'uta': 'https://gelbooru.com/index.php?page=post&s=list&tags=uta_%28one_piece%29',
#                                 'rebecca': 'https://gelbooru.com/index.php?page=post&s=list&tags=rebecca_%28one_piece%29+',
#                                 'carrot': "https://gelbooru.com/index.php?page=post&s=list&tags=carrot_%28one_piece%29+",
#                                 'bonney': "https://gelbooru.com/index.php?page=post&s=list&tags=jewelry_bonney+",
#                                 'baby_5': "https://gelbooru.com/index.php?page=post&s=list&tags=baby_5+",
#                                 'robin': "https://gelbooru.com/index.php?page=post&s=list&tags=nico_robin+",
#                                 'nami': "https://gelbooru.com/index.php?page=post&s=list&tags=nami_%28one_piece%29",
#
#                                 }
#
#     def setup(self):
#         print("Running setup...")
#
#         print("Config set...")
#
#         print("Setup finished...")
#
#     def download_one_piece(self):
#         urls = self._one_piece_urls
#
#         count = True
#
#         number = 0
#
#         for k, v in urls.items():
#             while number <= 15944:
#                 if count == True:
#                     print("URL: " + v)
#                     print("KEY!!!! ", k)
#
#                     try:
#                         page = requests.get(v)
#                         soup = BeautifulSoup(page.content, 'lxml')
#
#                         for a in soup.find_all('a', href=True):
#                             if "test.com" in a['href'] and "&id=" in a['href']:
#                                 print("Found the URL:", a['href'])
#
#                                 page = requests.get(a['href'])
#                                 soup = BeautifulSoup(page.content, 'lxml')
#
#                                 for img in soup.find_all('img', src=True):
#                                     if "gelbooru.com" in img['src'] and "sample" in img['src']:
#
#                                             filename = r"/Volumes/ExternalHD/workspace/python/Monke D. Luffy/hentai/one_piece/" + k + r"/"
#                                             # filename = r"/home/timmy/hentai/one_piece/" + k + r"/"
#
#                                             filename += ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6)) + '.jpg'
#
#                                             r = requests.get(img['src'], stream=True)
#
#                                             if r.status_code == 200:
#                                                 r.raw.decode_content = True
#                                                 with open(filename, 'wb') as f:
#                                                     shutil.copyfileobj(r.raw, f)
#
#                                                 print("Image sucessfully Download:", filename)
#
#                                             else:
#                                                 print("Image Couldn\'t be retreived.")
#                     except requests.exceptions.ReadTimeout:
#                         print("Read Timeout occurred.")
#                     finally:
#                         count = False
#                         number += 42
#
#                         time.sleep(5)
#                 elif count == False:
#                     try:
#                         print("COUNT: " + str(count))
#                         print("URL: " + v + "&pid=" + str(number))
#                         print("KEY!!!! ", k)
#
#                         print("Starting count not 0...")
#
#                         link = v + "&pid=" + str(number)
#
#                         page = requests.get(link)
#                         soup = BeautifulSoup(page.content, 'lxml')
#
#                         for a in soup.find_all('a', href=True):
#                             if "gelbooru.com" in a['href'] and "&id=" in a['href']:
#                                 print("Found the URL:", a['href'])
#
#                                 page = requests.get(a['href'])
#                                 soup = BeautifulSoup(page.content, 'lxml')
#
#                                 for img in soup.find_all('img', src=True):
#                                     if "gelbooru.com" in img['src'] and "sample" in img['src']:
#                                         filename = r"/Volumes/ExternalHD/workspace/python/Monke D. Luffy/hentai/one_piece/" + k + r"/"
#                                         # filename = r"/home/timmy/hentai/one_piece/" + k + r"/"
#
#                                         filename += ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6)) + '.jpg'
#
#                                         r = requests.get(img['src'], stream=True)
#
#                                         if r.status_code == 200:
#                                             r.raw.decode_content = True
#                                             with open(filename, 'wb') as f:
#                                                 shutil.copyfileobj(r.raw, f)
#
#                                             print("Image sucessfully Download:", filename)
#
#                                         else:
#                                             print("Image Couldn\'t be retreived.")
#
#                     except requests.exceptions.ReadTimeout:
#                         print("Read Timeout occurred.")
#                     finally:
#                         number += 42
#
#                         time.sleep(5)
#         number = 0
