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
            "luffy": ["monkey d luffy", "monkey_d_luffy", "luffy", "strawhat"],
            "zoro": ["roronoa zoro", "roronoa_zoro", "zoro"],
            "nami": ["nami", "nami_(one_piece)"],
            "sanji": ["vinsmoke sanji", "vinsmoke_sanji", "sanji", "black leg"],
            "robin": ["nico robin", "nico_robin", "robin", "robin_(alabasta)", "robin_(cosplay)"],
            "uta": ["uta", "uta_(one_piece)"],
            "rebecca": ["rebecca", "rebecca_(one_piece)"],
            "carrot": ["carrot", "carrot_(one_piece)"],
            "bonney": ["jewelry bonney", "jewelry_bonney", "bonney"],
            "baby_5": ["baby 5", "baby_5", "baby five", "baby_five"],
            "boa_hancock": ["boa hancock", "boa_hancock", "hancock"],
            "vivi": ["nefertari vivi", "nefertari_vivi", "vivi"],
            "vinsmoke_reiju": ["vinsmoke reiju", "vinsmoke_reiju", "reiju"],
            "charlotte_linlin": ["big mom", "big_mom", "charlotte_linlin", "charlotte linlin", "linlin"],
            "kuina": ["shimotsuki kuina", "shimotsuki_kuina", "kuina"],
            "charlotte_smoothie": ["charlotte_smoothie", "charlotte smoothie", "smoothie"],
            "shirahoshi": ["shirahoshi", "princess shirahoshi", "princess_shirahoshi"],
            "kouzuki_hiyori": ["hiyori", "kouzuki hiyori", "kouzuki_hiyori"],
            "catarina_devon": ["devon", "catarina devon", "catarina_devon"],
            "perona": ["perona", "'ghost princess' perona", "ghost princess perona", "'ghost_princess'_perona",
                       "ghost_princess_perona"],
            "charlotte_flampe": ["charlotte_flampe", "charlotte flampe", "flampe"],
            "kouzuki_toki": ["kouzuki toki", "kouzuki_toki", "toki"],
            "alvida": ["alvida", "alvida_(one_piece)"],
            "kikunojo": ["kikunojo", "kikunojo_(one_piece)", "kiku"],
            "vegapunk_lilith": ["vegapunk lilith", "vegapunk_lilith", "lilith"],
            "kaya": ["kaya", "kaya_(one_piece)"],
            "monet": ["monet", "monet_(one_piece)"],
            "wanda": ["wanda", "wanda_(one_piece)"],
            "nico_olvia": ["nico olvia", "nico_olvia", "olvia"],
            "nojiko": ["nojiko"],
            "charlotte_pudding": ["charlotte pudding", "charlotte_pudding", "pudding"],
            "vegapunk_atlas": ["vegapunk atlas", "vegapunk_atlas", "atlas"],
            "vegapunk_york": ["vegapunk york", "vegapunk_york", "york"],
            "stussy": ["stussy", "stussy_(one_piece)"],
            "tashigi": ["tashigi"],
            "hina": ["hina", "hina_(one_piece)"],
            "isuka": ["isuka", "isuka_(one_piece)"]
        },

        "dota2": {
            "lina": ["lina", "lina inverse"],
            "crystal_maiden": ["crystal maiden", "crystal_maiden", "rylai"],
            "invoker": ["invoker", "kael"],
            "windrunner": ["windranger", "windrunner", "lyralei", "windranger_(dota)"],
            "marci": ["marci", "marci_(dota)"],
            "dark_willow": ["dark willow", "dark_willow"],
            "mirana": ["mirana", "mirana_(dota)"],
            "broodmother": ["broodmother", "broodmother_(dota)"],
            "dawnbreaker": ["dawnbreaker", "dawnbreaker_(dota)", "dawnbreaker_(dota_2)"],
            "death_prophet": ["death prophet", "death_prophet_(dota)"],
            "enchantress": ["enchantress", "enchantress_(dota)", "enchantress_(dota_2)"],
            "legion_commander": ["legion commander", "legion_commander_(dota)"],
            "luna": ["luna", "luna_(dota)"],
            "naga_siren": ["naga siren", "naga_siren_(dota)"],
            "phantom_assassin": ["phantom assassin", "phantom_assassin_(dota)"],
            "queen_of_pain": ["queen of pain", "queen_of_pain_(dota)"],
            "snapfire": ["snapfire"],
            "spectre": ["spectre", "spectre_(dota)"],
            "templar_assassin": ["templar assassin", "templar_assassin_(dota)"],
            "vengeful_spirit": ["vengeful spirit", "vengeful_spirit_(dota_2)"]
        },

        "naruto": {
            "tsunade": ["tsunade", "lady tsunade", "princess tsunade"],
            "sakura": ["sakura haruno", "sakura_haruno"],
            "hinata": ["hinata hyuga", "hinata_hyuga"],
            "tenten": ["tenten"],
            "temari": ["temari"],
            "kushina": ["kushina uzumaki", "kushina_uzumaki"],
            "sarada": ["sarada uchiha", "sarada_uchiha"],
            "himawari": ["himawari uzumaki", "himawari_uzumaki"],
            "ino": ["ino yamanaka", "ino_yamanaka"],
            "kurenai": ["kurenai yuhi", "kurenai_yuhi"],
            "anko": ["anko mitarashi", "anko_mitarashi"],
            "shizune": ["shizune"],
            "karin": ["karin uzumaki", "karin_uzumaki"],
            "konan": ["konan"],
            "mei": ["mei terumi", "mei_terumi"],
            "samui": ["samui"],
            "karui": ["karui"],
            "mabui": ["mabui"],
            "yugao": ["yugao uzuki", "yugao_uzuki"],
            "tsume": ["tsume inuzuka", "tsume_inuzuka"],
            "hana": ["hana inuzuka", "hana_inuzuka"],
            "natsu": ["natsu hyuga", "natsu_hyuga"],
            "yakumo": ["yakumo kurama", "yakumo_kurama"],
            "tsunami": ["tsunami"],
            "ayame": ["ayame"],
            "yugito": ["yugito nii", "yugito_nii"],
            "fuu": ["fuu"],
            "hokuto": ["hokuto"],
            "hanabi": ["hanabi hyuga", "hanabi_hyuga"],
            "moegi": ["moegi"],
            "sumire": ["sumire kakei", "sumire_kakei"],
            "chocho": ["chocho akimichi", "chocho_akimichi"],
            "mirai": ["mirai sarutobi", "mirai_sarutobi"],
            "wasabi": ["wasabi izuno", "wasabi_izuno"],
            "namida": ["namida suzumeno", "namida_suzumeno"]
        },

        "fairy_tail": {
            "lucy": ["lucy heartfilia", "lucy_heartfilia"],
            "erza": ["erza scarlet", "erza_scarlet", "titania"],
            "wendy": ["wendy marvell", "wendy_marvell"],
            "juvia": ["juvia lockser", "juvia_lockser"],
            "levy": ["levy mcgarden", "levy_mcgarden"],
            "mirajane": ["mirajane strauss", "mirajane_strauss"],
            "lisanna": ["lisanna strauss", "lisanna_strauss"],
            "cana": ["cana alberona", "cana_alberona"],
            "evergreen": ["evergreen"],
            "bisca": ["bisca connell", "bisca_connell"],
            "laki": ["laki olietta", "laki_olietta"],
            "kinana": ["kinana"],
            "mavis": ["mavis vermillion", "mavis_vermillion"],
            "meredy": ["meredy"],
            "ultear": ["ultear milkovich", "ultear_milkovich"],
            "yukino": ["yukino agria", "yukino_agria"],
            "minerva": ["minerva orlando", "minerva_orlando"],
            "kagura": ["kagura mikazuchi", "kagura_mikazuchi"],
            "milliana": ["milliana"],
            "flare": ["flare corona", "flare_corona"],
            "jenny": ["jenny realight", "jenny_realight"],
            "sherry": ["sherry blendy", "sherry_blendy"],
            "chelia": ["chelia blendy", "chelia_blendy"],
            "sorano": ["sorano agria", "sorano_agria", "angel"],
            "brandish": ["brandish μ", "brandish mu"],
            "dimaria": ["dimaria yesta", "dimaria_yesta"],
            "irene": ["irene belserion", "irene_belserion"],
            "hisui": ["hisui e fiore", "hisui_e_fiore"]
        },

        "dragon_ball": {
            "bulma": ["bulma briefs", "bulma_briefs"],
            "chi_chi": ["chi chi", "chi_chi"],
            "videl": ["videl"],
            "pan": ["pan"],
            "android_18": ["android 18", "c-18", "lazuli"],
            "bulla": ["bulla", "bra"],
            "launch": ["launch", "lunch"],
            "marron": ["marron"],
            "mai": ["mai"],
            "ranfan": ["ranfan"],
            "vados": ["vados"],
            "caulifla": ["caulifla"],
            "kale": ["kale"],
            "ribrianne": ["ribrianne", "brianne de chateau"],
            "oceanus": ["oceanus shenron", "princess oto"],
            "gine": ["gine"],
            "fasha": ["fasha", "selypa"],
            "zangya": ["zangya"],
            "towa": ["towa"],
            "supreme_kai_of_time": ["supreme kai of time", "chronoa"],
            "arale": ["arale norimaki", "arale_norimaki"]
        },

        "attack_on_titan": {
            "mikasa": ["mikasa ackerman", "mikasa_ackerman"],
            "annie": ["annie leonhart", "annie_leonhart"],
            "historia": ["historia reiss", "historia_reiss", "christa"],
            "sasha": ["sasha braus", "sasha_braus"],
            "hange": ["hange zoe", "hanji"],
            "ymir": ["ymir", "freckled ymir"],
            "pieck": ["pieck finger", "pieck_finger"],
            "gabi": ["gabi braun", "gabi_braun"],
            "frieda": ["frieda reiss", "frieda_reiss"],
            "carla": ["carla yeager", "carla_yeager"],
            "dina": ["dina fritz", "dina_fritz"],
            "petra": ["petra ral", "petra_ral"],
            "rico": ["rico brzenska", "rico_brzenska"],
            "yelena": ["yelena"],
            "kiyomi": ["kiyomi azumabito", "kiyomi_azumabito"],
            "louise": ["louise"],
            "nifa": ["nifa"],
            "lynne": ["lynne"],
            "ilse": ["ilse langnar", "ilse_langnar"],
            "nanaba": ["nanaba"]
        },

        "demon_slayer": {
            "nezuko": ["nezuko kamado", "nezuko_kamado"],
            "kanao": ["kanao tsuyuri", "kanao_tsuyuri"],
            "shinobu": ["shinobu kocho", "shinobu_kocho"],
            "kanae": ["kanae kocho", "kanae_kocho"],
            "mitsuri": ["mitsuri kanroji", "mitsuri_kanroji"],
            "daki": ["daki", "ume"],
            "tamayo": ["tamayo"],
            "makio": ["makio"],
            "suma": ["suma"],
            "hinatsuru": ["hinatsuru"],
            "aoi": ["aoi kanzaki", "aoi_kanzaki"],
            "kiyo": ["kiyo terauchi", "kiyo_terauchi"],
            "sumi": ["sumi nakahara", "sumi_nakahara"],
            "naho": ["naho takada", "naho_takada"],
            "goto": ["goto", "goto_san"],
            "amane": ["amane"],
            "mukago": ["mukago"],
            "ruka": ["ruka"],
            "hinaki": ["hinaki ubuyashiki", "hinaki_ubuyashiki"],
            "nichika": ["nichika ubuyashiki", "nichika_ubuyashiki"],
            "kuina": ["kuina ubuyashiki", "kuina_ubuyashiki"]
        },

        "jujutsu_kaisen": {
            "nobara": ["nobara kugisaki", "nobara_kugisaki"],
            "maki": ["maki zenin", "maki_zenin"],
            "mei_mei": ["mei mei", "mei_mei"],
            "miwa": ["kasumi miwa", "kasumi_miwa"],
            "momo": ["momo nishimiya", "momo_nishimiya"],
            "mai": ["mai zenin", "mai_zenin"],
            "yuki": ["yuki tsukumo", "yuki_tsukumo"],
            "rika": ["rika orimoto", "rika_orimoto"],
            "utahime": ["utahime iori", "utahime_iori"],
            "tsumiki": ["tsumiki fushiguro", "tsumiki_fushiguro"],
            "manami": ["manami suda", "manami_suda"],
            "saori": ["saori rokujo", "saori_rokujo"],
            "shoko": ["shoko ieiri", "shoko_ieiri"],
            "mimiko": ["mimiko hasaba", "mimiko_hasaba"],
            "nanako": ["nanako hasaba", "nanako_hasaba"]
        },

        "cowboy_bebop": {
            "faye": ["faye valentine", "faye_valentine"],
            "ed": ["edward wong", "radical ed", "edward"],
            "julia": ["julia"],
            "meifa": ["meifa puzi", "meifa_puzi"],
            "judy": ["judy"],
            "annie": ["anastasia"],
            "alisa": ["alisa"],
            "vip": ["v.t.", "victoria terraforming"],
            "stella": ["stella bonnaro", "stella_bonnaro"],
            "coffee": ["coffee"],
            "katrina": ["katrina solensan", "katrina_solensan"]
        },

        "spy_x_family": {
            "yor": ["yor forger", "yor_forger", "thorn princess"],
            "anya": ["anya forger", "anya_forger"],
            "sylvia": ["sylvia sherwood", "sylvia_sherwood"],
            "fiona": ["fiona frost", "fiona_frost"],
            "becky": ["becky blackbell", "becky_blackbell"],
            "sharon": ["sharon", "shop_keeper"],
            "melinda": ["melinda desmond", "melinda_desmond"],
            "camilla": ["camilla", "shopkeeper_sister"],
            "karen": ["karen gloomy", "karen_gloomy"],
            "dominic": ["dominic", "handler"],
            "martha": ["martha", "landlady"]
        },

        "one_punch_man": {
            "fubuki": ["fubuki", "blizzard", "hellish blizzard"],
            "tatsumaki": ["tatsumaki", "tornado", "tornado of terror"],
            "psykos": ["psykos"],
            "suiko": ["suiko"],
            "lin_lin": ["lin lin"],
            "lily": ["lily of the three section staff", "lily"],
            "do_s": ["do-s", "monster princess"],
            "mosquito_girl": ["mosquito girl"],
            "mizuki": ["captain mizuki", "mizuki"],
            "shadow_ring": ["shadow ring"],
            "zenko": ["zenko", "metal bat's sister"],
            "madame_shibabawa": ["madame shibabawa"],
            "goddess_glasses": ["goddess glasses"],
            "swim": ["swim"],
            "pai": ["pai"]
        },

        "league_of_legends": {
            "ahri": ["ahri"],
            "lux": ["lux", "luxanna crownguard"],
            "jinx": ["jinx"],
            "vi": ["vi"],
            "caitlyn": ["caitlyn"],
            "leona": ["leona"],
            "diana": ["diana"],
            "ashe": ["ashe"],
            "katarina": ["katarina"],
            "miss_fortune": ["miss fortune", "sarah fortune"],
            "akali": ["akali"],
            "anivia": ["anivia"],
            "annie": ["annie"],
            "bel_veth": ["bel'veth", "belveth"],
            "briar": ["briar"],
            "cassiopeia": ["cassiopeia"],
            "elise": ["elise"],
            "evelynn": ["evelynn"],
            "fiora": ["fiora"],
            "gwen": ["gwen"],
            "illaoi": ["illaoi"],
            "irelia": ["irelia"],
            "janna": ["janna"],
            "kai_sa": ["kai'sa", "kaisa"],
            "kalista": ["kalista"],
            "karma": ["karma"],
            "kindred": ["kindred"],
            "leblanc": ["leblanc"],
            "lillia": ["lillia"],
            "lissandra": ["lissandra"],
            "morgana": ["morgana"],
            "nami": ["nami"],
            "neeko": ["neeko"],
            "nidalee": ["nidalee"],
            "nilah": ["nilah"],
            "orianna": ["orianna"],
            "poppy": ["poppy"],
            "qiyana": ["qiyana"],
            "rell": ["rell"],
            "riven": ["riven"],
            "samira": ["samira"],
            "senna": ["senna"],
            "seraphine": ["seraphine"],
            "sejuani": ["sejuani"],
            "senna": ["senna"],
            "shyvana": ["shyvana"],
            "sivir": ["sivir"],
            "sona": ["sona"],
            "soraka": ["soraka"],
            "syndra": ["syndra"],
            "taliyah": ["taliyah"],
            "tristana": ["tristana"],
            "vayne": ["vayne"],
            "vex": ["vex"],
            "xayah": ["xayah"],
            "yuumi": ["yuumi"],
            "zeri": ["zeri"],
            "zoe": ["zoe"],
            "zyra": ["zyra"]
        },

        "hunter_x_hunter": {
            "biscuit": ["biscuit krueger", "bisky"],
            "palm": ["palm siberia"],
            "machi": ["machi"],
            "shizuku": ["shizuku"],
            "canary": ["canary"],
            "neferpitou": ["neferpitou", "pitou"],
            "komugi": ["komugi"],
            "pakunoda": ["pakunoda"],
            "melody": ["melody", "senritsu"],
            "zazan": ["zazan"],
            "eliza": ["eliza"],
            "amane": ["amane"],
            "tsubone": ["tsubone"],
            "kalluto": ["kalluto zoldyck", "kalluto_zoldyck"],
            "kikyo": ["kikyo zoldyck", "kikyo_zoldyck"],
            "alluka": ["alluka zoldyck", "alluka_zoldyck"],
            "cheadle": ["cheadle yorkshire", "cheadle_yorkshire"],
            "menchi": ["menchi"],
            "ponzu": ["ponzu"]
        },

        "fullmetal_alchemist": {
            "winry": ["winry rockbell", "winry_rockbell"],
            "riza": ["riza hawkeye", "riza_hawkeye"],
            "olivier": ["olivier armstrong", "olivier_armstrong"],
            "izumi": ["izumi curtis", "izumi_curtis"],
            "mei": ["mei chang", "mei_chang"],
            "maria": ["maria ross", "maria_ross"],
            "gracia": ["gracia hughes", "gracia_hughes"],
            "elicia": ["elicia hughes", "elicia_hughes"],
            "lan_fan": ["lan fan", "lan_fan"],
            "paninya": ["paninya"],
            "sheska": ["sheska", "sciezka"],
            "rose": ["rose thomas", "rose_thomas"],
            "catherine": ["catherine elle armstrong", "catherine_armstrong"],
            "martel": ["martel"],
            "trisha": ["trisha elric", "trisha_elric"],
            "pinako": ["pinako rockbell", "pinako_rockbell"],
            "lust": ["lust"],
            "dante": ["dante"],
            "clara": ["clara", "psiren"]
        },

        "my_hero_academia": {
            "uraraka": ["ochaco uraraka", "ochaco_uraraka"],
            "asui": ["tsuyu asui", "tsuyu_asui", "froppy"],
            "yaoyorozu": ["momo yaoyorozu", "momo_yaoyorozu"],
            "jirou": ["kyoka jirou", "kyoka_jirou"],
            "hagakure": ["toru hagakure", "toru_hagakure"],
            "ashido": ["mina ashido", "mina_ashido", "pinky"],
            "mount_lady": ["mount lady", "yu takeyama"],
            "midnight": ["midnight", "nemuri kayama"],
            "mirko": ["mirko", "rumi usagiyama"],
            "ryuku": ["ryuku", "ryuko tatsuma"],
            "nejire": ["nejire hado", "nejire_hado"],
            "mandalay": ["mandalay", "shino sosaki"],
            "pixie_bob": ["pixie-bob", "ryuko tsuchikawa"],
            "ragdoll": ["ragdoll", "tomoko shiretoko"],
            "kendo": ["itsuka kendo", "itsuka_kendo"],
            "tsunotori": ["pony tsunotori", "pony_tsunotori"],
            "komori": ["kinoko komori", "kinoko_komori"],
            "kodai": ["yui kodai", "yui_kodai"],
            "yanagi": ["reiko yanagi", "reiko_yanagi"],
            "tokage": ["setsuna tokage", "setsuna_tokage"],
            "melissa": ["melissa shield", "melissa_shield"],
            "inko": ["inko midoriya", "inko_midoriya"],
            "fuyumi": ["fuyumi todoroki", "fuyumi_todoroki"],
            "eri": ["eri"],
            "nana": ["nana shimura", "nana_shimura"],
            "toga": ["himiko toga", "himiko_toga"]
        },

        "jojos_bizarre_adventure": {
            "jolyne": ["jolyne cujoh", "jolyne_cujoh"],
            "lisa_lisa": ["lisa lisa", "lisa_lisa"],
            "erina": ["erina pendleton", "erina_pendleton"],
            "trish": ["trish una", "trish_una"],
            "suzi_q": ["suzi q", "suzi_q"],
            "holly": ["holly kujo", "holly_kujo", "seiko"],
            "yukako": ["yukako yamagishi", "yukako_yamagishi"],
            "reimi": ["reimi sugimoto", "reimi_sugimoto"],
            "hot_pants": ["hot pants", "hot_pants"],
            "lucy": ["lucy steel", "lucy_steel"],
            "yasuho": ["yasuho hirose", "yasuho_hirose"],
            "hermes": ["hermes costello", "hermes_costello"],
            "foo_fighters": ["foo fighters", "f.f.", "ff"],
            "ermes": ["ermes costello", "ermes_costello"],
            "gwess": ["gwess"],
            "mariah": ["mariah"],
            "midler": ["midler", "rose"],
            "anne": ["anne"],
            "tomoko": ["tomoko higashikata", "tomoko_higashikata"]
        },

        "pokemon": {
            "misty": ["misty", "kasumi"],
            "may": ["may", "haruka"],
            "dawn": ["dawn", "hikari"],
            "serena": ["serena"],
            "iris": ["iris"],
            "lillie": ["lillie"],
            "cynthia": ["cynthia", "shirona"],
            "diantha": ["diantha"],
            "lusamine": ["lusamine"],
            "sabrina": ["sabrina"],
            "erika": ["erika"],
            "whitney": ["whitney"],
            "jasmine": ["jasmine"],
            "clair": ["clair"],
            "flannery": ["flannery"],
            "winona": ["winona"],
            "roxanne": ["roxanne"],
            "gardenia": ["gardenia"],
            "candice": ["candice"],
            "fantina": ["fantina"],
            "elesa": ["elesa"],
            "skyla": ["skyla"],
            "korrina": ["korrina"],
            "valerie": ["valerie"],
            "olympia": ["olympia"],
            "mallow": ["mallow"],
            "lana": ["lana"],
            "nessa": ["nessa"],
            "marnie": ["marnie"],
            "sonia": ["sonia"],
            "professor_juniper": ["professor juniper", "professor_juniper"],
            "nurse_joy": ["nurse joy", "joy"],
            "officer_jenny": ["officer jenny", "jenny"],
            "jessie": ["jessie", "musashi"],
            "bonnie": ["bonnie", "eureka"],
            "rosa": ["rosa"]
        },

        "hatsune_miku": {
            "miku": ["hatsune miku", "hatsune_miku", "miku", "initial miku", "initial_miku", "miku_(vocaloid)",
                     "miku_(project_diva)"],
            "meiko": ["meiko", "meiko_(vocaloid)", "meiko_(project_diva)"],
            "rin": ["kagamine rin", "kagamine_rin", "rin", "rin_(vocaloid)", "rin_(project_diva)"],
            "luka": ["megurine luka", "megurine_luka", "luka", "luka_(vocaloid)", "luka_(project_diva)"],
            "gumi": ["gumi", "megpoid", "gumi_(vocaloid)", "gumi_(project_diva)"],
            "teto": ["kasane teto", "kasane_teto", "teto", "teto_(utau)"],
            "neru": ["akita neru", "akita_neru", "neru", "neru_(derivative)"],
            "haku": ["yowane haku", "yowane_haku", "haku", "haku_(derivative)"],
            "una": ["otomachi una", "otomachi_una", "una", "una_(vocaloid)"],
            "ia": ["ia", "ia_(vocaloid)", "aria on the planetes"],
            "cul": ["cul", "cul_(vocaloid)"],
            "lily": ["lily", "lily_(vocaloid)"],
            "miki": ["sf-a2 miki", "sf_a2_miki", "miki", "miki_(vocaloid)"],
            "yukari": ["yuzuki yukari", "yuzuki_yukari", "yukari", "yukari_(vocaloid)"]
        },
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
        base_save_path=Path("./hentai") # ("/Volumes/ExternalHD/workspace/python/Monke D. Luffy/")
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
                'viola': "", # Need to add
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
