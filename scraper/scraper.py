import json
import sqlite3

# First, all imports
import sqlite3
from abc import ABC, abstractmethod

import requests
import torch
from PIL import Image
from bs4 import BeautifulSoup
import random
import string
import time
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
from dataclasses import dataclass
from urllib.parse import urljoin, parse_qs, urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
from pathlib import Path
from typing import Tuple, List, Optional
import urllib
import torch
import torch.nn as nn
import torchvision.models as models
import requests
import os
import gdown
import logging
from pathlib import Path
from typing import List, Tuple
import opennsfw2 as n2
import psutil
import numpy as np
from torchvision.transforms import transforms
from tqdm import tqdm

import concurrent.futures
from queue import Queue
from threading import Lock
import threading
from dataclasses import dataclass, field
from typing import Dict, Set
import time

import hashlib
import mimetypes
from urllib.parse import urlparse
import requests
import urllib.parse
from requests.exceptions import RequestException
from PIL import Image

"""
TODO: 
ADD LANA'S MOTHER
"""

"""
TODO:
ADD THE FOLLOWING WEBSITES:
Rule34 (rule34.paheal.net)
Paheal (paheal.net)
NHentai (nhentai.net)
E-Hentai (e-hentai.org)
Hentai Foundry (hentai-foundry.com)
Fakku (fakku.net)
Tsumino (tsumino.com)
AsmHentai (asmhentai.com)
Hentaifox (hentaifox.com)
Simply-Hentai (simply-hentai.com)
4chan (4chan.org) - /h/ board for hentai and adult content
8chan (8ch.net) - /h/ board for hentai and adult content
imagebam (imagebam.com)
imgur (imgur.com) - has a large hentai community, but be aware of the site's rules
Hentai2Read (hentai2read.com)
Doujinshi.org (doujinshi.org) - scanlated doujinshi and hentai manga
Pururin.io (pururin.io) - hentai and adult content aggregator
Xbooru (xbooru.com) - booru-style imageboard with a focus on adult content
Yande.re (yande.re) - booru-style imageboard with a focus on anime and manga
Booru.org (booru.org) - metasearch engine for various boorus, including those with adult content
MangaHentai (mangahentai.com)
HentaiManga (hentaimanga.com)
Hentai-Online (hentai-online.net)
Zerochan (zerochan.net) - anime and manga imageboard with a large collection of hentai images
Anime-Pictures (anime-pictures.net) - anime and manga imageboard with a section for adult content
Manga-Anime-Here (manga-anime-here.com) - manga and anime imageboard with a section for adult content
ImageFap (imagefap.com) - imageboard with a large collection of hentai images
Newgrounds (newgrounds.com) - flash animation and art community with some adult content
H-Manga (h-manga.com) - hentai manga and doujinshi website
Hentai-Pros (hentai-pros.com) - hentai manga and doujinshi website
Simply Hentai (simplyhentai.com) - hentai image and video website
Hentai Haven (hentaihaven.net) - hentai image and video website
AnimeHentai (animehentai.com) - anime and hentai image website
Doujins (doujins.com) - doujinshi and hentai manga website
H-Doujinshi (h-doujinshi.com) - doujinshi and hentai manga website
Doujinshi.org (doujinshi.org) - scanlated doujinshi and hentai manga website
MangaHentai (mangahentai.com) - hentai manga and doujinshi website
HentaiManga (hentaimanga.com) - hentai manga and doujinshi website
Wikimedia Commons (commons.wikimedia.org) - open-source image repository with some adult content
Pixabay (pixabay.com) - free stock photo and illustration website with some adult content
DeviantArt (deviantart.com) - art community with some adult content, including hentai
The Internet Archive (archive.org) - digital library with archives of hentai websites and imageboards
Google Groups (groups.google.com) - Usenet newsgroup archive with some adult content, including hentai
4plebs (4plebs.org) - imageboard with a large collection of hentai images
420chan (420chan.net) - imageboard with a /h/ board for adult content
7chan (7chan.org) - imageboard with a /h/ board for adult content
Imagearn (imagearn.com) - imageboard with a large collection of hentai images
Boorus (boorus.org) - booru-style imageboard with a focus on anime and manga
Hentaistream (hentaistream.com) - hentai streaming website with a large collection of videos
HentaiFox (hentaifox.com) - hentai video and image website
Simply Hentai Tube (simplyhentaitube.com) - hentai video website
Hentai Tube (hentaitube.com) - hentai video website
AnimeHentaiTube (animehentaitube.com) - anime and hentai video website
"""

"""
# Example Usage Guide

# 1. Basic Character Search
# For a basic search of a character, combine their base name with source:
base_url = "https://gelbooru.com/index.php?page=post&s=list&tags="
character = "kalifa_(one_piece)"
rating = "rating:safe" # or "rating:questionable" or "rating:explicit"
search_url = f"{base_url}{character}+{rating}"

# 2. Advanced Character Search with Specific Traits
# Combine multiple tags for more specific results:
character = "kalifa_(one_piece)"
traits = ["cp9", "battle_mode", "serious_agent"]
combined_tags = "+".join([character] + traits)
search_url = f"{base_url}{combined_tags}+{rating}"

# 3. State/Form Specific Search
# To find images of a character in specific states:
character = "conis_(one_piece)"
state = "resistance_mode"
location = "skypiea"
search_url = f"{base_url}{character}+{state}+{location}+{rating}"

# 4. Outfit/Appearance Search
character = "kalifa_(one_piece)"
outfit = "secretary_outfit"
search_url = f"{base_url}{character}+{outfit}+{rating}"

# 5. Time Period Specific Search
character = "kalifa_(one_piece)"
time_period = "water_7_arc"
search_url = f"{base_url}{character}+{time_period}+{rating}"

# 6. Combining Multiple Characters
characters = ["mozu", "kiwi", "square_sisters"]
combined_chars = "+".join(characters)
search_url = f"{base_url}{combined_chars}+{rating}"

# 7. Full Complex Search Example
def create_complex_search(character, traits, state, outfit, time_period, rating="rating:safe"):
    tags = [character] + traits + [state, outfit, time_period, rating]
    return f"{base_url}{'+'.join(filter(None, tags))}"

search_url = create_complex_search(
    character="kalifa_(one_piece)",
    traits=["cp9", "bubble_bubble_fruit"],
    state="battle_mode",
    outfit="agent_clothes",
    time_period="enies_lobby_arc"
)
"""

"""
 # Tag Usage Examples
    TAG_USAGE = {
        "Basic Search": {
            "character_only": "kaya_(one_piece)",
            "with_location": "kaya_(one_piece)+syrup_village",
            "with_state": "kaya_(one_piece)+studying_mode"
        },
        
        "Combined Tags": {
            "multiple_characters": "spandam's_secretary+enies_lobby",
            "character_and_role": "merry_(one_piece)+butler",
            "character_and_time": "kaya_(one_piece)+syrup_village_arc"
        },
        
        "Advanced Search": {
            "specific_outfit": "kaya_(one_piece)+mansion_clothes+medical_student_attire",
            "emotional_state": "kaya_(one_piece)+kind_kaya+determined_student",
            "time_period": "kaya_(one_piece)+syrup_village_arc+pre_timeskip"
        },
        
        "Filtering": {
            "rating_safe": "rating:safe+kaya_(one_piece)",
            "exclude_tags": "-adult+-suggestive+kaya_(one_piece)",
            "specific_artist": "artist:name+kaya_(one_piece)"
        }
    }

    # URL Construction Examples
    URL_EXAMPLES = {
        "Basic URL": "https://gelbooru.com/index.php?page=post&s=list&tags=kaya_(one_piece)",
        "Multiple Tags": "https://gelbooru.com/index.php?page=post&s=list&tags=kaya_(one_piece)+syrup_village+medical_student",
        "With Rating": "https://gelbooru.com/index.php?page=post&s=list&tags=kaya_(one_piece)+rating:safe",
        "Complex Search": "https://gelbooru.com/index.php?page=post&s=list&tags=kaya_(one_piece)+mansion_clothes+studying_mode+rating:safe"
    }
"""

"""
 # List of Arcs Not Yet Covered (Needing Character Details)
    MISSING_ARCS = {
        "Major Arcs": [
            "Marineford Arc",
            "Impel Down Arc",
            "Sabaody Archipelago Arc",
            "Thriller Bark Arc",
            "Dressrosa Arc",
            "Punk Hazard Arc",
            "Zou Arc",
            "Whole Cake Island Arc",
            "Wano Country Arc (Current)",
            "Return to Sabaody Arc"
        ],
        
        "Minor Canon Arcs": [
            "Romance Dawn Arc",
            "Loguetown Arc",
            "Reverse Mountain Arc",
            "Whiskey Peak Arc",
            "Jaya Arc",
            "Long Ring Long Land Arc",
            "Post-War Arc",
            "Return to Sabaody Arc",
            "Levely Arc"
        ],
        
        "Filler Arcs": [
            "Post-Alabasta Arc",
            "Goat Island Arc",
            "Ruluka Island Arc",
            "Navarone Arc",
            "Spa Island Arc",
            "Adventure of Nebulandia",
            "Silver Mine Arc",
            "Marine Rookie Arc",
            "Cidre Guild Arc"
        ],
        
        "Movies and Specials": [
            "Movie Character Arcs",
            "TV Special Character Arcs",
            "OVA Character Arcs"
        ]
    }
"""

def get_series_indicators():
    """
    Returns a dictionary of series indicators for character classification.
    Each series has multiple possible indicators that might appear in tags.
    """
    return {
        "one_piece": [
            "one piece",
            "one-piece",
            "onepiece",
            "(one piece)",
            "one_piece",
            "_one_piece",
            "(one_piece)",
            "op_",
            "op character"
        ],

        "dota2": [
            "dota",
            "dota 2",
            "dota2",
            "(dota)",
            "(dota 2)",
            "defense of the ancients",
            "dota_(series)",
            "(dota_2)",
            "dota_2"
        ],

        "fairy_tail": [
            "fairy tail",
            "fairytail",
            "fairy_tail",
            "(fairy tail)",
            "(fairytail)",
            "fairy_tail_guild",
            "_fairy_tail",
            "ft_"
        ],

        "dragon_ball": [
            "dragon ball",
            "dragonball",
            "dragon_ball",
            "dbz",
            "db_",
            "(dragon ball)",
            "dragon ball z",
            "dragon_ball_z",
            "dragon ball super",
            "dragon_ball_super",
            "dbs",
            "dbgt",
            "dragon ball gt"
        ],

        "attack_on_titan": [
            "attack on titan",
            "shingeki no kyojin",
            "shingekinokyojin",
            "(shingeki no kyojin)",
            "snk",
            "aot",
            "_snk_",
            "_aot_",
            "attack_on_titan"
        ],

        "demon_slayer": [
            "demon slayer",
            "kimetsu no yaiba",
            "kimetsunoyaiba",
            "(kimetsu no yaiba)",
            "kimetsu_no_yaiba",
            "demon_slayer",
            "_kny_",
            "kny"
        ],

        "jujutsu_kaisen": [
            "jujutsu kaisen",
            "jujutsukaisen",
            "jujutsu_kaisen",
            "(jujutsu kaisen)",
            "_jjk_",
            "jjk",
            "(jjk)"
        ],

        "cowboy_bebop": [
            "cowboy bebop",
            "cowboybebop",
            "cowboy_bebop",
            "(cowboy bebop)",
            "_bebop_",
            "bebop"
        ],

        "spy_x_family": [
            "spy x family",
            "spy×family",
            "spyxfamily",
            "spy_x_family",
            "spy_family",
            "(spy x family)",
            "sxf",
            "_sxf_"
        ],

        "one_punch_man": [
            "one punch man",
            "onepunchman",
            "one_punch_man",
            "(one punch man)",
            "opm",
            "_opm_",
            "one-punch man"
        ],

        "league_of_legends": [
            "league of legends",
            "leagueoflegends",
            "league_of_legends",
            "(league of legends)",
            "lol",
            "_lol_",
            "league",
            "(lol)"
        ],

        "hunter_x_hunter": [
            "hunter x hunter",
            "hunterxhunter",
            "hunter_x_hunter",
            "(hunter x hunter)",
            "hxh",
            "_hxh_",
            "hunter hunter"
        ],

        "fullmetal_alchemist": [
            "fullmetal alchemist",
            "fullmetalalchemist",
            "full metal alchemist",
            "fullmetal_alchemist",
            "(fullmetal alchemist)",
            "fma",
            "_fma_",
            "fmab",
            "fullmetal alchemist brotherhood",
            "hagane no renkinjutsushi"
        ],

        "my_hero_academia": [
            "my hero academia",
            "boku no hero academia",
            "myheroacademia",
            "my_hero_academia",
            "(my hero academia)",
            "mha",
            "_mha_",
            "bnha",
            "_bnha_",
            "boku_no_hero_academia"
        ],

        "jojos_bizarre_adventure": [
            "jojo's bizarre adventure",
            "jojos bizarre adventure",
            "jojo no kimyou na bouken",
            "jjba",
            "_jjba_",
            "jojos_bizarre_adventure",
            "(jojo)",
            "jojo"
        ],

        "pokemon": [
            "pokemon",
            "pokémon",
            "pocket monsters",
            "_pokemon_",
            "(pokemon)",
            "pkmn",
            "_pkmn_",
            "pokemon_series"
        ],

        "hatsune_miku": [
            "vocaloid",
            "hatsune miku",
            "hatsunemiku",
            "hatsune_miku",
            "(vocaloid)",
            "_vocaloid_",
            "project diva",
            "project_diva",
            "miku",
            "(miku)"
        ],

        "konosuba": [
            "konosuba",
            "kono subarashii sekai ni shukufuku wo",
            "_konosuba_",
            "(konosuba)",
            "gods blessing on this wonderful world",
            "kono_subarashii"
        ],

        "naruto": [
            "naruto",
            "_naruto_",
            "(naruto)",
            "naruto shippuden",
            "naruto_shippuden",
            "naruto_series",
            "narutoshippuden"
        ],

        "lycoris_recoil": [
            "lycoris recoil",
            "lycorisrecoil",
            "lycoris_recoil",
            "(lycoris recoil)",
            "_lycoris_",
            "lycoreco"
        ]
    }

class CharacterClassifier:
    """Handles character recognition and classification"""

    def __init__(self):
        self.series_indicators = get_series_indicators()

        # Character mappings by series
        self.CHARACTER_MAPPINGS = {
            "one_piece": {
                "monkey_d_luffy": ["monkey d luffy", "monkey_d_luffy", "luffy", "strawhat"],
                "roronoa_zoro": ["roronoa zoro", "roronoa_zoro", "zoro"],
                "nami": ["nami", "nami_(one_piece)"],
                "vinsmoke_sanji": ["vinsmoke sanji", "vinsmoke_sanji", "sanji", "black leg"],
                "nico_robin": ["nico robin", "nico_robin", "robin", "robin_(alabasta)", "robin_(cosplay)"],
                "uta": ["uta", "uta_(one_piece)"],
                "rebecca": ["rebecca", "rebecca_(one_piece)"],
                "carrot": ["carrot", "carrot_(one_piece)"],
                "jewelry_bonney": ["jewelry bonney", "jewelry_bonney", "bonney"],
                "baby_5": ["baby 5", "baby_5", "baby five", "baby_five"],
                "boa_hancock": ["boa hancock", "boa_hancock", "hancock"],
                "nefertari_vivi": ["nefertari vivi", "nefertari_vivi", "vivi"],
                "vinsmoke_reiju": ["vinsmoke reiju", "vinsmoke_reiju", "reiju"],
                "charlotte_linlin": ["big mom", "big_mom", "charlotte_linlin", "charlotte linlin", "linlin"],
                "shimotsuki_kuina": ["shimotsuki kuina", "shimotsuki_kuina", "kuina"],
                "charlotte_smoothie": ["charlotte_smoothie", "charlotte smoothie", "smoothie"],
                "shirahoshi": ["shirahoshi", "princess shirahoshi", "princess_shirahoshi"],
                "kouzuki_hiyori": ["kouzuki hiyori", "kouzuki_hiyori", "hiyori"],
                "catarina_devon": ["catarina devon", "catarina_devon", "devon"],
                "perona": ["perona", "'ghost princess' perona", "ghost princess perona"],
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
                "isuka": ["isuka", "isuka_(one_piece)"],
                "viola": ["viola", "viola_(one_piece)"],
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
                "tsunade_senju": ["tsunade senju", "tsunade", "lady tsunade", "princess tsunade"],
                "sakura_haruno": ["sakura haruno", "sakura_haruno"],
                "hinata_hyuga": ["hinata hyuga", "hinata_hyuga"],
                "tenten": ["tenten"],
                "temari": ["temari"],
                "kushina_uzumaki": ["kushina uzumaki", "kushina_uzumaki"],
                "sarada_uchiha": ["sarada uchiha", "sarada_uchiha"],
                "himawari_uzumaki": ["himawari uzumaki", "himawari_uzumaki"],
                "ino_yamanaka": ["ino yamanaka", "ino_yamanaka"],
                "kurenai_yuhi": ["kurenai yuhi", "kurenai_yuhi"],
                "anko_mitarashi": ["anko mitarashi", "anko_mitarashi"],
                "shizune": ["shizune"],
                "karin_uzumaki": ["karin uzumaki", "karin_uzumaki"],
                "konan": ["konan"],
                "mei_terumi": ["mei terumi", "mei_terumi"],
                "samui": ["samui"],
                "karui": ["karui"],
                "mabui": ["mabui"],
                "yugao_uzuki": ["yugao uzuki", "yugao_uzuki"],
                "tsume_inuzuka": ["tsume inuzuka", "tsume_inuzuka"],
                "hana_inuzuka": ["hana inuzuka", "hana_inuzuka"],
                "natsu_hyuga": ["natsu hyuga", "natsu_hyuga"],
                "yakumo_kurama": ["yakumo kurama", "yakumo_kurama"],
                "tsunami": ["tsunami"],
                "ayame": ["ayame"],
                "yugito_nii": ["yugito nii", "yugito_nii"],
                "fuu": ["fuu"],
                "hokuto": ["hokuto"],
                "hanabi_hyuga": ["hanabi hyuga", "hanabi_hyuga"],
                "moegi": ["moegi"],
                "sumire_kakei": ["sumire kakei", "sumire_kakei"],
                "chocho_akimichi": ["chocho akimichi", "chocho_akimichi"],
                "mirai_sarutobi": ["mirai sarutobi", "mirai_sarutobi"],
                "wasabi_izuno": ["wasabi izuno", "wasabi_izuno"],
                "namida_suzumeno": ["namida suzumeno", "namida_suzumeno"]
            },

            "fairy_tail": {
                "lucy_heartfilia": ["lucy heartfilia", "lucy_heartfilia"],
                "erza_scarlet": ["erza scarlet", "erza_scarlet", "titania"],
                "wendy_marvell": ["wendy marvell", "wendy_marvell"],
                "juvia_lockser": ["juvia lockser", "juvia_lockser"],
                "levy_mcgarden": ["levy mcgarden", "levy_mcgarden"],
                "mirajane_strauss": ["mirajane strauss", "mirajane_strauss"],
                "lisanna_strauss": ["lisanna strauss", "lisanna_strauss"],
                "cana_alberona": ["cana alberona", "cana_alberona"],
                "evergreen": ["evergreen"],
                "bisca_connell": ["bisca connell", "bisca_connell"],
                "laki_olietta": ["laki olietta", "laki_olietta"],
                "kinana": ["kinana"],
                "mavis_vermillion": ["mavis vermillion", "mavis_vermillion"],
                "meredy": ["meredy"],
                "ultear_milkovich": ["ultear milkovich", "ultear_milkovich"],
                "yukino_agria": ["yukino agria", "yukino_agria"],
                "minerva_orlando": ["minerva orlando", "minerva_orlando"],
                "kagura_mikazuchi": ["kagura mikazuchi", "kagura_mikazuchi"],
                "milliana": ["milliana"],
                "flare_corona": ["flare corona", "flare_corona"],
                "jenny_realight": ["jenny realight", "jenny_realight"],
                "sherry_blendy": ["sherry blendy", "sherry_blendy"],
                "chelia_blendy": ["chelia blendy", "chelia_blendy"],
                "sorano_agria": ["sorano agria", "sorano_agria", "angel"],
                "brandish_mu": ["brandish μ", "brandish mu"],
                "dimaria_yesta": ["dimaria yesta", "dimaria_yesta"],
                "irene_belserion": ["irene belserion", "irene_belserion"],
                "hisui_fiore": ["hisui e fiore", "hisui_e_fiore"]
            },

            "dragon_ball": {
                "bulma_briefs": ["bulma briefs", "bulma_briefs"],
                "chi_chi": ["chi chi", "chi_chi", "chi-chi"],
                "videl_satan": ["videl"],
                "pan": ["pan"],
                "android_18": ["android 18", "c-18", "lazuli"],
                "bulla_briefs": ["bulla", "bra"],
                "launch": ["launch", "lunch"],
                "marron": ["marron"],
                "mai": ["mai"],
                "ranfan": ["ranfan"],
                "vados": ["vados"],
                "caulifla": ["caulifla"],
                "kale": ["kale"],
                "ribrianne": ["ribrianne", "brianne de chateau"],
                "oceanus_shenron": ["oceanus shenron", "princess oto"],
                "gine": ["gine"],
                "fasha": ["fasha", "selypa"],
                "zangya": ["zangya"],
                "towa": ["towa"],
                "chronoa": ["supreme kai of time", "chronoa"],
                "arale_norimaki": ["arale norimaki", "arale_norimaki"]
            },

            "attack_on_titan": {
                "mikasa_ackerman": ["mikasa ackerman", "mikasa_ackerman"],
                "annie_leonhart": ["annie leonhart", "annie_leonhart"],
                "historia_reiss": ["historia reiss", "historia_reiss", "christa"],
                "sasha_braus": ["sasha braus", "sasha_braus"],
                "hange_zoe": ["hange zoe", "hanji"],
                "ymir": ["ymir", "freckled ymir"],
                "pieck_finger": ["pieck finger", "pieck_finger"],
                "gabi_braun": ["gabi braun", "gabi_braun"],
                "frieda_reiss": ["frieda reiss", "frieda_reiss"],
                "carla_yeager": ["carla yeager", "carla_yeager"],
                "dina_fritz": ["dina fritz", "dina_fritz"],
                "petra_ral": ["petra ral", "petra_ral"],
                "rico_brzenska": ["rico brzenska", "rico_brzenska"],
                "yelena": ["yelena"],
                "kiyomi_azumabito": ["kiyomi azumabito", "kiyomi_azumabito"],
                "louise": ["louise"],
                "nifa": ["nifa"],
                "lynne": ["lynne"],
                "ilse_langnar": ["ilse langnar", "ilse_langnar"],
                "nanaba": ["nanaba"]
            },

            "demon_slayer": {
                "nezuko_kamado": ["nezuko kamado", "nezuko_kamado"],
                "kanao_tsuyuri": ["kanao tsuyuri", "kanao_tsuyuri"],
                "shinobu_kocho": ["shinobu kocho", "shinobu_kocho"],
                "kanae_kocho": ["kanae kocho", "kanae_kocho"],
                "mitsuri_kanroji": ["mitsuri kanroji", "mitsuri_kanroji"],
                "daki": ["daki", "ume"],
                "tamayo": ["tamayo"],
                "makio": ["makio"],
                "suma": ["suma"],
                "hinatsuru": ["hinatsuru"],
                "aoi_kanzaki": ["aoi kanzaki", "aoi_kanzaki"],
                "kiyo_terauchi": ["kiyo terauchi", "kiyo_terauchi"],
                "sumi_nakahara": ["sumi nakahara", "sumi_nakahara"],
                "naho_takada": ["naho takada", "naho_takada"],
                "goto": ["goto", "goto_san"],
                "amane": ["amane"],
                "mukago": ["mukago"],
                "ruka": ["ruka"],
                "hinaki_ubuyashiki": ["hinaki ubuyashiki", "hinaki_ubuyashiki"],
                "nichika_ubuyashiki": ["nichika ubuyashiki", "nichika_ubuyashiki"],
                "kuina_ubuyashiki": ["kuina ubuyashiki", "kuina_ubuyashiki"]
            },

            "jujutsu_kaisen": {
                "nobara_kugisaki": ["nobara kugisaki", "nobara_kugisaki"],
                "maki_zenin": ["maki zenin", "maki_zenin"],
                "mei_mei": ["mei mei", "mei_mei"],
                "kasumi_miwa": ["kasumi miwa", "kasumi_miwa"],
                "momo_nishimiya": ["momo nishimiya", "momo_nishimiya"],
                "mai_zenin": ["mai zenin", "mai_zenin"],
                "yuki_tsukumo": ["yuki tsukumo", "yuki_tsukumo"],
                "rika_orimoto": ["rika orimoto", "rika_orimoto"],
                "utahime_iori": ["utahime iori", "utahime_iori"],
                "tsumiki_fushiguro": ["tsumiki fushiguro", "tsumiki_fushiguro"],
                "manami_suda": ["manami suda", "manami_suda"],
                "saori_rokujo": ["saori rokujo", "saori_rokujo"],
                "shoko_ieiri": ["shoko ieiri", "shoko_ieiri"],
                "mimiko_hasaba": ["mimiko hasaba", "mimiko_hasaba"],
                "nanako_hasaba": ["nanako hasaba", "nanako_hasaba"]
            },

            "cowboy_bebop": {
                "faye_valentine": ["faye valentine", "faye_valentine"],
                "edward_wong": ["edward wong", "radical ed", "edward"],
                "julia": ["julia"],
                "meifa": ["meifa puzi", "meifa_puzi"],
                "judy": ["judy"],
                "annie": ["anastasia"],
                "alisa": ["alisa"],
                "victoria_terraforming": ["v.t.", "victoria terraforming"],
                "stella_bonnaro": ["stella bonnaro", "stella_bonnaro"],
                "coffee": ["coffee"],
                "katrina_solensan": ["katrina solensan", "katrina_solensan"]
            },

            "spy_x_family": {
                "yor_forger": ["yor forger", "yor_forger", "thorn princess"],
                "anya_forger": ["anya forger", "anya_forger"],
                "sylvia_sherwood": ["sylvia sherwood", "sylvia_sherwood"],
                "fiona_frost": ["fiona frost", "fiona_frost"],
                "becky_blackbell": ["becky blackbell", "becky_blackbell"],
                "sharon": ["sharon", "shop_keeper"],
                "melinda_desmond": ["melinda desmond", "melinda_desmond"],
                "camilla": ["camilla", "shopkeeper_sister"],
                "karen_gloomy": ["karen gloomy", "karen_gloomy"],
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
                "captain_mizuki": ["captain mizuki", "mizuki"],
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
                "nami": ["nami", "nami_(league_of_legends)"],
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
                "biscuit_krueger": ["biscuit krueger", "bisky"],
                "palm_siberia": ["palm siberia"],
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
                "kalluto_zoldyck": ["kalluto zoldyck", "kalluto_zoldyck"],
                "kikyo_zoldyck": ["kikyo zoldyck", "kikyo_zoldyck"],
                "alluka_zoldyck": ["alluka zoldyck", "alluka_zoldyck"],
                "cheadle_yorkshire": ["cheadle yorkshire", "cheadle_yorkshire"],
                "menchi": ["menchi"],
                "ponzu": ["ponzu"]
            },

            "fullmetal_alchemist": {
                "winry_rockbell": ["winry rockbell", "winry_rockbell"],
                "riza_hawkeye": ["riza hawkeye", "riza_hawkeye"],
                "olivier_armstrong": ["olivier armstrong", "olivier_armstrong"],
                "izumi_curtis": ["izumi curtis", "izumi_curtis"],
                "mei_chang": ["mei chang", "mei_chang"],
                "maria_ross": ["maria ross", "maria_ross"],
                "gracia_hughes": ["gracia hughes", "gracia_hughes"],
                "elicia_hughes": ["elicia hughes", "elicia_hughes"],
                "lan_fan": ["lan fan", "lan_fan"],
                "paninya": ["paninya"],
                "sheska": ["sheska", "sciezka"],
                "rose_thomas": ["rose thomas", "rose_thomas"],
                "catherine_armstrong": ["catherine elle armstrong", "catherine_armstrong"],
                "martel": ["martel"],
                "trisha_elric": ["trisha elric", "trisha_elric"],
                "pinako_rockbell": ["pinako rockbell", "pinako_rockbell"],
                "lust": ["lust"],
                "dante": ["dante"],
                "clara": ["clara", "psiren"]
            },

            "my_hero_academia": {
                "ochaco_uraraka": ["ochaco uraraka", "ochaco_uraraka"],
                "tsuyu_asui": ["tsuyu asui", "tsuyu_asui", "froppy"],
                "momo_yaoyorozu": ["momo yaoyorozu", "momo_yaoyorozu"],
                "kyoka_jirou": ["kyoka jirou", "kyoka_jirou"],
                "toru_hagakure": ["toru hagakure", "toru_hagakure"],
                "mina_ashido": ["mina ashido", "mina_ashido", "pinky"],
                "yu_takeyama": ["mount lady", "yu takeyama"],
                "nemuri_kayama": ["midnight", "nemuri kayama"],
                "rumi_usagiyama": ["mirko", "rumi usagiyama"],
                "ryuko_tatsuma": ["ryuku", "ryuko tatsuma"],
                "nejire_hado": ["nejire hado", "nejire_hado"],
                "shino_sosaki": ["mandalay", "shino sosaki"],
                "ryuko_tsuchikawa": ["pixie-bob", "ryuko tsuchikawa"],
                "tomoko_shiretoko": ["ragdoll", "tomoko shiretoko"],
                "itsuka_kendo": ["itsuka kendo", "itsuka_kendo"],
                "pony_tsunotori": ["pony tsunotori", "pony_tsunotori"],
                "kinoko_komori": ["kinoko komori", "kinoko_komori"],
                "yui_kodai": ["yui kodai", "yui_kodai"],
                "reiko_yanagi": ["reiko yanagi", "reiko_yanagi"],
                "setsuna_tokage": ["setsuna tokage", "setsuna_tokage"],
                "melissa_shield": ["melissa shield", "melissa_shield"],
                "inko_midoriya": ["inko midoriya", "inko_midoriya"],
                "fuyumi_todoroki": ["fuyumi todoroki", "fuyumi_todoroki"],
                "eri": ["eri"],
                "nana_shimura": ["nana shimura", "nana_shimura"],
                "himiko_toga": ["himiko toga", "himiko_toga"]
            },

            "jojos_bizarre_adventure": {
                "jolyne_cujoh": ["jolyne cujoh", "jolyne_cujoh"],
                "lisa_lisa": ["lisa lisa", "lisa_lisa"],
                "erina_pendleton": ["erina pendleton", "erina_pendleton"],
                "trish_una": ["trish una", "trish_una"],
                "suzi_q": ["suzi q", "suzi_q"],
                "holly_kujo": ["holly kujo", "holly_kujo", "seiko"],
                "yukako_yamagishi": ["yukako yamagishi", "yukako_yamagishi"],
                "reimi_sugimoto": ["reimi sugimoto", "reimi_sugimoto"],
                "hot_pants": ["hot pants", "hot_pants"],
                "lucy_steel": ["lucy steel", "lucy_steel"],
                "yasuho_hirose": ["yasuho hirose", "yasuho_hirose"],
                "hermes_costello": ["hermes costello", "hermes_costello"],
                "foo_fighters": ["foo fighters", "f.f.", "ff"],
                "ermes_costello": ["ermes costello", "ermes_costello"],
                "gwess": ["gwess"],
                "mariah": ["mariah"],
                "midler": ["midler", "rose"],
                "anne": ["anne"],
                "tomoko_higashikata": ["tomoko higashikata", "tomoko_higashikata"]
            },

            "pokemon": {
                "misty_waterflower": ["misty", "kasumi"],
                "may_maple": ["may", "haruka"],
                "dawn_berlitz": ["dawn", "hikari"],
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
                "hatsune_miku": ["hatsune miku", "hatsune_miku", "miku", "initial miku", "initial_miku", "miku_(vocaloid)",
                                 "miku_(project_diva)"],
                "meiko": ["meiko", "meiko_(vocaloid)", "meiko_(project_diva)"],
                "kagamine_rin": ["kagamine rin", "kagamine_rin", "rin", "rin_(vocaloid)", "rin_(project_diva)"],
                "megurine_luka": ["megurine luka", "megurine_luka", "luka", "luka_(vocaloid)", "luka_(project_diva)"],
                "megpoid_gumi": ["gumi", "megpoid", "gumi_(vocaloid)", "gumi_(project_diva)"],
                "kasane_teto": ["kasane teto", "kasane_teto", "teto", "teto_(utau)"],
                "akita_neru": ["akita neru", "akita_neru", "neru", "neru_(derivative)"],
                "yowane_haku": ["yowane haku", "yowane_haku", "haku", "haku_(derivative)"],
                "otomachi_una": ["otomachi una", "otomachi_una", "una", "una_(vocaloid)"],
                "ia": ["ia", "ia_(vocaloid)", "aria on the planetes"],
                "cul": ["cul", "cul_(vocaloid)"],
                "lily": ["lily", "lily_(vocaloid)"],
                "sf_a2_miki": ["sf-a2 miki", "sf_a2_miki", "miki", "miki_(vocaloid)"],
                "yuzuki_yukari": ["yuzuki yukari", "yuzuki_yukari", "yukari", "yukari_(vocaloid)"]
            },

            "konosuba": {
                "aqua": ["aqua", "aqua_(konosuba)", "goddess_aqua", "useless_goddess"],
                "megumin": ["megumin", "megumin_(konosuba)", "explosion_girl", "crimson_demon_megumin"],
                "lalatina_dustiness": ["darkness", "darkness_(konosuba)", "dustiness_ford_lalatina", "lalatina",
                                       "crusader_darkness"],
                "wiz": ["wiz", "wiz_(konosuba)", "lich_wiz"],
                "yunyun": ["yunyun", "yun yun", "yun_yun", "yunyun_(konosuba)"],
                "chris": ["chris", "chris_(konosuba)", "eris", "eris_(konosuba)", "assistant_goddess"],
                "luna": ["luna", "luna_(konosuba)", "guild_receptionist"],
                "sena": ["sena", "sena_(konosuba)"],
                "wolbach": ["wolbach", "goddess_wolbach", "wolbach_(konosuba)"],
                "iris": ["iris", "iris_stylish_sword", "iris_(konosuba)"],
                "komekko": ["komekko", "komekko_(konosuba)", "megumin_sister"],
                "cecily": ["cecily", "cecily_(konosuba)", "axis_cult_cecily"],
                "arue": ["arue", "arue_(konosuba)"],
                "claire": ["claire", "claire_(konosuba)"],
                "sylvia": ["sylvia", "sylvia_(konosuba)"],
                "lean": ["lean", "lean_(konosuba)"],
                "verdia": ["verdia", "verdia_(konosuba)"],
                "hans": ["hans", "hans_(konosuba)"],
                "yuiyui": ["yuiyui", "crimson_demon_yuiyui", "yuiyui_(konosuba)"]
            },

            "lycoris_recoil": {
                "chisato_nishikigi": ["chisato nishikigi", "chisato_nishikigi", "chisato", "nishikigi"],
                "takina_inoue": ["takina inoue", "takina_inoue", "takina"],
                "mizuki_nakahara": ["mizuki nakahara", "mizuki_nakahara", "mizuki"],
                "kurumi_shinonome": ["kurumi shinonome", "kurumi_shinonome", "walnut", "kurumi"],
                "erika_karuizawa": ["erika karuizawa", "erika_karuizawa", "erika"],
                "sakura_otome": ["sakura otome", "sakura_otome", "sakura"],
                "fuki_himegama": ["fuki himegama", "fuki_himegama", "himegama"],
                "mika": ["mika"],
                "robota": ["robota"],
                "lucy": ["lucy"]
            },
        }

    def _create_reverse_index(self):
        """Create a reverse lookup index mapping aliases to (series, character) pairs"""
        self.alias_index = {}
        for series, char_mappings in self.CHARACTER_MAPPINGS.items():
            for char_name, aliases in char_mappings.items():
                for alias in aliases:
                    if alias not in self.alias_index:
                        self.alias_index[alias] = []
                    self.alias_index[alias].append((series, char_name))

    def _extract_series_from_url(self, url: str) -> str:
        """
        Extract series information from the URL if possible.

        Args:
            url (str): The source URL

        Returns:
            str: Series identifier or None
        """
        if not url:
            return None

        url = url.lower()
        series_markers = {
            "one_piece": ["_(one_piece)", "one piece"],
            "league_of_legends": ["_(league_of_legends)", "league of legends", "lol"],
            "naruto": ["_(naruto)", "naruto", "shippuden"],
            "fairy_tail": ["_(fairy_tail)", "fairy tail"],
            "dragon_ball": ["_(dragon_ball)", "dragon ball", "dragonball"],
            "attack_on_titan": ["_(shingeki_no_kyojin)", "shingeki_no_kyojin", "attack on titan"],
            "demon_slayer": ["_(kimetsu_no_yaiba)", "kimetsu_no_yaiba"],
            "jujutsu_kaisen": ["_(jujutsu_kaisen)", "jujutsu kaisen"],
            "cowboy_bebop": ["_(cowboy_bebop)", "cowboy bebop"],
            "spy_x_family": ["_(spy_x_family)", "spy x family"],
            "one_punch_man": ["_(one-punch_man)", "one punch man", "one_punch_man"],
            "hunter_x_hunter": ["_(hunter_x_hunter)", "hunter x hunter", "hunter_x_hunter"],
            "fullmetal_alchemist": ["_(fma)", "fullmetal alchemist", "fma", "hagane"],
            "my_hero_academia": ["_(boku_no_hero_academia)", "boku_no_hero_academia", "my hero academia"],
            "jojos_bizarre_adventure": ["_(jojo)", "jojo", "jojos bizarre adventure"],
            "pokemon": ["_(pokemon)", "pokemon", "pocket monsters"],
            "hatsune_miku": ["_(vocaloid)", "vocaloid", "hatsune miku"],
            "konosuba": ["_(konosuba)", "konosuba", "kono subarashii"],
            "lycoris_recoil": ["_(lycoris_recoil)", "lycoris recoil"],
            "dota2": ["_(dota)", "_(dota_2)", "dota 2", "dota"]
        }

        for series, markers in series_markers.items():
            if any(marker in url for marker in markers):
                return series
        return None

    def identify_character(self, tags: str, source_url: str = None) -> Tuple[str, str]:
        """
        Identify a character and their series from tags with improved disambiguation.

        Args:
            tags (str): Tag string from the URL
            source_url (str, optional): The original source URL for additional context

        Returns:
            Tuple[str, str]: (series name, character name)
        """
        if not tags:
            return ("unknown", "unknown")

        tags = tags.lower().replace('+', ' ').strip()

        # Special case handling for characters with similar names across series
        name_conflicts = {
            "sakura": {
                "lycoris_recoil": ["otome sakura", "sakura otome"],
                "naruto": ["haruno sakura", "sakura haruno"]
            },
            "nami": {
                "one_piece": ["nami_(one_piece)", "nami one piece"],
                "league_of_legends": ["nami_(league_of_legends)", "nami lol"]
            },
            "annie": {
                "league_of_legends": ["annie_(league_of_legends)", "annie lol"],
                "attack_on_titan": ["annie leonhart", "annie leonhardt"]
            },
            "luna": {
                "konosuba": ["luna_(konosuba)"],
                "dota2": ["luna_(dota)"]
            },
            "lily": {
                "one_punch_man": ["lily of the three section staff"],
                "vocaloid": ["lily_(vocaloid)"]
            },
            "robin": {
                "one_piece": ["nico robin", "robin_(alabasta)"],
                "fire_emblem": ["robin_(fire_emblem)"]
            }
        }

        # First try to determine series from the source URL
        url_series = self._extract_series_from_url(source_url) if source_url else None

        # Check for name conflicts first
        for base_name, series_dict in name_conflicts.items():
            if base_name in tags:
                # If we have a URL series and it's in the conflicts, use that
                if url_series and url_series in series_dict:
                    for alias in series_dict[url_series]:
                        if alias in tags:
                            char_mappings = self.CHARACTER_MAPPINGS[url_series]
                            for char_name, char_aliases in char_mappings.items():
                                if any(a in alias for a in char_aliases):
                                    return (url_series, char_name)

                # Otherwise check all conflict variations
                for series, aliases in series_dict.items():
                    if any(alias in tags for alias in aliases):
                        char_mappings = self.CHARACTER_MAPPINGS[series]
                        for char_name, char_aliases in char_mappings.items():
                            if any(alias in tags for alias in char_aliases):
                                return (series, char_name)

        # If we have a series from URL, prioritize that series first
        if url_series and url_series in self.CHARACTER_MAPPINGS:
            char_mappings = self.CHARACTER_MAPPINGS[url_series]
            for char_name, aliases in char_mappings.items():
                if any(alias in tags for alias in aliases):
                    return (url_series, char_name)

        # Try to determine series from tags
        detected_series = None
        for series, indicators in self.series_indicators.items():
            if any(indicator in tags for indicator in indicators):
                detected_series = series
                break

        # If we found a series in the tags, try matching characters from that series
        if detected_series:
            char_mappings = self.CHARACTER_MAPPINGS[detected_series]
            for char_name, aliases in char_mappings.items():
                if any(alias in tags for alias in aliases):
                    return (detected_series, char_name)

        # If no specific series match, look for exact character matches
        for series, char_mappings in self.CHARACTER_MAPPINGS.items():
            for char_name, aliases in char_mappings.items():
                if any(alias == tags for alias in aliases):
                    return (series, char_name)

        # Finally, try partial matches with series context
        for series, char_mappings in self.CHARACTER_MAPPINGS.items():
            for char_name, aliases in char_mappings.items():
                if any(alias in tags for alias in aliases):
                    # Double check if this match makes sense with URL context
                    if url_series and series != url_series:
                        continue
                    return (series, char_name)

        return ("unknown", "unknown")

    def get_character_aliases(self, series: str, character: str) -> List[str]:
        """Get all aliases for a character in a specific series."""
        if series in self.CHARACTER_MAPPINGS and character in self.CHARACTER_MAPPINGS[series]:
            return self.CHARACTER_MAPPINGS[series][character]
        return []

@dataclass
class ScraperConfig:
    """Configuration settings for the scraper"""
    base_save_path: Path
    request_timeout: int = 30
    page_delay: float = 2.0
    download_delay: float = 1.0
    retry_attempts: int = 3
    chunk_size: int = 8192
    headless: bool = True
    user_agent: Optional[str] = None
    filename_length: int = 8
    max_file_size: int = 50 * 1024 * 1024
    nsfw_threshold: float = 0.5
    debug: bool = False
    verbose_logging: bool = False

    def __post_init__(self):
        """Validate and process configuration after initialization."""
        # Convert base_save_path to Path object if it's a string
        if isinstance(self.base_save_path, str):
            self.base_save_path = Path(self.base_save_path)

        # Set default user agent if none provided
        if self.user_agent is None:
            self.user_agent = (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/91.0.4472.124 Safari/537.36'
            )

        # Validate numeric parameters
        if self.request_timeout <= 0:
            raise ValueError("request_timeout must be positive")
        if self.page_delay < 0:
            raise ValueError("page_delay must be non-negative")
        if self.download_delay < 0:
            raise ValueError("download_delay must be non-negative")
        if self.retry_attempts < 1:
            raise ValueError("retry_attempts must be at least 1")
        if self.chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if self.filename_length < 1:
            raise ValueError("filename_length must be at least 1")
        # if not 0 <= self.nsfw_threshold <= 1:
        #     raise ValueError("nsfw_threshold must be between 0 and 1")
        if self.max_file_size <= 0:
            raise ValueError("max_file_size must be positive")

    def to_dict(self):
        """Convert config to dictionary for logging/debugging."""
        return {
            'base_save_path': str(self.base_save_path),
            'request_timeout': self.request_timeout,
            'page_delay': self.page_delay,
            'download_delay': self.download_delay,
            'retry_attempts': self.retry_attempts,
            'chunk_size': self.chunk_size,
            'headless': self.headless,
            'user_agent': self.user_agent,
            'filename_length': self.filename_length,
            'max_file_size': self.max_file_size,
            'nsfw_threshold': self.nsfw_threshold,
            'debug': self.debug,
            'verbose_logging': self.verbose_logging
        }


class NSFWDetector:
    """Handles NSFW content detection using OpenNSFW2"""

    def __init__(self, threshold: float = 0.5):  # Increased default threshold for NSFW content
        self.threshold = threshold
        self._setup_logging()
        self._setup_model()

    def _setup_logging(self):
        """Configure logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('nsfw_detector.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _setup_model(self):
        """Initialize the NSFW detection model"""
        try:
            # Model will be automatically downloaded if not present
            self.model = n2.make_open_nsfw_model()
            self.logger.info("NSFW model loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize NSFW model: {str(e)}")
            raise

    def _process_image(self, image: Image.Image) -> float:
        """Process a single PIL Image and return NSFW score"""
        try:
            # Preprocess image using Yahoo's preprocessing
            processed_image = n2.preprocess_image(image, n2.Preprocessing.YAHOO)

            # Add batch dimension
            input_data = np.expand_dims(processed_image, axis=0)

            # Get prediction
            predictions = self.model.predict(input_data, verbose=0)

            # Return NSFW probability (second value in prediction)
            return float(predictions[0][1])
        except Exception as e:
            self.logger.error(f"Error processing image: {str(e)}")
            return 1.0  # Return high score on error to be safe

    def _process_frames(self, frames: List[Image.Image]) -> List[float]:
        """Process multiple frames in batch"""
        try:
            # Preprocess all frames
            processed_frames = [n2.preprocess_image(frame, n2.Preprocessing.YAHOO) for frame in frames]

            # Stack into batch
            batch = np.stack(processed_frames)

            # Get predictions
            predictions = self.model.predict(batch, verbose=0)

            # Return NSFW probabilities
            return [float(pred[1]) for pred in predictions]
        except Exception as e:
            self.logger.error(f"Error processing frames: {str(e)}")
            return [1.0] * len(frames)  # Return high scores on error

    def check_gif(self, gif_path: Path) -> Tuple[bool, float]:
        """Check if a GIF contains NSFW content"""
        try:
            with Image.open(str(gif_path)) as gif:
                frames = []
                frame_count = 0

                # Extract frames with proper handling of disposal methods
                while frame_count < 50:  # Limit frames to prevent memory issues
                    try:
                        # Convert to RGB to ensure consistent processing
                        frame = gif.convert('RGB')
                        frames.append(frame.copy())
                        frame_count += 1
                        gif.seek(gif.tell() + 1)
                    except EOFError:
                        break

                if not frames:
                    return True, 1.0  # Err on the side of caution if no frames

                # Process frames in batches
                batch_size = 16
                all_scores = []

                for i in range(0, len(frames), batch_size):
                    batch_frames = frames[i:i + batch_size]
                    scores = self._process_frames(batch_frames)
                    all_scores.extend(scores)

                # Calculate final results
                max_score = max(all_scores)
                avg_score = sum(all_scores) / len(all_scores)
                high_scores = sum(1 for score in all_scores if score > self.threshold)

                # Consider it NSFW if:
                # 1. Any frame has very high NSFW score
                # 2. Average score is high
                # 3. Multiple frames have above-threshold NSFW scores
                is_nsfw = (max_score > self.threshold or
                           avg_score > self.threshold * 0.8 or
                           high_scores >= 2)

                return is_nsfw, max_score

        except Exception as e:
            self.logger.error(f"Error analyzing GIF {gif_path}: {str(e)}")
            return True, 1.0  # Err on the side of caution

    def check_image(self, image_path: Path) -> Tuple[bool, float]:
        """Check if a static image contains NSFW content"""
        try:
            # For single images, we can use the simpler predict_image function
            nsfw_score = n2.predict_image(str(image_path))
            return nsfw_score > self.threshold, nsfw_score
        except Exception as e:
            self.logger.error(f"Error checking image {image_path}: {str(e)}")
            return True, 1.0

    def check_content(self, file_path: Path) -> Tuple[bool, float]:
        """Universal checker that handles both static images and GIFs"""
        try:
            with Image.open(str(file_path)) as img:
                is_gif = getattr(img, "is_animated", False)

            if is_gif:
                return self.check_gif(file_path)
            else:
                return self.check_image(file_path)
        except Exception as e:
            self.logger.error(f"Error determining file type: {str(e)}")
            return True, 1.0


from abc import ABC, abstractmethod
import logging
from typing import Dict, List, Optional
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from threading import Lock
from pathlib import Path
import time


@dataclass
class ScraperState:
    """Thread-safe state tracking for scraper"""
    active_characters: Set[str] = field(default_factory=set)
    completed_characters: Set[str] = field(default_factory=set)
    lock: threading.Lock = field(default_factory=threading.Lock)
    browser_lock: threading.Lock = field(default_factory=threading.Lock)
    logger: logging.Logger = field(default=None)

    def __post_init__(self):
        """Initialize logger after creation"""
        self.logger = logging.getLogger(__name__)

    def is_character_available(self, character: str) -> bool:
        """Check if character is available for processing"""
        self.logger.debug(f"Checking availability for {character}")
        with self.lock:
            is_available = character not in self.active_characters and character not in self.completed_characters
            self.logger.debug(f"{character} availability: {is_available}")
            return is_available

    def start_character(self, character: str) -> bool:
        """Mark character as being processed"""
        self.logger.debug(f"Attempting to start {character}")
        try:
            with self.lock:
                if character not in self.active_characters and character not in self.completed_characters:
                    self.active_characters.add(character)
                    self.logger.debug(f"Successfully started {character}")
                    return True
                self.logger.debug(f"Could not start {character} - already active or completed")
                return False
        except Exception as e:
            self.logger.error(f"Error starting {character}: {str(e)}")
            return False

    def complete_character(self, character: str) -> None:
        """Mark character as completed"""
        self.logger.debug(f"Attempting to complete {character}")
        try:
            with self.lock:
                if character in self.active_characters:
                    self.active_characters.remove(character)
                    self.completed_characters.add(character)
                    self.logger.debug(f"Successfully completed {character}")
        except Exception as e:
            self.logger.error(f"Error completing {character}: {str(e)}")

class HentaiScraper(ABC):
    """Enhanced abstract base class for scrapers with threading support"""

    def __init__(self, config: ScraperConfig):
        """Initialize the scraper with configuration"""
        self.config = config
        self.state = ScraperState()
        self.thread_local = threading.local()
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging with thread information"""
        log_format = '%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s'
        log_level = logging.DEBUG if self.config.verbose_logging else logging.INFO

        # Create a unique log file for each scraper class
        log_file = Path(f'{self.__class__.__name__.lower()}.log')

        # Configure root logger
        logging.basicConfig(
            level=log_level,
            format=log_format,
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

        # Create logger specific to this instance
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def setup(self) -> bool:
        """
        Setup scraper-specific requirements

        Returns:
            bool: True if setup was successful, False otherwise
        """
        pass

    @abstractmethod
    def process_character(self, character: str, urls: List[str], max_pages: int) -> None:
        """
        Process a single character's URLs

        Args:
            character (str): Character name being processed
            urls (List[str]): List of URLs to process for this character
            max_pages (int): Maximum number of pages to process per URL
        """
        pass

    def process_urls(self, urls: Dict[str, List[str]], max_pages: int = 380, max_workers: Optional[int] = None) -> None:
        """
        Process multiple URLs using thread pool

        Args:
            urls (Dict[str, List[str]]): Dictionary mapping character names to lists of URLs
            max_pages (int): Maximum number of pages to process per URL
            max_workers (Optional[int]): Maximum number of worker threads to use
        """
        if max_workers is None:
            max_workers = min(20, len(urls))  # Default to 20 threads or number of characters if less

        self.logger.info(f"Starting scraping with {max_workers} threads")

        # Ensure URLs are in correct format
        processed_urls = {
            char: [url] if isinstance(url, str) else url
            for char, url in urls.items()
        }

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_char = {}

            # Submit jobs to thread pool
            for character, url_list in processed_urls.items():
                if self.state.start_character(character):
                    future = executor.submit(self.process_character, character, url_list, max_pages)
                    future_to_char[future] = character

            # Process completed jobs
            for future in concurrent.futures.as_completed(future_to_char):
                character = future_to_char[future]
                try:
                    future.result()
                    self.logger.info(f"Completed processing for {character}")
                except Exception as e:
                    self.logger.error(f"Error processing {character}: {str(e)}")
                finally:
                    self.state.complete_character(character)

        self.logger.info(f"Completed scraping {len(self.state.completed_characters)} characters")
        self.logger.info("Completed characters: " + ", ".join(sorted(self.state.completed_characters)))

    @abstractmethod
    def cleanup(self) -> None:
        """
        Clean up resources used by the scraper.
        Should be called when scraping is complete or when handling errors.
        """
        pass

    def __enter__(self):
        """Context manager entry"""
        self.setup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()
        if exc_type is not None:
            self.logger.error(f"Error during scraping: {exc_type.__name__}: {exc_val}")
            return False
        return True

class GelbooruScraper(HentaiScraper):
    def __init__(self, config: ScraperConfig):
        self.config = config
        self.nsfw_detector = NSFWDetector(threshold=config.nsfw_threshold)
        self._setup_logging()
        self._setup_browser()
        self.setup()
        self.character_classifier = CharacterClassifier()

    def _setup_safety_model(self):
        """Set up the safety classification model."""
        try:
            from nudenet import NudeDetector
            self.safety_model = NudeDetector()
            self.logger.info("Successfully loaded safety classification model")
        except Exception as e:
            self.logger.error(f"Failed to load safety model: {str(e)}")
            raise

    def _check_image_safety(self, image_path: Path) -> bool:
        """
        Check if image is safe for processing.

        Args:
            image_path (Path): Path to image file

        Returns:
            bool: True if image is safe, False if NSFW
        """
        try:
            # Detect any NSFW content in the image
            detections = self.safety_model.detect(str(image_path))

            # If no detections, image is safe
            if not detections:
                return True

            # Calculate the total confidence of NSFW content
            total_confidence = sum(det['score'] for det in detections)
            avg_confidence = total_confidence / len(detections) if detections else 0

            # Log the safety check
            self.logger.debug(f"Safety check for {image_path}: NSFW confidence = {avg_confidence:.3f}")
            self.logger.debug(f"Detections: {detections}")

            # Return True if safe (average confidence below threshold)
            return avg_confidence < self.config.nsfw_threshold

        except Exception as e:
            self.logger.error(f"Error during safety check for {image_path}: {str(e)}")
            return False  # Fail safe - reject on error

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

    def _setup_browser(self):
        """Set up the Selenium WebDriver with proper configuration."""
        options = webdriver.ChromeOptions()
        if self.config.headless:
            options.add_argument('--headless=new')  # Updated headless argument

        # Add essential Chrome options for stability
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-extensions')
        options.add_argument('--start-maximized')
        options.add_argument(
            f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

        # Create service object for Chrome
        service = webdriver.ChromeService()

        try:
            self.browser = webdriver.Chrome(service=service, options=options)
            self.browser.set_window_size(1920, 1080)
            self.browser.set_page_load_timeout(30)  # Set page load timeout
            self.logger.info("Browser setup successful")
        except Exception as e:
            self.logger.error(f"Failed to initialize browser: {str(e)}")
            raise

    def _wait_for_page_load(self, timeout=30):
        """Wait for page to load completely."""
        try:
            WebDriverWait(self.browser, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            time.sleep(2)  # Small buffer for dynamic content
        except TimeoutException:
            self.logger.warning("Page load timeout - proceeding anyway")

    def _safe_navigate(self, url: str, max_retries=3) -> bool:
        """Safely navigate to a URL with retries."""
        for attempt in range(max_retries):
            try:
                self.browser.get(url)
                self._wait_for_page_load()

                # Verify we actually reached the page
                current_url = self.browser.current_url
                if not current_url or current_url == "about:blank":
                    raise Exception("Navigation failed - blank page")

                return True

            except Exception as e:
                self.logger.warning(f"Navigation attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    self.logger.error(f"Failed to navigate to {url} after {max_retries} attempts")
                    return False
                time.sleep(2 * (attempt + 1))  # Exponential backoff

                # Try to refresh the browser session if we're on the last attempt
                if attempt == max_retries - 2:
                    try:
                        self.browser.quit()
                        self._setup_browser()
                    except Exception as e:
                        self.logger.error(f"Failed to refresh browser session: {str(e)}")

        return False

    def _expand_image(self, page_url: str) -> Optional[str]:
        """Navigate to page and expand the image to get the full resolution URL."""
        if not self._safe_navigate(page_url):
            return None

        try:
            # Wait for the original image to be present first
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img#image"))
            )

            # Execute the resize transition JavaScript function
            self.browser.execute_script("resizeTransition();")

            # Wait for the expansion animation to complete
            time.sleep(2)

            try:
                # Wait for the image src to contain '/images/'
                def check_image_src(driver):
                    img = driver.find_element(By.CSS_SELECTOR, "img#image")
                    src = img.get_attribute("src")
                    return src and "/images/" in src

                # Wait for the condition to be true
                WebDriverWait(self.browser, 10).until(check_image_src)

                # Get the expanded image element and its src
                image = self.browser.find_element(By.CSS_SELECTOR, "img#image")
                src = image.get_attribute('src')

                # Verify we got a valid full-resolution URL
                if not src or not '/images/' in src or src.startswith('data:') or src.startswith('blob:'):
                    self.logger.warning(f"Failed to get full resolution image URL: {src}")
                    return None

                # Log successful expansion
                self.logger.info(f"Successfully retrieved full resolution image URL: {src}")
                return src

            except Exception as wait_error:
                self.logger.error(f"Error waiting for expanded image: {str(wait_error)}")
                return None

        except Exception as e:
            self.logger.error(f"Error expanding image on {page_url}: {str(e)}")

            # Take a screenshot for debugging if enabled
            if hasattr(self.config, 'debug') and self.config.debug:
                try:
                    screenshot_path = self.dirs['logs'] / f"error_screenshot_{int(time.time())}.png"
                    self.browser.save_screenshot(str(screenshot_path))
                    self.logger.debug(f"Error screenshot saved to {screenshot_path}")

                    # Also save page source for debugging
                    page_source_path = self.dirs['logs'] / f"error_source_{int(time.time())}.html"
                    with open(page_source_path, 'w', encoding='utf-8') as f:
                        f.write(self.browser.page_source)
                    self.logger.debug(f"Error page source saved to {page_source_path}")
                except Exception as screenshot_error:
                    self.logger.error(f"Failed to save error screenshot: {screenshot_error}")

            return None

    def _get_character_path(self, url: str, source_page: str) -> Path:
        """Extract character name from URL and create appropriate path"""
        try:
            if source_page and 'tags=' in source_page:
                tags = source_page.split('tags=')[-1].split('&')[0]
                tags = urllib.parse.unquote(tags)

                # Pass source_page to identify_character
                series = self.character_classifier.identify_character(tags, source_page)
                if series[0]:
                    return Path(series[0]) / series[1]

            return Path('raw')
        except Exception as e:
            self.logger.error(f"Error parsing character path: {str(e)}")
            return Path('raw')

    def _download_image(self, url: str, source_page: str = None) -> bool:
        """
        Download and save an image or GIF from the given URL after verifying it's not SFW.

        Args:
            url (str): URL of the image to download
            source_page (str, optional): URL of the page containing the image

        Returns:
            bool: True if download was successful and content is NSFW, False otherwise
        """
        import hashlib
        import mimetypes
        from urllib.parse import urlparse
        import requests
        import urllib.parse
        from requests.exceptions import RequestException
        from PIL import Image

        def _get_file_hash(file_path: Path) -> str:
            """Calculate MD5 hash of file"""
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()

        def _verify_image_file(file_path: Path) -> bool:
            """Verify if file is a valid image using PIL"""
            try:
                with Image.open(file_path) as img:
                    img.verify()
                    return True
            except Exception as e:
                self.logger.error(f"Image verification failed: {str(e)}")
                return False

        try:
            # Clean and validate URL
            if not url:
                self.logger.error("Invalid URL provided")
                return False

            # Get character-specific path
            char_path = self._get_character_path(url, source_page)

            # Generate filename and paths
            filename = self._generate_filename(url)
            temp_path = self.dirs['temp'] / f"temp_{filename}"
            final_path = self.config.base_save_path / char_path / filename

            self.logger.debug(f"Temp path: {temp_path}")
            self.logger.debug(f"Final path: {final_path}")

            # Create directories if they don't exist
            temp_path.parent.mkdir(parents=True, exist_ok=True)
            final_path.parent.mkdir(parents=True, exist_ok=True)

            # Check if file already exists
            if final_path.exists():
                self.logger.info(f"File already exists at {final_path}")
                return True

            # Download file with proper headers
            headers = {
                'User-Agent': self.config.user_agent,
                'Accept': 'image/webp,image/apng,image/gif,image/*,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': source_page if source_page else url
            }

            response = requests.get(url, stream=True, headers=headers, timeout=self.config.request_timeout)
            response.raise_for_status()

            # Save to temporary file
            self.logger.debug(f"Downloading to temporary file: {temp_path}")
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=self.config.chunk_size):
                    if chunk:
                        f.write(chunk)

            # Verify the file exists and is not empty
            if not temp_path.exists() or temp_path.stat().st_size == 0:
                raise ValueError("Downloaded file is empty or missing")

            # Verify it's a valid image/GIF file
            try:
                with Image.open(temp_path) as img:
                    img.verify()
                    is_gif = getattr(img, "is_animated", False)
            except Exception as e:
                self.logger.error(f"Invalid image file: {str(e)}")
                temp_path.unlink()
                return False

            # Check if content is NSFW
            is_nsfw, confidence = self.nsfw_detector.check_content(temp_path)

            if is_nsfw:  # Keep NSFW content
                # Calculate file hash
                file_hash = _get_file_hash(temp_path)

                # Move file to final location
                self.logger.debug(f"Moving file to final location: {final_path}")
                temp_path.rename(final_path)

                # Record successful download
                file_size = final_path.stat().st_size
                self._record_download(
                    url=url,
                    filename=filename,
                    status='success',
                    file_size=file_size,
                    md5_hash=file_hash,
                    source_page=source_page
                )

                self.logger.info(
                    f"Successfully downloaded NSFW {'GIF' if is_gif else 'image'}: "
                    f"{filename} ({file_size:,} bytes) to {final_path}"
                )
                return True
            else:
                self.logger.warning(
                    f"Skipping SFW {'GIF' if is_gif else 'image'} from {url} "
                    f"(confidence: {confidence:.2f})"
                )
                temp_path.unlink()
                return False

        except Exception as e:
            self.logger.error(f"Error downloading {url}: {str(e)}")
            if 'temp_path' in locals() and temp_path.exists():
                try:
                    temp_path.unlink()
                except Exception as cleanup_error:
                    self.logger.error(f"Error cleaning up temporary file: {cleanup_error}")
            return False

        except Exception as e:
            self.logger.error(f"Error downloading {url}: {str(e)}")
            if 'temp_path' in locals() and temp_path.exists():
                try:
                    temp_path.unlink()
                except Exception as cleanup_error:
                    self.logger.error(f"Error cleaning up temporary file: {cleanup_error}")
            return False

    def _generate_filename(self, url: str) -> str:
        """
        Generate a unique filename for the downloaded image.

        Args:
            url (str): Source URL of the image

        Returns:
            str: Generated filename
        """
        # Extract original extension if possible
        ext = os.path.splitext(urlparse(url).path)[1].lower()
        if not ext or ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            ext = '.jpg'  # Default to .jpg if no valid extension found

        # Generate random component
        random_suffix = ''.join(random.choices(
            string.ascii_lowercase + string.digits,
            k=self.config.filename_length
        ))

        # Create timestamp component
        timestamp = time.strftime('%Y%m%d_%H%M%S')

        # Combine components
        filename = f"img_{timestamp}_{random_suffix}{ext}"

        return filename

    def setup(self):
        """
        Perform initial setup operations including directory creation and validation.
        Creates the base directory structure and character subdirectories.
        """
        self.logger.info("Starting setup...")
        try:
            # Create base directory
            self.config.base_save_path.mkdir(parents=True, exist_ok=True)

            # Create subdirectories for organizing content
            subdirs = {
                'raw': self.config.base_save_path / 'raw',  # Store original downloads
                'processed': self.config.base_save_path / 'processed',  # Store processed images
                'metadata': self.config.base_save_path / 'metadata',  # Store JSON metadata
                'logs': self.config.base_save_path / 'logs',  # Store detailed logs
                'temp': self.config.base_save_path / 'temp'  # Temporary storage
            }

            # Create each subdirectory
            for dir_name, path in subdirs.items():
                path.mkdir(exist_ok=True)
                self.logger.info(f"Created directory: {path}")

            # Create or update metadata index
            metadata_file = subdirs['metadata'] / 'index.json'
            if not metadata_file.exists():
                metadata_file.write_text('{}')
                self.logger.info("Created new metadata index")

            # Validate directory permissions
            for dir_path in subdirs.values():
                if not os.access(dir_path, os.W_OK):
                    raise PermissionError(f"No write permission for directory: {dir_path}")

            # Create .gitignore if using version control
            gitignore_path = self.config.base_save_path / '.gitignore'
            if not gitignore_path.exists():
                gitignore_content = """
                   # Ignore temporary files
                   temp/
                   *.tmp

                   # Ignore logs
                   logs/
                   *.log

                   # Ignore raw downloads
                   raw/

                   # Ignore system files
                   .DS_Store
                   Thumbs.db
                   """
                gitignore_path.write_text(gitignore_content.strip())

            # Create status tracking file
            status_file = subdirs['metadata'] / 'status.json'
            if not status_file.exists():
                status_content = {
                    'last_run': None,
                    'total_downloads': 0,
                    'successful_downloads': 0,
                    'failed_downloads': 0,
                    'last_processed_url': None
                }
                import json
                with open(status_file, 'w') as f:
                    json.dump(status_content, f, indent=4)

            # Initialize download tracking database
            import sqlite3
            db_path = subdirs['metadata'] / 'downloads.db'
            conn = sqlite3.connect(str(db_path))
            c = conn.cursor()

            # Create downloads tracking table
            c.execute('''
                   CREATE TABLE IF NOT EXISTS downloads (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       url TEXT NOT NULL UNIQUE,
                       filename TEXT NOT NULL,
                       timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                       status TEXT,
                       file_size INTEGER,
                       md5_hash TEXT,
                       source_page TEXT
                   )
               ''')

            # Create failed downloads table
            c.execute('''
                   CREATE TABLE IF NOT EXISTS failed_downloads (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       url TEXT NOT NULL,
                       timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                       error_message TEXT,
                       attempts INTEGER DEFAULT 1
                   )
               ''')

            conn.commit()
            conn.close()

            # Update scraper attributes
            self.dirs = subdirs
            self.db_path = db_path

            self.logger.info("Setup completed successfully")
            return True

        except Exception as e:
            self.logger.error(f"Setup failed: {str(e)}")
            raise

    def _init_database_connection(self):
        """Initialize database connection and return connection object"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            return conn
        except Exception as e:
            self.logger.error(f"Failed to connect to database: {str(e)}")
            raise

    def _record_download(self, url: str, filename: str, status: str, file_size: int = None,
                         md5_hash: str = None, source_page: str = None):
        """Record download attempt in database"""
        try:
            conn = self._init_database_connection()
            c = conn.cursor()

            c.execute('''
                   INSERT INTO downloads 
                   (url, filename, status, file_size, md5_hash, source_page)
                   VALUES (?, ?, ?, ?, ?, ?)
               ''', (url, filename, status, file_size, md5_hash, source_page))

            conn.commit()
            conn.close()
        except Exception as e:
            self.logger.error(f"Failed to record download: {str(e)}")

    def _record_failure(self, url: str, error_message: str):
        """Record failed download attempt"""
        try:
            conn = self._init_database_connection()
            c = conn.cursor()

            # Check if URL already exists in failed_downloads
            c.execute('SELECT attempts FROM failed_downloads WHERE url = ?', (url,))
            result = c.fetchone()

            if result:
                # Update existing record
                c.execute('''
                       UPDATE failed_downloads 
                       SET attempts = attempts + 1,
                           error_message = ?,
                           timestamp = CURRENT_TIMESTAMP
                       WHERE url = ?
                   ''', (error_message, url))
            else:
                # Create new record
                c.execute('''
                       INSERT INTO failed_downloads (url, error_message)
                       VALUES (?, ?)
                   ''', (url, error_message))

            conn.commit()
            conn.close()
        except Exception as e:
            self.logger.error(f"Failed to record failure: {str(e)}")

    def process_urls(self, urls: Dict[str, str], max_pages: int = 380):
        """Process multiple URLs and download images with improved error handling and timeout management."""
        processed_count = 0

        try:
            for search_term, base_url in urls.items():
                self.logger.info(f"Processing search term: {search_term}")
                timeout_occurred = False

                for page_num in range(max_pages):
                    # Check if timeout occurred for this character
                    if timeout_occurred:
                        self.logger.info(f"Skipping remaining pages for {search_term} due to timeout")
                        break

                    current_url = f"{base_url}&pid={page_num * 42}" if page_num > 0 else base_url
                    self.logger.info(f"Processing page {page_num + 1}: {current_url}")

                    # Navigate to page with retry logic
                    if not self._safe_navigate(current_url):
                        self.logger.error(f"Skipping page {page_num + 1} due to navigation failure")
                        continue

                    try:
                        # Wait for thumbnail container to be present
                        WebDriverWait(self.browser, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "div.thumbnail-container"))
                        )

                        # Find all image links with explicit wait
                        links = WebDriverWait(self.browser, 10).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.thumbnail-preview a"))
                        )

                        image_urls = [link.get_attribute('href') for link in links if link.get_attribute('href')]
                        self.logger.info(f"Found {len(image_urls)} images on page {page_num + 1}")

                        for img_url in image_urls:
                            try:
                                full_image_url = self._expand_image(img_url)
                                if full_image_url:
                                    save_path = self.config.base_save_path
                                    save_path.mkdir(parents=True, exist_ok=True)

                                    if self._download_image(full_image_url, img_url):
                                        processed_count += 1
                                        time.sleep(self.config.download_delay)

                            except Exception as e:
                                self.logger.error(f"Error processing {img_url}: {str(e)}")
                                continue

                        # Add a page delay
                        time.sleep(self.config.page_delay)

                    except TimeoutException:
                        self.logger.error(f"Timeout on page {page_num + 1} for character {search_term}")
                        timeout_occurred = True  # Set flag to skip to next character
                        break  # Break the page loop to move to next character
                    except Exception as e:
                        self.logger.error(f"Error processing page {page_num + 1}: {str(e)}")
                        continue

                # Log completion or timeout for current character
                if timeout_occurred:
                    self.logger.info(f"Moving to next character due to timeout on {search_term}")
                else:
                    self.logger.info(f"Completed processing for {search_term}")

        except Exception as e:
            self.logger.error(f"Fatal error in process_urls: {str(e)}")
        finally:
            self.logger.info(f"Processed {processed_count} images successfully")
            try:
                self.browser.quit()
            except Exception as e:
                self.logger.error(f"Error closing browser: {str(e)}")

    # def __init__(self, config: ScraperConfig):
    #     self.config = config
    #     self.nsfw_detector = NSFWDetector(threshold=config.nsfw_threshold)
    #     self._setup_logging()
    #     self._setup_browser()
    #     self.setup()
    #
    # def _setup_safety_model(self):
    #     """Set up the safety classification model."""
    #     try:
    #         from nudenet import NudeDetector
    #         self.safety_model = NudeDetector()
    #         self.logger.info("Successfully loaded safety classification model")
    #     except Exception as e:
    #         self.logger.error(f"Failed to load safety model: {str(e)}")
    #         raise
    #
    # def _check_image_safety(self, image_path: Path) -> bool:
    #     """
    #     Check if image is safe for processing.
    #
    #     Args:
    #         image_path (Path): Path to image file
    #
    #     Returns:
    #         bool: True if image is safe, False if NSFW
    #     """
    #     try:
    #         # Detect any NSFW content in the image
    #         detections = self.safety_model.detect(str(image_path))
    #
    #         # If no detections, image is safe
    #         if not detections:
    #             return True
    #
    #         # Calculate the total confidence of NSFW content
    #         total_confidence = sum(det['score'] for det in detections)
    #         avg_confidence = total_confidence / len(detections) if detections else 0
    #
    #         # Log the safety check
    #         self.logger.debug(f"Safety check for {image_path}: NSFW confidence = {avg_confidence:.3f}")
    #         self.logger.debug(f"Detections: {detections}")
    #
    #         # Return True if safe (average confidence below threshold)
    #         return avg_confidence < self.config.nsfw_threshold
    #
    #     except Exception as e:
    #         self.logger.error(f"Error during safety check for {image_path}: {str(e)}")
    #         return False  # Fail safe - reject on error
    #
    # def _setup_logging(self):
    #     """Configure logging for the scraper."""
    #     logging.basicConfig(
    #         level=logging.INFO,
    #         format='%(asctime)s - %(levelname)s - %(message)s',
    #         handlers=[
    #             logging.FileHandler('scraper.log'),
    #             logging.StreamHandler()
    #         ]
    #     )
    #     self.logger = logging.getLogger(__name__)
    #
    # def _setup_browser(self):
    #     """Set up the Selenium WebDriver with proper configuration."""
    #     options = webdriver.ChromeOptions()
    #     if self.config.headless:
    #         options.add_argument('--headless=new')  # Updated headless argument
    #
    #     # Add essential Chrome options for stability
    #     options.add_argument('--no-sandbox')
    #     options.add_argument('--disable-dev-shm-usage')
    #     options.add_argument('--disable-gpu')
    #     options.add_argument('--disable-software-rasterizer')
    #     options.add_argument('--disable-extensions')
    #     options.add_argument('--start-maximized')
    #     options.add_argument(
    #         f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    #
    #     # Create service object for Chrome
    #     service = webdriver.ChromeService()
    #
    #     try:
    #         self.browser = webdriver.Chrome(service=service, options=options)
    #         self.browser.set_window_size(1920, 1080)
    #         self.browser.set_page_load_timeout(30)  # Set page load timeout
    #         self.logger.info("Browser setup successful")
    #     except Exception as e:
    #         self.logger.error(f"Failed to initialize browser: {str(e)}")
    #         raise
    #
    #
    #
    # def _wait_for_page_load(self, timeout=30):
    #     """Wait for page to load completely."""
    #     try:
    #         WebDriverWait(self.browser, timeout).until(
    #             lambda driver: driver.execute_script("return document.readyState") == "complete"
    #         )
    #         time.sleep(2)  # Small buffer for dynamic content
    #     except TimeoutException:
    #         self.logger.warning("Page load timeout - proceeding anyway")
    #
    # def _safe_navigate(self, url: str, max_retries=3) -> bool:
    #     """Safely navigate to a URL with retries."""
    #     for attempt in range(max_retries):
    #         try:
    #             self.browser.get(url)
    #             self._wait_for_page_load()
    #
    #             # Verify we actually reached the page
    #             current_url = self.browser.current_url
    #             if not current_url or current_url == "about:blank":
    #                 raise Exception("Navigation failed - blank page")
    #
    #             return True
    #
    #         except Exception as e:
    #             self.logger.warning(f"Navigation attempt {attempt + 1} failed: {str(e)}")
    #             if attempt == max_retries - 1:
    #                 self.logger.error(f"Failed to navigate to {url} after {max_retries} attempts")
    #                 return False
    #             time.sleep(2 * (attempt + 1))  # Exponential backoff
    #
    #             # Try to refresh the browser session if we're on the last attempt
    #             if attempt == max_retries - 2:
    #                 try:
    #                     self.browser.quit()
    #                     self._setup_browser()
    #                 except Exception as e:
    #                     self.logger.error(f"Failed to refresh browser session: {str(e)}")
    #
    #     return False
    #
    # def _expand_image(self, page_url: str) -> Optional[str]:
    #     """Navigate to page and expand the image to get the full resolution URL."""
    #     if not self._safe_navigate(page_url):
    #         return None
    #
    #     try:
    #         # Wait for the original image to be present first
    #         WebDriverWait(self.browser, 10).until(
    #             EC.presence_of_element_located((By.CSS_SELECTOR, "img#image"))
    #         )
    #
    #         # Execute the resize transition JavaScript function
    #         self.browser.execute_script("resizeTransition();")
    #
    #         # Wait for the expansion animation to complete
    #         time.sleep(2)
    #
    #         try:
    #             # Wait for the image src to contain '/images/'
    #             def check_image_src(driver):
    #                 img = driver.find_element(By.CSS_SELECTOR, "img#image")
    #                 src = img.get_attribute("src")
    #                 return src and "/images/" in src
    #
    #             # Wait for the condition to be true
    #             WebDriverWait(self.browser, 10).until(check_image_src)
    #
    #             # Get the expanded image element and its src
    #             image = self.browser.find_element(By.CSS_SELECTOR, "img#image")
    #             src = image.get_attribute('src')
    #
    #             # Verify we got a valid full-resolution URL
    #             if not src or not '/images/' in src or src.startswith('data:') or src.startswith('blob:'):
    #                 self.logger.warning(f"Failed to get full resolution image URL: {src}")
    #                 return None
    #
    #             # Log successful expansion
    #             self.logger.info(f"Successfully retrieved full resolution image URL: {src}")
    #             return src
    #
    #         except Exception as wait_error:
    #             self.logger.error(f"Error waiting for expanded image: {str(wait_error)}")
    #             return None
    #
    #     except Exception as e:
    #         self.logger.error(f"Error expanding image on {page_url}: {str(e)}")
    #
    #         # Take a screenshot for debugging if enabled
    #         if hasattr(self.config, 'debug') and self.config.debug:
    #             try:
    #                 screenshot_path = self.dirs['logs'] / f"error_screenshot_{int(time.time())}.png"
    #                 self.browser.save_screenshot(str(screenshot_path))
    #                 self.logger.debug(f"Error screenshot saved to {screenshot_path}")
    #
    #                 # Also save page source for debugging
    #                 page_source_path = self.dirs['logs'] / f"error_source_{int(time.time())}.html"
    #                 with open(page_source_path, 'w', encoding='utf-8') as f:
    #                     f.write(self.browser.page_source)
    #                 self.logger.debug(f"Error page source saved to {page_source_path}")
    #             except Exception as screenshot_error:
    #                 self.logger.error(f"Failed to save error screenshot: {screenshot_error}")
    #
    #         return None
    #
    # def _get_character_path(self, url: str, source_page: str) -> Path:
    #     """Extract character name from URL and create appropriate path."""
    #     try:
    #         # Extract tags from source page URL
    #         if 'tags=' in source_page:
    #             tags = source_page.split('tags=')[-1].split('&')[0]
    #             tags = urllib.parse.unquote(tags)  # Decode URL-encoded characters
    #
    #             # Parse character name from tags
    #             if '(' in tags and ')' in tags:
    #                 # Handle tags like "uta_(one_piece)"
    #                 character_tags = [tag for tag in tags.split() if '(' in tag and ')' in tag]
    #                 if character_tags:
    #                     character = character_tags[0]
    #                     series = character.split('(')[1].rstrip(')')
    #                     character_name = character.split('(')[0].rstrip('_')
    #
    #                     # Check if the character name matches any of the names in the CHARACTER_MAPPINGS
    #                     for franchise, characters in self.CHARACTER_MAPPINGS.items():
    #                         for primary_name, aliases in characters.items():
    #                             if character_name.lower() in [alias.lower() for alias in aliases]:
    #                                 return Path(franchise) / primary_name
    #
    #         # Default to raw directory if no character info found
    #         return Path('raw')
    #     except Exception as e:
    #         self.logger.error(f"Error parsing character path: {str(e)}")
    #         return Path('raw')
    #
    # def _download_image(self, url: str, source_page: str = None) -> bool:
    #     """
    #     Download and save an image or GIF from the given URL after verifying it's not SFW.
    #
    #     Args:
    #         url (str): URL of the image to download
    #         source_page (str, optional): URL of the page containing the image
    #
    #     Returns:
    #         bool: True if download was successful and content is NSFW, False otherwise
    #     """
    #     import hashlib
    #     import mimetypes
    #     from urllib.parse import urlparse
    #     import requests
    #     import urllib.parse
    #     from requests.exceptions import RequestException
    #     from PIL import Image
    #
    #     def _get_file_hash(file_path: Path) -> str:
    #         """Calculate MD5 hash of file"""
    #         hash_md5 = hashlib.md5()
    #         with open(file_path, "rb") as f:
    #             for chunk in iter(lambda: f.read(4096), b""):
    #                 hash_md5.update(chunk)
    #         return hash_md5.hexdigest()
    #
    #     def _verify_image_file(file_path: Path) -> bool:
    #         """Verify if file is a valid image using PIL"""
    #         try:
    #             with Image.open(file_path) as img:
    #                 img.verify()
    #                 return True
    #         except Exception as e:
    #             self.logger.error(f"Image verification failed: {str(e)}")
    #             return False
    #
    #     try:
    #         # Clean and validate URL
    #         if not url:
    #             self.logger.error("Invalid URL provided")
    #             return False
    #
    #         # Get character-specific path
    #         char_path = self._get_character_path(url, source_page)
    #
    #         # Generate filename and paths
    #         filename = self._generate_filename(url)
    #         temp_path = self.dirs['temp'] / f"temp_{filename}"
    #         final_path = self.config.base_save_path / char_path / filename
    #
    #         self.logger.debug(f"Temp path: {temp_path}")
    #         self.logger.debug(f"Final path: {final_path}")
    #
    #         # Create directories if they don't exist
    #         temp_path.parent.mkdir(parents=True, exist_ok=True)
    #         final_path.parent.mkdir(parents=True, exist_ok=True)
    #
    #         # Check if file already exists
    #         if final_path.exists():
    #             self.logger.info(f"File already exists at {final_path}")
    #             return True
    #
    #         # Download file with proper headers
    #         headers = {
    #             'User-Agent': self.config.user_agent,
    #             'Accept': 'image/webp,image/apng,image/gif,image/*,*/*;q=0.8',
    #             'Accept-Language': 'en-US,en;q=0.9',
    #             'Referer': source_page if source_page else url
    #         }
    #
    #         response = requests.get(url, stream=True, headers=headers, timeout=self.config.request_timeout)
    #         response.raise_for_status()
    #
    #         # Save to temporary file
    #         self.logger.debug(f"Downloading to temporary file: {temp_path}")
    #         with open(temp_path, 'wb') as f:
    #             for chunk in response.iter_content(chunk_size=self.config.chunk_size):
    #                 if chunk:
    #                     f.write(chunk)
    #
    #         # Verify the file exists and is not empty
    #         if not temp_path.exists() or temp_path.stat().st_size == 0:
    #             raise ValueError("Downloaded file is empty or missing")
    #
    #         # Verify it's a valid image/GIF file
    #         try:
    #             with Image.open(temp_path) as img:
    #                 img.verify()
    #                 is_gif = getattr(img, "is_animated", False)
    #         except Exception as e:
    #             self.logger.error(f"Invalid image file: {str(e)}")
    #             temp_path.unlink()
    #             return False
    #
    #         # Check if content is NSFW
    #         is_nsfw, confidence = self.nsfw_detector.check_content(temp_path)
    #
    #         if is_nsfw:  # Keep NSFW content
    #             # Calculate file hash
    #             file_hash = _get_file_hash(temp_path)
    #
    #             # Move file to final location
    #             self.logger.debug(f"Moving file to final location: {final_path}")
    #             temp_path.rename(final_path)
    #
    #             # Record successful download
    #             file_size = final_path.stat().st_size
    #             self._record_download(
    #                 url=url,
    #                 filename=filename,
    #                 status='success',
    #                 file_size=file_size,
    #                 md5_hash=file_hash,
    #                 source_page=source_page
    #             )
    #
    #             self.logger.info(
    #                 f"Successfully downloaded NSFW {'GIF' if is_gif else 'image'}: "
    #                 f"{filename} ({file_size:,} bytes) to {final_path}"
    #             )
    #             return True
    #         else:
    #             self.logger.warning(
    #                 f"Skipping SFW {'GIF' if is_gif else 'image'} from {url} "
    #                 f"(confidence: {confidence:.2f})"
    #             )
    #             temp_path.unlink()
    #             return False
    #
    #     except Exception as e:
    #         self.logger.error(f"Error downloading {url}: {str(e)}")
    #         if 'temp_path' in locals() and temp_path.exists():
    #             try:
    #                 temp_path.unlink()
    #             except Exception as cleanup_error:
    #                 self.logger.error(f"Error cleaning up temporary file: {cleanup_error}")
    #         return False
    #
    #     except Exception as e:
    #         self.logger.error(f"Error downloading {url}: {str(e)}")
    #         if 'temp_path' in locals() and temp_path.exists():
    #             try:
    #                 temp_path.unlink()
    #             except Exception as cleanup_error:
    #                 self.logger.error(f"Error cleaning up temporary file: {cleanup_error}")
    #         return False
    #
    # def _generate_filename(self, url: str) -> str:
    #     """
    #     Generate a unique filename for the downloaded image.
    #
    #     Args:
    #         url (str): Source URL of the image
    #
    #     Returns:
    #         str: Generated filename
    #     """
    #     # Extract original extension if possible
    #     ext = os.path.splitext(urlparse(url).path)[1].lower()
    #     if not ext or ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
    #         ext = '.jpg'  # Default to .jpg if no valid extension found
    #
    #     # Generate random component
    #     random_suffix = ''.join(random.choices(
    #         string.ascii_lowercase + string.digits,
    #         k=self.config.filename_length
    #     ))
    #
    #     # Create timestamp component
    #     timestamp = time.strftime('%Y%m%d_%H%M%S')
    #
    #     # Combine components
    #     filename = f"img_{timestamp}_{random_suffix}{ext}"
    #
    #     return filename
    #
    # def setup(self):
    #     """
    #     Perform initial setup operations including directory creation and validation.
    #     Creates the base directory structure and character subdirectories.
    #     """
    #     self.logger.info("Starting setup...")
    #     try:
    #         # Create base directory
    #         self.config.base_save_path.mkdir(parents=True, exist_ok=True)
    #
    #         # Create subdirectories for organizing content
    #         subdirs = {
    #             'raw': self.config.base_save_path / 'raw',  # Store original downloads
    #             'processed': self.config.base_save_path / 'processed',  # Store processed images
    #             'metadata': self.config.base_save_path / 'metadata',  # Store JSON metadata
    #             'logs': self.config.base_save_path / 'logs',  # Store detailed logs
    #             'temp': self.config.base_save_path / 'temp'  # Temporary storage
    #         }
    #
    #         # Create each subdirectory
    #         for dir_name, path in subdirs.items():
    #             path.mkdir(exist_ok=True)
    #             self.logger.info(f"Created directory: {path}")
    #
    #         # Create or update metadata index
    #         metadata_file = subdirs['metadata'] / 'index.json'
    #         if not metadata_file.exists():
    #             metadata_file.write_text('{}')
    #             self.logger.info("Created new metadata index")
    #
    #         # Validate directory permissions
    #         for dir_path in subdirs.values():
    #             if not os.access(dir_path, os.W_OK):
    #                 raise PermissionError(f"No write permission for directory: {dir_path}")
    #
    #         # Create .gitignore if using version control
    #         gitignore_path = self.config.base_save_path / '.gitignore'
    #         if not gitignore_path.exists():
    #             gitignore_content = """
    #             # Ignore temporary files
    #             temp/
    #             *.tmp
    #
    #             # Ignore logs
    #             logs/
    #             *.log
    #
    #             # Ignore raw downloads
    #             raw/
    #
    #             # Ignore system files
    #             .DS_Store
    #             Thumbs.db
    #             """
    #             gitignore_path.write_text(gitignore_content.strip())
    #
    #         # Create status tracking file
    #         status_file = subdirs['metadata'] / 'status.json'
    #         if not status_file.exists():
    #             status_content = {
    #                 'last_run': None,
    #                 'total_downloads': 0,
    #                 'successful_downloads': 0,
    #                 'failed_downloads': 0,
    #                 'last_processed_url': None
    #             }
    #             import json
    #             with open(status_file, 'w') as f:
    #                 json.dump(status_content, f, indent=4)
    #
    #         # Initialize download tracking database
    #         import sqlite3
    #         db_path = subdirs['metadata'] / 'downloads.db'
    #         conn = sqlite3.connect(str(db_path))
    #         c = conn.cursor()
    #
    #         # Create downloads tracking table
    #         c.execute('''
    #             CREATE TABLE IF NOT EXISTS downloads (
    #                 id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                 url TEXT NOT NULL UNIQUE,
    #                 filename TEXT NOT NULL,
    #                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    #                 status TEXT,
    #                 file_size INTEGER,
    #                 md5_hash TEXT,
    #                 source_page TEXT
    #             )
    #         ''')
    #
    #         # Create failed downloads table
    #         c.execute('''
    #             CREATE TABLE IF NOT EXISTS failed_downloads (
    #                 id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                 url TEXT NOT NULL,
    #                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    #                 error_message TEXT,
    #                 attempts INTEGER DEFAULT 1
    #             )
    #         ''')
    #
    #         conn.commit()
    #         conn.close()
    #
    #         # Update scraper attributes
    #         self.dirs = subdirs
    #         self.db_path = db_path
    #
    #         self.logger.info("Setup completed successfully")
    #         return True
    #
    #     except Exception as e:
    #         self.logger.error(f"Setup failed: {str(e)}")
    #         raise
    #
    # def _init_database_connection(self):
    #     """Initialize database connection and return connection object"""
    #     try:
    #         conn = sqlite3.connect(str(self.db_path))
    #         return conn
    #     except Exception as e:
    #         self.logger.error(f"Failed to connect to database: {str(e)}")
    #         raise
    #
    # def _record_download(self, url: str, filename: str, status: str, file_size: int = None,
    #                      md5_hash: str = None, source_page: str = None):
    #     """Record download attempt in database"""
    #     try:
    #         conn = self._init_database_connection()
    #         c = conn.cursor()
    #
    #         c.execute('''
    #             INSERT INTO downloads
    #             (url, filename, status, file_size, md5_hash, source_page)
    #             VALUES (?, ?, ?, ?, ?, ?)
    #         ''', (url, filename, status, file_size, md5_hash, source_page))
    #
    #         conn.commit()
    #         conn.close()
    #     except Exception as e:
    #         self.logger.error(f"Failed to record download: {str(e)}")
    #
    # def _record_failure(self, url: str, error_message: str):
    #     """Record failed download attempt"""
    #     try:
    #         conn = self._init_database_connection()
    #         c = conn.cursor()
    #
    #         # Check if URL already exists in failed_downloads
    #         c.execute('SELECT attempts FROM failed_downloads WHERE url = ?', (url,))
    #         result = c.fetchone()
    #
    #         if result:
    #             # Update existing record
    #             c.execute('''
    #                 UPDATE failed_downloads
    #                 SET attempts = attempts + 1,
    #                     error_message = ?,
    #                     timestamp = CURRENT_TIMESTAMP
    #                 WHERE url = ?
    #             ''', (error_message, url))
    #         else:
    #             # Create new record
    #             c.execute('''
    #                 INSERT INTO failed_downloads (url, error_message)
    #                 VALUES (?, ?)
    #             ''', (url, error_message))
    #
    #         conn.commit()
    #         conn.close()
    #     except Exception as e:
    #         self.logger.error(f"Failed to record failure: {str(e)}")
    #
    # def _get_character_path(self, url: str, source_page: str) -> Path:
    #     """Extract character name from URL and create appropriate path."""
    #     try:
    #         # Extract tags from source page URL
    #         if 'tags=' in source_page:
    #             tags = source_page.split('tags=')[-1].split('&')[0]
    #             tags = urllib.parse.unquote(tags)  # Decode URL-encoded characters
    #
    #             # Parse character name from tags
    #             if '(' in tags and ')' in tags:
    #                 # Handle tags like "uta_(one_piece)"
    #                 character_tags = [tag for tag in tags.split() if '(' in tag and ')' in tag]
    #                 if character_tags:
    #                     character = character_tags[0]
    #                     series = character.split('(')[1].rstrip(')')
    #                     character_name = character.split('(')[0].rstrip('_')
    #                     return Path(series) / character_name
    #
    #         # Default to raw directory if no character info found
    #         return Path('raw')
    #     except Exception as e:
    #         self.logger.error(f"Error parsing character path: {str(e)}")
    #         return Path('raw')
    #
    # def _process_page(self, url: str, character: str, processed_count: int) -> int:
    #     """Process a single page of results"""
    #     if not self._safe_navigate(url):
    #         return processed_count
    #
    #     try:
    #         links = WebDriverWait(self.browser, 10).until(
    #             EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.thumbnail-preview a"))
    #         )
    #
    #         image_urls = [link.get_attribute('href') for link in links if link.get_attribute('href')]
    #         self.logger.info(f"Found {len(image_urls)} images on page")
    #
    #         for img_url in image_urls:
    #             try:
    #                 full_image_url = self._expand_image(img_url)
    #                 if full_image_url and self._download_image(full_image_url, img_url):
    #                     processed_count += 1
    #                     time.sleep(self.config.download_delay)
    #             except Exception as e:
    #                 self.logger.error(f"Error processing {img_url}: {str(e)}")
    #
    #     except TimeoutException:
    #         self.logger.error(f"Timeout on page for character {character}")
    #         return processed_count
    #
    #     return processed_count
    #
    # def process_urls(self, urls: Dict[str, List[str]], max_pages: int = 380):
    #     """Process Gelbooru URLs"""
    #     processed_count = 0
    #
    #     try:
    #         for character, url_list in urls.items():
    #             self.logger.info(f"Processing character: {character}")
    #
    #             for base_url in url_list:
    #                 timeout_occurred = False
    #
    #                 for page_num in range(max_pages):
    #                     if timeout_occurred:
    #                         self.logger.info(f"Skipping remaining pages for {character} due to timeout")
    #                         break
    #
    #                     current_url = f"{base_url}&pid={page_num * 42}" if page_num > 0 else base_url
    #                     self._process_page(current_url, character, processed_count)
    #                     time.sleep(self.config.page_delay)
    #
    #     except Exception as e:
    #         self.logger.error(f"Fatal error in process_urls: {str(e)}")
    #     finally:
    #         self.logger.info(f"Processed {processed_count} images successfully")
    #         try:
    #             self.browser.quit()
    #         except Exception as e:
    #             self.logger.error(f"Error closing browser: {str(e)}")


class URLManager:
    """Manages URLs for different characters and sources"""

    @staticmethod
    def load_urls(filename: str) -> Dict[str, Dict[str, List[str]]]:
        """Load URLs from configuration file"""
        # Implementation for loading URLs from file
        pass

    @staticmethod
    def get_urls_for_scraper(scraper_type: str, urls: Dict[str, Dict[str, List[str]]]) -> Dict[str, List[str]]:
        """Get URLs specific to a scraper type"""
        return urls.get(scraper_type, {})


class ThreadedGelbooruScraper(HentaiScraper):
    def __init__(self, config: ScraperConfig):
        # Initialize logger first, before anything else
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

        # Now proceed with other initialization
        self.logger.info("Initializing ThreadedGelbooruScraper")
        self.config = config

        # Initialize important attributes
        self.thread_local = threading.local()
        self.state = ScraperState()
        self.db_lock = threading.Lock()
        self.character_classifier = CharacterClassifier()
        self.nsfw_detector = NSFWDetector(threshold=config.nsfw_threshold)

        # Create base directories
        self.dirs = {
            'raw': self.config.base_save_path / 'raw',
            'processed': self.config.base_save_path / 'processed',
            'metadata': self.config.base_save_path / 'metadata',
            'logs': self.config.base_save_path / 'logs',
            'temp': self.config.base_save_path / 'temp'
        }

        # Run setup
        self.setup()
        self.logger.info("ThreadedGelbooruScraper initialization complete")

    def _setup_logging(self):
        """Configure logging for the scraper."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def _setup_safety_model(self):
        """Set up the safety classification model."""
        try:
            from nudenet import NudeDetector
            self.safety_model = NudeDetector()
            self.logger.info("Successfully loaded safety classification model")
        except Exception as e:
            self.logger.error(f"Failed to load safety model: {str(e)}")
            raise

    def setup(self) -> bool:
        """Implementation of abstract setup method"""
        self.logger.info("Starting setup...")
        try:
            # Create base directory
            self.config.base_save_path.mkdir(parents=True, exist_ok=True)

            # Create directories
            for dir_name, path in self.dirs.items():
                path.mkdir(exist_ok=True)
                self.logger.info(f"Created directory: {path}")

            # Validate permissions
            for dir_path in self.dirs.values():
                if not os.access(dir_path, os.W_OK):
                    raise PermissionError(f"No write permission for directory: {dir_path}")

            # Create metadata index
            metadata_file = self.dirs['metadata'] / 'index.json'
            if not metadata_file.exists():
                metadata_file.write_text('{}')
                self.logger.info("Created new metadata index")

            # Create status file
            status_file = self.dirs['metadata'] / 'status.json'
            if not status_file.exists():
                status_content = {
                    'last_run': None,
                    'total_downloads': 0,
                    'successful_downloads': 0,
                    'failed_downloads': 0,
                    'last_processed_url': None
                }
                with open(status_file, 'w') as f:
                    json.dump(status_content, f, indent=4)

            # Initialize database
            self.db_path = self.dirs['metadata'] / 'downloads.db'
            conn = sqlite3.connect(str(self.db_path))
            c = conn.cursor()

            # Create tables
            c.execute('''
                   CREATE TABLE IF NOT EXISTS downloads (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       url TEXT NOT NULL UNIQUE,
                       filename TEXT NOT NULL,
                       timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                       status TEXT,
                       file_size INTEGER,
                       md5_hash TEXT,
                       source_page TEXT
                   )
               ''')

            c.execute('''
                   CREATE TABLE IF NOT EXISTS failed_downloads (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       url TEXT NOT NULL,
                       timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                       error_message TEXT,
                       attempts INTEGER DEFAULT 1
                   )
               ''')

            conn.commit()
            conn.close()

            self.logger.info("Setup completed successfully")
            return True

        except Exception as e:
            self.logger.error(f"Setup failed: {str(e)}")
            raise

    def _init_database_connection(self):
        """Initialize thread-local database connection and return connection object"""
        if not hasattr(self.thread_local, 'db_connection'):
            try:
                # Create a new connection for this thread
                self.thread_local.db_connection = sqlite3.connect(
                    str(self.db_path),
                    timeout=30.0  # Add timeout for busy database
                )
                # Enable WAL mode for better concurrent access
                with self.db_lock:
                    self.thread_local.db_connection.execute('PRAGMA journal_mode=WAL')
                    # Set busy timeout
                    self.thread_local.db_connection.execute('PRAGMA busy_timeout=30000')
                self.logger.debug(f"Created new database connection for thread {threading.current_thread().name}")
            except Exception as e:
                self.logger.error(f"Failed to connect to database: {str(e)}")
                raise

        return self.thread_local.db_connection

    def _record_download(self, url: str, filename: str, status: str, file_size: int = None,
                         md5_hash: str = None, source_page: str = None):
        """Record download attempt in database with thread safety"""
        try:
            conn = self._init_database_connection()

            with self.db_lock:  # Use lock for write operations
                c = conn.cursor()
                try:
                    c.execute('''
                        INSERT INTO downloads 
                        (url, filename, status, file_size, md5_hash, source_page)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (url, filename, status, file_size, md5_hash, source_page))

                    conn.commit()
                    self.logger.debug(f"Thread {threading.current_thread().name} recorded download: {filename}")
                except sqlite3.IntegrityError as e:
                    # Handle duplicate entries
                    self.logger.warning(f"Duplicate download record for URL: {url}")
                    conn.rollback()
                except Exception as e:
                    self.logger.error(f"Database error in record_download: {str(e)}")
                    conn.rollback()
                    raise
                finally:
                    c.close()

        except Exception as e:
            self.logger.error(f"Failed to record download: {str(e)}")

    def _record_failure(self, url: str, error_message: str):
        """Record failed download attempt with thread safety"""
        try:
            conn = self._init_database_connection()

            with self.db_lock:  # Use lock for write operations
                c = conn.cursor()
                try:
                    # Check if URL already exists in failed_downloads
                    c.execute('SELECT attempts FROM failed_downloads WHERE url = ?', (url,))
                    result = c.fetchone()

                    if result:
                        # Update existing record
                        c.execute('''
                            UPDATE failed_downloads 
                            SET attempts = attempts + 1,
                                error_message = ?,
                                timestamp = CURRENT_TIMESTAMP
                            WHERE url = ?
                        ''', (error_message, url))
                    else:
                        # Create new record
                        c.execute('''
                            INSERT INTO failed_downloads (url, error_message)
                            VALUES (?, ?)
                        ''', (url, error_message))

                    conn.commit()
                    self.logger.debug(f"Thread {threading.current_thread().name} recorded failure for URL: {url}")

                except Exception as e:
                    self.logger.error(f"Database error in record_failure: {str(e)}")
                    conn.rollback()
                    raise
                finally:
                    c.close()

        except Exception as e:
            self.logger.error(f"Failed to record failure: {str(e)}")

    def cleanup(self) -> None:
        """Implementation of abstract cleanup method"""
        self.logger.info("Starting cleanup...")
        try:
            # Close all thread-local browsers
            if hasattr(self, 'thread_local'):
                for thread_id, thread in threading._active.items():
                    try:
                        if hasattr(thread, '_thread_local'):
                            browser = getattr(thread._thread_local, 'browser', None)
                            if browser:
                                browser.quit()
                    except Exception as e:
                        self.logger.error(f"Error cleaning up browser for thread {thread_id}: {str(e)}")

            # Clean up temporary files
            if hasattr(self, 'dirs') and 'temp' in self.dirs:
                temp_dir = self.dirs['temp']
                for temp_file in temp_dir.glob('*'):
                    try:
                        temp_file.unlink()
                    except Exception as e:
                        self.logger.error(f"Error removing temporary file {temp_file}: {str(e)}")

            # Update status file
            if hasattr(self, 'dirs') and 'metadata' in self.dirs:
                status_file = self.dirs['metadata'] / 'status.json'
                if status_file.exists():
                    try:
                        with open(status_file, 'r') as f:
                            status = json.load(f)

                        status['last_run'] = time.strftime('%Y-%m-%d %H:%M:%S')
                        status['completed_characters'] = list(self.state.completed_characters)

                        with open(status_file, 'w') as f:
                            json.dump(status, f, indent=4)
                    except Exception as e:
                        self.logger.error(f"Error updating status file: {str(e)}")

            self.logger.info("Cleanup completed successfully")

            # Close thread-local database connections
            if hasattr(self.thread_local, 'db_connection'):
                try:
                    self.thread_local.db_connection.close()
                    delattr(self.thread_local, 'db_connection')
                    self.logger.debug(f"Closed database connection for thread {threading.current_thread().name}")
                except Exception as e:
                    self.logger.error(f"Error closing database connection: {str(e)}")

            # Call parent cleanup
            super().cleanup()


        except Exception as e:
            self.logger.error(f"Cleanup failed: {str(e)}")
            raise

    def _get_thread_browser(self):
        """Get or create a browser instance for the current thread with enhanced error handling"""
        browser_id = id(threading.current_thread())
        self.logger.debug(f"Getting browser for thread {threading.current_thread().name} (ID: {browser_id})")

        if not hasattr(self.thread_local, 'browser'):
            try:
                with self.state.browser_lock:
                    self.logger.info(f"Creating new browser for thread {threading.current_thread().name}")

                    options = webdriver.ChromeOptions()
                    if self.config.headless:
                        options.add_argument('--headless=new')

                    options.add_argument('--no-sandbox')
                    options.add_argument('--disable-dev-shm-usage')
                    options.add_argument('--disable-gpu')
                    options.add_argument('--disable-software-rasterizer')
                    options.add_argument('--disable-extensions')
                    options.add_argument('--start-maximized')
                    options.add_argument(f'user-agent={self.config.user_agent}')

                    # Add more stability options
                    options.add_argument('--disable-features=NetworkService')
                    options.add_argument('--disable-features=VizDisplayCompositor')
                    options.add_argument('--disable-dev-shm-usage')
                    options.add_argument('--no-first-run')
                    options.add_argument('--no-default-browser-check')
                    options.add_argument('--disable-background-networking')
                    options.add_argument('--disable-sync')
                    options.add_argument('--disable-translate')
                    options.add_argument('--hide-scrollbars')
                    options.add_argument('--metrics-recording-only')
                    options.add_argument('--mute-audio')
                    options.add_argument('--no-first-run')
                    options.add_argument('--safebrowsing-disable-auto-update')
                    options.add_argument('--password-store=basic')

                    service = webdriver.ChromeService()
                    browser = webdriver.Chrome(service=service, options=options)

                    # Set timeouts
                    browser.set_page_load_timeout(30)
                    browser.set_script_timeout(30)
                    browser.implicitly_wait(10)

                    self.thread_local.browser = browser
                    self.logger.info(f"Successfully created browser for thread {threading.current_thread().name}")

            except Exception as e:
                self.logger.error(f"Failed to create browser for thread {threading.current_thread().name}: {str(e)}")
                self.logger.exception("Full traceback:")
                raise

        return self.thread_local.browser

    def _safe_navigate(self, url: str, max_retries=3) -> bool:
        """Safely navigate to a URL with retries"""
        browser = self._get_thread_browser()
        self.logger.debug(f"Navigating to {url}")

        for attempt in range(max_retries):
            try:
                browser.get(url)
                WebDriverWait(browser, self.config.request_timeout).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                time.sleep(2)
                return True

            except Exception as e:
                self.logger.warning(f"Navigation attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    self.logger.error(f"Failed to navigate to {url} after {max_retries} attempts")
                    return False
                time.sleep(2 * (attempt + 1))

                if attempt == max_retries - 2:
                    try:
                        browser.quit()
                        delattr(self.thread_local, 'browser')
                        browser = self._get_thread_browser()
                    except Exception as e:
                        self.logger.error(f"Failed to refresh browser: {str(e)}")

        return False

    def _expand_image(self, page_url: str) -> Optional[str]:
        """Navigate to page and expand the image to get the full resolution URL"""
        browser = self._get_thread_browser()
        self.logger.debug(f"Expanding image from {page_url}")

        if not self._safe_navigate(page_url):
            return None

        try:
            # Wait for the original image
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img#image"))
            )

            # Execute resize transition
            browser.execute_script("resizeTransition();")
            time.sleep(2)

            try:
                # Wait for the expanded image
                WebDriverWait(browser, 10).until(
                    lambda driver: driver.find_element(By.CSS_SELECTOR, "img#image").get_attribute("src")
                                   and "/images/" in driver.find_element(By.CSS_SELECTOR, "img#image").get_attribute(
                        "src")
                )

                image = browser.find_element(By.CSS_SELECTOR, "img#image")
                src = image.get_attribute('src')

                if not src or not '/images/' in src:
                    self.logger.warning(f"Invalid image source: {src}")
                    return None

                self.logger.debug(f"Successfully expanded image: {src}")
                return src

            except Exception as wait_error:
                self.logger.error(f"Error waiting for expanded image: {str(wait_error)}")
                return None

        except Exception as e:
            self.logger.error(f"Error expanding image on {page_url}: {str(e)}")
            return None

    def _download_image(self, url: str, source_page: str = None) -> bool:
        """
        Download and save an image or GIF from the given URL.

        Args:
            url (str): URL of the image to download
            source_page (str, optional): URL of the page containing the image

        Returns:
            bool: True if download was successful, False otherwise
        """
        try:
            # Clean and validate URL
            if not url:
                self.logger.error("Invalid URL provided")
                return False

            # Get character-specific path
            char_path = self._get_character_path(url, source_page)

            # Generate filename and paths
            filename = self._generate_filename(url)
            temp_path = self.dirs['temp'] / f"temp_{filename}"
            final_path = self.config.base_save_path / char_path / filename

            self.logger.debug(f"Temp path: {temp_path}")
            self.logger.debug(f"Final path: {final_path}")

            # Create directories if they don't exist
            temp_path.parent.mkdir(parents=True, exist_ok=True)
            final_path.parent.mkdir(parents=True, exist_ok=True)

            # Check if file already exists
            if final_path.exists():
                self.logger.info(f"File already exists at {final_path}")
                return True

            # Download file with proper headers
            headers = {
                'User-Agent': self.config.user_agent,
                'Accept': 'image/webp,image/apng,image/gif,image/*,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': source_page if source_page else url
            }

            response = requests.get(url, stream=True, headers=headers, timeout=self.config.request_timeout)
            response.raise_for_status()

            # Save to temporary file
            self.logger.debug(f"Downloading to temporary file: {temp_path}")
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=self.config.chunk_size):
                    if chunk:
                        f.write(chunk)

            # Verify the file exists and is not empty
            if not temp_path.exists() or temp_path.stat().st_size == 0:
                raise ValueError("Downloaded file is empty or missing")

            # Verify it's a valid image/GIF file
            try:
                with Image.open(temp_path) as img:
                    img.verify()
                    is_gif = getattr(img, "is_animated", False)
            except Exception as e:
                self.logger.error(f"Invalid image file: {str(e)}")
                temp_path.unlink()
                return False

            # Check if content is NSFW
            is_nsfw, confidence = self.nsfw_detector.check_content(temp_path)

            if is_nsfw:  # Keep NSFW content
                # Calculate file hash
                file_hash = self._get_file_hash(temp_path)

                # Move file to final location
                temp_path.rename(final_path)

                # Record successful download
                self._record_download(
                    url=url,
                    filename=filename,
                    status='success',
                    file_size=final_path.stat().st_size,
                    md5_hash=file_hash,
                    source_page=source_page
                )

                self.logger.info(
                    f"Successfully downloaded NSFW {'GIF' if is_gif else 'image'}: "
                    f"{filename} to {final_path}"
                )
                return True
            else:
                self.logger.warning(
                    f"Skipping SFW {'GIF' if is_gif else 'image'} from {url} "
                    f"(confidence: {confidence:.2f})"
                )
                temp_path.unlink()
                return False

        except Exception as e:
            self.logger.error(f"Error downloading {url}: {str(e)}")
            if 'temp_path' in locals() and temp_path.exists():
                try:
                    temp_path.unlink()
                except Exception as cleanup_error:
                    self.logger.error(f"Error cleaning up temporary file: {cleanup_error}")
            return False

    def _get_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def _generate_filename(self, url: str) -> str:
        """Generate a unique filename for the downloaded image"""
        # Extract original extension if possible
        ext = os.path.splitext(urlparse(url).path)[1].lower()
        if not ext or ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            ext = '.jpg'  # Default to .jpg if no valid extension found

        # Generate random component
        random_suffix = ''.join(random.choices(
            string.ascii_lowercase + string.digits,
            k=self.config.filename_length
        ))

        # Create timestamp component
        timestamp = time.strftime('%Y%m%d_%H%M%S')

        # Combine components
        filename = f"img_{timestamp}_{random_suffix}{ext}"

        return filename

    def _get_character_path(self, url: str, source_page: str) -> Path:
        """Extract character name from URL and create appropriate path"""
        try:
            # Extract tags from source page URL
            if source_page and 'tags=' in source_page:
                tags = source_page.split('tags=')[-1].split('&')[0]
                tags = urllib.parse.unquote(tags)  # Decode URL-encoded characters

                # Use character classifier to identify character and series
                series = self.character_classifier.identify_character(tags)
                if series[0]:  # If we found a valid series and character
                    return Path(series[0]) / series[1]

            # Default to raw directory if no character info found
            return Path('raw')
        except Exception as e:
            self.logger.error(f"Error parsing character path: {str(e)}")
            return Path('raw')

    def process_urls(self, urls: Dict[str, str], max_pages: int = 380):
        """Process multiple URLs using thread pool with rolling queue of 4 concurrent scrapers"""
        try:
            self.logger.info(f"Starting scraping with 4 concurrent scrapers")
            self.logger.info(f"Total characters to process: {len(urls)}")

            # System diagnostics
            process = psutil.Process()
            self.logger.info(f"Current memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB")
            self.logger.info(f"Current thread count: {threading.active_count()}")
            self.logger.info("Current threads: " + ", ".join([t.name for t in threading.enumerate()]))

            # Create thread pool with exactly 4 workers
            self.logger.info("Creating thread pool executor...")
            executor = concurrent.futures.ThreadPoolExecutor(
                max_workers=4,
                thread_name_prefix="scraper"
            )
            self.logger.info("Thread pool executor created")

            try:
                # Convert all items to list for easier queueing
                remaining_chars = list(urls.items())
                active_futures = {}  # Track active futures
                completed_count = 0

                # Initial launch of first 4 characters
                initial_chars = remaining_chars[:4]
                remaining_chars = remaining_chars[4:]

                self.logger.info(f"Starting initial 4 characters: {[char for char, _ in initial_chars]}")

                # Submit initial tasks
                for character, url_list in initial_chars:
                    self.logger.info(f"Processing {character}")
                    url_list = [url_list] if isinstance(url_list, str) else url_list

                    if self.state.start_character(character):
                        self.logger.info(f"Lock acquired for {character}")
                        future = executor.submit(self._process_character_wrapper, character, url_list, max_pages)
                        active_futures[future] = character
                        self.logger.info(f"Task submitted for {character}")
                    else:
                        self.logger.warning(f"Could not acquire lock for {character}")

                # Process results and add new tasks as others complete
                while active_futures or remaining_chars:
                    # Wait for any future to complete
                    done, _ = concurrent.futures.wait(
                        active_futures.keys(),
                        timeout=None,
                        return_when=concurrent.futures.FIRST_COMPLETED
                    )

                    # Process completed futures
                    for future in done:
                        character = active_futures[future]
                        try:
                            future.result(timeout=30)
                            completed_count += 1
                            self.logger.info(f"Completed processing {character} ({completed_count}/{len(urls)})")
                        except Exception as e:
                            self.logger.error(f"Error processing {character}: {str(e)}")
                            self.logger.exception("Processing error traceback:")
                        finally:
                            self.state.complete_character(character)
                            del active_futures[future]

                        # Submit a new task if there are remaining characters
                        if remaining_chars:
                            next_char, next_urls = remaining_chars.pop(0)
                            self.logger.info(f"Starting next character: {next_char}")
                            next_urls = [next_urls] if isinstance(next_urls, str) else next_urls

                            if self.state.start_character(next_char):
                                future = executor.submit(self._process_character_wrapper, next_char, next_urls,
                                                         max_pages)
                                active_futures[future] = next_char
                                self.logger.info(f"Task submitted for {next_char}")
                            else:
                                self.logger.warning(f"Could not acquire lock for {next_char}")

                self.logger.info("All characters processed")

            finally:
                self.logger.info("Shutting down executor")
                executor.shutdown(wait=True)  # Changed to wait=True to ensure proper cleanup
                self.logger.info("Executor shutdown complete")

        except Exception as e:
            self.logger.error(f"Error in process_urls: {str(e)}")
            self.logger.exception("Error traceback:")
            raise

    def _process_character_wrapper(self, character: str, urls: List[str], max_pages: int) -> None:
        """Wrapper for process_character with enhanced error handling"""
        thread = threading.current_thread()
        self.logger.info(f"Thread {thread.name} starting {character}")

        try:
            result = self.process_character(character, urls, max_pages)
            self.logger.info(f"Thread {thread.name} completed {character}")
            return result
        except Exception as e:
            self.logger.error(f"Thread {thread.name} error processing {character}: {str(e)}")
            self.logger.exception("Error traceback:")
            raise

    def process_character(self, character: str, urls: List[str], max_pages: int = 380) -> None:
        """Process a single character's URLs with full implementation"""
        thread = threading.current_thread()
        self.logger.info(f"Thread {thread.name} processing {character}")

        try:
            browser = self._get_thread_browser()
            self.logger.info(f"Browser acquired for {character}")

            for url_index, base_url in enumerate(urls, 1):
                self.logger.info(f"Processing URL {url_index}/{len(urls)} for {character}: {base_url}")
                timeout_occurred = False

                for page_num in range(max_pages):
                    if timeout_occurred:
                        self.logger.info(f"Timeout occurred for {character}, moving to next URL")
                        break

                    current_url = f"{base_url}&pid={page_num * 42}" if page_num > 0 else base_url
                    self.logger.info(f"Processing page {page_num + 1} for {character}: {current_url}")

                    if not self._safe_navigate(current_url):
                        self.logger.error(f"Navigation failed for {character} on page {page_num + 1}")
                        continue

                    try:
                        # Wait for thumbnail container
                        self.logger.debug(f"Waiting for thumbnail container on {current_url}")
                        WebDriverWait(browser, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "div.thumbnail-container"))
                        )

                        # Find all image links
                        self.logger.debug(f"Finding image links on {current_url}")
                        links = WebDriverWait(browser, 10).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.thumbnail-preview a"))
                        )

                        image_urls = [link.get_attribute('href') for link in links if link.get_attribute('href')]
                        self.logger.info(f"Found {len(image_urls)} images for {character} on page {page_num + 1}")

                        # Process each image
                        for img_index, img_url in enumerate(image_urls, 1):
                            try:
                                self.logger.debug(f"Processing image {img_index}/{len(image_urls)} from {img_url}")
                                full_image_url = self._expand_image(img_url)

                                if full_image_url:
                                    if self._download_image(full_image_url, img_url):
                                        self.logger.info(f"Successfully downloaded image {img_index} for {character}")
                                    else:
                                        self.logger.warning(f"Failed to download image {img_index} for {character}")
                                    time.sleep(self.config.download_delay)

                            except Exception as e:
                                self.logger.error(f"Error processing image {img_url} for {character}: {str(e)}")
                                continue

                        time.sleep(self.config.page_delay)

                    except TimeoutException:
                        self.logger.error(f"Timeout on page {page_num + 1} for {character}")
                        timeout_occurred = True
                        break
                    except Exception as e:
                        self.logger.error(f"Error processing page {page_num + 1} for {character}: {str(e)}")
                        continue

        except Exception as e:
            self.logger.error(f"Fatal error processing {character}: {str(e)}")
            self.logger.exception("Error traceback:")
            raise
        finally:
            try:
                if hasattr(self.thread_local, 'browser'):
                    self.logger.info(f"Cleaning up browser for {character}")
                    self.thread_local.browser.quit()
                    delattr(self.thread_local, 'browser')
                    self.logger.info(f"Browser cleanup complete for {character}")
            except Exception as e:
                self.logger.error(f"Error cleaning up browser for {character}: {str(e)}")

class DanbooruScraper(HentaiScraper):
    """Scraper specifically for Danbooru"""

    def __init__(self, config: ScraperConfig):
        super().__init__(config)
        self.nsfw_detector = NSFWDetector(threshold=config.nsfw_threshold)
        self._setup_browser()
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.config.user_agent})

    def _setup_browser(self):
        """Set up Selenium WebDriver with Danbooru-specific configuration"""
        options = webdriver.ChromeOptions()
        if self.config.headless:
            options.add_argument('--headless=new')

        # Add standard Chrome options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-extensions')
        options.add_argument('--start-maximized')
        options.add_argument(f'user-agent={self.config.user_agent or "Mozilla/5.0"}')

        # Add Danbooru-specific options if needed
        # options.add_argument('--allow-running-insecure-content')  # If needed for Danbooru

        service = webdriver.ChromeService()

        try:
            self.browser = webdriver.Chrome(service=service, options=options)
            self.browser.set_window_size(1920, 1080)
            self.browser.set_page_load_timeout(self.config.request_timeout)
            self.logger.info("Browser setup successful")
        except Exception as e:
            self.logger.error(f"Failed to initialize browser: {str(e)}")
            raise

    def _get_page_content(self, url: str) -> Optional[BeautifulSoup]:
        """Get page content using requests with proper error handling"""
        try:
            response = self.session.get(url, timeout=self.config.request_timeout)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except Exception as e:
            self.logger.error(f"Error fetching page content: {str(e)}")
            return None

    def _extract_image_urls(self, soup: BeautifulSoup) -> List[str]:
        """Extract image URLs from Danbooru page"""
        image_urls = []
        try:
            articles = soup.select('article[data-id]')
            for article in articles:
                try:
                    # Get the large file version if available
                    img_url = article.get('data-file-url')
                    if img_url:
                        if not img_url.startswith('http'):
                            img_url = 'https://danbooru.donmai.us' + img_url
                        image_urls.append(img_url)
                except Exception as e:
                    self.logger.error(f"Error extracting image URL: {str(e)}")
                    continue
        except Exception as e:
            self.logger.error(f"Error processing page: {str(e)}")
        return image_urls

    def _process_page(self, url: str, character: str, processed_count: int) -> int:
        """Process a single page of Danbooru results"""
        try:
            soup = self._get_page_content(url)
            if not soup:
                return processed_count

            image_urls = self._extract_image_urls(soup)
            self.logger.info(f"Found {len(image_urls)} images on page")

            for img_url in image_urls:
                try:
                    if self._download_image(img_url, url):
                        processed_count += 1
                        time.sleep(self.config.download_delay)
                except Exception as e:
                    self.logger.error(f"Error processing {img_url}: {str(e)}")

            return processed_count

        except Exception as e:
            self.logger.error(f"Error processing page {url}: {str(e)}")
            return processed_count

    def _get_next_page_url(self, current_url: str, page: int) -> str:
        """Generate the URL for the next page"""
        if 'page=' in current_url:
            return current_url.replace(f'page={page}', f'page={page + 1}')
        else:
            return f"{current_url}&page={page + 1}"

    def process_urls(self, urls: Dict[str, str], max_pages: int = 380):
        """Process Danbooru URLs"""
        processed_count = 0

        try:
            for character, url_list in urls.items():
                self.logger.info(f"Processing character: {character}")

                for base_url in url_list:
                    page = 1
                    current_url = base_url

                    while page <= max_pages:
                        self.logger.info(f"Processing page {page} for {character}")

                        # Process the current page
                        new_count = self._process_page(current_url, character, processed_count)
                        if new_count == processed_count:  # No new images processed
                            self.logger.info(f"No new images found for {character} on page {page}")
                            break

                        processed_count = new_count
                        page += 1
                        current_url = self._get_next_page_url(base_url, page)

                        # Respect rate limits
                        time.sleep(self.config.page_delay)

        except Exception as e:
            self.logger.error(f"Fatal error in process_urls: {str(e)}")
        finally:
            self.logger.info(f"Processed {processed_count} images successfully")
            try:
                self.browser.quit()
            except Exception as e:
                self.logger.error(f"Error closing browser: {str(e)}")


# class CharacterTags:
#     """Character tag mappings between different image boards"""
#
#     ONE_PIECE_TAGS = {
#         # Original characters with expanded tags
#         "nami": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "nami", "nami_(one_piece)", "cat_burglar_nami",
#                 "straw_hat_navigator", "weather_witch",
#
#                 # Titles and positions
#                 "cat_burglar", "straw_hat_navigator", "weather_queen",
#                 "cartographer", "third_nakama", "bell-mère's_daughter",
#
#                 # Special abilities and techniques
#                 "weather_techniques", "climatact_user", "zeus_wielder",
#                 "thunder_breeder", "weather_egg", "mirage_tempo",
#                 "thunderbolt_tempo", "weather_manipulation",
#
#                 # Forms and states
#                 "weather_control", "mirage_form", "zeus_combination",
#                 "climatact_mode", "thunder_mode", "heat_mode",
#
#                 # Teams and affiliations
#                 "straw_hat_pirates", "arlong_pirates_(former)",
#                 "weatheria_student", "east_blue_natives",
#
#                 # Combat specialties
#                 "staff_wielder", "weather_control", "thunder_specialist",
#                 "strategy_expert", "climatact_master",
#
#                 # Time periods and versions
#                 "east_blue_saga", "grand_line_nami", "new_world_nami",
#                 "post_timeskip", "pre_timeskip", "wano_nami",
#
#                 # Outfits and appearances
#                 "bikini", "casual_wear", "fighting_outfit",
#                 "winter_clothes", "wano_outfit", "zou_outfit",
#                 "dressrosa_disguise", "whole_cake_outfit",
#
#                 # Emotional states
#                 "angry_nami", "happy_nami", "fighting_nami",
#                 "navigator_mode", "money_loving", "protective_nami",
#
#                 # Specific arcs and events
#                 "arlong_park_arc", "weatheria_training",
#                 "zou_arc", "whole_cake_island", "wano_country"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "nami_(one_piece)", "cat_burglar",
#
#                 # Abilities and roles
#                 "weather_control", "climatact", "navigator",
#
#                 # Time periods
#                 "pre_timeskip", "post_timeskip", "wano_arc",
#
#                 # Specific forms
#                 "zeus_wielder", "mirage_tempo"
#             ]
#         },
#
#         "robin": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "nico_robin", "robin_(one_piece)", "devil_child",
#                 "light_of_the_revolution", "ohara_survivor",
#
#                 # Titles and positions
#                 "devil_child", "miss_all_sunday_(former)",
#                 "archaeologist", "poneglyph_reader", "ohara_scholar",
#
#                 # Special abilities and techniques
#                 "hana_hana_no_mi", "flower_flower_fruit",
#                 "cien_fleur", "mil_fleur", "gigantesco_mano",
#                 "demonio_fleur", "wing_form", "spider_form",
#
#                 # Forms and states
#                 "demon_form", "wing_sprouted", "multiple_arms",
#                 "giant_limbs", "spider_form", "clutch_pose",
#
#                 # Teams and affiliations
#                 "straw_hat_pirates", "baroque_works_(former)",
#                 "revolutionary_army", "ohara_scholars",
#
#                 # Combat specialties
#                 "limb_multiplication", "assassination_techniques",
#                 "grappling_specialist", "intelligence_gathering",
#
#                 # Time periods and versions
#                 "pre_timeskip", "post_timeskip", "ohara_robin",
#                 "baroque_works_era", "enies_lobby", "wano_robin",
#
#                 # Outfits and appearances
#                 "casual_wear", "battle_outfit", "wano_kimono",
#                 "dressrosa_disguise", "zou_outfit", "formal_dress",
#
#                 # Emotional states
#                 "serious_robin", "mysterious_robin", "smiling_robin",
#                 "fighting_robin", "reading_robin", "protective_robin",
#
#                 # Specific arcs and events
#                 "alabasta_arc", "water_7", "enies_lobby",
#                 "thriller_bark", "dressrosa", "wano_country"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "nico_robin", "robin_(one_piece)",
#
#                 # Abilities and roles
#                 "hana_hana_no_mi", "archaeologist",
#
#                 # Time periods
#                 "pre_timeskip", "post_timeskip", "wano_arc",
#
#                 # Specific forms
#                 "demon_form", "wing_form", "multiple_arms"
#             ]
#         },
#
#         "yamato": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "yamato", "yamato_(one_piece)", "oni_princess",
#                 "kaido's_daughter", "oden's_successor",
#
#                 # Titles and positions
#                 "oni_princess", "self_proclaimed_oden",
#                 "guardian_of_wano", "samurai_aspirant",
#
#                 # Special abilities and techniques
#                 "mythical_zoan", "dog_dog_fruit", "divine_dog",
#                 "thunder_bagua", "ice_oni", "frozen_blast",
#
#                 # Forms and states
#                 "hybrid_form", "full_beast_form", "human_form",
#                 "fighting_stance", "ice_oni_mode", "guardian_mode",
#
#                 # Combat abilities
#                 "thunder_techniques", "ice_abilities", "club_wielder",
#                 "advanced_haki", "moon_following",
#
#                 # Teams and affiliations
#                 "beast_pirates_(former)", "wano_ally",
#                 "samurai_alliance", "onigashima_defender",
#
#                 # Time periods and versions
#                 "young_yamato", "prisoner_yamato", "freed_yamato",
#                 "alliance_yamato", "current_yamato",
#
#                 # Outfits and appearances
#                 "traditional_clothes", "battle_outfit", "casual_wear",
#                 "oni_mask", "samurai_armor", "festival_attire",
#
#                 # Emotional states
#                 "determined_yamato", "fighting_yamato", "proud_yamato",
#                 "excited_yamato", "serious_yamato", "friendly_yamato"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "yamato_(one_piece)", "oni_princess",
#
#                 # Abilities and forms
#                 "mythical_zoan", "hybrid_form", "ice_oni",
#
#                 # Relationships
#                 "kaido's_child", "oden's_successor",
#
#                 # Time periods
#                 "prisoner_era", "alliance_era", "current_era"
#             ]
#         },
#
#         # Charlotte Family with expanded tags
#         "big_mom": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "charlotte_linlin", "big_mom", "big_mom_(one_piece)",
#                 "queen_of_totland", "emperor_big_mom",
#
#                 # Titles and positions
#                 "yonko", "emperor", "queen_of_totland", "pirate_empress",
#                 "captain_of_big_mom_pirates", "rocks_pirates_former",
#
#                 # Special abilities and powers
#                 "soul_soul_fruit", "soru_soru_no_mi", "zeus_creator",
#                 "prometheus_creator", "napoleon_creator", "life_or_death",
#                 "soul_pocus", "ikoku_sovereignty",
#
#                 # Forms and states
#                 "normal_form", "skinny_form", "young_form",
#                 "hunger_pangs", "rage_mode", "amnesia_state",
#                 "soul_power", "homie_control",
#
#                 # Combat abilities
#                 "sword_techniques", "zeus_lightning", "prometheus_fire",
#                 "napoleon_blade", "life_force_drain", "soul_manipulation",
#
#                 # Time periods and versions
#                 "rocks_era", "young_linlin", "mother_caramel_era",
#                 "yonko_era", "current_big_mom", "wano_big_mom",
#
#                 # Homies and creations
#                 "zeus_wielder", "prometheus_wielder", "napoleon_wielder",
#                 "homie_creator", "soul_collector",
#
#                 # Emotional states
#                 "hunger_mode", "angry_big_mom", "motherly_mode",
#                 "empress_mode", "rampage_mode", "calm_big_mom",
#
#                 # Specific arcs and events
#                 "whole_cake_island", "wano_country", "rocks_flashback",
#                 "mother_caramel_flashback"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "charlotte_linlin", "big_mom_(one_piece)", "yonko",
#
#                 # Powers and abilities
#                 "soul_soul_fruit", "homie_creator", "emperor",
#
#                 # Forms and states
#                 "normal_form", "skinny_form", "young_form",
#
#                 # Time periods
#                 "rocks_era", "yonko_era", "current_era"
#             ]
#         },
#
#         "smoothie": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "charlotte_smoothie", "smoothie_(one_piece)",
#                 "minister_of_juice", "sweet_commander",
#
#                 # Titles and positions
#                 "sweet_commander", "minister_of_juice",
#                 "big_mom_pirates_executive", "charlotte_family",
#
#                 # Special abilities and powers
#                 "wring_wring_fruit", "shibo_shibo_no_mi",
#                 "liquid_manipulation", "size_manipulation",
#                 "juice_extraction", "sword_techniques",
#
#                 # Forms and states
#                 "normal_size", "giant_form", "battle_mode",
#                 "juice_extraction_mode", "sword_stance",
#
#                 # Combat specialties
#                 "sword_fighter", "liquid_manipulator",
#                 "size_enhancer", "long-range_fighter",
#
#                 # Teams and affiliations
#                 "big_mom_pirates", "charlotte_family",
#                 "sweet_commanders", "totland_ministers",
#
#                 # Time periods and versions
#                 "pre_wedding", "wedding_ceremony", "escape_pursuit",
#                 "current_smoothie",
#
#                 # Outfits and appearances
#                 "minister_outfit", "battle_gear", "casual_clothes",
#                 "formal_dress", "sword_bearer",
#
#                 # Emotional states
#                 "serious_smoothie", "commander_mode", "battle_ready",
#                 "calculating_smoothie", "dutiful_smoothie"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "charlotte_smoothie", "smoothie_(one_piece)",
#
#                 # Abilities and roles
#                 "wring_wring_fruit", "sweet_commander",
#
#                 # States and forms
#                 "normal_form", "giant_form", "battle_mode"
#             ]
#         },
#
#         "pudding": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "charlotte_pudding", "pudding_(one_piece)",
#                 "three_eye_tribe", "minister_of_chocolate",
#
#                 # Titles and positions
#                 "minister_of_chocolate", "cafe_owner",
#                 "third_eye_wielder", "charlotte_family",
#
#                 # Special abilities and powers
#                 "memory_manipulation", "third_eye_powers",
#                 "memo_memo_no_mi", "memory_alteration",
#                 "potential_poneglyph_reader",
#
#                 # Racial traits
#                 "three_eye_tribe", "third_eye", "hybrid_human",
#                 "special_lineage",
#
#                 # Forms and states
#                 "normal_mode", "third_eye_revealed", "memory_manipulation_mode",
#                 "chef_mode", "crying_state", "true_personality",
#
#                 # Teams and affiliations
#                 "charlotte_family", "cafe_staff", "big_mom_pirates",
#                 "sanji's_arranged_bride",
#
#                 # Time periods and versions
#                 "pre_wedding", "wedding_ceremony", "post_wedding",
#                 "childhood_pudding", "current_pudding",
#
#                 # Outfits and appearances
#                 "wedding_dress", "cafe_uniform", "casual_clothes",
#                 "formal_wear", "chef_outfit",
#
#                 # Emotional states
#                 "sweet_persona", "dark_personality", "crying_pudding",
#                 "loving_pudding", "conflicted_pudding", "true_feelings"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "charlotte_pudding", "pudding_(one_piece)",
#
#                 # Traits and abilities
#                 "three_eye_tribe", "memory_manipulation",
#
#                 # States and versions
#                 "sweet_persona", "dark_personality", "true_self"
#             ]
#         },
#
#         "brulee": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "charlotte_brulee", "brulee_(one_piece)",
#                 "mirror_witch", "mirror_world_master",
#
#                 # Special abilities and powers
#                 "mirror_mirror_fruit", "mira_mira_no_mi",
#                 "mirror_world_access", "mirror_creation",
#                 "reflection_powers", "mirror_transportation",
#
#                 # Forms and states
#                 "normal_form", "mirror_form", "reflection_form",
#                 "mirror_world_mode", "disguise_form",
#
#                 # Combat abilities
#                 "mirror_manipulation", "reflection_copying",
#                 "mirror_world_transport", "disguise_power",
#
#                 # Teams and affiliations
#                 "charlotte_family", "big_mom_pirates",
#                 "seducing_woods_guardian",
#
#                 # Locations and domains
#                 "mirror_world", "seducing_woods", "whole_cake_island",
#
#                 # Time periods and versions
#                 "pre_invasion", "mirror_world_battle", "current_brulee",
#
#                 # Emotional states
#                 "scared_brulee", "loyal_brulee", "angry_brulee",
#                 "sister_mode", "protective_brulee"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "charlotte_brulee", "brulee_(one_piece)",
#
#                 # Powers and abilities
#                 "mirror_mirror_fruit", "mirror_world",
#
#                 # States and forms
#                 "normal_form", "mirror_form", "disguise_form"
#             ]
#         },
#
#         "komurasaki": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "kozuki_hiyori", "komurasaki", "hiyori_(one_piece)",
#                 "wano_courtesan", "kozuki_princess", "lady_komurasaki",
#
#                 # Titles and positions
#                 "number_one_courtesan", "kozuki_heir", "oiran",
#                 "princess_of_wano", "shamisen_master", "flower_capital_beauty",
#
#                 # Family relationships
#                 "kozuki_clan", "oden's_daughter", "momonosuke's_sister",
#                 "toki's_daughter", "wano_royalty", "kozuki_bloodline",
#
#                 # Forms and identities
#                 "courtesan_form", "princess_form", "disguised_identity",
#                 "true_identity", "performing_artist", "oiran_persona",
#
#                 # Special skills
#                 "shamisen_playing", "dancing_skills", "royal_etiquette",
#                 "survival_skills", "deception_mastery", "musical_talent",
#
#                 # Time periods and versions
#                 "childhood_hiyori", "komurasaki_era", "revealed_identity",
#                 "current_hiyori", "wano_liberation", "twenty_years_later",
#
#                 # Locations
#                 "flower_capital", "wano_country", "pleasure_district",
#                 "kozuki_castle", "hidden_location",
#
#                 # Outfits and appearances
#                 "courtesan_kimono", "princess_attire", "casual_kimono",
#                 "disguise_outfit", "formal_wear", "battle_clothes",
#                 "oiran_makeup", "traditional_hairstyle",
#
#                 # Emotional states
#                 "elegant_komurasaki", "determined_hiyori", "proud_princess",
#                 "vengeful_hiyori", "caring_sister", "performer_mode",
#                 "true_feelings", "hidden_anger"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "kozuki_hiyori", "komurasaki", "hiyori_(one_piece)",
#
#                 # Roles and positions
#                 "courtesan", "princess", "kozuki_clan", "oiran",
#
#                 # States and forms
#                 "disguised_form", "true_identity", "performer_mode",
#
#                 # Time periods
#                 "past_era", "present_era", "wano_arc"
#             ]
#         },
#
#         "ulti": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "ulti", "ulti_(one_piece)", "tobi_roppo_member",
#                 "ancient_zoan_user", "headbutt_specialist",
#
#                 # Titles and positions
#                 "tobi_roppo", "beast_pirates_executive", "flying_six",
#                 "dinosaur_zoan", "pay-pay's_sister",
#
#                 # Special abilities and powers
#                 "ancient_zoan", "pachycephalosaurus_fruit",
#                 "headbutt_techniques", "dinosaur_form", "armament_haki",
#                 "observation_haki", "enhanced_strength",
#
#                 # Forms and states
#                 "human_form", "hybrid_form", "full_beast_form",
#                 "headbutt_mode", "rage_mode", "battle_mode",
#
#                 # Combat techniques
#                 "headbutt_smash", "ancient_power", "dinosaur_rush",
#                 "ulti_meteor", "sister_combination", "haki_enhanced_attacks",
#
#                 # Teams and affiliations
#                 "beast_pirates", "tobi_roppo", "kaido's_crew",
#                 "onigashima_forces", "animal_kingdom_pirates",
#
#                 # Relationships
#                 "page_one's_sister", "kaido's_subordinate",
#                 "flying_six_member", "beast_pirate_executive",
#
#                 # Time periods and versions
#                 "pre_raid", "onigashima_raid", "current_ulti",
#                 "beast_pirates_era", "wano_arc",
#
#                 # Outfits and appearances
#                 "beast_pirate_outfit", "battle_gear", "casual_clothes",
#                 "horned_headpiece", "dinosaur_features",
#
#                 # Emotional states
#                 "angry_ulti", "fighting_ulti", "protective_sister",
#                 "aggressive_mode", "playful_ulti", "serious_ulti"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "ulti", "ulti_(one_piece)", "tobi_roppo",
#
#                 # Powers and forms
#                 "ancient_zoan", "dinosaur_form", "hybrid_form",
#
#                 # Relations and roles
#                 "beast_pirates", "page_one's_sister", "flying_six",
#
#                 # States
#                 "battle_mode", "rage_mode", "normal_form"
#             ]
#         },
#
#         "black_maria": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "black_maria", "black_maria_(one_piece)",
#                 "pleasure_hall_queen", "tobi_roppo_member",
#
#                 # Titles and positions
#                 "tobi_roppo", "pleasure_hall_owner", "flying_six",
#                 "beast_pirates_executive", "ancient_zoan_user",
#
#                 # Special abilities and powers
#                 "ancient_zoan", "spider_spider_fruit", "marys_control",
#                 "rosamygale_grauvogeli", "spider_form",
#                 "fire_techniques", "web_creation", "venom_abilities",
#
#                 # Forms and states
#                 "human_form", "hybrid_form", "full_beast_form",
#                 "spider_mode", "battle_stance", "entertainment_mode",
#
#                 # Combat techniques
#                 "web_binding", "fire_manipulation", "spider_thread",
#                 "poison_mist", "weapon_master", "marys_surveillance",
#
#                 # Teams and affiliations
#                 "beast_pirates", "tobi_roppo", "kaido's_crew",
#                 "onigashima_forces", "pleasure_hall_staff",
#
#                 # Locations and domains
#                 "pleasure_hall", "onigashima", "wano_country",
#                 "entertainment_district", "spider_lair",
#
#                 # Time periods and versions
#                 "pre_raid", "onigashima_raid", "current_maria",
#                 "beast_pirates_era", "wano_arc",
#
#                 # Outfits and appearances
#                 "traditional_clothes", "battle_outfit", "pleasure_hall_attire",
#                 "spider_features", "hybrid_appearance",
#
#                 # Emotional states
#                 "sadistic_maria", "calculating_maria", "fighting_maria",
#                 "entertainer_mode", "serious_maria", "playful_maria"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "black_maria", "black_maria_(one_piece)",
#
#                 # Powers and roles
#                 "spider_spider_fruit", "tobi_roppo", "flying_six",
#
#                 # Forms and states
#                 "human_form", "hybrid_form", "spider_form",
#
#                 # Locations
#                 "pleasure_hall", "onigashima", "wano"
#             ]
#         },
#
#         "okiku": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "kikunojo", "o_kiku", "kiku_(one_piece)",
#                 "red_scabbard_member", "kawamatsu's_companion",
#
#                 # Titles and positions
#                 "red_scabbard", "akazaya_nine", "tea_house_worker",
#                 "samurai_of_wano", "oden's_retainer",
#
#                 # Special abilities and techniques
#                 "sword_techniques", "two_sword_style",
#                 "samurai_arts", "snow_country_style",
#                 "oden_two_sword_style",
#
#                 # Combat specialties
#                 "swordsmanship", "dual_wielding", "precision_strikes",
#                 "samurai_techniques", "armor_breaker",
#
#                 # Teams and affiliations
#                 "red_scabbards", "kozuki_clan", "wano_resistance",
#                 "tea_house_staff", "oden's_followers",
#
#                 # Time periods and versions
#                 "past_kiku", "present_kiku", "tea_house_kiku",
#                 "battle_kiku", "time_travel_survivor",
#
#                 # Outfits and appearances
#                 "kimono", "battle_armor", "tea_house_uniform",
#                 "samurai_gear", "traditional_clothes",
#                 "red_scabbard_attire",
#
#                 # Emotional states
#                 "gentle_kiku", "warrior_mode", "protective_kiku",
#                 "loyal_retainer", "determined_kiku"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "kikunojo", "o_kiku", "kiku_(one_piece)",
#
#                 # Roles and positions
#                 "red_scabbard", "samurai", "tea_house_worker",
#
#                 # Combat styles
#                 "swordsman", "two_sword_style", "samurai_arts"
#             ]
#         },
#
#         "otoko": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "toko", "o_toko", "toko_(one_piece)",
#                 "yasuie's_daughter", "ebisu_town_resident",
#
#                 # Roles and positions
#                 "kamuro", "komurasaki's_attendant",
#                 "ebisu_town_survivor", "smile_victim's_child",
#
#                 # Special characteristics
#                 "forced_smile", "smile_effect", "perpetual_laughter",
#                 "ebisu_condition", "tragic_past",
#
#                 # Relationships
#                 "yasuie's_daughter", "komurasaki's_helper",
#                 "hiyori's_friend", "tonoyasu's_child",
#
#                 # Time periods and versions
#                 "early_wano", "post_yasuie", "current_toko",
#                 "flower_capital_era", "rebellion_era",
#
#                 # Locations
#                 "ebisu_town", "flower_capital", "pleasure_district",
#                 "hidden_refuge",
#
#                 # Outfits and appearances
#                 "kamuro_outfit", "casual_clothes", "worker_attire",
#                 "flower_capital_dress", "poor_town_clothes",
#
#                 # Emotional states
#                 "laughing_toko", "grieving_toko", "brave_toko",
#                 "supportive_toko", "determined_toko"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "toko", "o_toko", "toko_(one_piece)",
#
#                 # Roles and relationships
#                 "kamuro", "yasuie's_daughter", "smile_victim",
#
#                 # States
#                 "forced_smile", "ebisu_condition"
#             ]
#         },
#
#         "otsuru": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "tsuru", "o_tsuru", "tsuru_(one_piece_wano)",
#                 "tea_house_owner", "wano_citizen",
#
#                 # Roles and positions
#                 "tea_house_proprietor", "resistance_supporter",
#                 "information_gatherer", "kiku's_employer",
#
#                 # Relationships
#                 "kinemon's_friend", "resistance_ally",
#                 "wano_citizen_leader", "community_pillar",
#
#                 # Time periods and versions
#                 "pre_raid", "current_tsuru", "resistance_era",
#                 "tea_house_period",
#
#                 # Locations
#                 "tea_house", "wano_country", "resistance_hideout",
#
#                 # Outfits and appearances
#                 "tea_house_kimono", "traditional_dress",
#                 "merchant_clothes", "working_attire",
#
#                 # Emotional states
#                 "caring_tsuru", "supportive_tsuru", "protective_tsuru",
#                 "determined_tsuru", "resistance_supporter"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "tsuru", "o_tsuru", "tsuru_(one_piece_wano)",
#
#                 # Roles
#                 "tea_house_owner", "resistance_supporter",
#                 "wano_citizen"
#             ]
#         },
#
#         "speed": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "speed", "speed_(one_piece)", "headliner",
#                 "beast_pirate_member",
#
#                 # Titles and positions
#                 "headliner", "beast_pirates_officer",
#                 "tama's_subordinate", "horse_smile_user",
#
#                 # Special abilities and powers
#                 "smile_fruit", "horse_form", "enhanced_speed",
#                 "transportation_ability", "artificial_zoan",
#
#                 # Forms and states
#                 "horse_form", "hybrid_form", "human_form",
#                 "tamed_state", "battle_mode",
#
#                 # Teams and affiliations
#                 "beast_pirates", "tama's_followers",
#                 "headliner_group", "kibi_dango_army",
#
#                 # Time periods and versions
#                 "beast_pirate_era", "tamed_version", "current_speed",
#                 "raid_participant",
#
#                 # Combat abilities
#                 "high_speed_movement", "cavalry_techniques",
#                 "transportation_specialist", "mounted_combat",
#
#                 # Emotional states
#                 "loyal_speed", "protective_speed", "determined_speed",
#                 "battle_ready_speed"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "speed", "speed_(one_piece)",
#
#                 # Powers and roles
#                 "smile_user", "headliner", "horse_form",
#
#                 # Affiliations
#                 "beast_pirates", "tama's_follower"
#             ]
#         },
#
#         "boa_hancock": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "boa_hancock", "hancock_(one_piece)", "pirate_empress",
#                 "snake_princess", "gorgon_sister", "warlord",
#
#                 # Titles and positions
#                 "shichibukai", "pirate_empress", "snake_princess",
#                 "kuja_leader", "amazon_lily_ruler", "former_slave",
#                 "most_beautiful_woman", "world's_beauty",
#
#                 # Special abilities and powers
#                 "love_love_fruit", "mero_mero_no_mi", "love_beam",
#                 "perfume_femur", "pistol_kiss", "slave_arrow",
#                 "conqueror's_haki", "armament_haki", "observation_haki",
#
#                 # Forms and states
#                 "normal_form", "snake_form", "petrification_mode",
#                 "battle_mode", "empress_mode", "angry_mode",
#                 "love_struck_mode", "serious_mode",
#
#                 # Combat abilities
#                 "petrification", "love_attacks", "haki_mastery",
#                 "martial_arts", "kuja_combat", "snake_weapons",
#
#                 # Teams and affiliations
#                 "kuja_pirates", "seven_warlords", "amazon_lily",
#                 "gorgon_sisters", "former_slaves", "luffy_allies",
#
#                 # Family relationships
#                 "elder_gorgon_sister", "marigold's_sister",
#                 "sandersonia's_sister", "kuja_ruler",
#
#                 # Special characteristics
#                 "gorgon_eyes", "snake_attributes", "back_mark",
#                 "celestial_mark", "beauty_mark", "royal_presence",
#
#                 # Time periods and versions
#                 "young_hancock", "slave_era", "warlord_era",
#                 "empress_era", "marineford_war", "current_hancock",
#
#                 # Outfits and appearances
#                 "empress_outfit", "battle_gear", "casual_dress",
#                 "qipao", "snake_themed_clothes", "royal_attire",
#                 "warrior_outfit", "formal_dress",
#
#                 # Emotional states
#                 "love_mode", "empress_mode", "angry_hancock",
#                 "disdainful_hancock", "loving_hancock", "protective_hancock",
#                 "serious_hancock", "contemptuous_hancock"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "boa_hancock", "hancock_(one_piece)", "pirate_empress",
#
#                 # Powers and abilities
#                 "mero_mero_no_mi", "love_love_fruit", "haki_user",
#
#                 # Titles and roles
#                 "shichibukai", "snake_princess", "kuja_leader",
#
#                 # States and forms
#                 "normal_form", "battle_mode", "love_struck",
#
#                 # Time periods
#                 "pre_timeskip", "post_timeskip", "current_era"
#             ]
#         },
#
#         "sandersonia": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "boa_sandersonia", "sandersonia_(one_piece)",
#                 "gorgon_sister", "anaconda_princess",
#
#                 # Titles and positions
#                 "kuja_warrior", "gorgon_sister", "amazon_lily_elite",
#                 "former_slave", "snake_specialist",
#
#                 # Special abilities and powers
#                 "snake_snake_fruit", "hebi_hebi_no_mi",
#                 "anaconda_model", "armament_haki",
#                 "observation_haki", "snake_form",
#
#                 # Forms and states
#                 "human_form", "hybrid_form", "full_snake_form",
#                 "battle_mode", "guardian_mode",
#
#                 # Combat abilities
#                 "snake_techniques", "haki_mastery", "kuja_combat",
#                 "zoan_powers", "snake_wrestling",
#
#                 # Teams and affiliations
#                 "kuja_warriors", "gorgon_sisters", "amazon_lily",
#                 "former_slaves", "hancock's_sister",
#
#                 # Family relationships
#                 "middle_gorgon_sister", "hancock's_sister",
#                 "marigold's_sister", "kuja_royal_family",
#
#                 # Special characteristics
#                 "gorgon_mark", "snake_eyes", "back_mark",
#                 "celestial_mark", "warrior_build",
#
#                 # Time periods and versions
#                 "young_sandersonia", "slave_era", "warrior_era",
#                 "current_sandersonia",
#
#                 # Emotional states
#                 "protective_sister", "warrior_mode", "serious_sandersonia",
#                 "battle_ready", "snake_fury"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "boa_sandersonia", "sandersonia_(one_piece)",
#
#                 # Powers and roles
#                 "snake_snake_fruit", "gorgon_sister", "kuja_warrior",
#
#                 # Forms and states
#                 "human_form", "hybrid_form", "snake_form"
#             ]
#         },
#
#         "marigold": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "boa_marigold", "marigold_(one_piece)",
#                 "gorgon_sister", "king_cobra_princess",
#
#                 # Titles and positions
#                 "kuja_warrior", "gorgon_sister", "amazon_lily_elite",
#                 "former_slave", "snake_specialist",
#
#                 # Special abilities and powers
#                 "snake_snake_fruit", "hebi_hebi_no_mi",
#                 "king_cobra_model", "armament_haki",
#                 "observation_haki", "snake_form",
#
#                 # Forms and states
#                 "human_form", "hybrid_form", "full_snake_form",
#                 "battle_mode", "guardian_mode",
#
#                 # Combat abilities
#                 "snake_techniques", "haki_mastery", "kuja_combat",
#                 "zoan_powers", "fire_techniques",
#
#                 # Teams and affiliations
#                 "kuja_warriors", "gorgon_sisters", "amazon_lily",
#                 "former_slaves", "hancock's_sister",
#
#                 # Family relationships
#                 "youngest_gorgon_sister", "hancock's_sister",
#                 "sandersonia's_sister", "kuja_royal_family",
#
#                 # Special characteristics
#                 "gorgon_mark", "snake_eyes", "back_mark",
#                 "celestial_mark", "warrior_build",
#
#                 # Time periods and versions
#                 "young_marigold", "slave_era", "warrior_era",
#                 "current_marigold",
#
#                 # Emotional states
#                 "protective_sister", "warrior_mode", "serious_marigold",
#                 "battle_ready", "snake_fury"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "boa_marigold", "marigold_(one_piece)",
#
#                 # Powers and roles
#                 "snake_snake_fruit", "gorgon_sister", "kuja_warrior",
#
#                 # Forms and states
#                 "human_form", "hybrid_form", "snake_form"
#             ]
#         },
#
#         "marguerite": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "marguerite", "marguerite_(one_piece)",
#                 "kuja_warrior", "amazon_lily_archer",
#
#                 # Titles and positions
#                 "kuja_warrior", "elite_archer", "amazon_lily_guard",
#                 "hancock's_subordinate", "luffy's_friend",
#
#                 # Special abilities and powers
#                 "archery_master", "haki_arrows", "kuja_combat",
#                 "snake_bow_user", "warrior_skills",
#
#                 # Combat specialties
#                 "bow_techniques", "snake_archery", "haki_mastery",
#                 "kuja_fighting_style", "ranged_combat",
#
#                 # Teams and affiliations
#                 "kuja_warriors", "amazon_lily", "hancock's_guards",
#                 "archer_division",
#
#                 # Time periods and versions
#                 "pre_timeskip", "post_timeskip", "current_marguerite",
#
#                 # Outfits and appearances
#                 "kuja_outfit", "warrior_attire", "tribal_clothes",
#                 "battle_gear", "amazon_dress",
#
#                 # Emotional states
#                 "friendly_marguerite", "curious_marguerite",
#                 "warrior_mode", "protective_marguerite"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "marguerite", "marguerite_(one_piece)",
#
#                 # Roles and abilities
#                 "kuja_warrior", "archer", "amazon_lily",
#
#                 # States
#                 "warrior_mode", "normal_state"
#             ]
#         },
#
#         "viola": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "viola", "viola_(one_piece)", "violet",
#                 "violet_(one_piece)", "princess_viola",
#                 "riku_viola", "dancing_queen",
#
#                 # Titles and positions
#                 "princess_of_dressrosa", "dancing_queen",
#                 "donquixote_officer_(former)", "riku_family",
#                 "tango_dancer", "spy_dancer",
#
#                 # Special abilities and powers
#                 "glare_glare_fruit", "giro_giro_no_mi",
#                 "clairvoyance", "x-ray_vision", "mind_reading",
#                 "tears_of_arte", "emotional_manipulation",
#
#                 # Combat abilities
#                 "dance_combat", "insight_attacks", "emotional_tactics",
#                 "assassination_techniques", "espionage_skills",
#
#                 # Forms and states
#                 "dancer_form", "princess_mode", "spy_mode",
#                 "battle_ready", "surveillance_state",
#
#                 # Teams and affiliations
#                 "riku_family", "dressrosa_royalty",
#                 "donquixote_pirates_(former)", "straw_hat_allies",
#
#                 # Family relationships
#                 "riku's_daughter", "rebecca's_aunt", "scarlett's_sister",
#                 "kyros'_sister_in_law", "dressrosa_royal_family",
#
#                 # Time periods and versions
#                 "pre_doflamingo", "spy_era", "liberation_era",
#                 "current_viola", "restored_princess",
#
#                 # Outfits and appearances
#                 "dancer_outfit", "princess_dress", "spy_clothes",
#                 "formal_attire", "battle_gear", "flamenco_dress",
#
#                 # Emotional states
#                 "determined_viola", "dancing_viola", "serious_viola",
#                 "protective_viola", "royal_demeanor", "spy_persona"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "viola", "viola_(one_piece)", "violet",
#
#                 # Powers and roles
#                 "glare_glare_fruit", "princess", "dancer",
#
#                 # States and forms
#                 "dancer_form", "princess_mode", "battle_mode"
#             ]
#         },
#
#         "rebecca": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "rebecca", "rebecca_(one_piece)", "gladiator_rebecca",
#                 "undefeated_woman", "scarlett's_daughter",
#
#                 # Titles and positions
#                 "dressrosa_princess", "gladiator_champion",
#                 "undefeated_woman", "riku_heir", "colosseum_fighter",
#
#                 # Combat abilities
#                 "observation_haki", "speed_fighting", "dodging_specialist",
#                 "sword_techniques", "gladiator_style", "kings_punch",
#
#                 # Special techniques
#                 "back_to_zero", "speed_slash", "defensive_combat",
#                 "survival_tactics", "sword_dance",
#
#                 # Teams and affiliations
#                 "riku_family", "dressrosa_royalty", "corrida_colosseum",
#                 "straw_hat_allies", "gladiator_block",
#
#                 # Family relationships
#                 "scarlett's_daughter", "kyros'_daughter", "viola's_niece",
#                 "riku's_granddaughter", "dressrosa_princess",
#
#                 # Time periods and versions
#                 "gladiator_era", "princess_era", "childhood_rebecca",
#                 "current_rebecca", "restored_princess",
#
#                 # Combat outfits and gear
#                 "gladiator_armor", "princess_dress", "battle_bikini",
#                 "royal_attire", "colosseum_gear",
#
#                 # Emotional states
#                 "fighting_rebecca", "determined_rebecca", "crying_rebecca",
#                 "protective_rebecca", "princess_mode", "warrior_spirit"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "rebecca", "rebecca_(one_piece)", "gladiator",
#
#                 # Roles and abilities
#                 "undefeated_woman", "sword_user", "princess",
#
#                 # States and forms
#                 "gladiator_mode", "princess_mode", "battle_mode"
#             ]
#         },
#
#         "scarlett": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "scarlett", "scarlett_(one_piece)", "princess_scarlett",
#                 "kyros'_wife", "rebecca's_mother",
#
#                 # Titles and positions
#                 "dressrosa_princess", "riku_family", "former_royalty",
#                 "flower_field_resident", "kyros'_beloved",
#
#                 # Family relationships
#                 "riku's_daughter", "viola's_sister", "rebecca's_mother",
#                 "kyros'_wife", "royal_bloodline",
#
#                 # Time periods and versions
#                 "princess_era", "love_story_era", "final_moments",
#                 "flashback_scarlett", "young_scarlett",
#
#                 # Outfits and appearances
#                 "princess_dress", "common_clothes", "flower_field_attire",
#                 "royal_garments", "civilian_disguise",
#
#                 # Emotional states
#                 "loving_mother", "devoted_wife", "determined_scarlett",
#                 "protective_mother", "princess_dignity"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "scarlett", "scarlett_(one_piece)", "princess",
#
#                 # Roles and relations
#                 "kyros'_wife", "rebecca's_mother", "royal_family"
#             ]
#         },
#
#         "baby_5": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "baby_5", "baby_5_(one_piece)", "baby_five",
#                 "arms_arms_fruit_user", "donquixote_officer",
#
#                 # Titles and positions
#                 "donquixote_executive", "assassin", "weapons_specialist",
#                 "sai's_wife", "happo_navy_member",
#
#                 # Special abilities and powers
#                 "arms_arms_fruit", "buki_buki_no_mi", "weapon_transformation",
#                 "full_body_weapons", "living_arsenal",
#
#                 # Forms and states
#                 "weapon_form", "human_form", "battle_mode",
#                 "servant_mode", "wife_mode", "assassin_mode",
#
#                 # Combat abilities
#                 "weapon_mastery", "assassination_skills",
#                 "transformation_techniques", "martial_arts",
#
#                 # Teams and affiliations
#                 "donquixote_pirates_(former)", "happo_navy",
#                 "sai's_wife", "chinjao_family",
#
#                 # Personality traits
#                 "people_pleaser", "easily_proposed_to",
#                 "devoted_servant", "loyal_wife",
#
#                 # Time periods and versions
#                 "donquixote_era", "dressrosa_arc", "married_life",
#                 "childhood_baby_5", "current_baby_5",
#
#                 # Outfits and appearances
#                 "maid_outfit", "battle_gear", "assassin_clothes",
#                 "weapon_forms", "casual_wear",
#
#                 # Emotional states
#                 "devoted_baby_5", "battle_ready", "loving_wife",
#                 "servant_mode", "assassin_persona"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "baby_5", "baby_5_(one_piece)", "baby_five",
#
#                 # Powers and roles
#                 "arms_arms_fruit", "assassin", "weapon_form",
#
#                 # States and affiliations
#                 "donquixote_pirates", "happo_navy", "sai's_wife"
#             ]
#         },
#
#         "tashigi": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "tashigi", "tashigi_(one_piece)", "marine_captain",
#                 "smoker's_subordinate", "sword_collector",
#
#                 # Titles and positions
#                 "marine_captain", "g-5_officer", "sword_specialist",
#                 "smoker's_right_hand", "marine_headquarters",
#
#                 # Special abilities and powers
#                 "swordsmanship", "rokushiki_trainee", "sword_mastery",
#                 "shigure_wielder", "martial_arts", "weapon_expert",
#
#                 # Combat specialties
#                 "sword_techniques", "meito_knowledge", "blade_mastery",
#                 "marine_combat", "sword_collection_expertise",
#
#                 # Teams and affiliations
#                 "marine_forces", "g-5_base", "sword_unit",
#                 "smoker_unit", "world_government",
#
#                 # Time periods and versions
#                 "pre_timeskip", "post_timeskip", "alabasta_arc",
#                 "punk_hazard", "current_tashigi", "loguetown_tashigi",
#
#                 # Forms and states
#                 "battle_mode", "training_mode", "officer_mode",
#                 "clumsy_state", "serious_mode", "determined_state",
#
#                 # Outfits and appearances
#                 "marine_uniform", "casual_clothes", "training_gear",
#                 "battle_outfit", "glasses", "captain_coat",
#
#                 # Emotional states
#                 "determined_tashigi", "serious_tashigi", "clumsy_tashigi",
#                 "fighting_tashigi", "professional_mode", "leadership_mode",
#
#                 # Specific arcs and events
#                 "loguetown_arc", "alabasta_saga", "punk_hazard",
#                 "dressrosa_events", "marine_operations"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "tashigi", "tashigi_(one_piece)", "marine_captain",
#
#                 # Roles and abilities
#                 "swordswoman", "g-5_officer", "glasses",
#
#                 # States and forms
#                 "battle_mode", "officer_mode", "training_mode",
#
#                 # Time periods
#                 "pre_timeskip", "post_timeskip", "current_era"
#             ]
#         },
#
#         "hina": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "hina", "hina_(one_piece)", "black_cage_hina",
#                 "marine_captain", "cage_specialist",
#
#                 # Titles and positions
#                 "marine_captain", "black_cage", "prison_specialist",
#                 "headquarters_officer", "marine_commander",
#
#                 # Special abilities and powers
#                 "cage_cage_fruit", "ori_ori_no_mi", "binding_powers",
#                 "cage_creation", "marine_combat", "imprisonment_specialist",
#
#                 # Combat abilities
#                 "cage_techniques", "binding_attacks", "marine_martial_arts",
#                 "capture_specialist", "restraining_moves",
#
#                 # Teams and affiliations
#                 "marine_forces", "marine_headquarters", "prison_unit",
#                 "world_government", "justice_enforcers",
#
#                 # Time periods and versions
#                 "pre_timeskip", "post_timeskip", "alabasta_arc",
#                 "marineford_war", "current_hina",
#
#                 # Forms and states
#                 "battle_mode", "commander_mode", "capture_mode",
#                 "officer_state", "serious_mode",
#
#                 # Outfits and appearances
#                 "marine_uniform", "captain_coat", "formal_uniform",
#                 "battle_gear", "casual_clothes",
#
#                 # Emotional states
#                 "serious_hina", "commanding_hina", "professional_hina",
#                 "battle_ready", "leadership_mode"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "hina", "hina_(one_piece)", "black_cage",
#
#                 # Powers and roles
#                 "cage_cage_fruit", "marine_captain",
#
#                 # States and forms
#                 "battle_mode", "officer_mode", "capture_mode"
#             ]
#         },
#
#         "momousagi": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "momousagi", "gion", "pink_rabbit",
#                 "vice_admiral_momousagi", "marine_leader",
#
#                 # Titles and positions
#                 "vice_admiral", "admiral_candidate", "headquarters_leader",
#                 "marine_executive", "high_ranking_officer",
#
#                 # Combat abilities
#                 "advanced_haki", "marine_combat", "leadership_skills",
#                 "strategic_command", "battlefield_control",
#
#                 # Teams and affiliations
#                 "marine_headquarters", "world_government",
#                 "vice_admiral_unit", "marine_leadership",
#
#                 # Time periods and versions
#                 "marine_era", "current_momousagi", "post_timeskip",
#                 "reverie_period",
#
#                 # Outfits and appearances
#                 "vice_admiral_uniform", "marine_formal_wear",
#                 "battle_attire", "officer_coat",
#
#                 # Emotional states
#                 "professional_mode", "commander_mode", "serious_momousagi",
#                 "leadership_presence"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "momousagi", "gion", "pink_rabbit",
#
#                 # Roles and positions
#                 "vice_admiral", "marine_officer",
#
#                 # States
#                 "commander_mode", "battle_mode"
#             ]
#         },
#
#         "tsuru": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "tsuru", "tsuru_(one_piece)", "great_staff_officer",
#                 "marine_legend", "cleaner",
#
#                 # Titles and positions
#                 "vice_admiral", "great_staff_officer", "marine_veteran",
#                 "strategic_commander", "legendary_marine",
#
#                 # Special abilities and powers
#                 "wash_wash_fruit", "woshu_woshu_no_mi", "cleansing_power",
#                 "strategic_genius", "veteran_combat", "advanced_haki",
#
#                 # Combat abilities
#                 "washing_techniques", "purification_powers",
#                 "tactical_combat", "leadership_skills", "marine_arts",
#
#                 # Teams and affiliations
#                 "marine_headquarters", "world_government",
#                 "vice_admiral_unit", "veteran_officers",
#
#                 # Time periods and versions
#                 "roger_era", "pre_timeskip", "post_timeskip",
#                 "marineford_war", "current_tsuru", "golden_age",
#
#                 # Forms and states
#                 "battle_mode", "commander_mode", "strategic_mode",
#                 "veteran_state", "leadership_presence",
#
#                 # Outfits and appearances
#                 "vice_admiral_uniform", "marine_coat",
#                 "formal_attire", "battle_gear",
#
#                 # Emotional states
#                 "wise_tsuru", "commanding_tsuru", "serious_tsuru",
#                 "strategic_mind", "veteran_presence"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "tsuru", "tsuru_(one_piece)", "great_staff_officer",
#
#                 # Powers and roles
#                 "wash_wash_fruit", "vice_admiral", "marine_legend",
#
#                 # States and eras
#                 "battle_mode", "commander_mode", "veteran_state"
#             ]
#         },
#
#         "stussy": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "stussy", "stussy_(one_piece)", "cp0_agent",
#                 "queen_of_pleasure", "world_noble_agent",
#
#                 # Titles and positions
#                 "cp0_operative", "undercover_agent", "intelligence_officer",
#                 "pleasure_district_queen", "world_government_agent",
#
#                 # Special abilities and powers
#                 "assassination_skills", "espionage_mastery",
#                 "combat_expertise", "undercover_operations",
#                 "intelligence_gathering",
#
#                 # Combat abilities
#                 "rokushiki", "stealth_techniques", "cp0_combat",
#                 "assassination_methods", "covert_operations",
#
#                 # Teams and affiliations
#                 "cipher_pol_0", "world_government", "intelligence_bureau",
#                 "undercover_network", "pleasure_district",
#
#                 # Time periods and versions
#                 "whole_cake_island", "current_stussy", "undercover_era",
#                 "cp0_period",
#
#                 # Forms and states
#                 "agent_mode", "undercover_mode", "battle_mode",
#                 "queen_persona", "operative_state",
#
#                 # Outfits and appearances
#                 "formal_dress", "agent_attire", "disguise_outfit",
#                 "battle_gear", "elegant_clothes",
#
#                 # Emotional states
#                 "professional_stussy", "undercover_persona",
#                 "serious_agent", "elegant_mode", "operative_mindset"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "stussy", "stussy_(one_piece)", "cp0",
#
#                 # Roles and abilities
#                 "agent", "assassin", "undercover_operative",
#
#                 # States and forms
#                 "agent_mode", "battle_mode", "undercover_mode"
#             ]
#         },
#
#         "koala": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "koala", "koala_(one_piece)", "revolutionary_officer",
#                 "fishman_karate_user", "former_slave",
#
#                 # Titles and positions
#                 "revolutionary_army_officer", "fishman_karate_instructor",
#                 "freedom_fighter", "assistant_fishman_karate_instructor",
#                 "east_army_officer",
#
#                 # Special abilities and powers
#                 "fishman_karate", "advanced_martial_arts",
#                 "revolutionary_techniques", "combat_expertise",
#                 "stealth_operations", "infiltration_skills",
#
#                 # Combat specialties
#                 "fishman_karate_moves", "revolutionary_combat",
#                 "martial_arts_master", "water_manipulation",
#                 "hand-to-hand_combat",
#
#                 # Teams and affiliations
#                 "revolutionary_army", "east_army", "sabo's_partner",
#                 "fishman_karate_practitioners", "former_sun_pirates",
#
#                 # Background elements
#                 "former_slave", "sun_pirates_mark", "fisher_tiger's_ward",
#                 "revolutionary_training", "freedom_fighter",
#
#                 # Time periods and versions
#                 "young_koala", "slave_era", "sun_pirates_era",
#                 "current_koala", "revolutionary_koala",
#
#                 # Forms and states
#                 "battle_mode", "instructor_mode", "revolutionary_mode",
#                 "stealth_mode", "teaching_state",
#
#                 # Outfits and appearances
#                 "revolutionary_uniform", "combat_gear", "training_outfit",
#                 "stealth_clothes", "casual_wear",
#
#                 # Emotional states
#                 "cheerful_koala", "serious_koala", "instructor_koala",
#                 "determined_koala", "battle_ready"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "koala", "koala_(one_piece)", "revolutionary_army",
#
#                 # Powers and roles
#                 "fishman_karate", "revolutionary_officer",
#
#                 # States and forms
#                 "battle_mode", "instructor_mode", "revolutionary_mode",
#
#                 # Time periods
#                 "young_koala", "current_era", "revolutionary_era"
#             ]
#         },
#
#         "belo_betty": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "belo_betty", "betty_(one_piece)", "east_army_commander",
#                 "revolutionary_commander", "flag_bearer",
#
#                 # Titles and positions
#                 "east_army_commander", "revolutionary_commander",
#                 "morale_booster", "army_leader", "flag_bearer",
#
#                 # Special abilities and powers
#                 "pump_pump_fruit", "mero_mero_no_mi", "morale_boost",
#                 "flag_powers", "inspiration_ability", "army_enhancement",
#
#                 # Combat abilities
#                 "revolutionary_combat", "flag_techniques",
#                 "leadership_skills", "army_command", "morale_control",
#
#                 # Teams and affiliations
#                 "revolutionary_army", "east_army", "dragon's_commanders",
#                 "liberation_forces", "revolutionary_leadership",
#
#                 # Time periods and versions
#                 "pre_reverie", "current_betty", "commander_era",
#                 "revolutionary_period",
#
#                 # Forms and states
#                 "commander_mode", "battle_mode", "rally_mode",
#                 "leadership_state", "inspiration_form",
#
#                 # Outfits and appearances
#                 "revolutionary_uniform", "commander_outfit", "battle_gear",
#                 "flag_bearer_clothes", "liberation_attire",
#
#                 # Emotional states
#                 "commanding_betty", "inspiring_betty", "determined_betty",
#                 "battle_ready", "leadership_mode"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "belo_betty", "betty_(one_piece)", "revolutionary_army",
#
#                 # Powers and roles
#                 "pump_pump_fruit", "east_army_commander",
#
#                 # States and forms
#                 "commander_mode", "battle_mode", "rally_mode"
#             ]
#         },
#
#         "lindbergh": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "lindbergh", "lindbergh_(one_piece)", "north_army_commander",
#                 "revolutionary_inventor", "tech_specialist",
#
#                 # Titles and positions
#                 "north_army_commander", "revolutionary_commander",
#                 "technology_officer", "weapons_developer",
#
#                 # Special abilities and powers
#                 "technological_expertise", "invention_skills",
#                 "revolutionary_tech", "combat_engineering",
#
#                 # Combat specialties
#                 "tech_warfare", "revolutionary_combat", "gadget_mastery",
#                 "invention_deployment", "strategic_technology",
#
#                 # Teams and affiliations
#                 "revolutionary_army", "north_army", "tech_division",
#                 "dragon's_commanders", "revolutionary_leadership",
#
#                 # Time periods and versions
#                 "pre_reverie", "current_lindbergh", "commander_era",
#                 "revolutionary_period",
#
#                 # Forms and states
#                 "inventor_mode", "battle_mode", "commander_mode",
#                 "tech_development_state",
#
#                 # Outfits and appearances
#                 "revolutionary_uniform", "tech_gear", "inventor_outfit",
#                 "commander_clothes", "battle_equipment"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "lindbergh", "lindbergh_(one_piece)", "revolutionary_army",
#
#                 # Roles and abilities
#                 "inventor", "north_army_commander", "tech_specialist"
#             ]
#         },
#
#         "karasu": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "karasu", "karasu_(one_piece)", "north_army_commander",
#                 "crow_commander", "revolutionary_leader",
#
#                 # Titles and positions
#                 "north_army_commander", "revolutionary_commander",
#                 "crow_master", "stealth_specialist",
#
#                 # Special abilities and powers
#                 "crow_abilities", "stealth_techniques",
#                 "revolutionary_combat", "crow_control",
#
#                 # Combat specialties
#                 "crow_warfare", "stealth_operations", "revolutionary_tactics",
#                 "shadow_combat", "bird_control",
#
#                 # Teams and affiliations
#                 "revolutionary_army", "north_army", "dragon's_commanders",
#                 "revolutionary_leadership", "stealth_division",
#
#                 # Forms and states
#                 "crow_form", "commander_mode", "battle_mode",
#                 "stealth_mode", "leadership_state",
#
#                 # Outfits and appearances
#                 "revolutionary_uniform", "crow_mask", "commander_gear",
#                 "stealth_outfit", "battle_attire"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "karasu", "karasu_(one_piece)", "revolutionary_army",
#
#                 # Roles and abilities
#                 "north_army_commander", "crow_master",
#
#                 # States and forms
#                 "crow_form", "stealth_mode", "commander_mode"
#             ]
#         },
#
#         "bellemere": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "bellemere", "bell-mère", "belle_mere_(one_piece)",
#                 "nami's_adoptive_mother", "marine_veteran",
#
#                 # Titles and positions
#                 "former_marine", "tangerine_farmer", "adoptive_mother",
#                 "marine_officer", "cocoyashi_resident",
#
#                 # Combat abilities
#                 "marine_training", "firearms_expert", "combat_skills",
#                 "marine_martial_arts", "tactical_expertise",
#
#                 # Teams and affiliations
#                 "marine_forces_(former)", "cocoyashi_village",
#                 "nami's_family", "nojiko's_family",
#
#                 # Time periods and versions
#                 "marine_days", "mother_era", "young_bellemere",
#                 "final_moments", "flashback_bellemere",
#
#                 # Special characteristics
#                 "marine_veteran", "protective_mother", "fierce_spirit",
#                 "strong_will", "sacrifice_for_family",
#
#                 # Outfits and appearances
#                 "marine_uniform", "casual_clothes", "farmer_outfit",
#                 "battle_gear", "civilian_attire",
#
#                 # Emotional states
#                 "protective_bellemere", "caring_mother", "fierce_marine",
#                 "determined_bellemere", "loving_parent"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "bellemere", "bell-mère", "belle_mere_(one_piece)",
#
#                 # Roles and positions
#                 "former_marine", "nami's_mother", "marine_veteran",
#
#                 # Time periods
#                 "marine_era", "mother_era", "flashback_era"
#             ]
#         },
#
#         "isuka": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "isuka", "isuka_(one_piece)", "drill_instructor",
#                 "marine_captain", "smoke_chaser",
#
#                 # Titles and positions
#                 "marine_captain", "training_instructor",
#                 "special_instructor", "ace's_pursuer",
#
#                 # Special abilities and powers
#                 "smoke_smoke_fruit", "smoke_powers", "marine_combat",
#                 "instructor_skills", "pursuit_specialist",
#
#                 # Combat abilities
#                 "smoke_manipulation", "marine_techniques",
#                 "training_expertise", "pursuit_tactics",
#
#                 # Teams and affiliations
#                 "marine_forces", "training_division",
#                 "pursuit_unit", "marine_headquarters",
#
#                 # Time periods and versions
#                 "pre_timeskip", "ace_era", "training_period",
#                 "marine_captain_era",
#
#                 # Forms and states
#                 "smoke_form", "instructor_mode", "battle_mode",
#                 "pursuit_mode", "training_state",
#
#                 # Outfits and appearances
#                 "marine_uniform", "captain_coat", "training_gear",
#                 "battle_outfit", "pursuit_attire"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "isuka", "isuka_(one_piece)", "marine_captain",
#
#                 # Powers and roles
#                 "smoke_smoke_fruit", "drill_instructor",
#
#                 # States and forms
#                 "smoke_form", "instructor_mode", "battle_mode"
#             ]
#         },
#
#         "ain": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "ain", "ain_(one_piece)", "neo_marines",
#                 "zephyr's_subordinate", "marine_officer",
#
#                 # Titles and positions
#                 "neo_marine_officer", "former_marine",
#                 "zephyr's_student", "special_forces",
#
#                 # Special abilities and powers
#                 "modo_modo_no_mi", "age_manipulation",
#                 "marine_combat", "tactical_skills",
#
#                 # Combat abilities
#                 "age_control", "marine_techniques", "tactical_combat",
#                 "special_operations", "age_regression",
#
#                 # Teams and affiliations
#                 "neo_marines", "former_marine_forces",
#                 "zephyr's_forces", "special_unit",
#
#                 # Time periods and versions
#                 "marine_era", "neo_marine_period", "film_z",
#                 "special_forces_era",
#
#                 # Forms and states
#                 "battle_mode", "officer_mode", "age_control_state",
#                 "tactical_mode", "combat_ready",
#
#                 # Outfits and appearances
#                 "neo_marine_uniform", "battle_gear", "officer_attire",
#                 "combat_outfit", "mission_gear"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "ain", "ain_(one_piece)", "neo_marines",
#
#                 # Powers and roles
#                 "modo_modo_no_mi", "marine_officer",
#
#                 # States and forms
#                 "battle_mode", "officer_mode", "age_control"
#             ]
#         },
#
#         "sadi": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "sadi", "sadi_(one_piece)", "chief_guard",
#                 "impel_down_officer", "sadistic_guard",
#
#                 # Titles and positions
#                 "chief_guard", "impel_down_staff", "torture_specialist",
#                 "prison_officer", "security_chief",
#
#                 # Combat abilities
#                 "whip_mastery", "torture_techniques", "combat_skills",
#                 "prison_control", "guard_expertise",
#
#                 # Teams and affiliations
#                 "impel_down", "world_government", "prison_staff",
#                 "security_forces", "guard_unit",
#
#                 # Time periods and versions
#                 "impel_down_arc", "prison_era", "current_sadi",
#
#                 # Forms and states
#                 "guard_mode", "battle_mode", "torture_mode",
#                 "command_state", "prison_duty",
#
#                 # Outfits and appearances
#                 "guard_uniform", "prison_attire", "battle_gear",
#                 "officer_outfit", "security_uniform"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "sadi", "sadi_(one_piece)", "impel_down",
#
#                 # Roles and abilities
#                 "chief_guard", "whip_user", "prison_officer",
#
#                 # States
#                 "guard_mode", "battle_mode", "command_mode"
#             ]
#         },
#
#         "domino": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "domino", "domino_(one_piece)", "impel_down_guard",
#                 "vice_chief_guard", "prison_officer",
#
#                 # Titles and positions
#                 "vice_chief_guard", "impel_down_staff",
#                 "security_officer", "prison_authority",
#
#                 # Combat abilities
#                 "guard_combat", "prison_techniques", "security_skills",
#                 "defensive_tactics", "staff_expertise",
#
#                 # Teams and affiliations
#                 "impel_down", "world_government", "prison_staff",
#                 "security_forces", "guard_unit",
#
#                 # Time periods and versions
#                 "impel_down_arc", "prison_era", "current_domino",
#
#                 # Forms and states
#                 "guard_mode", "officer_mode", "security_state",
#                 "prison_duty", "authority_mode",
#
#                 # Outfits and appearances
#                 "guard_uniform", "prison_attire", "officer_outfit",
#                 "security_gear", "staff_uniform"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "domino", "domino_(one_piece)", "impel_down",
#
#                 # Roles
#                 "vice_chief_guard", "prison_officer",
#
#                 # States
#                 "guard_mode", "officer_mode", "security_mode"
#             ]
#         },
#
#         "charlotte_pudding": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "charlotte_pudding", "pudding_(one_piece)",
#                 "three_eye_tribe", "charlotte_family",
#                 "sanji's_arranged_bride",
#
#                 # Titles and positions
#                 "minister_of_chocolate", "cafe_owner", "third_eye",
#                 "charlotte_daughter", "arranged_bride",
#
#                 # Special abilities and powers
#                 "memory_manipulation", "memo_memo_no_mi",
#                 "third_eye_powers", "memory_editing",
#                 "potential_poneglyph_reader",
#
#                 # Racial traits
#                 "three_eye_tribe", "third_eye", "hybrid_race",
#                 "special_lineage", "unique_abilities",
#
#                 # Combat abilities
#                 "memory_alteration", "deception_skills",
#                 "emotional_manipulation", "cooking_expertise",
#
#                 # Teams and affiliations
#                 "big_mom_pirates", "charlotte_family",
#                 "totland_ministers", "cafe_staff",
#
#                 # Forms and states
#                 "sweet_persona", "true_personality", "crying_state",
#                 "conflicted_mode", "chef_mode", "third_eye_revealed",
#
#                 # Special characteristics
#                 "split_personality", "memory_control", "cooking_skills",
#                 "third_eye_abilities", "emotional_instability",
#
#                 # Time periods and versions
#                 "pre_wedding", "wedding_ceremony", "post_wedding",
#                 "current_pudding", "childhood_pudding",
#
#                 # Outfits and appearances
#                 "wedding_dress", "cafe_uniform", "minister_outfit",
#                 "casual_clothes", "chef_attire",
#
#                 # Emotional states
#                 "sweet_pudding", "dark_pudding", "crying_pudding",
#                 "tsundere_mode", "conflicted_pudding"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "charlotte_pudding", "pudding_(one_piece)",
#
#                 # Powers and traits
#                 "three_eye_tribe", "memo_memo_no_mi",
#
#                 # States and forms
#                 "sweet_persona", "dark_persona", "third_eye_revealed"
#             ]
#         },
#
#         "charlotte_smoothie": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "charlotte_smoothie", "smoothie_(one_piece)",
#                 "sweet_commander", "longleg_tribe",
#
#                 # Titles and positions
#                 "sweet_commander", "minister_of_juice",
#                 "charlotte_daughter", "big_mom_executive",
#
#                 # Special abilities and powers
#                 "wring_wring_fruit", "shibo_shibo_no_mi",
#                 "liquid_extraction", "size_manipulation",
#                 "strength_enhancement",
#
#                 # Combat abilities
#                 "sword_techniques", "liquid_manipulation",
#                 "giant_form", "wringing_powers", "executive_combat",
#
#                 # Teams and affiliations
#                 "big_mom_pirates", "charlotte_family",
#                 "sweet_commanders", "totland_ministers",
#
#                 # Forms and states
#                 "normal_size", "giant_form", "battle_mode",
#                 "commander_mode", "juice_extraction",
#
#                 # Special characteristics
#                 "longleg_tribe", "executive_power", "massive_size",
#                 "liquid_powers", "commander_authority",
#
#                 # Time periods and versions
#                 "pre_wedding", "tea_party", "chase_period",
#                 "current_smoothie", "commander_era",
#
#                 # Outfits and appearances
#                 "commander_outfit", "minister_clothes", "battle_gear",
#                 "formal_attire", "pirate_uniform",
#
#                 # Emotional states
#                 "serious_smoothie", "commander_mode", "battle_ready",
#                 "executive_presence", "determined_smoothie"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "charlotte_smoothie", "smoothie_(one_piece)",
#
#                 # Powers and roles
#                 "wring_wring_fruit", "sweet_commander",
#
#                 # States and forms
#                 "normal_form", "giant_form", "battle_mode"
#             ]
#         },
#
#         "charlotte_amande": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "charlotte_amande", "amande_(one_piece)",
#                 "demon_lady", "snake_neck",
#
#                 # Titles and positions
#                 "minister_of_nuts", "charlotte_daughter",
#                 "big_mom_executive", "swordmaster",
#
#                 # Special abilities and powers
#                 "sword_mastery", "snake_neck_abilities",
#                 "executive_combat", "slow_killing_technique",
#
#                 # Combat abilities
#                 "sword_techniques", "slow_slicing", "neck_extension",
#                 "executive_fighting", "meito_wielder",
#
#                 # Teams and affiliations
#                 "big_mom_pirates", "charlotte_family",
#                 "totland_ministers", "executive_officers",
#
#                 # Forms and states
#                 "battle_mode", "executive_mode", "swordmaster_stance",
#                 "intimidation_mode", "minister_state",
#
#                 # Special characteristics
#                 "snake_neck", "long_neck_tribe", "sword_expert",
#                 "executive_authority", "intimidating_presence",
#
#                 # Time periods and versions
#                 "pre_wedding", "tea_party", "current_amande",
#                 "executive_era", "minister_period",
#
#                 # Outfits and appearances
#                 "executive_outfit", "minister_clothes", "battle_gear",
#                 "formal_attire", "pirate_uniform",
#
#                 # Emotional states
#                 "serious_amande", "cold_blooded", "executive_mode",
#                 "intimidating_presence", "calculated_amande"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "charlotte_amande", "amande_(one_piece)",
#
#                 # Roles and traits
#                 "minister_of_nuts", "snake_neck",
#
#                 # States and forms
#                 "battle_mode", "executive_mode", "swordmaster_mode"
#             ]
#         },
#
#         "charlotte_flampe": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "charlotte_flampe", "flampe_(one_piece)",
#                 "special_forces_commander", "charlotte_family",
#
#                 # Titles and positions
#                 "special_forces_leader", "charlotte_daughter",
#                 "hobby_hobby_squad_commander", "sniper_captain",
#
#                 # Special abilities and powers
#                 "dart_expertise", "leadership_skills",
#                 "sniper_abilities", "youth_division_command",
#
#                 # Combat abilities
#                 "dart_shooting", "tactical_command",
#                 "squad_leadership", "ranged_combat",
#
#                 # Teams and affiliations
#                 "big_mom_pirates", "charlotte_family",
#                 "special_forces", "hobby_hobby_squad",
#
#                 # Forms and states
#                 "commander_mode", "battle_mode", "sniper_mode",
#                 "leadership_state", "childish_state",
#
#                 # Special characteristics
#                 "youth_leader", "sibling_worship", "bratty_personality",
#                 "command_authority", "sniper_skills",
#
#                 # Time periods and versions
#                 "katakuri_fight", "current_flampe", "commander_era",
#
#                 # Outfits and appearances
#                 "commander_outfit", "special_forces_uniform",
#                 "casual_clothes", "battle_gear",
#
#                 # Emotional states
#                 "bratty_flampe", "commanding_flampe", "excited_flampe",
#                 "idolizing_mode", "childish_flampe"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "charlotte_flampe", "flampe_(one_piece)",
#
#                 # Roles and abilities
#                 "special_forces_commander", "sniper",
#
#                 # States and forms
#                 "commander_mode", "battle_mode", "childish_mode"
#             ]
#         },
#
#         "conis": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "conis", "conis_(one_piece)", "skypiean",
#                 "angel_island_resident", "sky_inhabitant",
#
#                 # Positions and roles
#                 "skypiean_guide", "angel_beach_resident",
#                 "cloud_fox_owner", "harp_player",
#
#                 # Special characteristics
#                 "skypiean_wings", "angel_resident", "musical_talent",
#                 "cloud_dweller", "sky_island_native",
#
#                 # Teams and affiliations
#                 "angel_island", "skypiea_resistance",
#                 "straw_hat_allies", "upper_yard_rebels",
#
#                 # Time periods and versions
#                 "skypiea_arc", "resistance_period", "current_conis",
#                 "pre_liberation", "post_liberation",
#
#                 # Outfits and appearances
#                 "skypiean_clothes", "angel_dress", "casual_wear",
#                 "traditional_outfit", "resistance_gear",
#
#                 # Emotional states
#                 "friendly_conis", "determined_conis", "helpful_conis",
#                 "brave_conis", "resistance_member"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "conis", "conis_(one_piece)", "skypiean",
#
#                 # Traits and roles
#                 "angel_wings", "sky_dweller",
#
#                 # States
#                 "guide_mode", "resistance_mode"
#             ]
#         },
#
#         "kalifa": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "kalifa", "kalifa_(one_piece)", "cp9_agent",
#                 "water_7_secretary", "bubble_master",
#
#                 # Titles and positions
#                 "cp9_agent", "iceburg's_secretary", "assassin",
#                 "government_agent", "undercover_operative",
#
#                 # Special abilities and powers
#                 "bubble_bubble_fruit", "awa_awa_no_mi",
#                 "rokushiki_master", "six_powers", "soap_powers",
#
#                 # Combat abilities
#                 "rokushiki", "soap_techniques", "assassination_skills",
#                 "martial_arts", "government_combat",
#
#                 # Teams and affiliations
#                 "cp9", "world_government", "galley-la_(former)",
#                 "cipher_pol", "assassin_unit",
#
#                 # Forms and states
#                 "secretary_mode", "agent_mode", "battle_mode",
#                 "bubble_form", "undercover_state",
#
#                 # Time periods and versions
#                 "water_7_arc", "enies_lobby_arc", "cp9_era",
#                 "secretary_period", "current_kalifa",
#
#                 # Outfits and appearances
#                 "secretary_outfit", "agent_clothes", "battle_gear",
#                 "office_attire", "assassin_uniform",
#
#                 # Emotional states
#                 "professional_kalifa", "serious_agent", "battle_ready",
#                 "undercover_mode", "assassin_mindset"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "kalifa", "kalifa_(one_piece)", "cp9",
#
#                 # Powers and roles
#                 "bubble_bubble_fruit", "rokushiki", "assassin",
#
#                 # States and forms
#                 "agent_mode", "battle_mode", "secretary_mode"
#             ]
#         },
#
#         "mozu_and_kiwi": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "mozu", "kiwi", "square_sisters",
#                 "franky_family", "water_7_duo",
#
#                 # Positions and roles
#                 "franky_family_members", "water_7_residents",
#                 "square_sisters", "shipwright_assistants",
#
#                 # Combat abilities
#                 "dual_fighting", "synchronized_combat",
#                 "square_style", "franky_family_techniques",
#
#                 # Teams and affiliations
#                 "franky_family", "galley-la_allies",
#                 "water_7_citizens", "straw_hat_allies",
#
#                 # Time periods and versions
#                 "water_7_arc", "enies_lobby_arc", "current_era",
#
#                 # Outfits and appearances
#                 "square_hair", "franky_family_clothes",
#                 "water_7_fashion", "matching_outfits",
#
#                 # Emotional states
#                 "synchronized_sisters", "loyal_members",
#                 "supportive_duo", "determined_sisters"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "mozu", "kiwi", "square_sisters",
#
#                 # Roles and affiliations
#                 "franky_family", "water_7",
#
#                 # States
#                 "synchronized_mode", "battle_mode"
#             ]
#         },
#
#         "kumadori's_mother": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "kumadori's_mother", "kumadori_mother",
#                 "cp9_agent_parent", "rokushiki_master",
#
#                 # Titles and positions
#                 "rokushiki_master", "cipher_pol_agent",
#                 "government_assassin", "martial_artist",
#
#                 # Combat abilities
#                 "rokushiki", "life_return", "assassination_skills",
#                 "martial_arts_master", "government_techniques",
#
#                 # Teams and affiliations
#                 "cipher_pol", "world_government",
#                 "assassination_unit", "kumadori_family",
#
#                 # Time periods and versions
#                 "flashback_era", "cipher_pol_days", "kumadori_childhood"
#             ],
#             "danbooru": [
#                 "kumadori's_mother", "kumadori_family",
#                 "cipher_pol", "rokushiki_master"
#             ]
#         },
#
#         # Baratie Arc
#         "zeff's_mother": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "zeff's_mother", "zeff_mother", "sanji_flashback",
#
#                 # Roles and positions
#                 "cook's_mother", "baratie_backstory", "east_blue_resident",
#
#                 # Time periods and versions
#                 "flashback_character", "zeff_childhood", "past_era"
#             ],
#             "danbooru": [
#                 "zeff's_mother", "baratie_arc", "flashback_character"
#             ]
#         },
#
#         # Drum Island Complete
#         "kureha": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "kureha", "kureha_(one_piece)", "dr_kureha",
#                 "witch_doctor", "drum_kingdom_doctor",
#
#                 # Titles and positions
#                 "doctor_kureha", "witch_of_drum", "medical_expert",
#                 "drum_castle_resident", "chopper's_mentor",
#
#                 # Special characteristics
#                 "medical_knowledge", "longevity_techniques",
#                 "doctor_skills", "winter_specialist", "mentor",
#
#                 # Teams and affiliations
#                 "drum_kingdom", "medical_practitioners",
#                 "chopper's_teachers", "castle_doctors",
#
#                 # Time periods and versions
#                 "drum_island_arc", "pre_timeskip", "current_kureha",
#                 "flashback_kureha", "doctor_era",
#
#                 # Outfits and appearances
#                 "doctor_coat", "winter_clothes", "medical_gear",
#                 "casual_wear", "drum_castle_attire",
#
#                 # Emotional states
#                 "stern_doctor", "caring_mentor", "wise_kureha",
#                 "teaching_mode", "medical_authority"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "kureha", "kureha_(one_piece)", "dr_kureha",
#
#                 # Roles and positions
#                 "doctor", "witch", "mentor",
#
#                 # States and periods
#                 "medical_mode", "teaching_mode", "drum_island"
#             ]
#         },
#
#         # Long Ring Long Land Complete
#         "porche": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "porche", "porche_(one_piece)", "foxy_pirate",
#                 "idol_performer", "foxy_crew",
#
#                 # Titles and positions
#                 "foxy_pirates_idol", "crew_performer",
#                 "davy_back_fighter", "crew_member",
#
#                 # Special abilities
#                 "performance_skills", "combat_abilities",
#                 "crew_support", "entertainment_talent",
#
#                 # Teams and affiliations
#                 "foxy_pirates", "davy_back_crew",
#                 "performance_unit", "foxy's_crew",
#
#                 # Time periods and versions
#                 "long_ring_long_land", "davy_back_fight",
#                 "current_porche", "pre_timeskip",
#
#                 # Outfits and appearances
#                 "performer_outfit", "pirate_clothes",
#                 "crew_uniform", "battle_gear",
#
#                 # Emotional states
#                 "cheerful_porche", "performing_mode",
#                 "competitive_spirit", "crew_loyalty"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "porche", "porche_(one_piece)",
#
#                 # Roles and affiliations
#                 "foxy_pirates", "performer",
#
#                 # States and forms
#                 "performance_mode", "battle_mode"
#             ]
#         },
#
#         # Amazon Lily Additional Character
#         "marguerite": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "marguerite", "marguerite_(one_piece)",
#                 "kuja_warrior", "amazon_lily_archer",
#
#                 # Titles and positions
#                 "kuja_warrior", "elite_archer", "amazon_guard",
#                 "hancock's_subordinate", "luffy's_friend",
#
#                 # Combat abilities
#                 "archery_master", "haki_arrows", "kuja_combat",
#                 "snake_bow_user", "warrior_skills",
#
#                 # Teams and affiliations
#                 "kuja_pirates", "amazon_lily", "hancock's_guards",
#                 "warrior_tribe", "snake_army",
#
#                 # Time periods and versions
#                 "amazon_lily_arc", "pre_timeskip", "current_marguerite",
#
#                 # Outfits and appearances
#                 "kuja_outfit", "warrior_attire", "tribal_clothes",
#                 "battle_gear", "amazon_dress",
#
#                 # Emotional states
#                 "friendly_marguerite", "curious_marguerite",
#                 "warrior_mode", "protective_marguerite"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "marguerite", "marguerite_(one_piece)",
#
#                 # Roles and abilities
#                 "kuja_warrior", "archer", "amazon_lily",
#
#                 # States and forms
#                 "warrior_mode", "battle_mode", "friendly_mode"
#             ]
#         },
#
#         "spandam's_secretary": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "spandam's_secretary", "enies_lobby_secretary",
#                 "government_worker", "tower_staff",
#
#                 # Titles and positions
#                 "cp9_secretary", "tower_of_justice_staff",
#                 "government_employee", "office_worker",
#
#                 # Teams and affiliations
#                 "enies_lobby", "world_government",
#                 "spandam's_staff", "tower_personnel",
#
#                 # Time periods and versions
#                 "enies_lobby_arc", "pre_timeskip",
#                 "tower_of_justice_era"
#             ],
#             "danbooru": [
#                 "spandam's_secretary", "enies_lobby",
#                 "tower_of_justice", "secretary"
#             ]
#         },
#
#         # Syrup Village Arc (Complete)
#         "kaya": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "kaya", "kaya_(one_piece)", "syrup_village_resident",
#                 "mansion_owner", "aspiring_doctor",
#
#                 # Titles and positions
#                 "mansion_mistress", "medical_student",
#                 "wealthy_heiress", "usopp's_friend",
#
#                 # Special characteristics
#                 "medical_knowledge", "kind_heart",
#                 "wealthy_background", "illness_recovery",
#
#                 # Teams and affiliations
#                 "syrup_village", "going_merry_donor",
#                 "usopp_pirates_supporter", "village_elite",
#
#                 # Time periods and versions
#                 "syrup_village_arc", "pre_timeskip",
#                 "current_kaya", "recovery_period",
#
#                 # Outfits and appearances
#                 "mansion_clothes", "casual_wear",
#                 "medical_student_attire", "wealthy_dress",
#
#                 # Emotional states
#                 "kind_kaya", "determined_student",
#                 "grateful_friend", "caring_personality"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "kaya", "kaya_(one_piece)",
#
#                 # Roles and positions
#                 "medical_student", "mansion_owner",
#
#                 # States and periods
#                 "recovery_mode", "studying_mode"
#             ]
#         },
#
#         "merry": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "merry", "merry_(one_piece)", "kaya's_butler",
#                 "mansion_servant", "loyal_butler",
#
#                 # Titles and positions
#                 "head_butler", "mansion_staff",
#                 "kaya's_servant", "household_manager",
#
#                 # Teams and affiliations
#                 "syrup_village", "mansion_staff",
#                 "kaya's_household", "village_elite",
#
#                 # Time periods and versions
#                 "syrup_village_arc", "pre_timeskip",
#                 "current_merry", "mansion_era",
#
#                 # Outfits and appearances
#                 "butler_uniform", "formal_wear",
#                 "servant_attire", "professional_clothes",
#
#                 # Emotional states
#                 "loyal_servant", "protective_butler",
#                 "caring_merry", "dutiful_staff"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "merry", "merry_(one_piece)",
#
#                 # Roles
#                 "butler", "servant",
#
#                 # States
#                 "service_mode", "protective_mode"
#             ]
#         },
#
#         # Orange Town Arc (Complete)
#         "chouchou's_owner": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "hocker", "pet_shop_owner",
#                 "orange_town_resident", "chouchou's_master",
#
#                 # Roles and positions
#                 "shop_owner", "pet_store_proprietor",
#                 "dog_owner", "town_resident",
#
#                 # Teams and affiliations
#                 "orange_town", "shop_keepers",
#                 "civilian_population",
#
#                 # Time periods and versions
#                 "orange_town_arc", "flashback_era",
#                 "pre_timeskip"
#             ],
#             "danbooru": [
#                 "hocker", "pet_shop_owner",
#                 "orange_town", "flashback_character"
#             ]
#         },
#
#         "rika": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "rika", "rika_(one_piece)", "shells_town_girl",
#                 "food_shop_daughter", "zoro's_friend",
#
#                 # Roles and positions
#                 "restaurant_helper", "civilian_child",
#                 "zoro_supporter", "town_resident",
#
#                 # Teams and affiliations
#                 "shells_town", "food_shop_family",
#                 "civilian_population", "zoro's_allies",
#
#                 # Time periods and versions
#                 "morgan_arc", "early_east_blue", "pre_timeskip",
#
#                 # Emotional states
#                 "grateful_rika", "brave_child", "helpful_rika",
#                 "kind_hearted", "caring_child"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "rika", "rika_(one_piece)",
#
#                 # Roles and locations
#                 "shells_town", "civilian",
#
#                 # States
#                 "child_character", "supporter"
#             ]
#         },
#
#         # Gaimon Arc (Island of Rare Animals)
#         "sarfunkel": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "sarfunkel", "sarfunkel_(one_piece)",
#                 "rare_animals_island", "gaimon's_partner",
#
#                 # Roles and positions
#                 "island_guardian", "animal_protector",
#                 "gaimon's_companion", "treasure_hunter",
#
#                 # Teams and affiliations
#                 "rare_animals_island", "island_protectors",
#                 "gaimon's_ally", "treasure_seekers",
#
#                 # Time periods and versions
#                 "post_timeskip", "cover_story_era",
#
#                 # Emotional states
#                 "protective_sarfunkel", "caring_guardian",
#                 "treasure_seeker", "animal_lover"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "sarfunkel", "sarfunkel_(one_piece)",
#
#                 # Roles
#                 "guardian", "protector",
#
#                 # States
#                 "cover_story_character"
#             ]
#         },
#
#         # Apis Arc (Warship Island)
#         "apis": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "apis", "apis_(one_piece)", "warship_island",
#                 "dragon_friend", "millennium_dragon_ally",
#
#                 # Roles and positions
#                 "dragon_protector", "island_resident",
#                 "lost_powers_user", "ryuuji's_friend",
#
#                 # Special abilities
#                 "animal_communication", "dragon_understanding",
#                 "ancient_powers", "lost_civilization_connection",
#
#                 # Teams and affiliations
#                 "warship_island", "straw_hat_allies",
#                 "dragon_protectors", "lost_civilization",
#
#                 # Time periods and versions
#                 "warship_island_arc", "filler_arc",
#                 "pre_timeskip", "childhood_apis",
#
#                 # Outfits and appearances
#                 "traditional_clothes", "island_outfit",
#                 "dragon_keeper_attire", "casual_wear",
#
#                 # Emotional states
#                 "protective_apis", "determined_apis",
#                 "caring_friend", "brave_child"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "apis", "apis_(one_piece)",
#
#                 # Roles and abilities
#                 "dragon_friend", "animal_communicator",
#
#                 # States
#                 "protective_mode", "child_character"
#             ]
#         },
#
#         # Post-Alabasta Arc
#         "adelle_bascùd": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "adelle", "adelle_(one_piece)", "goat_island",
#                 "mayor's_daughter", "island_defender",
#
#                 # Roles and positions
#                 "goat_island_resident", "defender",
#                 "village_protector", "zoro's_temporary_student",
#
#                 # Combat abilities
#                 "basic_swordsmanship", "defensive_skills",
#                 "island_protection", "beginner_fighter",
#
#                 # Teams and affiliations
#                 "goat_island", "island_defenders",
#                 "zoro's_students", "civilian_fighters",
#
#                 # Time periods and versions
#                 "post_alabasta", "filler_arc", "pre_timeskip",
#
#                 # Emotional states
#                 "determined_adelle", "protective_spirit",
#                 "learning_mode", "defensive_stance"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "adelle", "adelle_(one_piece)",
#
#                 # Roles
#                 "swordswoman", "defender",
#
#                 # States
#                 "student_mode", "protective_mode"
#             ]
#         },
#
#         # Ocean's Dream Arc
#         "abi": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "abi", "abi_(one_piece)", "dream_investigator",
#                 "memory_researcher", "sleeping_expert",
#
#                 # Roles and positions
#                 "dream_expert", "memory_specialist",
#                 "sleep_researcher", "arc_antagonist",
#
#                 # Special abilities
#                 "dream_investigation", "memory_analysis",
#                 "sleep_study", "research_skills",
#
#                 # Teams and affiliations
#                 "dream_researchers", "memory_scientists",
#                 "independent_investigator",
#
#                 # Time periods and versions
#                 "ocean's_dream_arc", "filler_arc",
#                 "pre_timeskip",
#
#                 # Emotional states
#                 "analytical_abi", "research_mode",
#                 "investigative_spirit", "determined_researcher"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "abi", "abi_(one_piece)",
#
#                 # Roles
#                 "researcher", "investigator",
#
#                 # States
#                 "analytical_mode", "research_mode"
#             ]
#         },
#
#         "jessica": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "jessica", "jessica_(one_piece)", "g8_base_cook",
#                 "jonathan's_wife", "marine_chef",
#
#                 # Titles and positions
#                 "head_chef", "marine_base_cook", "commander's_wife",
#                 "kitchen_supervisor", "g8_staff",
#
#                 # Special abilities
#                 "cooking_mastery", "kitchen_management",
#                 "food_expertise", "base_administration",
#
#                 # Teams and affiliations
#                 "marine_forces", "g8_base", "kitchen_staff",
#                 "jonathan's_family", "marine_support",
#
#                 # Time periods and versions
#                 "g8_arc", "filler_arc", "pre_timeskip",
#                 "navarone_base_era",
#
#                 # Outfits and appearances
#                 "chef_uniform", "kitchen_attire", "marine_base_clothes",
#                 "cooking_gear", "casual_wear",
#
#                 # Emotional states
#                 "professional_jessica", "caring_wife",
#                 "strict_chef", "base_defender"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "jessica", "jessica_(one_piece)",
#
#                 # Roles
#                 "chef", "marine_staff",
#
#                 # States
#                 "cooking_mode", "commander's_wife"
#             ]
#         },
#
#         # Rainbow Mist Arc
#         "henzo's_grandmother": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "henzo's_grandmother", "ruluka_elder",
#                 "rainbow_mist_resident", "island_elder",
#
#                 # Roles and positions
#                 "village_elder", "family_member",
#                 "ruluka_citizen", "historical_witness",
#
#                 # Teams and affiliations
#                 "ruluka_island", "village_elders",
#                 "henzo's_family", "island_residents",
#
#                 # Time periods and versions
#                 "rainbow_mist_arc", "filler_arc",
#                 "ruluka_flashback", "pre_timeskip"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "henzo's_grandmother", "ruluka_resident",
#
#                 # Roles
#                 "elder", "villager",
#
#                 # Time periods
#                 "flashback_character"
#             ]
#         },
#
#         # Ruluka Island Girl
#         "akibi": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "akibi", "akibi_(one_piece)", "ruluka_child",
#                 "rainbow_mist_victim", "lost_child",
#
#                 # Roles and positions
#                 "missing_child", "ruluka_resident",
#                 "mist_explorer", "ship_passenger",
#
#                 # Teams and affiliations
#                 "ruluka_island", "lost_children",
#                 "rainbow_mist_group", "wetton's_victims",
#
#                 # Time periods and versions
#                 "rainbow_mist_arc", "filler_arc",
#                 "pre_timeskip", "missing_period"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "akibi", "akibi_(one_piece)",
#
#                 # States
#                 "lost_child", "rainbow_mist"
#             ]
#         },
#
#         # Goat Island Arc
#         "yuki": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "yuki", "yuki_(one_piece)", "goat_island_resident",
#                 "zoro's_student", "island_defender",
#
#                 # Roles and positions
#                 "student_swordsman", "island_protector",
#                 "civilian_fighter", "training_participant",
#
#                 # Combat abilities
#                 "basic_swordsmanship", "defensive_skills",
#                 "training_experience", "beginner_fighter",
#
#                 # Teams and affiliations
#                 "goat_island", "zoro's_students",
#                 "island_defenders", "civilian_militia",
#
#                 # Time periods and versions
#                 "goat_island_arc", "filler_arc",
#                 "pre_timeskip", "training_period"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "yuki", "yuki_(one_piece)",
#
#                 # Roles
#                 "student", "defender",
#
#                 # States
#                 "training_mode", "protective_mode"
#             ]
#         },
#
#         # Lovely Land Arc
#         "lily": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "lily", "lily_(one_piece)", "lovely_land_resident",
#                 "spa_island_staff", "filler_character",
#
#                 # Roles and positions
#                 "spa_worker", "island_staff", "service_provider",
#                 "resort_employee", "lovely_land_civilian",
#
#                 # Teams and affiliations
#                 "spa_island", "lovely_land", "resort_staff",
#                 "service_industry", "island_workers",
#
#                 # Time periods and versions
#                 "lovely_land_arc", "filler_arc",
#                 "pre_timeskip", "spa_island_era",
#
#                 # Outfits and appearances
#                 "staff_uniform", "resort_clothes",
#                 "service_attire", "spa_outfit"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "lily", "lily_(one_piece)",
#
#                 # Roles
#                 "spa_worker", "staff_member",
#
#                 # States
#                 "service_mode", "working_state"
#             ]
#         },
#
#         "shirahoshi": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "shirahoshi", "shirahoshi_(one_piece)",
#                 "princess_shirahoshi", "mermaid_princess",
#                 "poseidon", "ancient_weapon",
#
#                 # Titles and positions
#                 "neptune's_daughter", "ryugu_princess",
#                 "ancient_weapon_poseidon", "mermaid_princess",
#                 "fishman_island_royalty",
#
#                 # Special abilities and powers
#                 "sea_kings_control", "poseidon_powers",
#                 "ancient_weapon_abilities", "sea_creature_communication",
#                 "voice_of_all_things",
#
#                 # Physical traits
#                 "giant_mermaid", "pink_hair", "royal_mermaid",
#                 "giant_size", "mermaid_tail", "princess_features",
#
#                 # Teams and affiliations
#                 "ryugu_kingdom", "neptune_family", "royal_family",
#                 "fishman_island", "mermaid_cove",
#
#                 # Family relationships
#                 "neptune's_daughter", "fukaboshi's_sister",
#                 "manboshi's_sister", "ryuboshi's_sister",
#                 "otohime's_daughter",
#
#                 # Time periods and versions
#                 "childhood_shirahoshi", "tower_period",
#                 "current_shirahoshi", "post_timeskip",
#
#                 # Outfits and appearances
#                 "princess_attire", "royal_clothes", "mermaid_outfit",
#                 "formal_dress", "casual_clothes", "tower_wear",
#
#                 # Emotional states
#                 "crying_shirahoshi", "brave_shirahoshi",
#                 "determined_princess", "scared_shirahoshi",
#                 "happy_shirahoshi", "royal_dignity"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "shirahoshi", "shirahoshi_(one_piece)",
#
#                 # Titles and roles
#                 "mermaid_princess", "poseidon",
#
#                 # States and forms
#                 "giant_mermaid", "royal_princess",
#
#                 # Time periods
#                 "fishman_island_arc", "post_timeskip"
#             ]
#         },
#
#         "otohime": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "otohime", "otohime_(one_piece)", "queen_otohime",
#                 "neptune's_wife", "ryugu_queen",
#
#                 # Titles and positions
#                 "ryugu_queen", "neptune's_consort",
#                 "fishman_island_queen", "royal_family",
#                 "peace_advocate",
#
#                 # Special abilities and powers
#                 "observation_haki", "emotional_perception",
#                 "diplomatic_skills", "royal_authority",
#
#                 # Family relationships
#                 "neptune's_wife", "shirahoshi's_mother",
#                 "fukaboshi's_mother", "ryuboshi's_mother",
#                 "manboshi's_mother",
#
#                 # Teams and affiliations
#                 "ryugu_kingdom", "neptune_family",
#                 "royal_family", "fishman_island",
#
#                 # Time periods and versions
#                 "flashback_otohime", "queen_era",
#                 "peace_movement", "pre_death",
#
#                 # Outfits and appearances
#                 "royal_attire", "queen_clothes",
#                 "diplomatic_dress", "formal_wear",
#
#                 # Emotional states
#                 "determined_otohime", "peaceful_queen",
#                 "diplomatic_mode", "motherly_love",
#                 "royal_dignity"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "otohime", "otohime_(one_piece)",
#
#                 # Roles and positions
#                 "queen", "peace_advocate",
#
#                 # States and periods
#                 "flashback_character", "royal_family"
#             ]
#         },
#
#         "madam_shyarly": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "madam_shyarly", "shyarly_(one_piece)",
#                 "mermaid_cafe_owner", "fortune_teller",
#
#                 # Titles and positions
#                 "cafe_owner", "fortune_teller", "seer",
#                 "mermaid_cafe_proprietor", "arlong's_sister",
#
#                 # Special abilities and powers
#                 "future_vision", "prophecy_ability",
#                 "crystal_ball_reading", "prediction_power",
#
#                 # Special characteristics
#                 "shark_mermaid", "business_owner",
#                 "fortune_telling", "prophetic_vision",
#
#                 # Teams and affiliations
#                 "mermaid_cafe", "fishman_island",
#                 "coral_hill", "business_district",
#
#                 # Time periods and versions
#                 "pre_timeskip", "post_timeskip",
#                 "fishman_island_arc", "current_shyarly",
#
#                 # Outfits and appearances
#                 "business_attire", "fortune_teller_clothes",
#                 "cafe_owner_outfit", "formal_wear",
#
#                 # Emotional states
#                 "professional_shyarly", "serious_fortune_teller",
#                 "business_mode", "prophetic_state"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "madam_shyarly", "shyarly_(one_piece)",
#
#                 # Roles and abilities
#                 "fortune_teller", "cafe_owner",
#
#                 # States and forms
#                 "shark_mermaid", "business_owner"
#             ]
#         },
#
#         "ishilly": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "ishilly", "ishilly_(one_piece)",
#                 "mermaid_cafe_worker", "mermaid_cove_resident",
#
#                 # Titles and positions
#                 "cafe_worker", "mermaid_attendant",
#                 "service_staff", "mermaid_cove_member",
#
#                 # Teams and affiliations
#                 "mermaid_cafe", "mermaid_cove",
#                 "fishman_island", "service_industry",
#
#                 # Time periods and versions
#                 "fishman_island_arc", "post_timeskip",
#                 "current_ishilly",
#
#                 # Outfits and appearances
#                 "cafe_uniform", "mermaid_outfit",
#                 "work_clothes", "service_attire",
#
#                 # Emotional states
#                 "cheerful_ishilly", "working_mode",
#                 "service_attitude", "friendly_demeanor"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "ishilly", "ishilly_(one_piece)",
#
#                 # Roles
#                 "mermaid", "cafe_worker",
#
#                 # States
#                 "service_mode", "working_state"
#             ]
#         },
#
#         "lilo": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "lilo", "lilo_(one_piece)", "bounty_hunter",
#                 "accino_family", "ice_hunter",
#
#                 # Roles and positions
#                 "bounty_hunter", "accino_family_member",
#                 "ice_hunter_team", "phoenix_pirates_hunter",
#
#                 # Teams and affiliations
#                 "accino_family", "ice_hunters", "bounty_hunters",
#                 "don_accino's_crew", "hunting_team",
#
#                 # Time periods and versions
#                 "ice_hunter_arc", "filler_arc", "pre_timeskip",
#
#                 # Emotional states
#                 "hunting_mode", "family_member", "professional_hunter"
#             ],
#             "danbooru": [
#                 "lilo", "lilo_(one_piece)", "bounty_hunter",
#                 "ice_hunter", "accino_family"
#             ]
#         },
#
#         # Little East Blue Arc
#         "daisy": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "daisy", "daisy_(one_piece)", "little_east_blue",
#                 "island_resident", "civilian_character",
#
#                 # Roles and positions
#                 "island_civilian", "local_resident",
#                 "east_blue_settler", "community_member",
#
#                 # Teams and affiliations
#                 "little_east_blue", "island_community",
#                 "civilian_population", "east_blue_migrants",
#
#                 # Time periods and versions
#                 "little_east_blue_arc", "filler_arc",
#                 "pre_timeskip", "island_era"
#             ],
#             "danbooru": [
#                 "daisy", "daisy_(one_piece)",
#                 "little_east_blue", "civilian"
#             ]
#         },
#
#         # Z's Ambition Arc
#         "shuzo's_wife": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "shuzo's_wife", "neo_marines_family",
#                 "marine_relative", "filler_character",
#
#                 # Roles and positions
#                 "marine_wife", "neo_marine_family",
#                 "supporting_character", "background_role",
#
#                 # Teams and affiliations
#                 "neo_marines", "marine_families",
#                 "civilian_support", "background_character",
#
#                 # Time periods and versions
#                 "z's_ambition_arc", "filler_arc",
#                 "neo_marine_era", "flashback_character"
#             ],
#             "danbooru": [
#                 "shuzo's_wife", "neo_marines",
#                 "marine_family", "flashback_character"
#             ]
#         },
#
#         "commander_jonathan's_wife": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "jessica", "jessica_(one_piece)", "navarone_chef",
#                 "g8_base_cook", "marine_wife",
#
#                 # Titles and positions
#                 "head_chef", "marine_base_cook", "commander's_wife",
#                 "kitchen_supervisor", "navarone_staff",
#
#                 # Special skills
#                 "culinary_expertise", "kitchen_management",
#                 "base_administration", "cooking_mastery",
#
#                 # Teams and affiliations
#                 "marine_base_g8", "navarone_staff",
#                 "marine_families", "kitchen_personnel",
#
#                 # Time periods and versions
#                 "g8_arc", "navarone_arc", "filler_arc",
#                 "pre_timeskip", "base_era"
#             ],
#             "danbooru": [
#                 "jessica", "jessica_(one_piece)",
#                 "marine_cook", "g8_arc"
#             ]
#         },
#
#         # Spa Island Arc
#         "lina": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "lina", "lina_(one_piece)", "spa_worker",
#                 "furo_island_staff", "service_staff",
#
#                 # Roles and positions
#                 "spa_attendant", "island_staff",
#                 "service_provider", "resort_worker",
#
#                 # Teams and affiliations
#                 "spa_island", "resort_staff",
#                 "service_industry", "furo_kingdom",
#
#                 # Time periods and versions
#                 "spa_island_arc", "filler_arc",
#                 "pre_timeskip", "resort_era",
#
#                 # Outfits and states
#                 "spa_uniform", "service_attire",
#                 "resort_clothes", "work_outfit"
#             ],
#             "danbooru": [
#                 "lina", "lina_(one_piece)",
#                 "spa_worker", "filler_character"
#             ]
#         },
#
#         # Adventure of Nebulandia
#         "komei's_sister": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "komei's_sister", "nebulandia_character",
#                 "marine_family", "filler_character",
#
#                 # Roles and positions
#                 "marine_relative", "supporting_character",
#                 "family_member", "background_character",
#
#                 # Teams and affiliations
#                 "marine_families", "nebulandia_residents",
#                 "komei's_family", "marine_background",
#
#                 # Time periods and versions
#                 "nebulandia_arc", "filler_special",
#                 "special_character", "marine_era"
#             ],
#             "danbooru": [
#                 "komei's_sister", "nebulandia",
#                 "marine_family", "special_character"
#             ]
#         },
#
#         # Silver Mine Arc
#         "myskina_acier": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "myskina_acier", "acier_(one_piece)",
#                 "silver_mine_prisoner", "resistance_member",
#
#                 # Roles and positions
#                 "mine_prisoner", "resistance_fighter",
#                 "escaped_prisoner", "rebel_leader",
#
#                 # Special characteristics
#                 "resistance_skills", "leadership_ability",
#                 "survival_expertise", "combat_experience",
#
#                 # Teams and affiliations
#                 "silver_mine_resistance", "escaped_prisoners",
#                 "rebel_faction", "prison_breakers",
#
#                 # Time periods and versions
#                 "silver_mine_arc", "filler_arc",
#                 "prison_era", "resistance_period",
#
#                 # Emotional states
#                 "determined_fighter", "rebellious_spirit",
#                 "resistance_leader", "freedom_seeker"
#             ],
#             "danbooru": [
#                 "myskina_acier", "silver_mine",
#                 "resistance_fighter", "prisoner"
#             ]
#         },
#
#         "carmel": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "carmel", "carmel_(one_piece)", "marine_rookie",
#                 "training_graduate", "new_marine",
#
#                 # Titles and positions
#                 "marine_graduate", "rookie_officer",
#                 "training_corp", "new_recruit",
#
#                 # Combat abilities
#                 "basic_training", "marine_combat",
#                 "rookie_skills", "military_training",
#
#                 # Teams and affiliations
#                 "marine_forces", "rookie_squad",
#                 "training_division", "new_recruits",
#
#                 # Time periods and versions
#                 "marine_rookie_arc", "filler_arc",
#                 "training_period", "graduation_era",
#
#                 # Outfits and appearances
#                 "marine_uniform", "training_gear",
#                 "rookie_outfit", "graduation_attire",
#
#                 # Emotional states
#                 "determined_rookie", "training_mode",
#                 "ambitious_marine", "learning_state"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "carmel", "carmel_(one_piece)",
#
#                 # Roles
#                 "marine_rookie", "trainee",
#
#                 # States
#                 "training_mode", "rookie_state"
#             ]
#         },
#
#         # Cidre Guild Arc
#         "ishigo_shitemanna": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "ishigo", "ishigo_(one_piece)",
#                 "cidre_guild_member", "female_pirate",
#
#                 # Titles and positions
#                 "guild_member", "pirate_brewer",
#                 "drink_specialist", "cidre_maker",
#
#                 # Special abilities
#                 "brewing_skills", "guild_techniques",
#                 "drink_creation", "combat_brewing",
#
#                 # Teams and affiliations
#                 "cidre_guild", "brewing_pirates",
#                 "drink_makers", "guild_forces",
#
#                 # Time periods and versions
#                 "cidre_guild_arc", "filler_arc",
#                 "guild_era", "brewing_period",
#
#                 # Outfits and appearances
#                 "guild_uniform", "brewer_outfit",
#                 "pirate_clothes", "work_gear",
#
#                 # Emotional states
#                 "professional_brewer", "guild_loyalty",
#                 "brewing_focus", "pirate_spirit"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "ishigo", "ishigo_(one_piece)",
#
#                 # Roles
#                 "cidre_guild", "brewer",
#
#                 # States
#                 "brewing_mode", "guild_member"
#             ]
#         },
#
#         # Marine Rookie Arc Additional
#         "bonham": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "bonham", "bonham_(one_piece)",
#                 "marine_instructor", "training_officer",
#
#                 # Titles and positions
#                 "marine_teacher", "training_supervisor",
#                 "drill_instructor", "veteran_marine",
#
#                 # Combat abilities
#                 "instructor_skills", "combat_training",
#                 "marine_techniques", "teaching_expertise",
#
#                 # Teams and affiliations
#                 "marine_forces", "training_division",
#                 "instructor_corps", "education_unit",
#
#                 # Time periods and versions
#                 "marine_rookie_arc", "filler_arc",
#                 "training_era", "instructor_period",
#
#                 # Outfits and appearances
#                 "marine_uniform", "instructor_attire",
#                 "training_gear", "official_dress",
#
#                 # Emotional states
#                 "strict_instructor", "teaching_mode",
#                 "professional_manner", "training_focus"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "bonham", "bonham_(one_piece)",
#
#                 # Roles
#                 "marine_instructor", "trainer",
#
#                 # States
#                 "teaching_mode", "instructor_state"
#             ]
#         },
#
#         # Cidre Guild Additional
#         "udetsuki": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "udetsuki", "udetsuki_(one_piece)",
#                 "cidre_guild_executive", "female_pirate",
#
#                 # Titles and positions
#                 "guild_executive", "senior_brewer",
#                 "pirate_officer", "drink_master",
#
#                 # Special abilities
#                 "advanced_brewing", "guild_mastery",
#                 "drink_expertise", "combat_brewing",
#
#                 # Teams and affiliations
#                 "cidre_guild", "brewing_pirates",
#                 "guild_leadership", "executive_team",
#
#                 # Time periods and versions
#                 "cidre_guild_arc", "filler_arc",
#                 "guild_era", "executive_period",
#
#                 # Outfits and appearances
#                 "executive_uniform", "guild_clothes",
#                 "pirate_attire", "brewer_gear",
#
#                 # Emotional states
#                 "leader_mode", "guild_pride",
#                 "executive_manner", "brewing_focus"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "udetsuki", "udetsuki_(one_piece)",
#
#                 # Roles
#                 "cidre_executive", "guild_leader",
#
#                 # States
#                 "executive_mode", "leadership_state"
#             ]
#         },
#
#         "sengoku's_secretary": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "sengoku's_secretary", "marine_hq_secretary",
#                 "fleet_admiral_staff", "headquarters_personnel",
#
#                 # Titles and positions
#                 "marine_secretary", "administrative_staff",
#                 "fleet_admiral_assistant", "hq_staff",
#
#                 # Roles and duties
#                 "battlefield_reporter", "war_correspondent",
#                 "marine_administrator", "communication_officer",
#
#                 # Teams and affiliations
#                 "marine_headquarters", "administrative_division",
#                 "fleet_admiral_office", "marine_staff",
#
#                 # Time periods and versions
#                 "marineford_war", "war_arc", "marine_era",
#                 "pre_timeskip", "headquarters_period",
#
#                 # Outfits and appearances
#                 "marine_uniform", "office_attire",
#                 "staff_clothes", "formal_wear",
#
#                 # Emotional states
#                 "professional_demeanor", "duty_bound",
#                 "official_manner", "wartime_focus"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "sengoku's_secretary", "marine_staff",
#
#                 # Roles
#                 "secretary", "administrator",
#
#                 # States
#                 "marineford_war", "official_duty"
#             ]
#         },
#
#         "domino": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "domino", "domino_(one_piece)",
#                 "impel_down_guard", "prison_staff",
#
#                 # Titles and positions
#                 "chief_guard", "prison_officer",
#                 "security_chief", "impel_down_staff",
#
#                 # Special abilities
#                 "prison_combat", "security_expertise",
#                 "guard_skills", "defensive_tactics",
#
#                 # Teams and affiliations
#                 "impel_down", "prison_guards",
#                 "world_government", "security_force",
#
#                 # Time periods and versions
#                 "impel_down_arc", "marineford_war",
#                 "pre_timeskip", "prison_era",
#
#                 # Outfits and appearances
#                 "guard_uniform", "security_outfit",
#                 "prison_attire", "official_uniform",
#
#                 # Emotional states
#                 "professional_guard", "dutiful_officer",
#                 "stern_demeanor", "security_focused"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "domino", "domino_(one_piece)",
#
#                 # Roles
#                 "chief_guard", "prison_officer",
#
#                 # States
#                 "guard_duty", "security_mode"
#             ]
#         },
#
#         "tsuru": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "tsuru", "tsuru_(one_piece)", "great_staff_officer",
#                 "marine_vice_admiral", "legendary_marine",
#
#                 # Titles and positions
#                 "vice_admiral", "great_staff_officer",
#                 "marine_legend", "strategic_commander",
#
#                 # Special abilities and powers
#                 "wash_wash_fruit", "woshu_woshu_no_mi",
#                 "marine_haki", "strategic_genius",
#                 "veteran_combat", "cleansing_power",
#
#                 # Combat specialties
#                 "devil_fruit_master", "tactical_expert",
#                 "marine_combat", "strategic_warfare",
#
#                 # Teams and affiliations
#                 "marine_headquarters", "vice_admirals",
#                 "marine_leadership", "strategy_division",
#
#                 # Time periods and versions
#                 "marineford_war", "roger_era", "pre_timeskip",
#                 "marine_veteran", "war_commander",
#
#                 # Outfits and appearances
#                 "marine_uniform", "vice_admiral_coat",
#                 "battle_attire", "formal_uniform",
#
#                 # Emotional states
#                 "strategic_mind", "veteran_composure",
#                 "commanding_presence", "battle_focus"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "tsuru", "tsuru_(one_piece)",
#
#                 # Roles and powers
#                 "vice_admiral", "wash_wash_fruit",
#
#                 # States and periods
#                 "marineford_war", "veteran_marine"
#             ]
#         },
#
#         "kairen": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "kairen", "kairen_(one_piece)",
#                 "marine_officer", "giant_squad",
#
#                 # Titles and positions
#                 "marine_giant", "giant_officer",
#                 "marine_warrior", "giant_division",
#
#                 # Combat abilities
#                 "giant_strength", "marine_combat",
#                 "size_advantage", "warrior_skills",
#
#                 # Teams and affiliations
#                 "marine_forces", "giant_squad",
#                 "marine_warriors", "headquarters_forces",
#
#                 # Time periods and versions
#                 "marineford_war", "war_arc",
#                 "pre_timeskip", "battle_era",
#
#                 # Outfits and appearances
#                 "marine_uniform", "giant_armor",
#                 "battle_gear", "warrior_attire",
#
#                 # Emotional states
#                 "battle_ready", "warrior_spirit",
#                 "marine_pride", "combat_focus"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "kairen", "kairen_(one_piece)",
#
#                 # Roles
#                 "marine_giant", "warrior",
#
#                 # States
#                 "battle_mode", "war_participant"
#             ]
#         },
#
#         "sadi": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "sadi", "sadi_(one_piece)", "chief_guard",
#                 "impel_down_officer", "torture_specialist",
#
#                 # Titles and positions
#                 "chief_guard", "torture_specialist",
#                 "prison_officer", "punishment_supervisor",
#                 "security_chief",
#
#                 # Special abilities and powers
#                 "whip_mastery", "torture_techniques",
#                 "combat_skills", "interrogation_expertise",
#                 "security_mastery",
#
#                 # Combat specialties
#                 "whip_techniques", "sadistic_combat",
#                 "guard_combat", "restraining_skills",
#                 "punishment_methods",
#
#                 # Teams and affiliations
#                 "impel_down", "prison_staff", "jailer_beasts",
#                 "world_government", "security_forces",
#
#                 # Time periods and versions
#                 "impel_down_arc", "prison_break",
#                 "pre_timeskip", "prison_era",
#
#                 # Outfits and appearances
#                 "guard_uniform", "chief_outfit",
#                 "prison_attire", "combat_gear",
#                 "security_uniform",
#
#                 # Emotional states
#                 "sadistic_mood", "professional_guard",
#                 "commanding_presence", "battle_ready",
#                 "torture_enthusiasm"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "sadi", "sadi_(one_piece)",
#
#                 # Roles and positions
#                 "chief_guard", "torture_specialist",
#
#                 # States and actions
#                 "guard_duty", "combat_mode"
#             ]
#         },
#
#         "sadie-chan": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "sadie-chan", "sadie_(one_piece)",
#                 "impel_down_guard", "torture_assistant",
#
#                 # Titles and positions
#                 "assistant_guard", "torture_staff",
#                 "prison_guard", "security_officer",
#
#                 # Combat abilities
#                 "guard_combat", "restraining_skills",
#                 "prison_techniques", "security_expertise",
#
#                 # Teams and affiliations
#                 "impel_down", "prison_guards",
#                 "torture_division", "security_staff",
#
#                 # Time periods and versions
#                 "impel_down_arc", "prison_break",
#                 "pre_timeskip", "guard_era",
#
#                 # Outfits and appearances
#                 "guard_uniform", "prison_gear",
#                 "security_outfit", "staff_attire",
#
#                 # Emotional states
#                 "dutiful_guard", "professional_manner",
#                 "security_focused", "vigilant_guard"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "sadie-chan", "sadie_(one_piece)",
#
#                 # Roles
#                 "prison_guard", "security_staff",
#
#                 # States
#                 "guard_duty", "security_mode"
#             ]
#         },
#
#         "saldeath": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "saldeath", "saldeath_(one_piece)",
#                 "blugori_commander", "impel_down_officer",
#
#                 # Titles and positions
#                 "blugori_leader", "prison_officer",
#                 "beast_commander", "security_supervisor",
#
#                 # Special abilities
#                 "beast_control", "command_skills",
#                 "prison_combat", "guard_expertise",
#
#                 # Teams and affiliations
#                 "impel_down", "blugori_unit",
#                 "prison_forces", "security_division",
#
#                 # Time periods and versions
#                 "impel_down_arc", "prison_break",
#                 "pre_timeskip", "command_era",
#
#                 # Outfits and appearances
#                 "commander_uniform", "prison_attire",
#                 "officer_gear", "guard_clothes",
#
#                 # Emotional states
#                 "commanding_presence", "professional_demeanor",
#                 "battle_ready", "leadership_mode"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "saldeath", "saldeath_(one_piece)",
#
#                 # Roles
#                 "blugori_commander", "prison_officer",
#
#                 # States
#                 "command_mode", "guard_duty"
#             ]
#         },
#
#         "charlotte_galette": {
#             "gelbooru": ["charlotte_galette", "galette"],
#             "danbooru": ["charlotte_galette"]
#         },
#         "charlotte_brulee": {
#             "gelbooru": ["charlotte_brulee", "brulee"],
#             "danbooru": ["charlotte_brulee"]
#         },
#
#         # Vegapunk satellites
#         "vegapunk_lilith": {
#             "gelbooru": ["vegapunk_lilith", "satellite_evil"],
#             "danbooru": ["vegapunk_lilith", "evil_satellite"]
#         },
#         "vegapunk_atlas": {
#             "gelbooru": ["vegapunk_atlas", "satellite_combat"],
#             "danbooru": ["vegapunk_atlas", "combat_satellite"]
#         },
#         "vegapunk_york": {
#             "gelbooru": ["vegapunk_york", "satellite_analysis"],
#             "danbooru": ["vegapunk_york", "analysis_satellite"]
#         },
#         "vegapunk_edison": {
#             "gelbooru": ["vegapunk_edison", "satellite_logic"],
#             "danbooru": ["vegapunk_edison", "logic_satellite"]
#         },
#
#         # New/Additional characters
#         "whitey_bay": {
#             "gelbooru": ["whitey_bay", "ice_witch"],
#             "danbooru": ["whitey_bay", "ice_witch_(one_piece)"]
#         },
#
#         "shakky": {
#             "gelbooru": ["shakky", "shakuyaku"],
#             "danbooru": ["shakuyaku"]
#         },
#
#         # New character tags
#         "ann": {
#             "gelbooru": ["ann_(one_piece)", "ann"],
#             "danbooru": ["ann_(one_piece)"]
#         },
#
#         "aphelandra": {
#             "gelbooru": ["aphelandra_(one_piece)", "kuja_warrior"],
#             "danbooru": ["aphelandra"]
#         },
#
#
#         "baccarat": {
#             "gelbooru": ["baccarat_(one_piece)", "lucky_lucky_fruit"],
#             "danbooru": ["baccarat"]
#         },
#
#         "carina": {
#             "gelbooru": ["carina_(one_piece)", "ghost_lady"],
#             "danbooru": ["carina"]
#         },
#
#         "ein": {
#             "gelbooru": ["ein_(one_piece)", "neo_marine"],
#             "danbooru": ["ein"]
#         },
#
#         "honey_queen": {
#             "gelbooru": ["honey_queen", "baroque_works"],
#             "danbooru": ["honey_queen"]
#         },
#
#         "laki": {
#             "gelbooru": ["laki_(one_piece)", "shandian"],
#             "danbooru": ["laki"]
#         },
#
#         "lily_enstomach": {
#             "gelbooru": ["lily_enstomach", "lily_the_glutton"],
#             "danbooru": ["lily_enstomach"]
#         },
#
#         "mero": {
#             "gelbooru": ["mero_(one_piece)", "kuja"],
#             "danbooru": ["mero"]
#         },
#
#         "miss_valentine": {
#             "gelbooru": ["miss_valentine", "kilo_kilo_fruit"],
#             "danbooru": ["miss_valentine"]
#         },
#
#         "moda": {
#             "gelbooru": ["moda_(one_piece)", "thriller_bark"],
#             "danbooru": ["moda"]
#         },
#
#         "mousse": {
#             "gelbooru": ["mousse_(one_piece)", "kuja"],
#             "danbooru": ["mousse"]
#         },
#
#         "nico_olvia": {
#             "gelbooru": ["nico_olvia", "ohara_scholar"],
#             "danbooru": ["nico_olvia"]
#         },
#
#         "nojiko": {
#             "gelbooru": ["nojiko", "belle-mere_daughter"],
#             "danbooru": ["nojiko"]
#         },
#
#         "ro": {
#             "gelbooru": ["ro_(one_piece)", "kuja"],
#             "danbooru": ["ro"]
#         },
#
#         "stella": {
#             "gelbooru": ["stella_(one_piece)", "water_7"],
#             "danbooru": ["stella"]
#         },
#
#         "tama": {
#             "gelbooru": ["tama_(one_piece)", "wano_kunoichi"],
#             "danbooru": ["tama"]
#         },
#
#         "victoria_cindry": {
#             "gelbooru": ["victoria_cindry", "cindry", "thriller_bark"],
#             "danbooru": ["victoria_cindry"]
#         },
#
#         "wanda": {
#             "gelbooru": ["wanda_(one_piece)", "mink_tribe"],
#             "danbooru": ["wanda"]
#         },
#
#         "uta": {
#             "gelbooru": ["uta_(one_piece)", "world_diva", "shanks_daughter"],
#             "danbooru": ["uta", "world_diva"]
#         },
#     },
#
#     DOTA2_TAGS = {
#         # Core Heroes
#         "lina": {
#             "names": ["lina", "lina_inverse", "slayer", "fire_sorceress"],
#             "titles": ["slayer", "fire_mage", "dragon_slave_wielder", "pyromancer"],
#             "forms": ["base_form", "arcana_form", "battle_mode", "flame_state"],
#             "abilities": ["dragon_slave", "light_strike_array", "fiery_soul", "laguna_blade"],
#             "relationships": ["crystal_maiden's_rival", "fire_elementalist"],
#             "outfits": ["battle_sorceress", "flame_witch_attire", "arcana_form"]
#         },
#         "crystal_maiden": {
#             "names": ["rylai", "crystal_maiden", "frost_sorceress", "ice_maiden"],
#             "titles": ["frost_mage", "ice_sorceress", "crystal_mistress"],
#             "forms": ["base_form", "arcana_form", "frost_state"],
#             "abilities": ["crystal_nova", "frostbite", "arcane_aura", "freezing_field"],
#             "relationships": ["lina's_sister", "frost_elementalist"],
#             "outfits": ["frost_robes", "ice_queen_attire", "arcana_form"]
#         },
#         "windranger": {
#             "names": ["lyralei", "windranger", "windrunner", "ginger_archer"],
#             "titles": ["ranger", "wind_archer", "powershot_master"],
#             "forms": ["base_form", "arcana_form", "focus_fire_mode"],
#             "abilities": ["shackleshot", "powershot", "windrun", "focus_fire"],
#             "relationships": ["drow_ranger's_rival", "nature's_protector"],
#             "outfits": ["ranger_garb", "wind_attire", "arcana_form"]
#         },
#         "drow_ranger": {
#             "names": ["traxex", "drow_ranger", "frost_archer"],
#             "titles": ["ranger", "frost_marksman", "silent_hunter"],
#             "forms": ["base_form", "marksmanship_mode", "frost_state"],
#             "abilities": ["frost_arrows", "gust", "marksmanship", "multishot"],
#             "relationships": ["windranger's_rival", "frost_hunter"],
#             "outfits": ["ranger_armor", "frost_attire", "basic_garb"]
#         },
#         "templar_assassin": {
#             "names": ["lanaya", "templar_assassin", "psi_blade_master"],
#             "titles": ["assassin", "hidden_one", "psi_master"],
#             "forms": ["base_form", "meld_form", "psionic_state"],
#             "abilities": ["psi_blades", "meld", "psi_traps", "refraction"],
#             "relationships": ["hidden_temple_member", "secret_keeper"],
#             "outfits": ["temple_garb", "assassin_attire", "psionic_armor"]
#         },
#         "dark_willow": {
#             "names": ["mireska", "dark_willow", "bramble_maiden"],
#             "titles": ["fae_witch", "thorned_enchantress", "shadow_realm_dweller"],
#             "forms": ["base_form", "shadow_realm_form", "cursed_crown_state"],
#             "abilities": ["bramble_maze", "shadow_realm", "cursed_crown", "terrorize"],
#             "relationships": ["fae_realm_exile", "thorned_witch"],
#             "outfits": ["fae_garments", "thorned_attire", "shadow_wear"]
#         },
#         "death_prophet": {
#             "names": ["krobelus", "death_prophet", "ghost_summoner"],
#             "titles": ["prophet", "spirit_caller", "exorcist"],
#             "forms": ["base_form", "exorcism_form", "spirit_form"],
#             "abilities": ["crypt_swarm", "silence", "spirit_siphon", "exorcism"],
#             "relationships": ["spirit_realm_walker", "death_seer"],
#             "outfits": ["prophet_robes", "spirit_caller_attire", "ghost_form"]
#         },
#         "queen_of_pain": {
#             "names": ["akasha", "queen_of_pain", "pain_mistress"],
#             "titles": ["succubus", "pain_bringer", "demon_queen"],
#             "forms": ["base_form", "arcana_form", "demon_state"],
#             "abilities": ["shadow_strike", "blink", "scream_of_pain", "sonic_wave"],
#             "relationships": ["demon_realm_ruler", "pain_dealer"],
#             "outfits": ["demon_attire", "succubus_form", "arcana_garb"]
#         },
#         "enchantress": {
#             "names": ["aiushtha", "enchantress", "nature's_attendant"],
#             "titles": ["sprite", "forest_guardian", "enchanted_one"],
#             "forms": ["base_form", "nature_form", "sproink_state"],
#             "abilities": ["untouchable", "enchant", "nature's_attendants", "impetus"],
#             "relationships": ["nature's_friend", "forest_protector"],
#             "outfits": ["forest_garb", "nature_attire", "sprite_form"]
#         },
#         "winter_wyvern": {
#             "names": ["auroth", "winter_wyvern", "frost_dragon"],
#             "titles": ["wyvern", "frost_keeper", "arctic_scholar"],
#             "forms": ["base_form", "winter_form", "arctic_flight"],
#             "abilities": ["arctic_burn", "splinter_blast", "cold_embrace", "winter's_curse"],
#             "relationships": ["ice_realm_guardian", "frost_keeper"],
#             "outfits": ["wyvern_scales", "frost_armor", "arctic_form"]
#         },
#         "legion_commander": {
#             "names": ["tresdin", "legion_commander", "duel_master"],
#             "titles": ["commander", "legion_leader", "duel_seeker"],
#             "forms": ["base_form", "duel_mode", "commander_state"],
#             "abilities": ["overwhelming_odds", "press_the_attack", "moment_of_courage", "duel"],
#             "relationships": ["bronze_legion_leader", "duel_master"],
#             "outfits": ["commander_armor", "legion_attire", "battle_gear"]
#         },
#         "marci": {
#             "names": ["marci", "mirana's_companion", "silent_guardian"],
#             "titles": ["bodyguard", "loyal_companion", "silent_warrior"],
#             "forms": ["base_form", "unleash_form", "warrior_state"],
#             "abilities": ["dispose", "rebound", "sidekick", "unleash"],
#             "relationships": ["mirana's_friend", "davion's_ally"],
#             "outfits": ["bodyguard_attire", "warrior_gear", "casual_wear"]
#         },
#
#         "dawnbreaker": {
#             "names": ["valora", "dawnbreaker", "solar_guardian"],
#             "titles": ["celestial_warrior", "star_forger", "light_bringer"],
#             "forms": ["base_form", "celestial_form", "starbreak_mode"],
#             "abilities": ["starbreaker", "celestial_hammer", "luminosity", "solar_guardian"],
#             "relationships": ["celestial_guardian", "star_warrior"],
#             "outfits": ["celestial_armor", "star_forged_attire", "light_wear"]
#         },
#         "luna": {
#             "names": ["luna", "moon_rider", "night_stalker"],
#             "titles": ["moon_warrior", "nova_tamer", "nightsilver_hunter"],
#             "forms": ["base_form", "lunar_form", "eclipse_mode"],
#             "abilities": ["lucent_beam", "moon_glaive", "lunar_blessing", "eclipse"],
#             "relationships": ["nova's_master", "nightsilver_warrior"],
#             "outfits": ["lunar_armor", "moon_rider_gear", "nova_rider_attire"]
#         },
#         "mirana": {
#             "names": ["mirana", "priestess_of_the_moon", "moon_princess"],
#             "titles": ["princess", "moon_priestess", "sacred_arrow_master"],
#             "forms": ["base_form", "starfall_mode", "lunar_blessing"],
#             "abilities": ["starstorm", "sacred_arrow", "leap", "moonlight_shadow"],
#             "relationships": ["selemene's_champion", "marci's_companion"],
#             "outfits": ["priestess_garb", "moon_armor", "royal_attire"]
#         },
#         "naga_siren": {
#             "names": ["slithice", "naga_siren", "tide_caller"],
#             "titles": ["siren", "ocean_singer", "tide_commander"],
#             "forms": ["base_form", "song_form", "mirror_mode"],
#             "abilities": ["mirror_image", "ensnare", "rip_tide", "song_of_the_siren"],
#             "relationships": ["deep_ones_leader", "ocean_warrior"],
#             "outfits": ["siren_scales", "ocean_armor", "deep_one_garb"]
#         },
#         "phantom_assassin": {
#             "names": ["mortred", "phantom_assassin", "veiled_sister"],
#             "titles": ["assassin", "coup_master", "blur_walker"],
#             "forms": ["base_form", "arcana_form", "blur_state"],
#             "abilities": ["stifling_dagger", "phantom_strike", "blur", "coup_de_grace"],
#             "relationships": ["veiled_sisters_member", "oracle's_prophecy"],
#             "outfits": ["assassin_gear", "veiled_attire", "arcana_form"]
#         },
#         "spectre": {
#             "names": ["mercurial", "spectre", "phantom_shade"],
#             "titles": ["spectral_assassin", "haunt_walker", "shade_stalker"],
#             "forms": ["base_form", "arcana_form", "haunt_mode"],
#             "abilities": ["spectral_dagger", "desolate", "dispersion", "haunt"],
#             "relationships": ["phantom_realm_walker", "void_hunter"],
#             "outfits": ["spectral_form", "void_armor", "arcana_attire"]
#         },
#         "vengeful_spirit": {
#             "names": ["shendelzare", "vengeful_spirit", "skywrath_princess"],
#             "titles": ["fallen_princess", "netherswap_master", "avenger"],
#             "forms": ["base_form", "fallen_form", "vengeance_mode"],
#             "abilities": ["magic_missile", "wave_of_terror", "vengeance_aura", "nether_swap"],
#             "relationships": ["skywrath_mage's_love", "fallen_royal"],
#             "outfits": ["fallen_armor", "spirit_form", "royal_remnants"]
#         },
#         "broodmother": {
#             "names": ["black_arachnia", "broodmother", "web_weaver"],
#             "titles": ["spider_queen", "web_master", "spawn_mother"],
#             "forms": ["base_form", "web_form", "insatiable_hunger"],
#             "abilities": ["spawn_spiderlings", "spin_web", "incapacitating_bite", "insatiable_hunger"],
#             "relationships": ["spiderling_mother", "web_master"],
#             "outfits": ["spider_carapace", "web_weaver_form", "arachnid_armor"]
#         },
#         "medusa": {
#             "names": ["medusa", "gorgon", "stone_gaze"],
#             "titles": ["gorgon", "stone_queen", "serpent_bearer"],
#             "forms": ["base_form", "stone_form", "mana_shield"],
#             "abilities": ["split_shot", "mystic_snake", "mana_shield", "stone_gaze"],
#             "relationships": ["gorgon_sister", "stone_wielder"],
#             "outfits": ["gorgon_scales", "serpent_armor", "stone_crown"]
#         },
#         "snapfire": {
#             "names": ["beatrix", "snapfire", "cookie_baker"],
#             "titles": ["gun_granny", "cookie_master", "dragon_tamer"],
#             "forms": ["base_form", "mortimer_ride", "cookie_mode"],
#             "abilities": ["scatterblast", "firesnap_cookie", "lil_shredder", "mortimer_kisses"],
#             "relationships": ["mortimer's_rider", "keen_inventor"],
#             "outfits": ["granny_gear", "dragon_rider_attire", "keen_wear"]
#         },
#         "hoodwink": {
#             "names": ["hoodwink", "forest_trickster", "acorn_archer"],
#             "titles": ["sharpshooter", "forest_ranger", "acorn_master"],
#             "forms": ["base_form", "bushwhack_mode", "sharpshooter_stance"],
#             "abilities": ["acorn_shot", "bushwhack", "scurry", "sharpshooter"],
#             "relationships": ["forest_dweller", "nature_trickster"],
#             "outfits": ["ranger_fur", "forest_gear", "acorn_armor"]
#         },
#
#         # "lina": {
#         #     "gelbooru": ["lina", "lina_(dota)", "slayer"],
#         #     "danbooru": ["lina_(dota)", "the_slayer"]
#         # },
#         # "crystal_maiden": {
#         #     "gelbooru": ["crystal_maiden", "rylai", "cm"],
#         #     "danbooru": ["crystal_maiden", "rylai"]
#         # },
#         # "windrunner": {
#         #     "gelbooru": ["windranger", "windrunner", "lyralei"],
#         #     "danbooru": ["windranger", "lyralei"]
#         # },
#         # "drow_ranger": {
#         #     "gelbooru": ["drow_ranger", "traxex"],
#         #     "danbooru": ["drow_ranger", "traxex"]
#         # },
#         # "templar_assassin": {
#         #     "gelbooru": ["templar_assassin", "lanaya"],
#         #     "danbooru": ["templar_assassin", "lanaya"]
#         # },
#         #
#         # # Intelligence Heroes
#         # "dark_willow": {
#         #     "gelbooru": ["dark_willow", "mireska"],
#         #     "danbooru": ["dark_willow", "mireska_sunbreeze"]
#         # },
#         # "death_prophet": {
#         #     "gelbooru": ["death_prophet", "krobelus"],
#         #     "danbooru": ["death_prophet", "krobelus"]
#         # },
#         # "queen_of_pain": {
#         #     "gelbooru": ["queen_of_pain", "akasha"],
#         #     "danbooru": ["queen_of_pain", "akasha"]
#         # },
#         # "enchantress": {
#         #     "gelbooru": ["enchantress", "aiushtha"],
#         #     "danbooru": ["enchantress", "aiushtha"]
#         # },
#         # "winter_wyvern": {
#         #     "gelbooru": ["winter_wyvern", "auroth"],
#         #     "danbooru": ["winter_wyvern", "auroth"]
#         # },
#         #
#         # # Strength Heroes
#         # "legion_commander": {
#         #     "gelbooru": ["legion_commander", "tresdin"],
#         #     "danbooru": ["legion_commander", "tresdin"]
#         # },
#         # "marci": {
#         #     "gelbooru": ["marci", "marci_(dota)"],
#         #     "danbooru": ["marci", "marci_(dota)"]
#         # },
#         # "dawnbreaker": {
#         #     "gelbooru": ["dawnbreaker", "valora"],
#         #     "danbooru": ["dawnbreaker", "valora"]
#         # },
#         #
#         # # Agility Heroes
#         # "luna": {
#         #     "gelbooru": ["luna_(dota)", "moon_rider"],
#         #     "danbooru": ["luna_(dota)", "moon_rider"]
#         # },
#         # "mirana": {
#         #     "gelbooru": ["mirana", "princess_of_the_moon"],
#         #     "danbooru": ["mirana", "princess_of_the_moon"]
#         # },
#         # "naga_siren": {
#         #     "gelbooru": ["naga_siren", "slithice"],
#         #     "danbooru": ["naga_siren", "slithice"]
#         # },
#         # "phantom_assassin": {
#         #     "gelbooru": ["phantom_assassin", "mortred"],
#         #     "danbooru": ["phantom_assassin", "mortred"]
#         # },
#         # "spectre": {
#         #     "gelbooru": ["spectre", "mercurial"],
#         #     "danbooru": ["spectre", "mercurial"]
#         # },
#         # "vengeful_spirit": {
#         #     "gelbooru": ["vengeful_spirit", "shendelzare"],
#         #     "danbooru": ["vengeful_spirit", "shendelzare"]
#         # },
#         #
#         # # Additional Heroes
#         # "broodmother": {
#         #     "gelbooru": ["broodmother", "black_arachnia"],
#         #     "danbooru": ["broodmother", "black_arachnia"]
#         # },
#         # "medusa": {
#         #     "gelbooru": ["medusa_(dota)", "gorgon"],
#         #     "danbooru": ["medusa_(dota)", "gorgon"]
#         # },
#         # "snapfire": {
#         #     "gelbooru": ["snapfire", "beatrix"],
#         #     "danbooru": ["snapfire", "beatrix"]
#         # },
#         # "hoodwink": {
#         #     "gelbooru": ["hoodwink", "hoodwink_(dota)"],
#         #     "danbooru": ["hoodwink", "hoodwink_(dota)"]
#         # },
#         #
#         # # Personas
#         # "anti_mage_persona": {
#         #     "gelbooru": ["anti_mage_persona", "wei"],
#         #     "danbooru": ["anti_mage_persona", "wei"]
#         # },
#         # "keeper_of_the_light_persona": {
#         #     "gelbooru": ["keeper_of_the_light_persona", "wraith_of_the_wilds"],
#         #     "danbooru": ["kotl_persona", "wraith_persona"]
#         # },
#         # "oracle_persona": {
#         #     "gelbooru": ["oracle_persona", "fortune's_tout"],
#         #     "danbooru": ["oracle_persona", "fortune_tout"]
#         # }
#     },
#
#     LEAGUE_OF_LEGENDS_TAGS = {
#         # Popular champions with expanded tags
#         "ahri": {
#             "names": [
#                 "ahri", "nine_tailed_fox", "gumiho",
#                 "vastayan_charmer", "fox_mage"
#             ],
#             "titles": [
#                 "nine_tailed_fox", "charm_weaver",
#                 "essence_thief", "vastayan_assassin"
#             ],
#             "forms": [
#                 "base_form", "spirit_rush_form",
#                 "fox_form", "k/da_form",
#                 "star_guardian_form"
#             ],
#             "abilities": [
#                 "orb_of_deception", "fox_fire",
#                 "charm", "spirit_rush",
#                 "essence_theft"
#             ],
#             "affiliations": [
#                 "vastaya", "k/da",
#                 "star_guardians", "runeterra_champions"
#             ],
#             "relationships": [
#                 "vastayan_tribe", "k/da_member",
#                 "star_guardian_team", "spirit_walker"
#             ],
#             "outfits": [
#                 "classic", "k/da",
#                 "star_guardian", "spirit_blossom",
#                 "arcade"
#             ]
#         },
#         "kaisa": {
#             "names": [
#                 "kai'sa", "daughter_of_the_void",
#                 "void_hunter", "icathian_survivor"
#             ],
#             "titles": [
#                 "void_seeker", "void_hunter",
#                 "k/da_dancer", "icathian_rain"
#             ],
#             "forms": [
#                 "base_form", "void_enhanced",
#                 "k/da_form", "bullet_angel"
#             ],
#             "abilities": [
#                 "icathian_rain", "void_seeker",
#                 "supercharge", "killer_instinct"
#             ],
#             "affiliations": [
#                 "void_survivors", "k/da",
#                 "icathian_warriors", "void_hunters"
#             ],
#             "relationships": [
#                 "kassadin's_daughter", "k/da_member",
#                 "void_survivor", "malzahar's_nemesis"
#             ],
#             "outfits": [
#                 "classic", "k/da",
#                 "bullet_angel", "arcade",
#                 "lagoon_dragon"
#             ]
#         },
#         "jinx": {
#             "names": [
#                 "jinx", "loose_cannon",
#                 "powder", "mayhem_maker"
#             ],
#             "titles": [
#                 "loose_cannon", "mayhem_queen",
#                 "star_guardian_leader", "zaunite_menace"
#             ],
#             "forms": [
#                 "base_form", "super_mega_death_rocket",
#                 "star_guardian_form", "arcane_form"
#             ],
#             "abilities": [
#                 "switcheroo", "zap",
#                 "flame_chompers", "super_mega_death_rocket"
#             ],
#             "affiliations": [
#                 "zaun", "star_guardians",
#                 "lane_sisters", "piltover_menace"
#             ],
#             "relationships": [
#                 "vi's_sister", "ekko's_friend",
#                 "caitlyn's_nemesis", "star_guardian_leader"
#             ],
#             "outfits": [
#                 "classic", "star_guardian",
#                 "arcane", "odyssey",
#                 "heartseeker"
#             ]
#         },
#
#         "katarina": {
#             "names": ["katarina_du_couteau", "sinister_blade", "noxian_assassin"],
#             "titles": ["sinister_blade", "noxian_elite", "assassin_prodigy"],
#             "forms": ["base_form", "death_lotus_mode", "battle_queen_form"],
#             "abilities": ["bouncing_blade", "preparation", "shunpo", "death_lotus"],
#             "relationships": ["garen's_rival", "cassiopeia's_sister", "talon's_adoptive_sister"],
#             "outfits": ["classic", "battle_queen", "blood_moon", "death_sworn"]
#         },
#         "leblanc": {
#             "names": ["leblanc", "the_deceiver", "pale_woman", "matron"],
#             "titles": ["the_deceiver", "black_rose_leader", "pale_woman"],
#             "forms": ["base_form", "mimic_form", "coven_form"],
#             "abilities": ["sigil_of_malice", "distortion", "ethereal_chains", "mimic"],
#             "relationships": ["black_rose_leader", "swain's_nemesis", "vladimir's_mentor"],
#             "outfits": ["classic", "coven", "championship", "elderwood"]
#         },
#         "zoe": {
#             "names": ["zoe", "aspect_of_twilight", "twilight_trickster"],
#             "titles": ["aspect_of_twilight", "cosmic_messenger", "trickster"],
#             "forms": ["base_form", "portal_jump_form", "cyber_pop_form"],
#             "abilities": ["paddle_star", "spell_thief", "sleepy_trouble_bubble", "portal_jump"],
#             "relationships": ["aurelion_sol's_sealer", "aspect_host", "myisha's_successor"],
#             "outfits": ["classic", "cyber_pop", "arcanist", "star_guardian"]
#         },
#         "bel_veth": {
#             "names": ["bel'veth", "empress_of_the_void", "void_empress"],
#             "titles": ["empress_of_the_void", "lavender_sea", "city_devourer"],
#             "forms": ["base_form", "true_form", "battle_boss_form"],
#             "abilities": ["void_surge", "above_and_below", "royal_maelstrom", "endless_banquet"],
#             "relationships": ["void_ruler", "kai'sa's_enemy", "malzahar's_superior"],
#             "outfits": ["classic", "battle_boss"]
#         },
#         "nilah": {
#             "names": ["nilah", "joy_unbound", "water_dancer"],
#             "titles": ["the_unbound_joy", "water_ascetic", "asem_warrior"],
#             "forms": ["base_form", "jubilant_veil_form", "star_guardian_form"],
#             "abilities": ["formless_blade", "jubilant_veil", "mounting_dispair", "apotheosis"],
#             "relationships": ["asem_warrior", "star_guardian_member", "joy_demon_host"],
#             "outfits": ["classic", "star_guardian"]
#         },
#         "renata": {
#             "names": ["renata_glasc", "chem_baroness", "zaun_matron"],
#             "titles": ["chem_baroness", "glasc_industries_ceo", "zaun_leader"],
#             "forms": ["base_form", "admiral_form", "hostile_takeover_mode"],
#             "abilities": ["handshake", "bailout", "loyalty_program", "hostile_takeover"],
#             "relationships": ["zaun_leader", "chemtech_pioneer", "silco's_rival"],
#             "outfits": ["classic", "admiral"]
#         },
#         "gwen": {
#             "names": ["gwen", "hallowed_seamstress", "doll_champion"],
#             "titles": ["the_hallowed_seamstress", "blessed_doll", "isolde's_creation"],
#             "forms": ["base_form", "hallowed_mist_form", "space_groove_form"],
#             "abilities": ["snip_snip", "hallowed_mist", "skip_n_slash", "needlework"],
#             "relationships": ["isolde's_creation", "viego's_doll", "shadow_isles_defender"],
#             "outfits": ["classic", "space_groove", "cafe_cuties"]
#         },
#         "akali": {
#             "names": ["akali", "rogue_assassin", "kinkou_ninja"],
#             "titles": ["rogue_assassin", "k/da_ninja", "kinkou_rebel"],
#             "forms": ["base_form", "shroud_form", "k/da_form"],
#             "abilities": ["five_point_strike", "twilight_shroud", "shuriken_flip", "perfect_execution"],
#             "relationships": ["k/da_member", "shen's_student", "kennen's_peer"],
#             "outfits": ["classic", "k/da", "true_damage", "crime_city_nightmare"]
#         },
#         "evelynn": {
#             "names": ["evelynn", "agony's_embrace", "demon_shade"],
#             "titles": ["agony's_embrace", "demon_queen", "k/da_diva"],
#             "forms": ["base_form", "demon_shade_form", "k/da_form"],
#             "abilities": ["hate_spike", "allure", "whiplash", "last_caress"],
#             "relationships": ["k/da_member", "twisted_fate's_nemesis", "demon_sister"],
#             "outfits": ["classic", "k/da", "coven", "sugar_rush"]
#         },
#         "irelia": {
#             "names": ["irelia", "blade_dancer", "xan_warrior"],
#             "titles": ["blade_dancer", "ionian_captain", "defiant_blade"],
#             "forms": ["base_form", "blade_surge_form", "divine_sword_form"],
#             "abilities": ["bladesurge", "defiant_dance", "flawless_duet", "vanguard's_edge"],
#             "relationships": ["ionian_defender", "karma's_ally", "syndra's_rival"],
#             "outfits": ["classic", "divine_sword", "high_noon", "sentinel"]
#         },
#
#         "kayle": {
#             "names": ["kayle", "righteous", "judicator"],
#             "titles": ["the_righteous", "judicator", "winged_protector"],
#             "forms": ["base_form", "exalted_form", "transcended_form"],
#             "abilities": ["radiant_blast", "celestial_blessing", "starfire_spellblade", "divine_judgment"],
#             "relationships": ["morgana's_sister", "aspect_of_justice", "targon's_champion"],
#             "outfits": ["classic", "pentakill", "psyops", "dragonslayer"]
#         },
#         "morgana": {
#             "names": ["morgana", "fallen_angel", "dark_angel"],
#             "titles": ["the_fallen", "dark_angel", "sinful_succor"],
#             "forms": ["base_form", "fallen_form", "coven_form"],
#             "abilities": ["dark_binding", "tormented_shadow", "black_shield", "soul_shackles"],
#             "relationships": ["kayle's_sister", "aspect_reject", "coven_member"],
#             "outfits": ["classic", "coven", "bewitching", "dawnbringer"]
#         },
#         "neeko": {
#             "names": ["neeko", "curious_chameleon", "vastayan_shapeshifter"],
#             "titles": ["curious_chameleon", "vastayan_mimic", "spirit_bloomer"],
#             "forms": ["base_form", "shapeshifted_form", "star_guardian_form"],
#             "abilities": ["blooming_burst", "shapesplitter", "tangle_barbs", "pop_blossom"],
#             "relationships": ["vastayan_survivor", "nidalee's_friend", "star_guardian_member"],
#             "outfits": ["classic", "star_guardian", "shan_hai_scrolls"]
#         },
#         "samira": {
#             "names": ["samira", "desert_rose", "style_master"],
#             "titles": ["the_desert_rose", "style_incarnate", "mercenary_queen"],
#             "forms": ["base_form", "style_master_form", "high_noon_form"],
#             "abilities": ["flair", "wild_rush", "blade_whirl", "inferno_trigger"],
#             "relationships": ["noxian_mercenary", "sivir's_rival", "style_master"],
#             "outfits": ["classic", "psyops", "high_noon", "space_groove"]
#         },
#         "seraphine": {
#             "names": ["seraphine", "starry_songstress", "piltover_idol"],
#             "titles": ["starry_songstress", "rising_star", "k/da_collaborator"],
#             "forms": ["base_form", "stage_form", "k/da_form"],
#             "abilities": ["high_note", "surround_sound", "beat_drop", "encore"],
#             "relationships": ["k/da_collaborator", "piltover_star", "zaun_bridge"],
#             "outfits": ["classic", "k/da_all_out", "graceful_phoenix"]
#         },
#         "senna": {
#             "names": ["senna", "redeemer", "shadow_sentinel"],
#             "titles": ["the_redeemer", "shadow's_embrace", "sentinel_of_light"],
#             "forms": ["base_form", "wraith_form", "true_damage_form"],
#             "abilities": ["piercing_darkness", "last_embrace", "curse_of_the_black_mist", "dawning_shadow"],
#             "relationships": ["lucian's_wife", "thresh's_victim", "sentinel_leader"],
#             "outfits": ["classic", "true_damage", "project", "high_noon"]
#         },
#
#         # "ahri": {
#         #     "gelbooru": ["ahri", "ahri_%28league_of_legends%29", "nine_tailed_fox"],
#         #     "danbooru": ["ahri", "nine_tailed_fox_(lol)"]
#         # },
#         # "kaisa": {
#         #     "gelbooru": ["kai%27sa", "kaisa", "daughter_of_the_void"],
#         #     "danbooru": ["kai'sa", "void_hunter"]
#         # },
#         # "jinx": {
#         #     "gelbooru": ["jinx_%28league_of_legends%29", "loose_cannon"],
#         #     "danbooru": ["jinx_(league_of_legends)", "the_loose_cannon"]
#         # },
#         #
#         # # Mid lane champions
#         # "katarina": {
#         #     "gelbooru": ["katarina_%28league_of_legends%29", "sinister_blade"],
#         #     "danbooru": ["katarina", "the_sinister_blade"]
#         # },
#         # "leblanc": {
#         #     "gelbooru": ["leblanc_%28league_of_legends%29", "the_deceiver"],
#         #     "danbooru": ["leblanc", "deceiver"]
#         # },
#         # "zoe": {
#         #     "gelbooru": ["zoe_%28league_of_legends%29", "aspect_of_twilight"],
#         #     "danbooru": ["zoe_(league_of_legends)", "twilight_aspect"]
#         # },
#         #
#         # # New/Recent champions
#         # "bel_veth": {
#         #     "gelbooru": ["bel%27veth", "empress_of_the_void"],
#         #     "danbooru": ["bel'veth", "void_empress"]
#         # },
#         # "nilah": {
#         #     "gelbooru": ["nilah_%28league_of_legends%29", "joy_unbound"],
#         #     "danbooru": ["nilah", "the_unbound_joy"]
#         # },
#         # "renata": {
#         #     "gelbooru": ["renata_glasc", "chem_baroness"],
#         #     "danbooru": ["renata", "glasc_industries"]
#         # },
#         # "gwen": {
#         #     "gelbooru": ["gwen_%28league_of_legends%29", "hallowed_seamstress"],
#         #     "danbooru": ["gwen", "the_hallowed_seamstress"]
#         # },
#         #
#         # # Additional champions with expanded tags
#         # "akali": {
#         #     "gelbooru": ["akali", "rogue_assassin"],
#         #     "danbooru": ["akali", "the_rogue_assassin"]
#         # },
#         # "evelynn": {
#         #     "gelbooru": ["evelynn_%28league_of_legends%29", "agony's_embrace"],
#         #     "danbooru": ["evelynn", "agony_embrace"]
#         # },
#         # "irelia": {
#         #     "gelbooru": ["irelia", "blade_dancer"],
#         #     "danbooru": ["irelia", "the_blade_dancer"]
#         # },
#         # "kayle": {
#         #     "gelbooru": ["kayle_%28league_of_legends%29", "righteous"],
#         #     "danbooru": ["kayle", "the_righteous"]
#         # },
#         # "morgana": {
#         #     "gelbooru": ["morgana_%28league_of_legends%29", "fallen"],
#         #     "danbooru": ["morgana", "the_fallen"]
#         # },
#         # "neeko": {
#         #     "gelbooru": ["neeko_%28league_of_legends%29", "curious_chameleon"],
#         #     "danbooru": ["neeko", "the_curious_chameleon"]
#         # },
#         # "samira": {
#         #     "gelbooru": ["samira_%28league_of_legends%29", "desert_rose"],
#         #     "danbooru": ["samira", "the_desert_rose"]
#         # },
#         # "seraphine": {
#         #     "gelbooru": ["seraphine_%28league_of_legends%29", "starry_eyed_songstress"],
#         #     "danbooru": ["seraphine", "the_starry_songstress"]
#         # },
#         # "senna": {
#         #     "gelbooru": ["senna_%28league_of_legends%29", "redeemer"],
#         #     "danbooru": ["senna", "the_redeemer"]
#         # }
#     },
#
#     POKEMON_TAGS = {
#         # Main characters with expanded tags
#         "misty": {
#             "names": [
#                 "kasumi", "misty", "water_princess",
#                 "cerulean_gym_leader"
#             ],
#             "titles": [
#                 "water_gym_leader", "cerulean_sister",
#                 "kanto_gym_leader", "water_trainer"
#             ],
#             "forms": [
#                 "base_form", "gym_leader_form",
#                 "alola_form", "swimmer_form"
#             ],
#             "affiliations": [
#                 "cerulean_gym", "kanto_gym_leaders",
#                 "cerulean_sisters", "pokemon_league"
#             ],
#             "abilities": [
#                 "water_pokemon_training", "swimming_expertise",
#                 "gym_leadership", "battle_tactics"
#             ],
#             "relationships": [
#                 "cerulean_sister", "ash's_companion",
#                 "brock's_friend", "psyduck's_trainer"
#             ],
#             "outfits": [
#                 "gym_leader_outfit", "swimming_attire",
#                 "casual_clothes", "alola_outfit"
#             ]
#         },
#         "may": {
#             "names": [
#                 "haruka", "may", "princess_of_hoenn",
#                 "contest_star"
#             ],
#             "titles": [
#                 "pokemon_coordinator", "contest_champion",
#                 "hoenn_princess", "blaziken_trainer"
#             ],
#             "forms": [
#                 "base_form", "contest_form",
#                 "coordinator_mode", "battle_stance"
#             ],
#             "affiliations": [
#                 "hoenn_coordinators", "pokemon_contests",
#                 "petalburg_gym_family", "contest_circuit"
#             ],
#             "abilities": [
#                 "pokemon_coordination", "contest_performance",
#                 "battle_style", "seal_coordination"
#             ],
#             "relationships": [
#                 "norman's_daughter", "max's_sister",
#                 "ash's_companion", "drew's_rival"
#             ],
#             "outfits": [
#                 "coordinator_outfit", "contest_dress",
#                 "traveling_clothes", "battle_gear"
#             ]
#         },
#         "dawn": {
#             "names": [
#                 "hikari", "dawn", "contest_prodigy",
#                 "sinnoh_coordinator"
#             ],
#             "titles": [
#                 "top_coordinator", "contest_star",
#                 "piplup_trainer", "sinnoh_princess"
#             ],
#             "forms": [
#                 "base_form", "contest_form",
#                 "cheerleader_form", "winter_form"
#             ],
#             "affiliations": [
#                 "sinnoh_coordinators", "pokemon_contests",
#                 "contest_circuit", "twinleaf_town"
#             ],
#             "abilities": [
#                 "pokemon_coordination", "contest_performance",
#                 "seal_mastery", "battle_choreography"
#             ],
#             "relationships": [
#                 "johanna's_daughter", "ash's_companion",
#                 "kenny's_childhood_friend", "zoey's_rival"
#             ],
#             "outfits": [
#                 "coordinator_dress", "contest_outfit",
#                 "cheerleader_uniform", "winter_clothes"
#             ]
#         },
#
#         "sabrina": {
#             "names": ["sabrina", "natsume", "psychic_master"],
#             "titles": ["psychic_gym_leader", "kanto_gym_leader", "psychic_prodigy"],
#             "forms": ["base_form", "gym_leader_form", "psychic_mode"],
#             "abilities": ["psychic_powers", "pokemon_training", "telekinesis"],
#             "relationships": ["kanto_gym_leader", "haunter's_friend", "psychic_trainer"],
#             "outfits": ["gym_leader_uniform", "casual_attire", "psychic_garb"]
#         },
#         "elesa": {
#             "names": ["elesa", "kamitsure", "shining_beauty"],
#             "titles": ["electric_gym_leader", "top_model", "nimbasa_leader"],
#             "forms": ["base_form", "model_form", "gym_leader_form"],
#             "abilities": ["electric_pokemon_training", "modeling", "battle_expertise"],
#             "relationships": ["unova_gym_leader", "fashion_icon", "skyla's_friend"],
#             "outfits": ["gym_leader_outfit", "model_attire", "electric_uniform"]
#         },
#         "nessa": {
#             "names": ["nessa", "rurina", "water_model"],
#             "titles": ["water_gym_leader", "galar_model", "hulbury_leader"],
#             "forms": ["base_form", "dynamax_form", "model_form"],
#             "abilities": ["water_pokemon_training", "modeling", "dynamax_control"],
#             "relationships": ["galar_gym_leader", "model_trainer", "sonia's_friend"],
#             "outfits": ["gym_uniform", "swimsuit", "model_clothes"]
#         },
#         "cynthia": {
#             "names": ["cynthia", "shirona", "champion"],
#             "titles": ["sinnoh_champion", "mythology_expert", "battle_queen"],
#             "forms": ["base_form", "champion_form", "ancient_researcher"],
#             "abilities": ["champion_level_training", "archaeological_expertise", "battle_mastery"],
#             "relationships": ["sinnoh_champion", "grandmother's_student", "dawn's_mentor"],
#             "outfits": ["champion_attire", "casual_clothes", "research_gear"]
#         },
#         "diantha": {
#             "names": ["diantha", "carnet", "movie_star"],
#             "titles": ["kalos_champion", "actor_champion", "movie_queen"],
#             "forms": ["base_form", "mega_evolution_form", "actress_form"],
#             "abilities": ["mega_evolution", "champion_battling", "acting"],
#             "relationships": ["kalos_champion", "movie_star", "gardevoir's_trainer"],
#             "outfits": ["champion_dress", "movie_costume", "casual_attire"]
#         },
#         "gloria": {
#             "names": ["gloria", "yuuri", "galar_champion", "shield_trainer"],
#             "titles": ["galar_champion", "dynamax_master", "crown_tundra_explorer"],
#             "forms": ["base_form", "champion_form", "dynamax_trainer"],
#             "abilities": ["dynamax_control", "champion_skills", "pokemon_training"],
#             "relationships": ["hop's_rival", "champion_trainer", "galar_hero"],
#             "outfits": ["trainer_uniform", "champion_outfit", "casual_wear"]
#         },
#         "leaf": {
#             "names": ["leaf", "blue", "green", "kanto_heroine"],
#             "titles": ["kanto_champion", "pokedex_holder", "oak's_trainer"],
#             "forms": ["base_form", "champion_form", "lets_go_form"],
#             "abilities": ["pokemon_training", "pokedex_completion", "battle_expertise"],
#             "relationships": ["red's_counterpart", "oak's_student", "kanto_trainer"],
#             "outfits": ["classic_outfit", "lets_go_attire", "champion_wear"]
#         },
#         "hilda": {
#             "names": ["hilda", "touko", "unova_hero"],
#             "titles": ["unova_champion", "hero_of_truth", "pokemon_trainer"],
#             "forms": ["base_form", "hero_form", "trainer_form"],
#             "abilities": ["pokemon_training", "truth_seeker", "battle_mastery"],
#             "relationships": ["bianca's_friend", "n's_counterpart", "champion_trainer"],
#             "outfits": ["trainer_outfit", "hero_attire", "casual_clothes"]
#         },
#         "rosa": {
#             "names": ["rosa", "mei", "unova_movie_star"],
#             "titles": ["pokestar_actress", "unova_trainer", "pokemon_world_tournament_champion"],
#             "forms": ["base_form", "actress_form", "pwt_champion"],
#             "abilities": ["pokemon_training", "acting", "battle_expertise"],
#             "relationships": ["nate's_counterpart", "pokestar_studios_star", "unova_trainer"],
#             "outfits": ["trainer_outfit", "movie_costumes", "pwt_uniform"]
#         },
#
#         "melony": {
#             "names": ["melony", "ice_master", "circhester_leader"],
#             "titles": ["ice_gym_leader", "circhester_master", "snow_queen"],
#             "forms": ["base_form", "dynamax_form", "gym_leader_form"],
#             "abilities": ["ice_pokemon_training", "dynamax_control", "gym_leadership"],
#             "relationships": ["gordie's_mother", "galar_gym_leader", "ice_specialist"],
#             "outfits": ["gym_uniform", "winter_wear", "casual_attire"]
#         },
#         "klara": {
#             "names": ["klara", "poison_idol", "isle_trainer"],
#             "titles": ["poison_type_master", "idol_trainer", "dojo_trainer"],
#             "forms": ["base_form", "idol_form", "battle_form"],
#             "abilities": ["poison_pokemon_training", "idol_performance", "battle_tactics"],
#             "relationships": ["mustard's_student", "avery's_rival", "dojo_trainer"],
#             "outfits": ["dojo_uniform", "idol_costume", "training_gear"]
#         },
#         "oleana": {
#             "names": ["oleana", "macro_cosmos_president", "rose's_secretary"],
#             "titles": ["company_president", "macro_cosmos_leader", "battle_executive"],
#             "forms": ["base_form", "executive_form", "battle_mode"],
#             "abilities": ["business_management", "pokemon_training", "corporate_leadership"],
#             "relationships": ["rose's_secretary", "macro_cosmos_leader", "bede's_superior"],
#             "outfits": ["business_suit", "executive_attire", "battle_outfit"]
#         },
#         "bea": {
#             "names": ["bea", "fighting_master", "stow_on_side_leader"],
#             "titles": ["fighting_gym_leader", "karate_master", "battle_expert"],
#             "forms": ["base_form", "dynamax_form", "fighting_stance"],
#             "abilities": ["fighting_pokemon_training", "martial_arts", "dynamax_control"],
#             "relationships": ["galar_gym_leader", "allister's_colleague", "martial_artist"],
#             "outfits": ["gym_uniform", "karate_gi", "training_clothes"]
#         },
#         "acerola": {
#             "names": ["acerola", "ghost_princess", "elite_member"],
#             "titles": ["ghost_elite_four", "trial_captain", "royal_descendant"],
#             "forms": ["base_form", "trial_captain_form", "elite_four_form"],
#             "abilities": ["ghost_pokemon_training", "trial_leadership", "elite_four_skills"],
#             "relationships": ["elite_four_member", "trial_captain", "nanu's_ward"],
#             "outfits": ["trial_captain_clothes", "elite_four_uniform", "casual_attire"]
#         },
#
#         # "misty": {
#         #     "gelbooru": ["misty_%28pokemon%29", "kasumi", "water_gym_leader"],
#         #     "danbooru": ["misty_(pokemon)", "kasumi_(pokemon)"]
#         # },
#         # "may": {
#         #     "gelbooru": ["may_%28pokemon%29", "haruka", "hoenn_coordinator"],
#         #     "danbooru": ["may_(pokemon)", "haruka_(pokemon)"]
#         # },
#         # "dawn": {
#         #     "gelbooru": ["dawn_%28pokemon%29", "hikari", "sinnoh_coordinator"],
#         #     "danbooru": ["dawn_(pokemon)", "hikari_(pokemon)"]
#         # },
#         #
#         # # Gym Leaders
#         # "sabrina": {
#         #     "gelbooru": ["sabrina_%28pokemon%29", "psychic_gym_leader"],
#         #     "danbooru": ["sabrina_(pokemon)", "saffron_gym_leader"]
#         # },
#         # "elesa": {
#         #     "gelbooru": ["elesa_%28pokemon%29", "electric_model"],
#         #     "danbooru": ["elesa", "nimbasa_gym_leader"]
#         # },
#         # "nessa": {
#         #     "gelbooru": ["nessa_%28pokemon%29", "water_model"],
#         #     "danbooru": ["nessa", "hulbury_gym_leader"]
#         # },
#         #
#         # # Champions and Elite Four
#         # "cynthia": {
#         #     "gelbooru": ["cynthia_%28pokemon%29", "shirona"],
#         #     "danbooru": ["cynthia_(pokemon)", "sinnoh_champion"]
#         # },
#         # "diantha": {
#         #     "gelbooru": ["diantha_%28pokemon%29", "kalos_champion"],
#         #     "danbooru": ["diantha", "carnet"]
#         # },
#         #
#         # # New/Additional characters
#         # "gloria": {
#         #     "gelbooru": ["gloria_%28pokemon%29", "yuuri", "sword_shield_protagonist"],
#         #     "danbooru": ["gloria_(pokemon)", "female_protagonist_swsh"]
#         # },
#         # "leaf": {
#         #     "gelbooru": ["leaf_%28pokemon%29", "green", "blue"],
#         #     "danbooru": ["leaf_(pokemon)", "female_protagonist_rgby"]
#         # },
#         # "hilda": {
#         #     "gelbooru": ["hilda_%28pokemon%29", "touko"],
#         #     "danbooru": ["hilda_(pokemon)", "female_protagonist_bw"]
#         # },
#         # "rosa": {
#         #     "gelbooru": ["rosa_%28pokemon%29", "mei"],
#         #     "danbooru": ["rosa_(pokemon)", "female_protagonist_bw2"]
#         # },
#         # "melony": {
#         #     "gelbooru": ["melony_%28pokemon%29", "ice_gym_leader"],
#         #     "danbooru": ["melony", "circhester_gym_leader"]
#         # },
#         # "klara": {
#         #     "gelbooru": ["klara_%28pokemon%29", "poison_gym_leader"],
#         #     "danbooru": ["klara", "isle_of_armor_trainer"]
#         # },
#         # "oleana": {
#         #     "gelbooru": ["oleana_%28pokemon%29", "macro_cosmos"],
#         #     "danbooru": ["oleana", "rose's_secretary"]
#         # },
#         # "bea": {
#         #     "gelbooru": ["bea_%28pokemon%29", "fighting_gym_leader"],
#         #     "danbooru": ["bea_(pokemon)", "stow_on_side_gym_leader"]
#         # },
#         # "acerola": {
#         #     "gelbooru": ["acerola_%28pokemon%29", "ghost_elite_four"],
#         #     "danbooru": ["acerola", "alola_elite_four"]
#         # }
#     },
#
#     NARUTO_TAGS = {
#         # Main characters with expanded tags
#         "tsunade": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "tsunade", "tsunade_(naruto)", "senju_tsunade", "tsunade_senju",
#
#                 # Official titles and positions
#                 "godaime_hokage", "fifth_hokage", "princess_tsunade", "lady_tsunade",
#                 "legendary_sannin", "legendary_sucker", "slug_princess",
#
#                 # Clan and family relationships
#                 "senju_clan", "princess_of_the_senju", "granddaughter_of_the_first_hokage",
#                 "tsunade_of_the_sannin", "senju_clan_head",
#
#                 # Special states and forms
#                 "sage_mode_tsunade", "hundred_healings", "byakugou_seal",
#                 "strength_of_a_hundred_seal", "creation_rebirth",
#                 "young_tsunade", "drunken_tsunade", "angry_tsunade",
#                 "battle_tsunade", "transformed_tsunade",
#
#                 # Combat abilities and powers
#                 "medical_ninja", "super_strength", "summoning_technique",
#                 "katsuyu_summoner", "healing_technique", "chakra_enhanced_strength",
#                 "ninja_art_mitotic_regeneration",
#
#                 # Teams and affiliations
#                 "sannin", "team_hiruzen", "konoha_council", "hokage",
#                 "konohagakure", "allied_shinobi_forces_leader",
#
#                 # Personal relationships
#                 "dan's_lover", "nawaki's_sister", "jiraiya's_teammate",
#                 "orochimaru's_teammate", "sakura's_master", "shizune's_master",
#
#                 # Specific appearances and outfits
#                 "hokage_robe", "green_jacket", "gambling_tsunade",
#                 "casual_tsunade", "formal_tsunade", "medical_tsunade",
#
#                 # Time periods and ages
#                 "young_tsunade", "first_war_tsunade", "second_war_tsunade",
#                 "wandering_tsunade", "hokage_tsunade", "boruto_era_tsunade"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "tsunade", "senju_tsunade", "godaime_hokage",
#                 "princess_tsunade", "legendary_sannin",
#
#                 # States and abilities
#                 "hundred_healings", "byakugou_seal", "strength_of_a_hundred",
#                 "medical_ninja", "super_strength", "summoning_jutsu",
#
#                 # Affiliations
#                 "team_hiruzen", "sannin", "hokage", "konoha_ninja",
#
#                 # Time periods
#                 "young_version", "classic_tsunade", "boruto_era"
#             ]
#         },
#
#         "sakura": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "haruno_sakura", "sakura_(naruto)", "sakura_haruno",
#                 "sakura_uchiha", "uchiha_sakura",
#
#                 # Special forms and states
#                 "inner_sakura", "adult_sakura", "young_sakura",
#                 "hundred_healings_sakura", "byakugou_sakura",
#                 "chunin_sakura", "jonin_sakura", "doctor_sakura",
#
#                 # Titles and positions
#                 "konoha_medical_ninja", "tsunade's_apprentice",
#                 "head_medical_ninja", "hospital_director",
#
#                 # Teams and affiliations
#                 "team_7", "team_kakashi", "konoha_11",
#                 "allied_shinobi_forces", "konoha_hospital",
#                 "medical_corps", "rescue_sasuke_team",
#
#                 # Relationships
#                 "sasuke's_wife", "sarada's_mother", "tsunade's_student",
#                 "ino's_rival", "naruto's_teammate", "kakashi's_student",
#
#                 # Abilities and powers
#                 "chakra_enhanced_strength", "medical_ninjutsu",
#                 "byakugou_seal", "hundred_healings",
#                 "cherry_blossom_impact", "chakra_control",
#
#                 # Emotional states
#                 "crying_sakura", "angry_sakura", "determined_sakura",
#                 "happy_sakura", "serious_sakura", "fighting_sakura",
#
#                 # Time periods and versions
#                 "part_1_sakura", "part_2_sakura", "boruto_era_sakura",
#                 "academy_sakura", "genin_sakura", "war_arc_sakura",
#
#                 # Outfits and appearances
#                 "casual_sakura", "medical_uniform", "chunin_vest",
#                 "battle_outfit", "formal_wear", "winter_outfit"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "haruno_sakura", "sakura_(naruto)", "uchiha_sakura",
#
#                 # Forms and states
#                 "inner_sakura", "adult_sakura", "young_sakura",
#                 "hundred_healings", "byakugou_seal",
#
#                 # Roles and abilities
#                 "medical_ninja", "super_strength", "chakra_control",
#
#                 # Teams and affiliations
#                 "team_seven", "konoha_11", "medical_corps",
#
#                 # Time periods
#                 "classic_sakura", "shippuden_sakura", "boruto_era"
#             ]
#         },
#
#         "hinata": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "hyuuga_hinata", "hinata_hyuuga", "hinata_(naruto)",
#                 "uzumaki_hinata", "hinata_uzumaki",
#
#                 # Titles and positions
#                 "byakugan_princess", "hyuuga_heiress", "gentle_fist_master",
#                 "naruto's_wife", "himawari's_mother", "boruto's_mother",
#
#                 # Clan and family relationships
#                 "hyuuga_clan", "main_branch_member", "hanabi's_sister",
#                 "hiashi's_daughter", "neji's_cousin", "uzumaki_family",
#
#                 # Special states and forms
#                 "twin_lion_fists", "gentle_step_twin_lion_fists",
#                 "protective_eight_trigrams_sixty-four_palms",
#                 "byakugan_activated", "gentle_fist_stance",
#
#                 # Combat abilities and powers
#                 "byakugan", "gentle_fist", "eight_trigrams",
#                 "protective_eight_trigrams", "chakra_control",
#                 "twin_lion_fists_mode", "air_palm",
#
#                 # Teams and affiliations
#                 "team_8", "team_kurenai", "konoha_11",
#                 "allied_shinobi_forces", "konohagakure",
#
#                 # Emotional states and personalities
#                 "shy_hinata", "determined_hinata", "confident_hinata",
#                 "fighting_hinata", "blushing_hinata", "brave_hinata",
#
#                 # Time periods and versions
#                 "young_hinata", "academy_hinata", "genin_hinata",
#                 "chunin_hinata", "war_arc_hinata", "the_last_hinata",
#                 "adult_hinata", "boruto_era_hinata",
#
#                 # Outfits and appearances
#                 "mission_outfit", "casual_hinata", "formal_kimono",
#                 "training_outfit", "winter_coat", "wedding_dress"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "hyuuga_hinata", "hinata_(naruto)", "uzumaki_hinata",
#
#                 # Powers and abilities
#                 "byakugan", "gentle_fist", "twin_lion_fists",
#
#                 # Relationships and roles
#                 "hyuuga_clan", "team_eight", "naruto's_wife",
#
#                 # Time periods
#                 "young_hinata", "teen_hinata", "adult_hinata",
#                 "the_last_version", "boruto_era"
#             ]
#         },
#
#         "ino": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "yamanaka_ino", "ino_(naruto)", "ino_yamanaka",
#                 "ino_sai", "mrs_yamanaka",
#
#                 # Titles and positions
#                 "head_of_yamanaka_clan", "konoha_intelligence_division",
#                 "interrogation_unit_leader", "sensor_type",
#
#                 # Clan and family relationships
#                 "yamanaka_clan", "inoichi's_daughter", "sai's_wife",
#                 "inojin's_mother", "ino-shika-cho",
#
#                 # Special abilities and techniques
#                 "mind_transfer_jutsu", "mind_destruction_jutsu",
#                 "chakra_transfer", "medical_ninjutsu", "sensory_abilities",
#                 "mind_transmission", "flower_ninja_art",
#
#                 # Teams and affiliations
#                 "team_10", "team_asuma", "konoha_11",
#                 "allied_shinobi_forces", "yamanaka_flower_shop",
#                 "konoha_barrier_team", "sensory_unit",
#
#                 # Emotional states and personalities
#                 "confident_ino", "angry_ino", "determined_ino",
#                 "flirting_ino", "serious_ino", "fighting_ino",
#
#                 # Time periods and versions
#                 "young_ino", "academy_ino", "genin_ino",
#                 "chunin_ino", "war_arc_ino", "adult_ino",
#                 "boruto_era_ino",
#
#                 # Outfits and appearances
#                 "purple_outfit", "ninja_uniform", "casual_ino",
#                 "flower_shop_apron", "war_outfit", "formal_wear"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "yamanaka_ino", "ino_(naruto)", "ino_yamanaka",
#
#                 # Powers and abilities
#                 "mind_transfer", "sensor_type", "medical_ninja",
#
#                 # Teams and affiliations
#                 "team_ten", "ino-shika-cho", "yamanaka_clan",
#
#                 # Time periods
#                 "young_ino", "teen_ino", "adult_ino",
#                 "boruto_era"
#             ]
#         },
#
#         "tenten": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "tenten", "tenten_(naruto)", "ten_ten",
#
#                 # Titles and positions
#                 "weapons_specialist", "tool_specialist",
#                 "rising_twin_dragons", "konoha_weapons_expert",
#
#                 # Combat specialties and abilities
#                 "weapon_summoning", "ninja_tool_specialist",
#                 "fuinjutsu_expert", "rising_twin_dragons",
#                 "bashosen_wielder", "sealed_weapons_master",
#
#                 # Teams and affiliations
#                 "team_guy", "team_9", "konoha_11",
#                 "allied_shinobi_forces", "konohagakure",
#
#                 # Fighting styles and techniques
#                 "twin_rising_dragons", "weapon_control",
#                 "ninja_tool_summoning", "sealing_techniques",
#                 "bashosen_techniques", "weapon_barrage",
#
#                 # Emotional states and personalities
#                 "determined_tenten", "serious_tenten", "fighting_tenten",
#                 "cheerful_tenten", "focused_tenten",
#
#                 # Time periods and versions
#                 "young_tenten", "academy_tenten", "genin_tenten",
#                 "chunin_tenten", "war_arc_tenten", "adult_tenten",
#                 "boruto_era_tenten",
#
#                 # Outfits and appearances
#                 "chinese_style_outfit", "mission_gear", "casual_tenten",
#                 "weapons_shop_outfit", "training_outfit", "formal_wear"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "tenten", "tenten_(naruto)",
#
#                 # Abilities and specialties
#                 "weapons_master", "tool_specialist", "rising_dragons",
#
#                 # Teams and time periods
#                 "team_guy", "konoha_11", "adult_version",
#                 "young_tenten", "boruto_era"
#             ]
#         },
#
#         "kurenai": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "yuuhi_kurenai", "kurenai_yuhi", "kurenai_(naruto)",
#                 "sarutobi_kurenai", "mirai's_mother",
#
#                 # Titles and positions
#                 "genjutsu_mistress", "jonin_sensei", "team_8_leader",
#                 "konoha_jonin", "genjutsu_specialist",
#
#                 # Family relationships
#                 "asuma's_wife", "mirai's_mother", "sarutobi_clan",
#                 "yuhi_clan", "konoha_elite",
#
#                 # Special abilities and techniques
#                 "genjutsu_master", "illusion_techniques",
#                 "demonic_illusion", "tree_binding_death",
#                 "flower_petal_escape", "chakra_control",
#
#                 # Teams and affiliations
#                 "team_8_leader", "konoha_jonin", "kurenai_squad",
#                 "hinata's_teacher", "kiba's_teacher", "shino's_teacher",
#
#                 # Time periods and versions
#                 "young_kurenai", "chunin_kurenai", "jonin_kurenai",
#                 "pregnant_kurenai", "war_arc_kurenai", "adult_kurenai",
#                 "boruto_era_kurenai",
#
#                 # States and appearances
#                 "battle_ready", "teaching_mode", "casual_kurenai",
#                 "formal_dress", "maternity_wear", "mourning_kurenai",
#
#                 # Emotional states
#                 "serious_kurenai", "caring_kurenai", "determined_kurenai",
#                 "grieving_kurenai", "motherly_kurenai"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "yuuhi_kurenai", "kurenai_(naruto)", "sarutobi_kurenai",
#
#                 # Abilities and roles
#                 "genjutsu_master", "jonin_sensei", "team_8",
#
#                 # Relationships
#                 "asuma's_wife", "mirai's_mother",
#
#                 # Time periods
#                 "young_kurenai", "pregnant_kurenai", "adult_kurenai"
#             ]
#         },
#
#         "anko": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "mitarashi_anko", "anko_mitarashi", "anko_(naruto)",
#
#                 # Titles and positions
#                 "special_jonin", "chunin_exam_proctor",
#                 "torture_specialist", "snake_mistress",
#                 "orochimaru's_former_student",
#
#                 # Combat specialties
#                 "snake_summoner", "cursed_seal_bearer",
#                 "hidden_shadow_snake_hands", "poison_specialist",
#                 "torture_and_interrogation_force",
#
#                 # Special states and forms
#                 "cursed_seal_active", "snake_form", "battle_mode",
#                 "young_anko", "chunin_exam_anko", "adult_anko",
#
#                 # Techniques and abilities
#                 "snake_techniques", "shadow_snake_hands",
#                 "multiple_striking_shadow_snakes", "senbon_techniques",
#                 "cursed_seal_techniques",
#
#                 # Teams and affiliations
#                 "konoha_torture_and_interrogation", "exam_proctors",
#                 "orochimaru's_students", "academy_teacher",
#
#                 # Time periods and versions
#                 "young_anko", "orochimaru's_student_anko",
#                 "special_jonin_anko", "war_arc_anko",
#                 "academy_teacher_anko", "boruto_era_anko",
#
#                 # States and appearances
#                 "battle_ready_anko", "casual_anko", "teacher_anko",
#                 "exam_proctor_anko", "overweight_anko", "slim_anko",
#
#                 # Emotional states
#                 "playful_anko", "serious_anko", "angry_anko",
#                 "sadistic_anko", "cheerful_anko"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "mitarashi_anko", "anko_(naruto)",
#
#                 # Abilities and roles
#                 "snake_summoner", "special_jonin", "exam_proctor",
#
#                 # States and forms
#                 "cursed_seal", "snake_techniques",
#
#                 # Time periods
#                 "young_anko", "adult_anko", "boruto_era"
#             ]
#         },
#
#         "shizune": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "shizune", "shizune_(naruto)", "kato_shizune",
#
#                 # Titles and positions
#                 "medical_ninja", "tsunade's_assistant",
#                 "hokage_assistant", "poison_expert",
#                 "konoha_hospital_director",
#
#                 # Relationships and connections
#                 "dan's_niece", "tsunade's_apprentice",
#                 "tonton's_caretaker", "medical_corps_leader",
#
#                 # Special abilities and techniques
#                 "medical_ninjutsu", "poison_techniques",
#                 "chakra_scalpel", "healing_techniques",
#                 "needle_techniques", "summoning_technique",
#
#                 # Teams and affiliations
#                 "hokage's_office", "medical_corps",
#                 "konoha_hospital", "tsunade's_group",
#
#                 # Combat specialties
#                 "poison_specialist", "senbon_user",
#                 "medical_techniques", "defensive_specialist",
#
#                 # Time periods and versions
#                 "young_shizune", "traveling_shizune",
#                 "hokage_assistant_shizune", "war_arc_shizune",
#                 "boruto_era_shizune",
#
#                 # States and appearances
#                 "medical_uniform", "casual_shizune",
#                 "battle_ready", "office_attire",
#
#                 # Emotional states
#                 "worried_shizune", "serious_shizune",
#                 "caring_shizune", "professional_shizune"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "shizune", "shizune_(naruto)", "kato_shizune",
#
#                 # Roles and abilities
#                 "medical_ninja", "tsunade's_assistant",
#                 "poison_expert",
#
#                 # Time periods
#                 "young_shizune", "adult_shizune", "boruto_era"
#             ]
#         },
#
#         "sarada": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "uchiha_sarada", "sarada_uchiha", "sarada_(naruto)",
#                 "sarada_uzumaki", "sakura's_daughter",
#
#                 # Titles and positions
#                 "future_hokage_candidate", "team_7_new_generation",
#                 "uchiha_heir", "konoha_genin", "academy_top_student",
#
#                 # Clan and family relationships
#                 "uchiha_clan", "sasuke's_daughter", "sakura's_daughter",
#                 "uzumaki_boruto's_teammate", "mitsuki's_teammate",
#                 "konohamaru's_student",
#
#                 # Special abilities and powers
#                 "sharingan", "sharingan_user", "chakra_enhanced_strength",
#                 "lightning_release", "fire_release", "chidori_user",
#                 "cha_strength", "cop_jutsu",
#
#                 # Forms and states
#                 "sharingan_activated", "glasses_on", "glasses_off",
#                 "fighting_stance", "training_mode", "angry_sarada",
#
#                 # Teams and affiliations
#                 "team_konohamaru", "new_team_7", "konoha_academy",
#                 "konohagakure", "uchiha_survivor",
#
#                 # Combat specialties
#                 "sharingan_techniques", "super_strength",
#                 "lightning_style", "fire_style", "shuriken_jutsu",
#
#                 # Outfits and appearances
#                 "ninja_outfit", "casual_clothes", "academy_uniform",
#                 "training_gear", "uchiha_crest", "mission_outfit",
#
#                 # Time periods and versions
#                 "academy_sarada", "genin_sarada", "chunin_exam_sarada",
#                 "teen_sarada", "young_sarada",
#
#                 # Emotional states
#                 "determined_sarada", "studying_sarada", "curious_sarada",
#                 "battle_ready_sarada", "happy_sarada", "serious_sarada"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "uchiha_sarada", "sarada_(naruto)",
#
#                 # Powers and abilities
#                 "sharingan", "super_strength", "glasses",
#
#                 # Teams and roles
#                 "team_konohamaru", "new_team_seven",
#
#                 # States and forms
#                 "sharingan_active", "training_mode", "battle_mode",
#
#                 # Time periods
#                 "academy_student", "genin_sarada", "teen_sarada"
#             ]
#         },
#
#         "himawari": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "uzumaki_himawari", "himawari_uzumaki",
#                 "himawari_(naruto)", "naruto's_daughter",
#
#                 # Family relationships
#                 "uzumaki_clan", "hyuuga_clan", "naruto's_daughter",
#                 "hinata's_daughter", "boruto's_sister", "kawaki's_sister",
#
#                 # Special abilities and powers
#                 "byakugan", "gentle_fist", "prodigy",
#                 "byakugan_princess", "gentle_fist_user",
#
#                 # Forms and states
#                 "byakugan_activated", "fighting_stance",
#                 "training_mode", "civilian_mode",
#
#                 # Activities and roles
#                 "academy_student", "ninja_trainee", "artist",
#                 "flower_pressing", "training_session",
#
#                 # Outfits and appearances
#                 "casual_outfit", "training_clothes", "academy_uniform",
#                 "festival_kimono", "summer_dress", "winter_outfit",
#
#                 # Time periods and versions
#                 "young_himawari", "academy_himawari", "teen_himawari",
#                 "child_himawari", "growing_himawari",
#
#                 # Emotional states
#                 "happy_himawari", "curious_himawari", "angry_himawari",
#                 "determined_himawari", "playful_himawari", "serious_himawari"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "uzumaki_himawari", "himawari_(naruto)",
#
#                 # Powers and abilities
#                 "byakugan", "gentle_fist",
#
#                 # Family connections
#                 "naruto's_daughter", "hinata's_daughter",
#
#                 # Time periods
#                 "young_himawari", "academy_student", "teen_version"
#             ]
#         },
#
#         "chocho": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "akimichi_chocho", "chocho_akimichi",
#                 "chocho_(naruto)", "butterfly_mode_user",
#
#                 # Clan and family relationships
#                 "akimichi_clan", "karui's_daughter", "choji's_daughter",
#                 "inojin's_teammate", "shikadai's_teammate",
#
#                 # Special abilities and powers
#                 "butterfly_mode", "expansion_jutsu", "super_multi_size",
#                 "lightning_release", "yang_release", "calorie_control",
#
#                 # Forms and states
#                 "butterfly_mode_active", "expanded_form",
#                 "slim_form", "fighting_stance", "training_mode",
#
#                 # Teams and affiliations
#                 "team_10", "new_ino-shika-cho", "konoha_genin",
#                 "moegi's_student", "konohagakure",
#
#                 # Combat specialties
#                 "expansion_techniques", "butterfly_techniques",
#                 "akimichi_clan_jutsu", "taijutsu_specialist",
#
#                 # Outfits and appearances
#                 "ninja_outfit", "casual_clothes", "training_gear",
#                 "mission_outfit", "chunin_exam_outfit",
#
#                 # Time periods and versions
#                 "academy_chocho", "genin_chocho", "chunin_exam_chocho",
#                 "teen_chocho", "young_chocho",
#
#                 # Emotional states
#                 "confident_chocho", "determined_chocho", "happy_chocho",
#                 "battle_ready_chocho", "relaxed_chocho", "serious_chocho"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "akimichi_chocho", "chocho_(naruto)",
#
#                 # Powers and abilities
#                 "butterfly_mode", "expansion_jutsu",
#
#                 # Teams and roles
#                 "team_ten", "new_ino-shika-cho",
#
#                 # States and forms
#                 "butterfly_form", "expanded_form", "slim_form",
#
#                 # Time periods
#                 "academy_student", "genin_chocho", "teen_chocho"
#             ]
#         },
#
#         "temari": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "temari", "temari_(naruto)", "nara_temari",
#                 "sand_princess", "wind_mistress",
#
#                 # Titles and positions
#                 "sand_ambassador", "wind_user", "jonin_commander",
#                 "sand_siblings", "kazekage's_sister",
#
#                 # Family relationships
#                 "gaara's_sister", "kankuro's_sister", "shikamaru's_wife",
#                 "shikadai's_mother", "fourth_kazekage's_daughter",
#
#                 # Special abilities and powers
#                 "wind_release", "fan_techniques", "summoning_jutsu",
#                 "great_wind_scythe", "wind_master", "kamatari_summoner",
#
#                 # Combat specialties
#                 "fan_wielder", "long-range_fighter", "strategist",
#                 "wind_techniques", "desert_warfare_specialist",
#
#                 # Teams and affiliations
#                 "sunagakure", "sand_siblings", "allied_shinobi_forces",
#                 "nara_clan", "konoha_liaison",
#
#                 # Time periods and versions
#                 "young_temari", "chunin_exam_temari", "war_arc_temari",
#                 "adult_temari", "boruto_era_temari",
#
#                 # States and appearances
#                 "battle_ready", "diplomatic_mode", "training_mode",
#                 "casual_temari", "angry_temari", "serious_temari",
#
#                 # Outfits and appearances
#                 "sand_uniform", "formal_kimono", "battle_outfit",
#                 "jonin_vest", "casual_clothes", "winter_outfit"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "temari", "temari_(naruto)", "nara_temari",
#
#                 # Powers and roles
#                 "wind_user", "fan_wielder", "sand_sister",
#
#                 # Time periods
#                 "young_temari", "adult_temari", "boruto_era"
#             ]
#         },
#
#         "mei": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "terumi_mei", "mei_terumi", "mei_(naruto)",
#                 "mizukage_mei", "fifth_mizukage",
#
#                 # Titles and positions
#                 "fifth_mizukage", "godaime_mizukage", "village_leader",
#                 "water_mistress", "lava_style_user",
#
#                 # Special abilities and powers
#                 "lava_release", "boil_release", "water_release",
#                 "lava_style", "vapor_style", "water_dragon",
#
#                 # Combat specialties
#                 "kekkei_genkai_user", "multiple_bloodline_traits",
#                 "ninjutsu_master", "long-range_fighter",
#
#                 # Teams and affiliations
#                 "kirigakure", "mizukage", "allied_shinobi_forces",
#                 "water_country", "mist_village",
#
#                 # Time periods and versions
#                 "young_mei", "civil_war_mei", "mizukage_mei",
#                 "war_arc_mei", "retired_mei", "boruto_era_mei",
#
#                 # States and appearances
#                 "battle_ready", "kage_mode", "formal_attire",
#                 "casual_mei", "serious_mei", "flirty_mei",
#
#                 # Outfits and appearances
#                 "mizukage_robes", "battle_outfit", "formal_dress",
#                 "casual_clothes", "wedding_dress"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "terumi_mei", "mei_(naruto)", "mizukage",
#
#                 # Powers and abilities
#                 "lava_release", "boil_release", "water_release",
#
#                 # Time periods
#                 "young_mei", "mizukage_era", "retired_mei"
#             ]
#         },
#
#         "konan": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "konan", "konan_(naruto)", "angel_of_amegakure",
#                 "paper_angel", "origami_angel", "lady_angel",
#
#                 # Titles and positions
#                 "akatsuki_member", "ame_orphan", "amegakure_leader",
#                 "pain's_partner", "yahiko's_friend", "nagato's_companion",
#
#                 # Special abilities and powers
#                 "paper_style", "paper_techniques", "angel_mode",
#                 "paper_clone", "paper_butterfly", "paper_weapons",
#                 "dance_of_the_shikigami", "paper_ocean",
#
#                 # Forms and states
#                 "angel_form", "paper_form", "battle_mode",
#                 "origami_form", "paper_dispersal", "winged_form",
#
#                 # Teams and affiliations
#                 "akatsuki", "amegakure", "original_akatsuki",
#                 "ame_orphans", "rain_village", "pain's_group",
#
#                 # Combat specialties
#                 "paper_manipulation", "flight_capable", "long-range_fighter",
#                 "trap_specialist", "origami_master", "paper_bombs",
#
#                 # Time periods and versions
#                 "young_konan", "orphan_konan", "akatsuki_konan",
#                 "amegakure_konan", "final_battle_konan",
#
#                 # Outfits and appearances
#                 "akatsuki_cloak", "paper_dress", "casual_konan",
#                 "battle_outfit", "origami_flower", "rain_village_attire",
#
#                 # Emotional states
#                 "serious_konan", "determined_konan", "calm_konan",
#                 "fighting_konan", "loyal_konan", "protective_konan"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "konan", "konan_(naruto)", "angel_(naruto)",
#
#                 # Abilities and forms
#                 "paper_techniques", "angel_form", "origami_style",
#
#                 # Affiliations
#                 "akatsuki", "amegakure", "pain's_partner",
#
#                 # Time periods
#                 "young_konan", "akatsuki_era", "leader_konan"
#             ]
#         },
#
#         "guren": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "guren", "guren_(naruto)", "crystal_style_user",
#                 "orochimaru's_subordinate", "crystal_mistress",
#
#                 # Special abilities and powers
#                 "crystal_release", "crystal_style", "crystal_armor",
#                 "crystal_mirrors", "crystal_prison", "crystal_blades",
#
#                 # Forms and states
#                 "crystal_form", "battle_mode", "crystal_armor_mode",
#                 "cursed_seal_form", "protective_mode",
#
#                 # Combat specialties
#                 "crystal_manipulation", "kekkei_genkai_user",
#                 "mid-range_fighter", "defensive_specialist",
#
#                 # Teams and affiliations
#                 "sound_village", "orochimaru's_forces", "yuukimaru's_guardian",
#
#                 # Time periods and versions
#                 "young_guren", "sound_ninja_guren", "reformed_guren",
#
#                 # Outfits and appearances
#                 "battle_outfit", "sound_uniform", "casual_guren",
#                 "crystal_enhanced_clothing",
#
#                 # Emotional states
#                 "proud_guren", "protective_guren", "fierce_guren",
#                 "caring_guren", "determined_guren"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "guren", "guren_(naruto)",
#
#                 # Powers and abilities
#                 "crystal_release", "crystal_style",
#
#                 # Affiliations
#                 "sound_village", "orochimaru's_subordinate",
#
#                 # States and forms
#                 "crystal_form", "battle_mode", "protective_mode"
#             ]
#         },
#
#         "kaguya": {
#             "gelbooru": [
#                 # Base names and identifiers
#                 "ootsutsuki_kaguya", "kaguya_ootsutsuki", "kaguya_(naruto)",
#                 "rabbit_goddess", "demon_goddess", "chakra_progenitor",
#
#                 # Titles and positions
#                 "rabbit_goddess", "mother_of_chakra", "progenitor_of_chakra",
#                 "ten_tails_jinchuuriki", "first_chakra_wielder",
#
#                 # Special abilities and powers
#                 "rinne_sharingan", "byakugan", "all_killing_ash_bones",
#                 "amenominaka", "yomotsu_hirasaka", "infinite_tsukuyomi",
#                 "chakra_absorption", "dimension_shifting", "truth-seeking_orbs",
#
#                 # Forms and states
#                 "goddess_form", "ten_tails_form", "rabbit_goddess_mode",
#                 "dimension_travel_mode", "sealed_form", "awakened_form",
#
#                 # Combat specialties
#                 "dimensional_manipulation", "chakra_control",
#                 "bone_manipulation", "gravity_manipulation",
#                 "space-time_techniques",
#
#                 # Family relationships
#                 "hagoromo's_mother", "hamura's_mother", "first_ancestor",
#                 "chakra_ancestor", "otsutsuki_clan_member",
#
#                 # Time periods and versions
#                 "human_kaguya", "goddess_kaguya", "sealed_kaguya",
#                 "resurrected_kaguya", "prime_kaguya",
#
#                 # Emotional states
#                 "wrathful_kaguya", "powerful_kaguya", "divine_kaguya",
#                 "maternal_kaguya", "betrayed_kaguya"
#             ],
#             "danbooru": [
#                 # Core identifiers
#                 "ootsutsuki_kaguya", "kaguya_(naruto)", "rabbit_goddess",
#
#                 # Powers and abilities
#                 "rinne_sharingan", "byakugan", "truth_seeking_orbs",
#
#                 # Forms and states
#                 "goddess_form", "ten_tails_form", "sealed_form",
#
#                 # Time periods
#                 "human_era", "goddess_era", "modern_revival"
#             ]
#         },
#     },
#
#     DRAGON_BALL_TAGS = {
#         # Main characters with expanded tags
#         "bulma": {
#             "names": [
#                 "bulma", "bulma_briefs", "briefs_bulma",
#                 "capsule_corp_heiress", "vegeta's_wife"
#             ],
#             "titles": [
#                 "capsule_corporation_president", "scientific_genius",
#                 "dragon_radar_inventor", "time_machine_creator",
#                 "z_fighter_support"
#             ],
#             "forms": [
#                 "young_bulma", "namek_saga_bulma",
#                 "android_saga_bulma", "future_bulma",
#                 "super_bulma", "gt_bulma"
#             ],
#             "affiliations": [
#                 "capsule_corporation", "z_fighters",
#                 "brief_family", "dragon_ball_gang",
#                 "universe_7_support"
#             ],
#             "relationships": [
#                 "vegeta's_wife", "trunks_mother",
#                 "bulla's_mother", "dr_brief's_daughter",
#                 "goku's_first_friend"
#             ],
#             "abilities": [
#                 "genius_intellect", "scientific_expertise",
#                 "mechanical_engineering", "invention_creation",
#                 "dragon_radar_operation", "vehicle_piloting"
#             ],
#             "time_periods": [
#                 "dragon_ball", "dragon_ball_z",
#                 "dragon_ball_super", "dragon_ball_gt",
#                 "future_timeline"
#             ],
#             "outfits": [
#                 "capsule_corp_outfit", "bunny_costume",
#                 "namek_armor", "battle_suit",
#                 "formal_dress", "lab_coat"
#             ]
#         },
#
#         "android_18": {
#             "names": [
#                 "android_18", "lazuli", "cyborg_18",
#                 "c-18", "human_android"
#             ],
#             "titles": [
#                 "red_ribbon_android", "infinite_energy_model",
#                 "krillin's_wife", "marron's_mother",
#                 "tournament_fighter"
#             ],
#             "forms": [
#                 "cyborg_form", "human_form", "suppressed_power",
#                 "full_power", "tournament_mode",
#                 "controlled_by_cell"
#             ],
#             "affiliations": [
#                 "z_fighters", "red_ribbon_army_(former)",
#                 "universe_7_team", "earth's_defenders",
#                 "krillin_family"
#             ],
#             "abilities": [
#                 "infinite_energy", "energy_absorption",
#                 "superhuman_strength", "flight",
#                 "energy_attacks", "barrier_generation"
#             ],
#             "relationships": [
#                 "android_17's_twin", "krillin's_wife",
#                 "marron's_mother", "dr_gero's_creation",
#                 "z_fighter_ally"
#             ],
#             "time_periods": [
#                 "android_saga", "cell_saga",
#                 "majin_buu_saga", "super_era",
#                 "tournament_of_power"
#             ],
#             "outfits": [
#                 "original_outfit", "casual_clothes",
#                 "ranger_uniform", "tournament_gi",
#                 "winter_clothing"
#             ]
#         },
#
#         "chi_chi": {
#             "names": [
#                 "chi-chi", "son_chi-chi", "ox_princess",
#                 "goku's_wife", "fire_mountain_princess"
#             ],
#             "titles": [
#                 "ox_king's_daughter", "martial_artist",
#                 "son_family_matriarch", "strongest_human_woman",
#                 "fire_mountain_princess"
#             ],
#             "forms": [
#                 "young_chi-chi", "tournament_fighter",
#                 "married_chi-chi", "mother_chi-chi",
#                 "grandmother_chi-chi"
#             ],
#             "affiliations": [
#                 "son_family", "z_fighters_family",
#                 "fire_mountain_kingdom", "earth's_defenders",
#                 "martial_artists"
#             ],
#             "abilities": [
#                 "martial_arts", "superhuman_strength",
#                 "ki_manipulation", "flying_nimbus_riding",
#                 "household_mastery"
#             ],
#             "relationships": [
#                 "goku's_wife", "gohan's_mother",
#                 "goten's_mother", "ox_king's_daughter",
#                 "videl's_mother-in-law"
#             ],
#             "time_periods": [
#                 "dragon_ball", "saiyan_saga",
#                 "cell_saga", "buu_saga",
#                 "super_era"
#             ],
#             "outfits": [
#                 "battle_armor", "tournament_outfit",
#                 "casual_clothes", "housewife_attire",
#                 "chinese_dress"
#             ]
#         },
#
#         "caulifla": {
#             "names": [
#                 "caulifla", "saiyan_universe_6",
#                 "kefla_fusion_component", "super_saiyan_prodigy"
#             ],
#             "titles": [
#                 "universe_6_saiyan", "saiyan_gang_leader",
#                 "super_saiyan_prodigy", "kefla_fusion_half",
#                 "tournament_warrior"
#             ],
#             "forms": [
#                 "base_form", "super_saiyan",
#                 "super_saiyan_2", "kefla_fusion",
#                 "controlled_berserker"
#             ],
#             "affiliations": [
#                 "universe_6", "team_universe_6",
#                 "saiyan_gang", "tournament_of_power_team",
#                 "sadala_defense_force"
#             ],
#             "abilities": [
#                 "super_saiyan_transformation", "ki_manipulation",
#                 "rapid_power_growth", "energy_attacks",
#                 "fusion_capability"
#             ],
#             "relationships": [
#                 "kale's_mentor", "champa's_warrior",
#                 "universe_6_fighter", "cabba's_rival",
#                 "kefla_fusion_component"
#             ],
#             "time_periods": [
#                 "universe_6_saga", "tournament_of_power",
#                 "super_era", "universe_survival"
#             ],
#             "outfits": [
#                 "universe_6_outfit", "training_clothes",
#                 "battle_suit", "casual_wear",
#                 "saiyan_armor"
#             ]
#         },
#
#         "kale": {
#             "names": [
#                 "kale", "universe_6_broly",
#                 "legendary_super_saiyan_u6",
#                 "berserker_saiyan"
#             ],
#             "titles": [
#                 "legendary_super_saiyan",
#                 "universe_6_berserker",
#                 "caulifla's_protege",
#                 "kefla_fusion_component"
#             ],
#             "forms": [
#                 "base_form", "super_saiyan",
#                 "legendary_super_saiyan",
#                 "controlled_berserker",
#                 "mastered_berserker"
#             ],
#             "affiliations": [
#                 "universe_6", "team_universe_6",
#                 "caulifla's_gang", "tournament_of_power_team",
#                 "sadala_defense_force"
#             ],
#             "abilities": [
#                 "legendary_transformation",
#                 "unlimited_power_growth",
#                 "ki_manipulation",
#                 "energy_attacks",
#                 "fusion_capability"
#             ],
#             "relationships": [
#                 "caulifla's_protege",
#                 "champa's_warrior",
#                 "universe_6_fighter",
#                 "kefla_fusion_component"
#             ],
#             "time_periods": [
#                 "universe_6_saga",
#                 "tournament_of_power",
#                 "super_era",
#                 "universe_survival"
#             ],
#             "outfits": [
#                 "universe_6_outfit",
#                 "training_clothes",
#                 "battle_suit",
#                 "casual_wear"
#             ]
#         },
#
#         "android_21": {
#             "names": [
#                 "android_21", "a21", "majin_21",
#                 "lab_coat_21", "good_21", "evil_21"
#             ],
#             "titles": [
#                 "red_ribbon_scientist", "perfect_android",
#                 "majin_hybrid", "cell_replica_creator",
#                 "artificial_life_form"
#             ],
#             "forms": [
#                 "human_form", "majin_form", "true_form",
#                 "evil_form", "good_form", "lab_coat_form",
#                 "transformed_state", "cell_absorbed_form"
#             ],
#             "affiliations": [
#                 "red_ribbon_army", "red_ribbon_scientists",
#                 "android_line", "cell's_derivatives",
#                 "majin_species"
#             ],
#             "abilities": [
#                 "power_absorption", "cellular_manipulation",
#                 "regeneration", "transformation",
#                 "energy_manipulation", "candy_beam",
#                 "intelligence", "scientific_knowledge"
#             ],
#             "relationships": [
#                 "dr_gero's_colleague", "cell's_template",
#                 "android_16_creator", "majin_buu_cells",
#                 "cell_dna_carrier"
#             ],
#             "time_periods": [
#                 "fighters_era", "red_ribbon_era",
#                 "alternate_timeline", "game_timeline"
#             ],
#             "outfits": [
#                 "lab_coat", "scientist_outfit",
#                 "majin_form_attire", "battle_suit",
#                 "transformed_outfit"
#             ]
#         },
#
#         "cheelai": {
#             "names": [
#                 "cheelai", "broly's_friend",
#                 "frieza_force_deserter", "vampire_survivor"
#             ],
#             "titles": [
#                 "frieza_force_scout", "broly's_companion",
#                 "dragon_ball_wisher", "vampire_deserter"
#             ],
#             "forms": [
#                 "frieza_force_uniform", "casual_outfit",
#                 "combat_ready", "planet_vampa_survivor"
#             ],
#             "affiliations": [
#                 "frieza_force_(former)", "broly's_group",
#                 "planet_vampa_residents", "earth_allies"
#             ],
#             "abilities": [
#                 "combat_training", "scouter_operation",
#                 "piloting_skills", "survival_skills",
#                 "quick_thinking"
#             ],
#             "relationships": [
#                 "broly's_friend", "lemo's_partner",
#                 "paragus_ally", "frieza_force_deserter",
#                 "goku_ally"
#             ],
#             "time_periods": [
#                 "broly_movie", "frieza_force_era",
#                 "planet_vampa_period", "super_era"
#             ],
#             "outfits": [
#                 "frieza_force_armor", "casual_clothes",
#                 "vampa_gear", "earth_clothing"
#             ]
#         },
#
#         "towa": {
#             "names": [
#                 "towa", "demon_scientist",
#                 "dabura's_sister", "time_breaker",
#                 "demon_realm_scientist"
#             ],
#             "titles": [
#                 "demon_realm_scientist", "time_breaker_leader",
#                 "dark_demon_realm_elite", "dabura's_sister"
#             ],
#             "forms": [
#                 "base_form", "scientist_mode",
#                 "demon_goddess_form", "darkness_form",
#                 "corrupted_form"
#             ],
#             "affiliations": [
#                 "demon_realm", "time_breakers",
#                 "dark_demon_realm", "demon_scientists"
#             ],
#             "abilities": [
#                 "time_manipulation", "dark_magic",
#                 "scientific_genius", "energy_manipulation",
#                 "mind_control", "demon_powers"
#             ],
#             "relationships": [
#                 "dabura's_sister", "mira's_creator",
#                 "demon_realm_royal", "fu's_mother",
#                 "time_patrol_enemy"
#             ],
#             "time_periods": [
#                 "xenoverse_era", "time_breach_period",
#                 "demon_realm_era", "dark_king_era"
#             ],
#             "outfits": [
#                 "demon_scientist_outfit", "battle_suit",
#                 "dark_queen_attire", "research_gear"
#             ]
#         },
#
#         "chronoa": {
#             "names": [
#                 "supreme_kai_of_time", "chronoa",
#                 "time_patrol_founder", "time_keeper"
#             ],
#             "titles": [
#                 "supreme_kai_of_time", "time_patrol_leader",
#                 "tokitoki_city_founder", "time_nest_guardian"
#             ],
#             "forms": [
#                 "kai_form", "powered_up_form",
#                 "time_power_unleashed", "supreme_kai_state"
#             ],
#             "affiliations": [
#                 "time_patrol", "supreme_kai_realm",
#                 "time_nest", "tokitoki_city"
#             ],
#             "abilities": [
#                 "time_manipulation", "kai_powers",
#                 "timeline_management", "history_correction",
#                 "supreme_kai_magic"
#             ],
#             "relationships": [
#                 "tokitoki's_partner", "time_patroller_leader",
#                 "trunks_mentor", "elder_kai_colleague"
#             ],
#             "time_periods": [
#                 "xenoverse_era", "time_patrol_founding",
#                 "demon_realm_crisis", "time_breaker_war"
#             ],
#             "outfits": [
#                 "supreme_kai_robes", "time_patrol_uniform",
#                 "casual_attire", "ceremonial_dress"
#             ]
#         },
#
#         "videl": {
#             "names": [
#                 "videl", "videl_satan", "great_saiyawoman",
#                 "pan's_mother", "gohan's_wife"
#             ],
#             "titles": [
#                 "great_saiyawoman", "satan_city_defender",
#                 "martial_arts_champion", "mr_satan's_daughter",
#                 "crime_fighter"
#             ],
#             "forms": [
#                 "base_form", "great_saiyawoman",
#                 "fighting_form", "mother_form",
#                 "teen_videl", "adult_videl"
#             ],
#             "affiliations": [
#                 "z_fighters_family", "satan_city_police",
#                 "orange_star_high", "world_tournament",
#                 "son_family"
#             ],
#             "abilities": [
#                 "martial_arts", "ki_control",
#                 "flight", "superhuman_strength",
#                 "crime_fighting_skills"
#             ],
#             "time_periods": [
#                 "great_saiyaman_saga", "majin_buu_saga",
#                 "super_era", "gt_timeline"
#             ],
#             "outfits": [
#                 "great_saiyawoman_costume", "school_uniform",
#                 "fighting_gi", "casual_clothes",
#                 "training_outfit"
#             ]
#         },
#
#         "launch": {
#             "names": [
#                 "launch", "lunchi", "blonde_launch",
#                 "blue_launch", "split_personality"
#             ],
#             "titles": [
#                 "personality_switcher", "kame_house_resident",
#                 "tien's_admirer", "reformed_criminal"
#             ],
#             "forms": [
#                 "good_form_(blue)", "bad_form_(blonde)",
#                 "sneeze_transformation", "normal_state"
#             ],
#             "affiliations": [
#                 "kame_house", "z_fighters_support",
#                 "tien_group", "dragon_ball_gang"
#             ],
#             "abilities": [
#                 "personality_switch", "weapons_expertise",
#                 "driving_skills", "combat_abilities",
#                 "cooking_skills"
#             ],
#             "time_periods": [
#                 "dragon_ball", "early_z",
#                 "piccolo_jr_saga", "saiyan_saga"
#             ],
#             "outfits": [
#                 "casual_dress", "combat_gear",
#                 "housekeeping_clothes", "biker_outfit"
#             ]
#         },
#
#         "marron": {
#             "names": [
#                 "marron", "krillin's_daughter",
#                 "android_18's_daughter"
#             ],
#             "titles": [
#                 "z_fighter_child", "kame_house_resident",
#                 "human_android_hybrid"
#             ],
#             "forms": [
#                 "child_form", "teen_form",
#                 "gt_timeline_form"
#             ],
#             "affiliations": [
#                 "z_fighters_family", "kame_house",
#                 "earth's_defenders_family"
#             ],
#             "abilities": [
#                 "potential_fighter", "human_strength",
#                 "possible_android_traits"
#             ],
#             "time_periods": [
#                 "majin_buu_saga", "super_era",
#                 "peaceful_era", "gt_timeline"
#             ],
#             "outfits": [
#                 "casual_clothes", "kame_house_attire",
#                 "party_dress", "beach_wear"
#             ]
#         },
#
#         "pan": {
#             "names": [
#                 "pan", "son_pan", "quarter_saiyan",
#                 "gt_pan", "super_pan"
#             ],
#             "titles": [
#                 "quarter_saiyan", "world_tournament_junior",
#                 "space_explorer", "satan_city_defender"
#             ],
#             "forms": [
#                 "base_form", "angry_form",
#                 "potential_unleashed", "gt_form",
#                 "baby_pan"
#             ],
#             "affiliations": [
#                 "son_family", "z_fighters",
#                 "satan_city_school", "world_tournament"
#             ],
#             "abilities": [
#                 "flight", "ki_blast",
#                 "martial_arts", "saiyan_power",
#                 "superhuman_strength"
#             ],
#             "time_periods": [
#                 "end_of_z", "gt_era",
#                 "super_era", "peaceful_timeline"
#             ],
#             "outfits": [
#                 "gi_outfit", "casual_clothes",
#                 "school_uniform", "gt_adventure_gear"
#             ]
#         },
#
#         "bulla": {
#             "names": [
#                 "bulla", "bra", "vegeta's_daughter",
#                 "bulma's_daughter", "saiyan_princess"
#             ],
#             "titles": [
#                 "saiyan_princess", "capsule_corp_heiress",
#                 "half_saiyan", "royal_bloodline"
#             ],
#             "forms": [
#                 "base_form", "teen_form",
#                 "gt_form", "super_form"
#             ],
#             "affiliations": [
#                 "brief_family", "saiyan_royalty",
#                 "capsule_corporation", "z_fighters_family"
#             ],
#             "abilities": [
#                 "potential_saiyan_power", "intelligence",
#                 "capsule_corp_technology", "fashion_sense"
#             ],
#             "time_periods": [
#                 "end_of_z", "gt_era",
#                 "super_era", "peaceful_timeline"
#             ],
#             "outfits": [
#                 "casual_fashion", "capsule_corp_style",
#                 "gt_outfit", "shopping_attire"
#             ]
#         },
#
#         "vados": {
#             "names": [
#                 "vados", "universe_6_angel",
#                 "champa's_attendant", "whis's_sister"
#             ],
#             "titles": [
#                 "angel_attendant", "universe_6_guide",
#                 "champa's_teacher", "angel_sister"
#             ],
#             "forms": [
#                 "angel_form", "powered_state",
#                 "training_mode", "staff_wielding"
#             ],
#             "affiliations": [
#                 "universe_6", "angels",
#                 "champa's_staff", "grand_priest_family"
#             ],
#             "abilities": [
#                 "angel_powers", "time_rewind",
#                 "ultra_instinct", "staff_manipulation",
#                 "universe_travel"
#             ],
#             "time_periods": [
#                 "universe_6_saga", "tournament_of_power",
#                 "super_era", "god_of_destruction_era"
#             ],
#             "outfits": [
#                 "angel_robes", "universe_6_attire",
#                 "training_gear", "formal_angel_dress"
#             ]
#         },
#
#
#     },
#
#     ATTACK_ON_TITAN_TAGS = {
#         # Main characters with expanded tags
#         "mikasa": {
#             "names": [
#                 "mikasa_ackerman", "mikasa", "scarf_girl",
#                 "ackerman_prodigy", "humanity's_strongest_woman"
#             ],
#             "titles": [
#                 "104th_cadet", "survey_corps_elite",
#                 "captain_rank", "special_operations_squad",
#                 "hizuru_heir"
#             ],
#             "forms": [
#                 "cadet_mikasa", "veteran_mikasa",
#                 "post_timeskip_mikasa", "battle_mode",
#                 "ackerman_power_active"
#             ],
#             "affiliations": [
#                 "survey_corps", "104th_training_corps",
#                 "special_operations_squad", "alliance_member",
#                 "paradise_military"
#             ],
#             "relationships": [
#                 "eren's_adoptive_sister", "armin's_friend",
#                 "levi's_subordinate", "ackerman_clan",
#                 "azumabito_clan"
#             ],
#             "abilities": [
#                 "ackerman_power", "3dmg_mastery",
#                 "combat_prodigy", "superhuman_strength",
#                 "battle_instincts", "swordsmanship"
#             ],
#             "time_periods": [
#                 "trainee_era", "trost_arc", "clash_of_titans",
#                 "uprising_arc", "return_to_shiganshina",
#                 "marley_arc", "rumbling_arc"
#             ],
#             "outfits": [
#                 "cadet_uniform", "survey_corps_uniform",
#                 "casual_clothes", "battle_gear",
#                 "anti_personnel_gear", "hizuru_robes"
#             ]
#         },
#
#         "annie": {
#             "names": [
#                 "annie_leonhart", "female_titan",
#                 "annie_leonhardt", "warrior_annie",
#                 "crystal_maiden"
#             ],
#             "titles": [
#                 "warrior_unit", "female_titan_shifter",
#                 "104th_graduate", "military_police_member",
#                 "marley_warrior"
#             ],
#             "forms": [
#                 "female_titan_form", "human_form",
#                 "crystallized_form", "partial_transformation",
#                 "hardened_form", "combat_stance"
#             ],
#             "affiliations": [
#                 "marley_military", "warrior_unit",
#                 "104th_training_corps", "military_police",
#                 "paradise_alliance"
#             ],
#             "abilities": [
#                 "titan_shifting", "crystallization",
#                 "martial_arts", "hardening_ability",
#                 "scream_ability", "calling_titans"
#             ],
#             "relationships": [
#                 "warrior_candidate", "mr_leonhart's_daughter",
#                 "armin's_interest", "bertholdt's_comrade",
#                 "reiner's_teammate"
#             ],
#             "time_periods": [
#                 "warrior_training", "cadet_days",
#                 "military_police_era", "crystal_stasis",
#                 "rumbling_arc"
#             ],
#             "outfits": [
#                 "trainee_uniform", "military_police_uniform",
#                 "warrior_gear", "casual_clothes",
#                 "combat_suit"
#             ]
#         },
#
#         "historia": {
#             "names": [
#                 "historia_reiss", "christa_lenz",
#                 "queen_historia", "goddess_krista",
#                 "true_heir"
#             ],
#             "titles": [
#                 "queen_of_the_walls", "true_royal",
#                 "104th_cadet", "survey_corps_member",
#                 "reiss_heir"
#             ],
#             "forms": [
#                 "christa_persona", "true_historia",
#                 "queen_form", "battle_ready",
#                 "royal_blood_activated"
#             ],
#             "affiliations": [
#                 "survey_corps", "royal_government",
#                 "104th_training_corps", "reiss_family",
#                 "paradise_military"
#             ],
#             "relationships": [
#                 "ymir's_friend", "rod_reiss_daughter",
#                 "frieda's_sister", "eren's_key_ally",
#                 "farmer's_partner"
#             ],
#             "abilities": [
#                 "royal_blood_power", "3dmg_skill",
#                 "leadership_ability", "combat_training",
#                 "royal_authority"
#             ],
#             "time_periods": [
#                 "cadet_era", "uprising_arc",
#                 "coronation_period", "pregnancy_arc",
#                 "rumbling_era"
#             ],
#             "outfits": [
#                 "trainee_uniform", "survey_corps_uniform",
#                 "queen_attire", "casual_clothes",
#                 "royal_dress", "farm_clothes"
#             ]
#         },
#
#         "pieck": {
#             "names": [
#                 "pieck_finger", "pieck", "cart_titan",
#                 "panzer_unit_commander", "warrior_pieck"
#             ],
#             "titles": [
#                 "cart_titan_shifter", "warrior_unit_member",
#                 "marley_elite", "quadrupedal_titan",
#                 "intelligent_titan"
#             ],
#             "forms": [
#                 "cart_titan_form", "human_form",
#                 "armored_cart_form", "combat_mode",
#                 "quadrupedal_mode", "artillery_platform"
#             ],
#             "affiliations": [
#                 "marley_military", "warrior_unit",
#                 "panzer_unit", "titan_research",
#                 "paradise_alliance"
#             ],
#             "abilities": [
#                 "titan_shifting", "extended_transformation",
#                 "strategic_thinking", "endurance_capability",
#                 "equipment_compatibility", "adaptive_combat"
#             ],
#             "relationships": [
#                 "warrior_commander", "zeke's_subordinate",
#                 "porco's_comrade", "panzer_unit_leader",
#                 "marley_loyalist"
#             ],
#             "time_periods": [
#                 "warrior_training", "marley_arc",
#                 "liberio_raid", "paradise_invasion",
#                 "rumbling_arc"
#             ],
#             "outfits": [
#                 "warrior_uniform", "military_gear",
#                 "casual_clothes", "hospital_gown",
#                 "infiltration_outfit"
#             ]
#         },
#
#         "gabi": {
#             "names": [
#                 "gabi_braun", "warrior_candidate",
#                 "armored_titan_candidate", "marley_prodigy"
#             ],
#             "titles": [
#                 "top_warrior_candidate", "reiner's_cousin",
#                 "marley_elite_trainee", "armored_heir"
#             ],
#             "forms": [
#                 "warrior_cadet", "infiltrator_mode",
#                 "combat_ready", "sniper_form",
#                 "prison_escapee"
#             ],
#             "affiliations": [
#                 "marley_military", "warrior_unit_cadets",
#                 "braun_family", "liberio_internment",
#                 "paradise_allies"
#             ],
#             "abilities": [
#                 "marksmanship", "combat_training",
#                 "tactical_thinking", "athletic_prowess",
#                 "leadership_potential"
#             ],
#             "relationships": [
#                 "reiner's_cousin", "falco's_rival",
#                 "colt's_student", "kaya's_friend",
#                 "warrior_family"
#             ],
#             "time_periods": [
#                 "warrior_training", "liberio_arc",
#                 "paradise_infiltration", "rumbling_arc",
#                 "alliance_era"
#             ],
#             "outfits": [
#                 "warrior_cadet_uniform", "civilian_disguise",
#                 "combat_gear", "paradise_clothes",
#                 "alliance_attire"
#             ]
#         },
#
#         "hitch": {
#             "names": [
#                 "hitch_dreyse", "military_police_officer",
#                 "stohess_district_guard", "annie's_roommate"
#             ],
#             "titles": [
#                 "military_police_member", "interior_guard",
#                 "stohess_supervisor", "cadet_graduate"
#             ],
#             "forms": [
#                 "police_officer", "guard_duty",
#                 "casual_mode", "investigation_mode"
#             ],
#             "affiliations": [
#                 "military_police_brigade", "interior_forces",
#                 "stohess_district", "104th_graduates"
#             ],
#             "abilities": [
#                 "police_duties", "investigation_skills",
#                 "3dmg_proficiency", "combat_training",
#                 "leadership_capability"
#             ],
#             "relationships": [
#                 "annie's_former_roommate", "marlowe's_friend",
#                 "police_brigade_member", "paradise_defender"
#             ],
#             "time_periods": [
#                 "cadet_corps", "military_police_era",
#                 "uprising_arc", "timeskip_period",
#                 "rumbling_arc"
#             ],
#             "outfits": [
#                 "military_police_uniform", "casual_clothes",
#                 "guard_outfit", "investigation_gear"
#             ]
#         },
#
#         "traute": {
#             "names": [
#                 "traute_caven", "anti_personnel_leader",
#                 "interior_squad_captain", "kenny_squad"
#             ],
#             "titles": [
#                 "anti_personnel_commander", "interior_police",
#                 "elite_squad_member", "kenny's_subordinate"
#             ],
#             "forms": [
#                 "combat_mode", "squad_leader",
#                 "anti_personnel_gear", "pursuit_form"
#             ],
#             "affiliations": [
#                 "interior_military_police", "anti_personnel_squad",
#                 "kenny's_squad", "central_government"
#             ],
#             "abilities": [
#                 "anti_personnel_3dmg", "leadership_skills",
#                 "combat_expertise", "tactical_planning",
#                 "marksmanship"
#             ],
#             "relationships": [
#                 "kenny's_second", "squad_commander",
#                 "interior_police_elite", "government_loyalist"
#             ],
#             "time_periods": [
#                 "pre_uprising", "uprising_arc",
#                 "kenny_squad_era", "government_control"
#             ],
#             "outfits": [
#                 "anti_personnel_uniform", "combat_gear",
#                 "interior_police_attire", "mission_outfit"
#             ]
#         }
#     }
#
#     DEMON_SLAYER_TAGS = {
#         # Hashira and main characters
#         "shinobu": {
#             "names": [
#                 "kochou_shinobu", "shinobu_kocho",
#                 "insect_hashira", "butterfly_mansion_master",
#                 "poison_hashira"
#             ],
#             "titles": [
#                 "insect_hashira", "butterfly_mansion_leader",
#                 "poison_master", "wisteria_poison_expert",
#                 "demon_slayer_corps_pillar"
#             ],
#             "forms": [
#                 "hashira_form", "butterfly_dance_stance",
#                 "poison_combat_mode", "medical_form",
#                 "training_mode", "final_battle_form"
#             ],
#             "affiliations": [
#                 "demon_slayer_corps", "hashira",
#                 "butterfly_mansion", "medical_corps",
#                 "kochou_family"
#             ],
#             "abilities": [
#                 "insect_breathing", "poison_mastery",
#                 "medical_expertise", "butterfly_dance_technique",
#                 "enhanced_speed", "poison_mixing"
#             ],
#             "relationships": [
#                 "kanae's_sister", "kanao's_mentor",
#                 "butterfly_mansion_leader", "giyu's_colleague",
#                 "douma's_nemesis"
#             ],
#             "weapons": [
#                 "nichirin_sword", "wisteria_poison",
#                 "modified_sword", "poison_compounds",
#                 "medical_tools"
#             ],
#             "outfits": [
#                 "demon_slayer_uniform", "hashira_haori",
#                 "butterfly_pattern", "medical_attire",
#                 "training_clothes"
#             ]
#         },
#
#         "kanao": {
#             "names": [
#                 "tsuyuri_kanao", "kanao_tsuyuri",
#                 "butterfly_student", "flower_breathing_user",
#                 "shinobu's_successor"
#             ],
#             "titles": [
#                 "tsuguko", "flower_breathing_master",
#                 "butterfly_estate_warrior", "demon_hunter",
#                 "enhanced_vision_user"
#             ],
#             "forms": [
#                 "combat_form", "enhanced_vision_state",
#                 "flower_breathing_stance", "training_mode",
#                 "final_selection_form"
#             ],
#             "affiliations": [
#                 "demon_slayer_corps", "butterfly_mansion",
#                 "kochou_family_(adopted)", "tsuguko",
#                 "final_selection_survivors"
#             ],
#             "abilities": [
#                 "flower_breathing", "enhanced_eyesight",
#                 "superhuman_reflexes", "coin_toss_decision",
#                 "butterfly_dance_techniques"
#             ],
#             "relationships": [
#                 "shinobu's_student", "kanae's_student",
#                 "tanjiro's_love_interest", "butterfly_mansion_resident",
#                 "aoi's_friend"
#             ],
#             "weapons": [
#                 "nichirin_sword", "flower_breathing_blade",
#                 "decision_coin", "training_weapons"
#             ],
#             "outfits": [
#                 "demon_slayer_uniform", "butterfly_estate_clothing",
#                 "training_attire", "casual_wear",
#                 "final_battle_gear"
#             ]
#         },
#
#         "mitsuri": {
#             "names": [
#                 "kanroji_mitsuri", "mitsuri_kanroji",
#                 "love_hashira", "love_pillar",
#                 "pink_hashira"
#             ],
#             "titles": [
#                 "love_hashira", "serpentine_warrior",
#                 "demon_slayer_corps_pillar", "love_breathing_creator",
#                 "unique_muscle_composition_user"
#             ],
#             "forms": [
#                 "hashira_form", "love_breathing_stance",
#                 "serpentine_movement", "combat_mode",
#                 "awakened_form"
#             ],
#             "affiliations": [
#                 "demon_slayer_corps", "hashira",
#                 "love_hashira_lineage", "final_battle_corps",
#                 "obanai's_lover"
#             ],
#             "abilities": [
#                 "love_breathing", "superhuman_flexibility",
#                 "unique_muscle_structure", "enhanced_strength",
#                 "whip-like_techniques"
#             ],
#             "relationships": [
#                 "obanai's_love_interest", "hashira_member",
#                 "shinobu's_friend", "iguro's_partner",
#                 "demon_slayer_corps_pillar"
#             ],
#             "weapons": [
#                 "nichirin_sword", "whip-like_blade",
#                 "flexible_weapon", "love_breathing_tools"
#             ],
#             "outfits": [
#                 "demon_slayer_uniform", "hashira_haori",
#                 "modified_uniform", "love_pattern",
#                 "battle_attire"
#             ]
#         },
#
#         "daki": {
#             "names": [
#                 "daki", "ume", "sixth_upper_moon",
#                 "oiran_demon", "entertainment_district_demon"
#             ],
#             "titles": [
#                 "upper_six", "courtesan_demon",
#                 "entertainment_district_terror",
#                 "sixth_upper_rank", "oiran_killer"
#             ],
#             "forms": [
#                 "demon_form", "oiran_form",
#                 "combined_form_(with_gyutaro)",
#                 "enraged_form", "belt_demon_form"
#             ],
#             "affiliations": [
#                 "twelve_kizuki", "upper_moons",
#                 "entertainment_district", "demon_organization",
#                 "muzan's_demons"
#             ],
#             "abilities": [
#                 "sash_manipulation", "body_modification",
#                 "regeneration", "demon_art",
#                 "flesh_belt_creation"
#             ],
#             "relationships": [
#                 "gyutaro's_sister", "muzan's_demon",
#                 "upper_moon_member", "uzui's_enemy",
#                 "demon_hierarchy"
#             ],
#             "time_periods": [
#                 "human_life", "demon_transformation",
#                 "entertainment_district_arc", "upper_moon_era"
#             ],
#             "outfits": [
#                 "oiran_kimono", "demon_form_attire",
#                 "battle_outfit", "entertainment_district_clothes",
#                 "ceremonial_garments"
#             ]
#         },
#
#         "nakime": {
#             "names": [
#                 "nakime", "biwa_demon",
#                 "fortress_creator", "dimensional_demon"
#             ],
#             "titles": [
#                 "infinity_castle_master", "biwa_player",
#                 "fortress_demon", "upper_rank",
#                 "dimensional_controller"
#             ],
#             "forms": [
#                 "demon_form", "biwa_playing_form",
#                 "castle_control_mode", "combat_form"
#             ],
#             "affiliations": [
#                 "twelve_kizuki", "upper_moons",
#                 "infinity_castle", "muzan's_demons"
#             ],
#             "abilities": [
#                 "fortress_control", "dimensional_manipulation",
#                 "biwa_techniques", "castle_creation",
#                 "space_distortion"
#             ],
#             "relationships": [
#                 "muzan's_servant", "upper_moon_member",
#                 "infinity_castle_guardian", "demon_organization"
#             ],
#             "weapons": [
#                 "biwa", "demon_arts",
#                 "fortress_manipulation", "dimensional_powers"
#             ],
#             "outfits": [
#                 "demon_form_clothing", "traditional_wear",
#                 "musician_attire", "battle_gear"
#             ]
#         },
#
#         "nezuko": {
#             "names": [
#                 "kamado_nezuko", "nezuko",
#                 "demon_nezuko", "bamboo_girl",
#                 "tanjiro's_sister"
#             ],
#             "titles": [
#                 "special_demon", "sunlight_resistant",
#                 "blood_demon_art_user", "kamado_survivor"
#             ],
#             "forms": [
#                 "demon_form", "berserk_form",
#                 "awakened_form", "controlled_demon",
#                 "adult_form", "human_form"
#             ],
#             "affiliations": [
#                 "kamado_family", "demon_kind",
#                 "tanjiro's_group", "urokodaki's_care"
#             ],
#             "abilities": [
#                 "blood_demon_art", "flame_generation",
#                 "size_manipulation", "regeneration",
#                 "supernatural_strength"
#             ],
#             "relationships": [
#                 "tanjiro's_sister", "urokodaki's_ward",
#                 "zenitsu's_love_interest", "giyu's_exception",
#                 "tamayo's_patient"
#             ],
#             "time_periods": [
#                 "human_life", "demon_transformation",
#                 "recovery_period", "final_battle"
#             ],
#             "outfits": [
#                 "pink_kimono", "bamboo_muzzle",
#                 "battle_torn_clothes", "human_clothes",
#                 "casual_wear"
#             ]
#         },
#
#         "tamayo": {
#             "names": [
#                 "tamayo", "doctor_tamayo",
#                 "medicine_maker", "rebel_demon"
#             ],
#             "titles": [
#                 "demon_doctor", "medicine_creator",
#                 "muzan's_betrayer", "cure_researcher"
#             ],
#             "forms": [
#                 "demon_form", "doctor_form",
#                 "combat_form", "disguised_form"
#             ],
#             "affiliations": [
#                 "independent_demon", "medical_research",
#                 "demon_resistance", "yushiro's_mentor"
#             ],
#             "abilities": [
#                 "blood_manipulation", "medicine_creation",
#                 "memory_manipulation", "healing_arts",
#                 "demon_techniques"
#             ],
#             "relationships": [
#                 "yushiro's_savior", "muzan's_enemy",
#                 "tanjiro's_ally", "nezuko's_doctor"
#             ],
#             "time_periods": [
#                 "muzan_era", "independent_period",
#                 "research_years", "final_battle"
#             ],
#             "outfits": [
#                 "doctor_kimono", "disguise_clothes",
#                 "battle_attire", "formal_wear"
#             ]
#         },
#
#         "kanae": {
#             "names": [
#                 "kochou_kanae", "kanae_kocho",
#                 "former_flower_hashira", "shinobu's_sister"
#             ],
#             "titles": [
#                 "flower_hashira", "butterfly_mansion_master",
#                 "demon_slayer_corps_pillar", "flower_breathing_user"
#             ],
#             "forms": [
#                 "hashira_form", "flower_breathing_stance",
#                 "combat_mode", "final_battle_form"
#             ],
#             "affiliations": [
#                 "demon_slayer_corps", "hashira",
#                 "butterfly_mansion", "kochou_family"
#             ],
#             "abilities": [
#                 "flower_breathing", "enhanced_speed",
#                 "superior_swordsmanship", "hashira_level_combat"
#             ],
#             "relationships": [
#                 "shinobu's_sister", "kanao's_adoptive_mother",
#                 "butterfly_mansion_leader", "douma's_victim"
#             ],
#             "weapons": [
#                 "nichirin_sword", "flower_breathing_blade",
#                 "hashira_equipment"
#             ],
#             "outfits": [
#                 "demon_slayer_uniform", "hashira_haori",
#                 "butterfly_pattern", "casual_wear"
#             ]
#         },
#
#         "aoi": {
#             "names": [
#                 "aoi_kanzaki", "kanzaki_aoi",
#                 "butterfly_mansion_nurse", "medical_corps"
#             ],
#             "titles": [
#                 "medical_corps_member", "support_staff",
#                 "butterfly_mansion_assistant", "healing_expert"
#             ],
#             "forms": [
#                 "nurse_form", "training_mode",
#                 "medical_stance", "support_role"
#             ],
#             "affiliations": [
#                 "demon_slayer_corps", "butterfly_mansion",
#                 "medical_support", "training_staff"
#             ],
#             "abilities": [
#                 "medical_knowledge", "herb_expertise",
#                 "physical_rehabilitation", "training_instruction"
#             ],
#             "relationships": [
#                 "shinobu's_assistant", "kanao's_friend",
#                 "butterfly_mansion_staff", "inosuke's_trainer"
#             ],
#             "activities": [
#                 "medical_treatment", "rehabilitation_support",
#                 "demon_slayer_training", "herb_preparation"
#             ],
#             "outfits": [
#                 "butterfly_mansion_uniform", "medical_attire",
#                 "training_clothes", "casual_wear"
#             ]
#         },
#
#         "hinatsuru": {
#             "names": [
#                 "hinatsuru", "uzui's_wife",
#                 "shinobi_wife", "kunoichi"
#             ],
#             "titles": [
#                 "sound_hashira's_wife", "ninja_wife",
#                 "entertainment_district_infiltrator", "kunoichi"
#             ],
#             "forms": [
#                 "ninja_form", "disguise_form",
#                 "infiltration_mode", "combat_stance"
#             ],
#             "affiliations": [
#                 "uzui_clan", "demon_slayer_support",
#                 "shinobi_organization", "uzui's_wives"
#             ],
#             "abilities": [
#                 "ninja_techniques", "infiltration_skills",
#                 "combat_expertise", "disguise_mastery"
#             ],
#             "relationships": [
#                 "uzui's_wife", "makio's_sister-wife",
#                 "suma's_sister-wife", "shinobi_partner"
#             ],
#             "weapons": [
#                 "kunai", "ninja_tools",
#                 "infiltration_equipment", "shinobi_gear"
#             ],
#             "outfits": [
#                 "shinobi_outfit", "disguise_clothes",
#                 "infiltration_wear", "casual_attire"
#             ]
#         },
#
#         "makio": {
#             "names": [
#                 "makio", "uzui's_wife",
#                 "kunoichi_wife", "shinobi_warrior"
#             ],
#             "titles": [
#                 "sound_hashira's_wife", "ninja_wife",
#                 "entertainment_district_infiltrator", "kunoichi"
#             ],
#             "forms": [
#                 "ninja_form", "disguise_form",
#                 "combat_mode", "infiltration_stance"
#             ],
#             "affiliations": [
#                 "uzui_clan", "demon_slayer_support",
#                 "shinobi_organization", "uzui's_wives"
#             ],
#             "abilities": [
#                 "ninja_arts", "combat_skills",
#                 "infiltration_expertise", "shinobi_techniques"
#             ],
#             "relationships": [
#                 "uzui's_wife", "hinatsuru's_sister-wife",
#                 "suma's_sister-wife", "shinobi_team"
#             ],
#             "weapons": [
#                 "ninja_weapons", "infiltration_tools",
#                 "shinobi_equipment", "combat_gear"
#             ],
#             "outfits": [
#                 "ninja_attire", "disguise_outfit",
#                 "combat_wear", "casual_clothes"
#             ]
#         },
#
#         "suma": {
#             "names": [
#                 "suma", "uzui's_wife",
#                 "emotional_kunoichi", "shinobi_spouse"
#             ],
#             "titles": [
#                 "sound_hashira's_wife", "ninja_wife",
#                 "entertainment_district_infiltrator", "kunoichi"
#             ],
#             "forms": [
#                 "ninja_form", "emotional_state",
#                 "infiltration_mode", "combat_ready"
#             ],
#             "affiliations": [
#                 "uzui_clan", "demon_slayer_support",
#                 "shinobi_organization", "uzui's_wives"
#             ],
#             "abilities": [
#                 "ninja_techniques", "infiltration_skills",
#                 "emotional_strength", "combat_expertise"
#             ],
#             "relationships": [
#                 "uzui's_wife", "makio's_sister-wife",
#                 "hinatsuru's_sister-wife", "shinobi_team"
#             ],
#             "weapons": [
#                 "kunoichi_weapons", "ninja_tools",
#                 "infiltration_gear", "combat_equipment"
#             ],
#             "outfits": [
#                 "shinobi_clothes", "disguise_attire",
#                 "infiltration_outfit", "casual_wear"
#             ]
#         },
#
#         "rengoku_mother": {
#             "names": [
#                 "ruka_rengoku", "rengoku's_mother",
#                 "kyojuro's_mother", "senjuro's_mother"
#             ],
#             "titles": [
#                 "rengoku_matriarch", "flame_hashira's_mother",
#                 "swordsman's_wife", "rengoku_family"
#             ],
#             "forms": [
#                 "sickly_form", "mother_form",
#                 "bedridden_state", "final_moments"
#             ],
#             "affiliations": [
#                 "rengoku_family", "flame_breathing_lineage",
#                 "hashira_family", "demon_slayer_relatives"
#             ],
#             "relationships": [
#                 "shinjuro's_wife", "kyojuro's_mother",
#                 "senjuro's_mother", "rengoku_family_member"
#             ],
#             "time_periods": [
#                 "pre_illness", "sickness_era",
#                 "kyojuro's_childhood", "final_days"
#             ],
#             "outfits": [
#                 "sick_bed_clothes", "family_kimono",
#                 "casual_wear", "traditional_attire"
#             ]
#         },
#
#         "susamaru": {
#             "names": [
#                 "susamaru", "temari_demon",
#                 "ball_demon", "temple_demon"
#             ],
#             "titles": [
#                 "temari_demon", "twelve_kizuki_pretender",
#                 "ball_wielder", "temple_destroyer"
#             ],
#             "forms": [
#                 "demon_form", "combat_form",
#                 "temari_wielding", "enhanced_strength"
#             ],
#             "affiliations": [
#                 "muzan's_demons", "demon_organization",
#                 "temple_demons", "yazaki_residence"
#             ],
#             "abilities": [
#                 "temari_manipulation", "demon_strength",
#                 "regeneration", "ball_multiplication",
#                 "enhanced_speed"
#             ],
#             "relationships": [
#                 "yahaba's_partner", "muzan's_subordinate",
#                 "tamayo's_enemy", "demon_associate"
#             ],
#             "weapons": [
#                 "temari_balls", "demon_powers",
#                 "enhanced_strength", "regeneration"
#             ],
#             "outfits": [
#                 "demon_attire", "battle_clothes",
#                 "traditional_wear", "combat_gear"
#             ]
#         },
#
#         "mukago": {
#             "names": [
#                 "mukago", "lower_moon_demon",
#                 "spider_family_demon", "rui's_family"
#             ],
#             "titles": [
#                 "spider_demon", "spider_family_member",
#                 "natagumo_mountain_demon", "demon_sister"
#             ],
#             "forms": [
#                 "demon_form", "spider_form",
#                 "combat_mode", "family_member_form"
#             ],
#             "affiliations": [
#                 "spider_family", "demon_organization",
#                 "rui's_demons", "natagumo_mountain"
#             ],
#             "abilities": [
#                 "spider_powers", "web_manipulation",
#                 "demon_strength", "regeneration"
#             ],
#             "relationships": [
#                 "rui's_family_member", "spider_demon_sister",
#                 "demon_subordinate", "false_family_member"
#             ],
#             "weapons": [
#                 "spider_threads", "demon_abilities",
#                 "web_techniques", "spider_powers"
#             ],
#             "outfits": [
#                 "spider_demon_clothes", "family_attire",
#                 "demon_garments", "battle_wear"
#             ]
#         },
#
#         "kacho": {
#             "names": [
#                 "kacho", "butterfly_mansion_girl",
#                 "medical_corps", "support_staff"
#             ],
#             "titles": [
#                 "medical_support", "butterfly_mansion_staff",
#                 "healing_assistant", "corps_helper"
#             ],
#             "forms": [
#                 "support_form", "medical_mode",
#                 "assistance_role", "training_form"
#             ],
#             "affiliations": [
#                 "butterfly_mansion", "medical_corps",
#                 "demon_slayer_support", "healing_team"
#             ],
#             "abilities": [
#                 "medical_knowledge", "support_skills",
#                 "healing_techniques", "rehabilitation_expertise"
#             ],
#             "relationships": [
#                 "butterfly_mansion_staff", "shinobu's_assistant",
#                 "medical_team_member", "support_worker"
#             ],
#             "activities": [
#                 "medical_assistance", "rehabilitation_support",
#                 "healing_duties", "mansion_maintenance"
#             ],
#             "outfits": [
#                 "medical_uniform", "butterfly_mansion_clothes",
#                 "support_staff_attire", "work_wear"
#             ]
#         },
#
#         "kiyo": {
#             "names": [
#                 "kiyo", "butterfly_mansion_girl",
#                 "medical_support", "healing_assistant"
#             ],
#             "titles": [
#                 "medical_staff", "butterfly_mansion_helper",
#                 "healing_support", "mansion_assistant"
#             ],
#             "forms": [
#                 "support_form", "medical_mode",
#                 "assistance_role", "helper_form"
#             ],
#             "affiliations": [
#                 "butterfly_mansion", "medical_corps",
#                 "demon_slayer_support", "healing_team"
#             ],
#             "abilities": [
#                 "medical_aid", "support_skills",
#                 "healing_assistance", "rehabilitation_help"
#             ],
#             "relationships": [
#                 "butterfly_mansion_staff", "aoi's_colleague",
#                 "medical_team_member", "support_worker"
#             ],
#             "activities": [
#                 "medical_support", "healing_assistance",
#                 "mansion_duties", "patient_care"
#             ],
#             "outfits": [
#                 "medical_uniform", "butterfly_mansion_attire",
#                 "support_clothes", "work_uniform"
#             ]
#         },
#
#         "sumi": {
#             "names": [
#                 "sumi", "butterfly_mansion_girl",
#                 "medical_support", "quiet_helper"
#             ],
#             "titles": [
#                 "medical_staff", "butterfly_mansion_assistant",
#                 "healing_support", "quiet_worker"
#             ],
#             "forms": [
#                 "support_form", "medical_mode",
#                 "assistance_role", "helper_form"
#             ],
#             "affiliations": [
#                 "butterfly_mansion", "medical_corps",
#                 "demon_slayer_support", "healing_team"
#             ],
#             "abilities": [
#                 "medical_support", "quiet_efficiency",
#                 "healing_assistance", "careful_work"
#             ],
#             "relationships": [
#                 "butterfly_mansion_staff", "aoi's_colleague",
#                 "medical_team_member", "support_worker"
#             ],
#             "activities": [
#                 "medical_assistance", "quiet_support",
#                 "mansion_duties", "patient_care"
#             ],
#             "outfits": [
#                 "medical_uniform", "butterfly_mansion_clothes",
#                 "support_attire", "work_wear"
#             ]
#         },
#
#         "teiko": {
#             "names": [
#                 "teiko", "gyutaro's_victim",
#                 "entertainment_district_resident", "brothel_woman"
#             ],
#             "titles": [
#                 "entertainment_district_worker", "yuukaku_resident",
#                 "gyutaro's_target", "historical_victim"
#             ],
#             "forms": [
#                 "human_form", "victim_state",
#                 "flashback_form", "historical_figure"
#             ],
#             "affiliations": [
#                 "entertainment_district", "yuukaku_workers",
#                 "historical_victims", "brothel_staff"
#             ],
#             "relationships": [
#                 "gyutaro's_victim", "district_worker",
#                 "daki's_predecessor", "historical_character"
#             ],
#             "time_periods": [
#                 "pre-daki_era", "gyutaro's_time",
#                 "entertainment_district_past", "flashback_period"
#             ],
#             "outfits": [
#                 "courtesan_clothes", "period_attire",
#                 "yuukaku_dress", "historical_costume"
#             ]
#         },
#
#
#     }
#
#     JUJUTSU_KAISEN_TAGS = {
#         # Main characters
#           "nobara": {
#             "names": [
#                 "kugisaki_nobara", "nobara_kugisaki",
#                 "hammer_wielder", "straw_doll_user"
#             ],
#             "titles": [
#                 "first_year_student", "jujutsu_sorcerer",
#                 "tokyo_high_student", "straw_doll_technique_user"
#             ],
#             "forms": [
#                 "base_form", "resonance_mode",
#                 "black_flash_state", "battle_mode",
#                 "cursed_energy_enhanced"
#             ],
#             "affiliations": [
#                 "tokyo_jujutsu_high", "first_year_class",
#                 "gojo's_students", "yuji's_classmate"
#             ],
#             "abilities": [
#                 "straw_doll_technique", "resonance",
#                 "black_flash", "hairpin_nails",
#                 "cursed_energy_manipulation"
#             ],
#             "relationships": [
#                 "yuji's_classmate", "megumi's_classmate",
#                 "gojo's_student", "saori's_friend",
#                 "fumi's_friend"
#             ],
#             "weapons": [
#                 "hammer", "nails",
#                 "straw_dolls", "cursed_tools"
#             ],
#             "outfits": [
#                 "school_uniform", "battle_attire",
#                 "casual_clothes", "mission_gear",
#                 "training_outfit"
#             ]
#         },
#
#         "maki": {
#             "names": [
#                 "zenin_maki", "maki_zenin",
#                 "cursed_tools_expert", "hr_warrior"
#             ],
#             "titles": [
#                 "zenin_outcast", "cursed_tools_specialist",
#                 "heavenly_restriction_bearer", "second_year_student"
#             ],
#             "forms": [
#                 "restricted_form", "awakened_form",
#                 "zero_cursed_energy", "enhanced_physical_state",
#                 "post_mai_form"
#             ],
#             "affiliations": [
#                 "tokyo_jujutsu_high", "zenin_clan_(former)",
#                 "second_year_class", "kyoto_sister_school"
#             ],
#             "abilities": [
#                 "superhuman_strength", "enhanced_senses",
#                 "weapon_mastery", "cursed_tool_expertise",
#                 "physical_enhancement"
#             ],
#             "relationships": [
#                 "mai's_twin", "megumi's_cousin",
#                 "zenin_clan_member", "panda's_friend",
#                 "toji's_parallel"
#             ],
#             "weapons": [
#                 "cursed_tools", "special_grade_weapons",
#                 "multiple_weapons", "combat_tools"
#             ],
#             "outfits": [
#                 "school_uniform", "combat_gear",
#                 "training_clothes", "mission_attire",
#                 "casual_wear"
#             ]
#         },
#
#         "miwa": {
#             "names": [
#                 "kasumi_miwa", "miwa_kasumi",
#                 "simple_domain_user", "sword_user"
#             ],
#             "titles": [
#                 "kyoto_student", "swordsman",
#                 "simple_domain_wielder", "new_shadow_style_user"
#             ],
#             "forms": [
#                 "base_form", "simple_domain",
#                 "sword_stance", "combat_mode"
#             ],
#             "affiliations": [
#                 "kyoto_jujutsu_high", "second_year_class",
#                 "kyoto_sister_school", "swordsman_group"
#             ],
#             "abilities": [
#                 "simple_domain", "swordsmanship",
#                 "new_shadow_style", "basic_cursed_energy"
#             ],
#             "relationships": [
#                 "mechamaru's_friend", "kamo's_classmate",
#                 "todo's_classmate", "miyo's_senior"
#             ],
#             "weapons": [
#                 "katana", "cursed_sword",
#                 "simple_domain_technique"
#             ],
#             "outfits": [
#                 "school_uniform", "battle_gear",
#                 "training_clothes", "casual_wear"
#             ]
#         },
#
#         "mai": {
#             "names": [
#                 "zenin_mai", "mai_zenin",
#                 "construction_user", "maki's_twin"
#             ],
#             "titles": [
#                 "kyoto_student", "zenin_clan_member",
#                 "construction_technique_user", "cursed_energy_wielder"
#             ],
#             "forms": [
#                 "base_form", "construction_mode",
#                 "combat_stance", "final_form"
#             ],
#             "affiliations": [
#                 "kyoto_jujutsu_high", "zenin_clan",
#                 "second_year_class", "kyoto_sister_school"
#             ],
#             "abilities": [
#                 "construction", "cursed_energy_manipulation",
#                 "bullet_creation", "limited_constructs"
#             ],
#             "relationships": [
#                 "maki's_twin", "megumi's_cousin",
#                 "zenin_clan_member", "kyoto_student"
#             ],
#             "weapons": [
#                 "constructed_bullets", "cursed_tools",
#                 "created_weapons"
#             ],
#             "outfits": [
#                 "school_uniform", "combat_attire",
#                 "kyoto_uniform", "casual_clothes"
#             ]
#         },
#
#         "rika": {
#             "names": [
#                 "orimoto_rika", "queen_of_curses",
#                 "yuta's_curse", "special_grade_curse"
#             ],
#             "titles": [
#                 "queen_of_curses", "special_grade_cursed_spirit",
#                 "yuta's_bound_spirit", "curse_remnant"
#             ],
#             "forms": [
#                 "cursed_spirit_form", "bound_form",
#                 "battle_form", "protective_mode",
#                 "ring_form"
#             ],
#             "abilities": [
#                 "immense_cursed_energy", "copying_techniques",
#                 "curse_manipulation", "physical_manifestation",
#                 "protective_binding"
#             ],
#             "relationships": [
#                 "yuta's_childhood_friend", "bound_spirit",
#                 "okkotsu's_power", "curse_partner"
#             ],
#             "outfits": [
#                 "spirit_form", "school_uniform_(memory)",
#                 "cursed_manifestation", "bound_spirit_appearance"
#             ]
#         },
#
#         "uraume": {
#             "names": [
#                 "uraume", "sukuna's_servant",
#                 "frost_human", "ancient_sorcerer"
#             ],
#             "titles": [
#                 "frost_technique_user", "sukuna's_assistant",
#                 "ancient_jujutsu_user", "heian_era_sorcerer"
#             ],
#             "abilities": [
#                 "ice_manipulation", "frost_technique",
#                 "ancient_jujutsu", "cursed_energy_control",
#                 "cooking_techniques"
#             ],
#             "forms": [
#                 "human_form", "combat_form",
#                 "frost_mode", "ancient_state"
#             ],
#             "relationships": [
#                 "sukuna's_servant", "heian_era_ally",
#                 "kenjaku's_associate", "ancient_sorcerer"
#             ],
#             "outfits": [
#                 "modern_clothes", "battle_attire",
#                 "chef_uniform", "ancient_garments"
#             ]
#         },
#
#         "takako": {
#             "names": [
#                 "uro_takako", "sky_manipulator",
#                 "ancient_sorcerer", "curved_sky_user"
#             ],
#             "titles": [
#                 "heian_sorcerer", "sky_technique_user",
#                 "culling_game_player", "ancient_warrior"
#             ],
#             "abilities": [
#                 "sky_manipulation", "thin_ice_technique",
#                 "aerial_control", "cursed_energy_manipulation"
#             ],
#             "forms": [
#                 "combat_form", "sky_manipulation_mode",
#                 "thin_ice_state", "battle_stance"
#             ],
#             "relationships": [
#                 "heian_era_sorcerer", "ryu's_opponent",
#                 "culling_game_participant", "ancient_warrior"
#             ],
#             "outfits": [
#                 "battle_attire", "traditional_clothes",
#                 "heian_era_garments", "combat_gear"
#             ]
#         },
#
#         "mei_mei": {
#             "names": [
#                 "mei_mei", "crow_user",
#                 "mercenary_sorcerer", "grade_1_sorcerer"
#             ],
#             "titles": [
#                 "grade_1_sorcerer", "cursed_technique_user",
#                 "mercenary_jujutsu_user", "crow_controller"
#             ],
#             "abilities": [
#                 "bird_manipulation", "crow_control",
#                 "cursed_technique", "tactical_analysis",
#                 "combat_expertise"
#             ],
#             "forms": [
#                 "combat_form", "crow_control_mode",
#                 "battle_stance", "mercenary_mode"
#             ],
#             "relationships": [
#                 "ui_ui's_sister", "nanami's_colleague",
#                 "gojo's_associate", "jujutsu_society_member"
#             ],
#             "outfits": [
#                 "business_suit", "combat_gear",
#                 "mission_attire", "casual_clothes"
#             ]
#         },
#
#         "tsumiki": {
#             "names": [
#                 "fushiguro_tsumiki", "megumi's_sister",
#                 "coma_patient", "culling_game_target"
#             ],
#             "titles": [
#                 "cursed_object", "coma_victim",
#                 "megumi's_motivation", "culling_game_vessel"
#             ],
#             "states": [
#                 "coma_state", "awakened_state",
#                 "vessel_form", "cursed_state"
#             ],
#             "relationships": [
#                 "megumi's_sister", "toji's_stepdaughter",
#                 "culling_game_participant", "kenjaku's_vessel"
#             ],
#             "outfits": [
#                 "hospital_gown", "school_uniform",
#                 "casual_clothes", "modern_attire"
#             ]
#         },
#
#         "utahime": {
#             "names": [
#                 "iori_utahime", "kyoto_teacher",
#                 "jujutsu_instructor", "singing_voice_user"
#             ],
#             "titles": [
#                 "kyoto_instructor", "jujutsu_teacher",
#                 "semi_grade_1_sorcerer", "singing_voice_wielder"
#             ],
#             "abilities": [
#                 "singing_voice_technique", "cursed_energy_manipulation",
#                 "barrier_techniques", "teaching_expertise"
#             ],
#             "forms": [
#                 "teacher_mode", "combat_form",
#                 "technique_activation", "defensive_stance"
#             ],
#             "relationships": [
#                 "gojo's_colleague", "kyoto_staff",
#                 "student_mentor", "jujutsu_society_member"
#             ],
#             "outfits": [
#                 "teacher_attire", "combat_uniform",
#                 "formal_wear", "training_clothes"
#             ]
#         },
#
#         "yuki": {
#             "names": [
#                 "tsukumo_yuki", "special_grade_sorcerer",
#                 "wandering_sorcerer", "curse_researcher"
#             ],
#             "titles": [
#                 "special_grade_sorcerer", "curse_investigator",
#                 "jujutsu_researcher", "wandering_special_grade"
#             ],
#             "abilities": [
#                 "unknown_technique", "immense_cursed_energy",
#                 "special_grade_power", "research_expertise"
#             ],
#             "forms": [
#                 "battle_form", "research_mode",
#                 "investigation_state", "combat_stance"
#             ],
#             "relationships": [
#                 "geto's_former_classmate", "gojo's_peer",
#                 "amai's_mentor", "jujutsu_society_member"
#             ],
#             "outfits": [
#                 "casual_attire", "battle_gear",
#                 "research_clothes", "travel_wear"
#             ]
#         }
#     }
#
#     SPY_X_FAMILY_TAGS = {
#         "yor": {
#             "names": [
#                 "yor_forger", "thorn_princess", "yor_briar",
#                 "assassin_wife", "garden_witch", "cleaning_lady"
#             ],
#             "titles": [
#                 "thorn_princess", "city_hall_clerk",
#                 "forger_family_mother", "garden_assassin",
#                 "ostanian_assassin"
#             ],
#             "forms": [
#                 "base_form", "assassin_mode", "drunk_state",
#                 "combat_form", "mother_mode", "wedding_form"
#             ],
#             "affiliations": [
#                 "garden_organization", "berlint_city_hall",
#                 "forger_family", "garden_assassins",
#                 "ostanian_government"
#             ],
#             "abilities": [
#                 "superhuman_strength", "assassination_techniques",
#                 "weapon_mastery", "acrobatic_combat",
#                 "enhanced_durability"
#             ],
#             "relationships": [
#                 "loid's_wife", "anya's_mother", "yuri's_sister",
#                 "garden_member", "berlint_employee"
#             ],
#             "outfits": [
#                 "assassin_dress", "work_uniform", "casual_attire",
#                 "evening_gown", "combat_dress", "cleaning_outfit"
#             ]
#         },
#         "anya": {
#             "names": [
#                 "anya_forger", "subject_007", "test_subject",
#                 "starlight_anya", "spy_wars_fan", "peanut_lover"
#             ],
#             "titles": [
#                 "eden_academy_student", "telepathic_child",
#                 "forger_family_daughter", "esper",
#                 "imperial_scholar"
#             ],
#             "forms": [
#                 "base_form", "crying_face", "smug_face",
#                 "excited_state", "telepathy_mode",
#                 "school_mode"
#             ],
#             "affiliations": [
#                 "forger_family", "eden_academy",
#                 "cecile_hall", "former_test_subject",
#                 "imperial_scholars"
#             ],
#             "abilities": [
#                 "telepathy", "mind_reading",
#                 "emotional_sensing", "precognition",
#                 "intuitive_aptitude"
#             ],
#             "relationships": [
#                 "loid's_daughter", "yor's_daughter",
#                 "bond's_owner", "damian's_classmate",
#                 "becky's_friend"
#             ],
#             "outfits": [
#                 "school_uniform", "casual_clothes",
#                 "pajamas", "elegant_dress",
#                 "spy_wars_costume"
#             ]
#         },
#         "fiona": {
#             "names": [
#                 "fiona_frost", "nightfall", "agent_nightfall",
#                 "twilight's_student", "frost"
#             ],
#             "titles": [
#                 "westalian_spy", "twilight's_apprentice",
#                 "handler_agent", "wise_operative"
#             ],
#             "forms": [
#                 "base_form", "spy_mode", "disguise_form",
#                 "combat_ready", "civilian_mode"
#             ],
#             "affiliations": [
#                 "wise", "westalian_intelligence",
#                 "twilight's_students", "handler_division"
#             ],
#             "abilities": [
#                 "disguise_mastery", "combat_skills",
#                 "intelligence_gathering", "infiltration",
#                 "analytical_abilities"
#             ],
#             "relationships": [
#                 "twilight's_student", "yor's_rival",
#                 "wise_operative", "handler's_agent"
#             ],
#             "outfits": [
#                 "spy_suit", "civilian_clothes",
#                 "mission_gear", "formal_attire"
#             ]
#         },
#         "lady_in_black": {
#             "names": [
#                 "lady_in_black", "handler",
#                 "wise_commander", "mission_director"
#             ],
#             "titles": [
#                 "wise_handler", "operation_director",
#                 "spy_commander", "mission_coordinator"
#             ],
#             "forms": [
#                 "base_form", "command_mode",
#                 "mission_briefing", "strategic_planning"
#             ],
#             "affiliations": [
#                 "wise", "westalian_intelligence",
#                 "handler_division", "command_structure"
#             ],
#             "abilities": [
#                 "strategic_planning", "operation_management",
#                 "agent_handling", "intelligence_analysis"
#             ],
#             "relationships": [
#                 "twilight's_handler", "wise_commander",
#                 "agent_supervisor", "operation_director"
#             ],
#             "outfits": [
#                 "black_suit", "handler_uniform",
#                 "formal_wear", "command_attire"
#             ]
#         },
#         "sharon": {
#             "names": [
#                 "sharon", "shop_keeper",
#                 "store_owner", "berlint_merchant"
#             ],
#             "titles": [
#                 "shop_owner", "store_proprietor",
#                 "merchant", "business_owner"
#             ],
#             "forms": [
#                 "base_form", "shopkeeper_mode",
#                 "business_mode", "civilian_form"
#             ],
#             "affiliations": [
#                 "berlint_merchants", "shop_owners_association",
#                 "civilian_sector", "commercial_district"
#             ],
#             "abilities": [
#                 "business_management", "customer_service",
#                 "merchandise_knowledge", "shop_keeping"
#             ],
#             "relationships": [
#                 "civilian_merchant", "store_owner",
#                 "customer_servant", "business_operator"
#             ],
#             "outfits": [
#                 "shop_uniform", "casual_wear",
#                 "business_attire", "merchant_clothes"
#             ]
#         },
#     },
#
#     COWBOY_BEBOP_TAGS = {
#         # Main characters
#         "faye": {
#           "names": [
#             "faye_valentine", "poker_alice",
#             "romani_faye", "sleeping_beauty"
#           ],
#           "titles": [
#             "bounty_hunter", "bebop_crew_member",
#             "gambling_queen", "cryo_survivor"
#           ],
#           "forms": [
#             "base_form", "cryo_state",
#             "younger_self", "beta_cassette_version",
#             "injured_state"
#           ],
#           "affiliations": [
#             "bebop_crew", "bounty_hunters",
#             "singapore_medical_facility", "gambling_circuit"
#           ],
#           "abilities": [
#             "combat_skills", "piloting",
#             "gambling_expertise", "marksmanship",
#             "deception_tactics"
#           ],
#           "relationships": [
#             "bebop_crew_member", "spike's_partner",
#             "jet's_crewmate", "whitney's_debtor"
#           ],
#           "outfits": [
#             "yellow_vinyl", "red_jacket",
#             "casino_dress", "racing_suit",
#             "singapore_hospital_gown"
#           ]
#         },
#         "ed": {
#           "names": [
#             "edward_wong_hau_pepelu_tivrusky_iv",
#             "françoise_appledelhi", "radical_ed",
#             "net_diver"
#           ],
#           "titles": [
#             "hacker_extraordinaire", "bebop_crew_member",
#             "net_diver", "earth_child"
#           ],
#           "forms": [
#             "base_form", "hacker_mode",
#             "sleep_mode", "exploration_mode"
#           ],
#           "affiliations": [
#             "bebop_crew", "net_divers",
#             "earth_orphans", "appledelhi_family"
#           ],
#           "abilities": [
#             "hacking", "computer_expertise",
#             "tracking_skills", "data_analysis",
#             "system_infiltration"
#           ],
#           "relationships": [
#             "bebop_crew_member", "ein's_friend",
#             "appledelhi's_child", "tomato_user"
#           ],
#           "outfits": [
#             "white_shirt", "black_shorts",
#             "goggles", "barefoot_style"
#           ]
#         },
#         "julia": {
#           "names": [
#             "julia", "spike's_angel",
#             "syndicate_woman", "vicious_ex"
#           ],
#           "titles": [
#             "red_dragon_member", "syndicate_associate",
#             "femme_fatale", "underground_operative"
#           ],
#           "forms": [
#             "base_form", "syndicate_mode",
#             "fugitive_state", "past_self"
#           ],
#           "affiliations": [
#             "red_dragon_syndicate", "criminal_underground",
#             "annie's_associates", "syndicate_fugitives"
#           ],
#           "abilities": [
#             "marksmanship", "survival_skills",
#             "driving_expertise", "covert_operations"
#           ],
#           "relationships": [
#             "spike's_lover", "vicious_ex",
#             "annie's_friend", "syndicate_member"
#           ],
#           "outfits": [
#             "black_dress", "casual_attire",
#             "syndicate_gear", "fugitive_clothes"
#           ]
#         },
#         "meifa": {
#           "names": [
#             "meifa_puzi", "feng_shui_master",
#             "compass_girl", "puzi's_daughter"
#           ],
#           "titles": [
#             "feng_shui_practitioner", "fortune_teller",
#             "compass_master", "spiritual_guide"
#           ],
#           "forms": [
#             "base_form", "divination_mode",
#             "compass_reading", "meditation_state"
#           ],
#           "affiliations": [
#             "feng_shui_practitioners", "mars_residents",
#             "puzi_family", "spiritual_community"
#           ],
#           "abilities": [
#             "feng_shui", "compass_reading",
#             "spiritual_sensing", "fortune_telling"
#           ],
#           "relationships": [
#             "puzi's_daughter", "jet's_associate",
#             "spiritual_heir", "mars_resident"
#           ],
#           "outfits": [
#             "traditional_clothes", "casual_wear",
#             "mars_attire", "meditation_robes"
#           ]
#         },
#         "judy": {
#           "names": [
#             "judy", "big_shot_host",
#             "bounty_show_presenter", "tv_personality"
#           ],
#           "titles": [
#             "show_host", "tv_presenter",
#             "bounty_announcer", "media_personality"
#           ],
#           "forms": [
#             "base_form", "show_mode",
#             "presenter_form", "off_camera"
#           ],
#           "affiliations": [
#             "big_shot_show", "tv_network",
#             "media_industry", "bounty_channel"
#           ],
#           "abilities": [
#             "presenting", "public_speaking",
#             "bounty_information", "entertainment"
#           ],
#           "relationships": [
#             "punch's_co-host", "tv_personality",
#             "show_partner", "network_employee"
#           ],
#           "outfits": [
#             "cowgirl_costume", "show_outfit",
#             "western_wear", "tv_costume"
#           ]
#         },
#         "alisa": {
#           "names": [
#             "alisa", "jet's_ex",
#             "police_informant", "bar_owner"
#           ],
#           "titles": [
#             "bar_proprietor", "former_detective_partner",
#             "information_broker", "business_owner"
#           ],
#           "forms": [
#             "base_form", "bartender_mode",
#             "informant_state", "past_self"
#           ],
#           "affiliations": [
#             "issp_informants", "bar_owners",
#             "ganymede_residents", "underground_network"
#           ],
#           "abilities": [
#             "information_gathering", "business_management",
#             "networking", "bartending"
#           ],
#           "relationships": [
#             "jet's_ex_girlfriend", "rhint's_supporter",
#             "bar_owner", "police_contact"
#           ],
#           "outfits": [
#             "casual_clothes", "bar_attire",
#             "business_wear", "ganymede_fashion"
#           ]
#         },
#         "v.t": {
#           "names": [
#             "victoria_terpsichore", "v.t.",
#             "space_trucker", "cargo_hauler"
#           ],
#           "titles": [
#             "veteran_trucker", "cargo_specialist",
#             "hauling_expert", "space_transporter"
#           ],
#           "forms": [
#             "base_form", "trucker_mode",
#             "transport_state", "business_mode"
#           ],
#           "affiliations": [
#             "space_truckers", "cargo_haulers",
#             "transport_network", "trucker_community"
#           ],
#           "abilities": [
#             "space_navigation", "cargo_handling",
#             "vehicle_operation", "route_planning"
#           ],
#           "relationships": [
#             "trucker_community_member", "spike's_contact",
#             "cargo_network_member", "space_hauler"
#           ],
#           "outfits": [
#             "trucker_gear", "work_clothes",
#             "space_suit", "casual_wear"
#           ]
#         },
#         "katerina": {
#           "names": [
#             "katerina_solensan", "environmental_activist",
#             "eco_warrior", "revenge_seeker"
#           ],
#           "titles": [
#             "environmental_activist", "terrorist_leader",
#             "eco_warrior", "resistance_fighter"
#           ],
#           "forms": [
#             "base_form", "activist_mode",
#             "combat_state", "disguised_form"
#           ],
#           "affiliations": [
#             "environmental_activists", "resistance_movement",
#             "space_terrorists", "eco_warriors"
#           ],
#           "abilities": [
#             "leadership", "tactical_planning",
#             "combat_skills", "environmental_knowledge"
#           ],
#           "relationships": [
#             "resistance_leader", "environmental_activist",
#             "space_terrorist", "movement_leader"
#           ],
#           "outfits": [
#             "activist_gear", "combat_suit",
#             "disguise_clothes", "casual_wear"
#           ]
#         },
#     }
#
#     HATSUNE_MIKU_TAGS = {
#         # Main Vocaloids
#         "miku": {
#             "names": ["hatsune_miku", "miku", "initial_miku", "cv01", "virtual_diva"],
#             "titles": ["virtual_idol", "vocaloid_princess", "digital_singer", "sound_of_the_future"],
#             "forms": ["base_form", "append_form", "v3_form", "v4x_form", "nt_form"],
#             "abilities": ["perfect_pitch", "wide_vocal_range", "tempo_control", "voice_synthesis"],
#             "relationships": ["crypton_family_member", "kaito's_partner", "kagamine_twins_mentor"],
#             "outfits": ["default_outfit", "project_diva_attire", "racing_miku", "snow_miku", "magical_mirai"],
#             "gelbooru": ["hatsune_miku", "miku_%28vocaloid%29", "initial_miku", "miku_%28project_diva%29"],
#             "danbooru": ["hatsune_miku", "miku_(vocaloid)", "project_diva"]
#         },
#
#         "luka": {
#             "names": ["megurine_luka", "luka", "cv03", "pink_diva"],
#             "titles": ["mature_vocaloid", "bilingual_singer", "voice_enchantress"],
#             "forms": ["base_form", "v2_form", "v4x_form", "english_voicebank"],
#             "abilities": ["dual_language_synthesis", "low_range_specialist", "smooth_transitions"],
#             "relationships": ["crypton_family_member", "miku's_mentor", "kaito's_duet_partner"],
#             "outfits": ["default_outfit", "project_diva_attire", "kimono_style", "concert_dress"],
#             "gelbooru": ["megurine_luka", "luka_%28vocaloid%29", "luka_%28project_diva%29"],
#             "danbooru": ["megurine_luka", "project_diva"]
#         },
#
#         "meiko": {
#             "names": ["meiko", "cv01_meiko", "sakine_meiko", "red_diva"],
#             "titles": ["first_japanese_vocaloid", "veteran_singer", "sake_lover"],
#             "forms": ["base_form", "v3_form", "power_form", "straight_form"],
#             "abilities": ["powerful_voice", "wide_range", "mature_tonality"],
#             "relationships": ["crypton_family_senior", "kaito's_counterpart", "miku's_senior"],
#             "outfits": ["default_red_outfit", "project_diva_attire", "kimono_style"],
#             "gelbooru": ["meiko_%28vocaloid%29", "meiko_%28project_diva%29"],
#             "danbooru": ["meiko_(vocaloid)", "project_diva"]
#         },
#
#         "rin": {
#             "names": ["kagamine_rin", "cv02_rin", "yellow_diva"],
#             "titles": ["mirror_sound", "vocal_princess", "twin_vocalist"],
#             "forms": ["base_form", "append_form", "v4x_form", "power_form"],
#             "abilities": ["high_range_vocals", "duo_synthesis", "mirror_harmonies"],
#             "relationships": ["len's_mirror", "crypton_family_member", "miku's_junior"],
#             "outfits": ["default_outfit", "project_diva_attire", "swimmer_style", "princess_form"],
#             "gelbooru": ["kagamine_rin", "rin_%28vocaloid%29", "rin_%28project_diva%29"],
#             "danbooru": ["kagamine_rin", "rin_(vocaloid)"]
#         },
#         "gumi": {
#             "names": ["gumi", "megpoid", "green_diva"],
#             "titles": ["internet_co_voice", "carrot_princess", "voice_veteran"],
#             "forms": ["base_form", "v3_form", "v4_form", "english_form"],
#             "abilities": ["clear_voice", "wide_range", "bilingual_synthesis"],
#             "relationships": ["internet_co_family", "lily's_companion", "cross_synthesis_specialist"],
#             "outfits": ["default_green", "native_dress", "casual_wear", "concert_attire"],
#             "gelbooru": ["gumi_%28vocaloid%29", "megpoid"],
#             "danbooru": ["gumi", "megpoid"]
#         },
#         "ia": {
#             "names": ["ia", "aria_planetes", "spiritual_diva"],
#             "titles": ["1st_place_voice", "ethereal_singer", "space_vocalist"],
#             "forms": ["base_form", "rocks_form", "spiritual_form"],
#             "abilities": ["gentle_synthesis", "clear_tones", "electronic_fusion"],
#             "relationships": ["one_place_family", "aria_successor", "vocaloid3_generation"],
#             "outfits": ["default_outfit", "rocks_attire", "concert_dress", "casual_wear"],
#             "gelbooru": ["ia_%28vocaloid%29", "aria_planetes"],
#             "danbooru": ["ia_(vocaloid)", "aria"]
#         },
#         "yukari": {
#             "names": ["yuzuki_yukari", "voiceroid_yukari", "purple_voice"],
#             "titles": ["rabbit_vocalist", "ah_software_voice", "dual_system_singer"],
#             "forms": ["base_form", "ex_form", "voiceroid_form"],
#             "abilities": ["dual_synthesis", "natural_speech", "voice_acting"],
#             "relationships": ["ah_software_family", "voiceroid_member", "vocaloid_crossover"],
#             "outfits": ["default_outfit", "rabbit_theme", "casual_wear", "voice_forms"],
#             "gelbooru": ["yuzuki_yukari", "yukari_%28vocaloid%29"],
#             "danbooru": ["yuzuki_yukari", "voiceroid"]
#         },
#
#         "teto": {
#             "names": ["kasane_teto", "utau_teto", "chimera_voice"],
#             "titles": ["utau_pioneer", "chimera_vocalist", "drill_hair_idol"],
#             "forms": ["base_form", "chimera_form", "append_form"],
#             "abilities": ["multi_voice_synthesis", "drill_spin", "high_pitch_mastery"],
#             "relationships": ["utau_family", "miku's_friend", "vocaloid_collaborator"],
#             "outfits": ["default_red", "concert_attire", "casual_wear"],
#             "gelbooru": ["kasane_teto", "utau", "teto_%28utau%29"],
#             "danbooru": ["kasane_teto", "utau"]
#         },
#         "neru": {
#             "names": ["akita_neru", "derivative_neru", "yellow_phone"],
#             "titles": ["phone_master", "tsundere_idol", "fanmade_diva"],
#             "forms": ["base_form", "phone_mode", "tsundere_state"],
#             "abilities": ["phone_mastery", "attitude_projection", "tsundere_power"],
#             "relationships": ["derivative_family", "miku's_rival", "fan_creation"],
#             "outfits": ["yellow_outfit", "casual_wear", "phone_costume"],
#             "gelbooru": ["akita_neru", "neru_%28derivative%29"],
#             "danbooru": ["akita_neru", "derivative"]
#         },
#         "haku": {
#             "names": ["yowane_haku", "failed_miku", "white_voice"],
#             "titles": ["failed_diva", "drinking_queen", "mirror_shadow"],
#             "forms": ["base_form", "drunk_form", "depression_mode"],
#             "abilities": ["deep_voice", "drinking_tolerance", "mirror_singing"],
#             "relationships": ["derivative_family", "miku's_shadow", "neru's_friend"],
#             "outfits": ["grey_outfit", "drinking_clothes", "mirror_costume"],
#             "gelbooru": ["yowane_haku", "haku_%28derivative%29"],
#             "danbooru": ["yowane_haku", "derivative"]
#         },
#
#         # "miku": {
#         #     "gelbooru": [
#         #         "hatsune_miku",
#         #         "miku_%28vocaloid%29",
#         #         "initial_miku",
#         #         "miku_%28project_diva%29"
#         #     ],
#         #     "danbooru": [
#         #         "hatsune_miku",
#         #         "miku_(vocaloid)",
#         #         "project_diva"
#         #     ]
#         # },
#         # "meiko": {
#         #     "gelbooru": ["meiko_%28vocaloid%29", "meiko_%28project_diva%29"],
#         #     "danbooru": ["meiko_(vocaloid)", "project_diva"]
#         # },
#         # "rin": {
#         #     "gelbooru": [
#         #         "kagamine_rin",
#         #         "rin_%28vocaloid%29",
#         #         "rin_%28project_diva%29"
#         #     ],
#         #     "danbooru": ["kagamine_rin", "rin_(vocaloid)"]
#         # },
#         #
#         # # Popular derivatives
#         # "teto": {
#         #     "gelbooru": ["kasane_teto", "utau", "teto_%28utau%29"],
#         #     "danbooru": ["kasane_teto", "utau"]
#         # },
#         # "neru": {
#         #     "gelbooru": ["akita_neru", "neru_%28derivative%29"],
#         #     "danbooru": ["akita_neru", "derivative"]
#         # },
#         # "haku": {
#         #     "gelbooru": ["yowane_haku", "haku_%28derivative%29"],
#         #     "danbooru": ["yowane_haku", "derivative"]
#         # },
#         #
#         # # Additional Vocaloids
#         # "luka": {
#         #     "gelbooru": [
#         #         "megurine_luka",
#         #         "luka_%28vocaloid%29",
#         #         "luka_%28project_diva%29"
#         #     ],
#         #     "danbooru": ["megurine_luka", "project_diva"]
#         # },
#         # "gumi": {
#         #     "gelbooru": ["gumi_%28vocaloid%29", "megpoid"],
#         #     "danbooru": ["gumi", "megpoid"]
#         # },
#         # "ia": {
#         #     "gelbooru": ["ia_%28vocaloid%29", "aria_planetes"],
#         #     "danbooru": ["ia_(vocaloid)", "aria"]
#         # },
#         # "yukari": {
#         #     "gelbooru": ["yuzuki_yukari", "yukari_%28vocaloid%29"],
#         #     "danbooru": ["yuzuki_yukari", "voiceroid"]
#         # }
#     }
#
#     LYCORIS_RECOIL_TAGS = {
#         "chisato": {
#             "names": ["nishikigi_chisato", "chisato", "lycoris_number_08"],
#             "titles": ["former_top_lycoris", "cafe_worker", "artificial_heart_bearer"],
#             "forms": ["base_form", "combat_mode", "cafe_uniform", "civilian_disguise"],
#             "abilities": ["superhuman_reflexes", "bullet_deflection", "close_combat_mastery"],
#             "relationships": ["takina's_partner", "mizuki's_subordinate", "yoshimatsu's_patient"],
#             "outfits": ["cafe_uniform", "casual_wear", "combat_gear", "school_uniform"],
#             "gelbooru": ["nishikigi_chisato", "lycoris", "artificial_heart"],
#             "danbooru": ["nishikigi_chisato", "blonde_hair"]
#         },
#
#         "takina": {
#             "names": ["inoue_takina", "takina", "lycoris_trainee"],
#             "titles": ["former_da_member", "cafe_worker", "elite_lycoris"],
#             "forms": ["base_form", "combat_mode", "cafe_uniform", "trainee_form"],
#             "abilities": ["marksmanship", "tactical_analysis", "close_quarters_combat"],
#             "relationships": ["chisato's_partner", "mizuki's_subordinate", "da_outcast"],
#             "outfits": ["cafe_uniform", "combat_gear", "casual_wear", "school_uniform"],
#             "gelbooru": ["inoue_takina", "lycoris", "da_trainee"],
#             "danbooru": ["inoue_takina", "black_hair"]
#         },
#
#         "himegama": {
#             "names": ["himegama", "instructor_himegama", "training_master"],
#             "titles": ["lycoris_instructor", "combat_teacher", "training_specialist"],
#             "forms": ["base_form", "instructor_mode", "combat_form"],
#             "abilities": ["combat_training", "tactical_instruction", "leadership"],
#             "relationships": ["lycoris_trainer", "takina's_instructor", "da_member"],
#             "outfits": ["instructor_uniform", "combat_gear", "formal_wear"],
#             "gelbooru": ["himegama_%28lycoris_recoil%29", "instructor"],
#             "danbooru": ["himegama", "teacher"]
#         },
#         "mika": {
#             "names": ["mika", "cafe_owner", "lilybell_manager"],
#             "titles": ["cafe_manager", "business_owner", "lycoris_supporter"],
#             "forms": ["base_form", "manager_mode", "casual_form"],
#             "abilities": ["business_management", "coffee_brewing", "support_operations"],
#             "relationships": ["chisato's_employer", "takina's_boss", "cafe_owner"],
#             "outfits": ["cafe_uniform", "casual_wear", "business_attire"],
#             "gelbooru": ["mika_%28lycoris_recoil%29", "cafe_owner"],
#             "danbooru": ["mika_(lycoris_recoil)", "cafe_manager"]
#         },
#
#         # "chisato": {
#         #     "gelbooru": ["nishikigi_chisato", "lycoris", "artificial_heart"],
#         #     "danbooru": ["nishikigi_chisato", "blonde_hair"]
#         # },
#         # "takina": {
#         #     "gelbooru": ["inoue_takina", "lycoris", "da_trainee"],
#         #     "danbooru": ["inoue_takina", "black_hair"]
#         # },
#         # "mizuki": {
#         #     "gelbooru": ["nakahara_mizuki", "radio_operator"],
#         #     "danbooru": ["nakahara_mizuki", "commander"]
#         # },
#         # "kurumi": {
#         #     "gelbooru": ["kurumi_%28lycoris_recoil%29", "walnut", "hacker"],
#         #     "danbooru": ["kurumi_(lycoris_recoil)", "hacker"]
#         # },
#         # "sakura": {
#         #     "gelbooru": ["otome_sakura", "lycoris"],
#         #     "danbooru": ["otome_sakura", "division_commander"]
#         # },
#         # "himegama": {
#         #     "gelbooru": ["himegama_%28lycoris_recoil%29", "instructor"],
#         #     "danbooru": ["himegama", "teacher"]
#         # },
#         # "mika": {
#         #     "gelbooru": ["mika_%28lycoris_recoil%29", "cafe_owner"],
#         #     "danbooru": ["mika_(lycoris_recoil)", "cafe_manager"]
#         # }
#     }
#
#     FAIRY_TAIL_TAGS = {
#         "erza": {
#             "names": ["erza_scarlet", "titania", "queen_of_fairies"],
#             "titles": ["s_class_wizard", "fairy_queen", "requip_master"],
#             "forms": ["base_form", "heaven's_wheel", "black_wing", "purgatory", "clear_heart"],
#             "abilities": ["requip_magic", "sword_magic", "telekinesis", "artificial_eye"],
#             "relationships": ["jellal's_childhood_friend", "team_natsu_member", "fairy_tail_s_class"],
#             "outfits": ["heart_kreuz_armor", "heaven's_wheel_armor", "flight_armor", "casual_wear"],
#             "gelbooru": ["erza_scarlet", "titania", "requip_mage"],
#             "danbooru": ["erza_scarlet", "knight"]
#         },
#
#         "lucy": {
#             "names": ["lucy_heartfilia", "lucky_lucy", "princess"],
#             "titles": ["celestial_wizard", "heartfilia_heiress", "fairy_tail_wizard"],
#             "forms": ["base_form", "star_dress_aquarius", "star_dress_leo", "star_dress_virgo"],
#             "abilities": ["celestial_spirit_magic", "urano_metria", "gottfried", "star_dress"],
#             "relationships": ["team_natsu_member", "heartfilia_heiress", "natsu's_partner"],
#             "outfits": ["default_outfit", "star_dress_forms", "celestial_clothes", "casual_wear"],
#             "gelbooru": ["lucy_heartfilia", "celestial_wizard", "fairy_tail"],
#             "danbooru": ["lucy_heartfilia", "celestial_spirit_mage"]
#         },
#
#         "mirajane": {
#             "names": ["mirajane_strauss", "demon_mirajane", "mira"],
#             "titles": ["s_class_wizard", "she_devil", "takeover_master"],
#             "forms": ["base_form", "satan_soul", "sitri", "halphas"],
#             "abilities": ["takeover_magic", "transformation_magic", "demon_powers"],
#             "relationships": ["strauss_sibling", "fairy_tail_s_class", "model"],
#             "outfits": ["bar_dress", "demon_forms", "photo_shoot_attire", "casual_wear"],
#             "gelbooru": ["mirajane_strauss", "demon_takeover", "s_class"],
#             "danbooru": ["mirajane_strauss", "demon_mirajane"]
#         },
#         "wendy": {
#             "names": ["wendy_marvell", "sky_maiden", "sky_sorceress"],
#             "titles": ["sky_dragon_slayer", "healing_wizard", "maiden_of_the_sky"],
#             "forms": ["base_form", "dragon_force", "enchantment_mode"],
#             "abilities": ["sky_dragon_slayer_magic", "healing_magic", "support_enchantments"],
#             "relationships": ["team_natsu_member", "carla's_partner", "grandeeney's_daughter"],
#             "outfits": ["default_outfit", "dragon_force_form", "school_uniform", "casual_wear"],
#             "gelbooru": ["wendy_marvell", "sky_dragon_slayer", "dragon_force"],
#             "danbooru": ["wendy_marvell", "sky_maiden"]
#         },
#         "juvia": {
#             "names": ["juvia_lockser", "juvia_of_the_deep", "rain_woman"],
#             "titles": ["water_wizard", "former_phantom", "fairy_tail_member"],
#             "forms": ["base_form", "water_body", "rage_mode"],
#             "abilities": ["water_magic", "water_body", "water_lock"],
#             "relationships": ["gray's_admirer", "fairy_tail_member", "former_phantom_lord"],
#             "outfits": ["blue_outfit", "swimsuit", "winter_coat", "casual_wear"],
#             "gelbooru": ["juvia_lockser", "water_mage", "gray_stalker"],
#             "danbooru": ["juvia_lockser", "water_woman"]
#         },
#         "mavis": {
#             "names": ["mavis_vermillion", "fairy_tactician", "first_master"],
#             "titles": ["fairy_strategist", "founding_master", "fairy_heart"],
#             "forms": ["base_form", "astral_form", "fairy_heart_form"],
#             "abilities": ["illusion_magic", "fairy_law", "fairy_sphere"],
#             "relationships": ["zeref's_love", "fairy_tail_founder", "zera's_friend"],
#             "outfits": ["founding_dress", "fairy_wings", "casual_dress"],
#             "gelbooru": ["mavis_vermillion", "fairy_tactician", "first_master"],
#             "danbooru": ["mavis_vermillion", "founding_master"]
#         },
#
#         "brandish": {
#             "names": ["brandish_μ", "country_demolisher", "mass_manipulator"],
#             "titles": ["spriggan_12", "country_toppler", "mass_manipulation_mage"],
#             "forms": ["base_form", "battle_mode", "relaxed_form"],
#             "abilities": ["mass_manipulation", "country_level_magic", "size_alteration"],
#             "relationships": ["spriggan_12_member", "dimaria's_friend", "lucy's_admirer"],
#             "outfits": ["revealing_outfit", "swimsuit", "spriggan_uniform"],
#             "gelbooru": ["brandish_μ", "spriggan_12", "mass_manipulation"],
#             "danbooru": ["brandish", "country_toppler"]
#         },
#         "dimaria": {
#             "names": ["dimaria_yesta", "time_goddess", "valkyrie"],
#             "titles": ["spriggan_12", "chronos_avatar", "war_goddess"],
#             "forms": ["base_form", "god_soul_chronos", "valkyrie_form"],
#             "abilities": ["time_manipulation", "god_soul_takeover", "age_seal"],
#             "relationships": ["spriggan_12_member", "brandish's_friend", "chronos_vessel"],
#             "outfits": ["armor_outfit", "valkyrie_gear", "casual_wear"],
#             "gelbooru": ["dimaria_yesta", "spriggan_12", "age_seal"],
#             "danbooru": ["dimaria_yesta", "time_goddess"]
#         },
#
#         # "lucy": {
#         #     "gelbooru": ["lucy_heartfilia", "celestial_wizard", "fairy_tail"],
#         #     "danbooru": ["lucy_heartfilia", "celestial_spirit_mage"]
#         # },
#         # "erza": {
#         #     "gelbooru": ["erza_scarlet", "titania", "requip_mage"],
#         #     "danbooru": ["erza_scarlet", "knight"]
#         # },
#         # "mirajane": {
#         #     "gelbooru": ["mirajane_strauss", "demon_takeover", "s_class"],
#         #     "danbooru": ["mirajane_strauss", "demon_mirajane"]
#         # },
#         # "wendy": {
#         #     "gelbooru": ["wendy_marvell", "sky_dragon_slayer", "dragon_force"],
#         #     "danbooru": ["wendy_marvell", "sky_maiden"]
#         # },
#         # "juvia": {
#         #     "gelbooru": ["juvia_lockser", "water_mage", "gray_stalker"],
#         #     "danbooru": ["juvia_lockser", "water_woman"]
#         # },
#         # "mavis": {
#         #     "gelbooru": ["mavis_vermillion", "fairy_tactician", "first_master"],
#         #     "danbooru": ["mavis_vermillion", "founding_master"]
#         # },
#         # "brandish": {
#         #     "gelbooru": ["brandish_μ", "spriggan_12", "mass_manipulation"],
#         #     "danbooru": ["brandish", "country_toppler"]
#         # },
#         # "dimaria": {
#         #     "gelbooru": ["dimaria_yesta", "spriggan_12", "age_seal"],
#         #     "danbooru": ["dimaria_yesta", "time_goddess"]
#         # }
#     }
#
#     ONE_PUNCH_MAN_TAGS = {
#         "fubuki": {
#             "names": ["fubuki", "hellish_blizzard", "blizzard_of_hell"],
#             "titles": ["b_class_rank_1", "group_leader", "esper_prodigy"],
#             "forms": ["base_form", "psychic_mode", "battle_form"],
#             "abilities": ["psychokinesis", "telekinesis", "hell_storm", "psychic_whirlwind"],
#             "relationships": ["tatsumaki's_sister", "blizzard_group_leader", "saitama_group_ally"],
#             "outfits": ["hero_dress", "casual_wear", "battle_outfit", "formal_attire"],
#             "gelbooru": ["fubuki", "blizzard", "hellish_blizzard", "b_class_hero"],
#             "danbooru": ["fubuki", "tornado_sister"]
#         },
#
#         "tatsumaki": {
#             "names": ["tatsumaki", "terrible_tornado", "tornado_of_terror"],
#             "titles": ["s_class_rank_2", "strongest_esper", "hero_association_elite"],
#             "forms": ["base_form", "full_power", "serious_mode"],
#             "abilities": ["psychokinesis", "flight", "barrier_creation", "energy_projection"],
#             "relationships": ["fubuki's_sister", "blast's_acquaintance", "hero_association_member"],
#             "outfits": ["hero_dress", "casual_wear", "battle_damaged"],
#             "gelbooru": ["tatsumaki", "tornado_terror", "s_class_hero"],
#             "danbooru": ["tatsumaki", "tornado"]
#         },
#
#         "psykos": {
#             "names": ["psykos", "monster_queen", "esper_leader"],
#             "titles": ["monster_association_executive", "esper_genius", "monster_queen"],
#             "forms": ["base_form", "monster_form", "psykos_orochi"],
#             "abilities": ["psychic_powers", "monster_transformation", "future_vision"],
#             "relationships": ["monster_association_leader", "fubuki's_former_friend", "orochi's_creator"],
#             "outfits": ["monster_form", "human_form", "battle_dress"],
#             "gelbooru": ["psykos", "monster_association", "esper"],
#             "danbooru": ["psykos", "monster_executive"]
#         },
#         "do_s": {
#             "names": ["do-s", "monster_princess", "dominatrix_monster"],
#             "titles": ["monster_princess", "demon_level_threat", "whip_master"],
#             "forms": ["base_form", "monster_form", "battle_mode"],
#             "abilities": ["mind_control", "whip_mastery", "superhuman_strength"],
#             "relationships": ["monster_association_member", "sweet_mask's_opponent"],
#             "outfits": ["monster_suit", "battle_armor", "dominatrix_gear"],
#             "gelbooru": ["do-s", "monster_princess", "whip"],
#             "danbooru": ["monster_princess", "dominatrix_monster"]
#         },
#         "lin_lin": {
#             "names": ["lin_lin", "martial_artist", "tournament_fighter"],
#             "titles": ["super_fight_contestant", "martial_artist", "fighter"],
#             "forms": ["base_form", "fighting_stance", "tournament_mode"],
#             "abilities": ["martial_arts", "combat_expertise", "fighting_techniques"],
#             "relationships": ["super_fight_participant", "martial_arts_community"],
#             "outfits": ["fighting_gear", "tournament_uniform", "training_clothes"],
#             "gelbooru": ["lin_lin_%28one-punch_man%29", "martial_artist"],
#             "danbooru": ["lin_lin", "super_fight"]
#         },
#
#         "suiko": {
#             "names": ["suiko", "tank_top_girl", "martial_artist"],
#             "titles": ["tank_top_member", "martial_arts_prodigy", "fighter"],
#             "forms": ["base_form", "fighting_stance", "training_mode"],
#             "abilities": ["martial_arts", "tank_top_magic", "combat_expertise"],
#             "relationships": ["tank_top_group", "suiryu's_sister", "martial_artist"],
#             "outfits": ["tank_top", "martial_arts_gear", "casual_wear"],
#             "gelbooru": ["suiko_%28one-punch_man%29", "tank_top_group"],
#             "danbooru": ["suiko", "tank_topper"]
#         },
#
#         # "fubuki": {
#         #     "gelbooru": ["fubuki", "blizzard", "hellish_blizzard", "b_class_hero"],
#         #     "danbooru": ["fubuki", "tornado_sister"]
#         # },
#         # "tatsumaki": {
#         #     "gelbooru": ["tatsumaki", "tornado_terror", "s_class_hero"],
#         #     "danbooru": ["tatsumaki", "tornado"]
#         # },
#         # "psykos": {
#         #     "gelbooru": ["psykos", "monster_association", "esper"],
#         #     "danbooru": ["psykos", "monster_executive"]
#         # },
#         # "do_s": {
#         #     "gelbooru": ["do-s", "monster_princess", "whip"],
#         #     "danbooru": ["monster_princess", "dominatrix_monster"]
#         # },
#         # "lin_lin": {
#         #     "gelbooru": ["lin_lin_%28one-punch_man%29", "martial_artist"],
#         #     "danbooru": ["lin_lin", "super_fight"]
#         # },
#         # "suiko": {
#         #     "gelbooru": ["suiko_%28one-punch_man%29", "tank_top_group"],
#         #     "danbooru": ["suiko", "tank_topper"]
#         # }
#     }
#
# class URLs:
#     """Central URL configuration for all scrapers and characters"""
#
#     # Base URLs for different sites
#     GELBOORU_BASE = "https://gelbooru.com/index.php?page=post&s=list&tags="
#     DANBOORU_BASE = "https://danbooru.donmai.us/posts?tags="
#
#     # One Piece Characters
#     ONE_PIECE_URLS = {
#         # Main crew and allies
#         "nami": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}nami+",
#                 f"{GELBOORU_BASE}nami_(one_piece)+",
#                 f"{GELBOORU_BASE}cat_burglar_nami+",
#                 f"{GELBOORU_BASE}weather_witch+",
#                 f"{GELBOORU_BASE}climatact+nami+",
#                 f"{GELBOORU_BASE}post_timeskip_nami+",
#                 f"{GELBOORU_BASE}pre_timeskip_nami+",
#                 f"{GELBOORU_BASE}wano_nami+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}nami+",
#                 f"{DANBOORU_BASE}nami_(one_piece)+",
#                 f"{DANBOORU_BASE}cat_burglar+",
#                 f"{DANBOORU_BASE}weather_control+nami+"
#             ]
#         },
#
#         "robin": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}nico_robin+",
#                 f"{GELBOORU_BASE}robin_(one_piece)+",
#                 f"{GELBOORU_BASE}devil_child+",
#                 f"{GELBOORU_BASE}hana_hana_no_mi+",
#                 f"{GELBOORU_BASE}post_timeskip_robin+",
#                 f"{GELBOORU_BASE}pre_timeskip_robin+",
#                 f"{GELBOORU_BASE}wano_robin+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}nico_robin+",
#                 f"{DANBOORU_BASE}robin_(one_piece)+",
#                 f"{DANBOORU_BASE}hana_hana_no_mi+"
#             ]
#         },
#
#         "yamato": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}yamato+",
#                 f"{GELBOORU_BASE}yamato_(one_piece)+",
#                 f"{GELBOORU_BASE}oni_princess+",
#                 f"{GELBOORU_BASE}hybrid_form+yamato+",
#                 f"{GELBOORU_BASE}ice_oni+yamato+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}yamato_(one_piece)+",
#                 f"{DANBOORU_BASE}oni_princess+",
#                 f"{DANBOORU_BASE}hybrid_form+yamato+"
#             ]
#         },
#
#         # Charlotte Family
#         "big_mom": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}charlotte_linlin+",
#                 f"{GELBOORU_BASE}big_mom+",
#                 f"{GELBOORU_BASE}big_mom_(one_piece)+",
#                 f"{GELBOORU_BASE}young_linlin+",
#                 f"{GELBOORU_BASE}soul_soul_fruit+",
#                 f"{GELBOORU_BASE}yonko+big_mom+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}charlotte_linlin+",
#                 f"{DANBOORU_BASE}big_mom_(one_piece)+",
#                 f"{DANBOORU_BASE}soul_soul_fruit+"
#             ]
#         },
#
#         "smoothie": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}charlotte_smoothie+",
#                 f"{GELBOORU_BASE}smoothie_(one_piece)+",
#                 f"{GELBOORU_BASE}sweet_commander+smoothie+",
#                 f"{GELBOORU_BASE}wring_wring_fruit+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}charlotte_smoothie+",
#                 f"{DANBOORU_BASE}smoothie_(one_piece)+",
#                 f"{DANBOORU_BASE}sweet_commander+"
#             ]
#         },
#
#         "pudding": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}charlotte_pudding+",
#                 f"{GELBOORU_BASE}pudding_(one_piece)+",
#                 f"{GELBOORU_BASE}three_eye_tribe+",
#                 f"{GELBOORU_BASE}memo_memo_no_mi+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}charlotte_pudding+",
#                 f"{DANBOORU_BASE}pudding_(one_piece)+",
#                 f"{DANBOORU_BASE}three_eye_tribe+"
#             ]
#         },
#
#         "brulee": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}charlotte_brulee+",
#                 f"{GELBOORU_BASE}brulee_(one_piece)+",
#                 f"{GELBOORU_BASE}mirror_mirror_fruit+",
#                 f"{GELBOORU_BASE}mirror_world+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}charlotte_brulee+",
#                 f"{DANBOORU_BASE}brulee_(one_piece)+",
#                 f"{DANBOORU_BASE}mirror_world+"
#             ]
#         },
#
#         "komurasaki": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}kozuki_hiyori+",
#                 f"{GELBOORU_BASE}komurasaki+",
#                 f"{GELBOORU_BASE}hiyori_(one_piece)+",
#                 f"{GELBOORU_BASE}oiran+hiyori+",
#                 f"{GELBOORU_BASE}princess_hiyori+",
#                 f"{GELBOORU_BASE}wano_arc+hiyori+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}kozuki_hiyori+",
#                 f"{DANBOORU_BASE}komurasaki+",
#                 f"{DANBOORU_BASE}hiyori_(one_piece)+"
#             ]
#         },
#
#         "ulti": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}ulti+",
#                 f"{GELBOORU_BASE}ulti_(one_piece)+",
#                 f"{GELBOORU_BASE}tobi_roppo+ulti+",
#                 f"{GELBOORU_BASE}dinosaur_form+ulti+",
#                 f"{GELBOORU_BASE}beast_pirates+ulti+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}ulti+",
#                 f"{DANBOORU_BASE}ulti_(one_piece)+",
#                 f"{DANBOORU_BASE}tobi_roppo+ulti+"
#             ]
#         },
#
#         "black_maria": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}black_maria+",
#                 f"{GELBOORU_BASE}black_maria_(one_piece)+",
#                 f"{GELBOORU_BASE}spider_form+maria+",
#                 f"{GELBOORU_BASE}tobi_roppo+maria+",
#                 f"{GELBOORU_BASE}beast_pirates+black_maria+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}black_maria+",
#                 f"{DANBOORU_BASE}black_maria_(one_piece)+",
#                 f"{DANBOORU_BASE}spider_form+maria+"
#             ]
#         },
#
#         "o_kiku": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}kikunojo+",
#                 f"{GELBOORU_BASE}o_kiku+",
#                 f"{GELBOORU_BASE}kiku_(one_piece)+",
#                 f"{GELBOORU_BASE}red_scabbard+kiku+",
#                 f"{GELBOORU_BASE}samurai+kiku+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}kikunojo+",
#                 f"{DANBOORU_BASE}o_kiku+",
#                 f"{DANBOORU_BASE}kiku_(one_piece)+"
#             ]
#         },
#
#         "o_toko": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}toko+",
#                 f"{GELBOORU_BASE}o_toko+",
#                 f"{GELBOORU_BASE}toko_(one_piece)+",
#                 f"{GELBOORU_BASE}kamuro+toko+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}toko+",
#                 f"{DANBOORU_BASE}o_toko+",
#                 f"{DANBOORU_BASE}toko_(one_piece)+"
#             ]
#         },
#
#         "o_tsuru": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}tsuru+wano+",
#                 f"{GELBOORU_BASE}o_tsuru+",
#                 f"{GELBOORU_BASE}tsuru_(one_piece_wano)+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}tsuru+wano+",
#                 f"{DANBOORU_BASE}o_tsuru+",
#                 f"{DANBOORU_BASE}tsuru_(one_piece_wano)+"
#             ]
#         },
#
#         "speed": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}speed+",
#                 f"{GELBOORU_BASE}speed_(one_piece)+",
#                 f"{GELBOORU_BASE}headliner+speed+",
#                 f"{GELBOORU_BASE}horse_smile+speed+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}speed+",
#                 f"{DANBOORU_BASE}speed_(one_piece)+",
#                 f"{DANBOORU_BASE}smile_user+speed+"
#             ]
#         },
#
#         "boa_hancock": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}boa_hancock+",
#                 f"{GELBOORU_BASE}hancock_(one_piece)+",
#                 f"{GELBOORU_BASE}pirate_empress+",
#                 f"{GELBOORU_BASE}snake_princess+",
#                 f"{GELBOORU_BASE}love_love_fruit+hancock+",
#                 f"{GELBOORU_BASE}shichibukai+hancock+",
#                 f"{GELBOORU_BASE}kuja_pirates+hancock+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}boa_hancock+",
#                 f"{DANBOORU_BASE}hancock_(one_piece)+",
#                 f"{DANBOORU_BASE}pirate_empress+",
#                 f"{DANBOORU_BASE}snake_princess+"
#             ]
#         },
#
#         "sandersonia": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}boa_sandersonia+",
#                 f"{GELBOORU_BASE}sandersonia_(one_piece)+",
#                 f"{GELBOORU_BASE}gorgon_sister+sandersonia+",
#                 f"{GELBOORU_BASE}snake_form+sandersonia+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}boa_sandersonia+",
#                 f"{DANBOORU_BASE}sandersonia_(one_piece)+",
#                 f"{DANBOORU_BASE}gorgon_sister+"
#             ]
#         },
#
#         "marigold": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}boa_marigold+",
#                 f"{GELBOORU_BASE}marigold_(one_piece)+",
#                 f"{GELBOORU_BASE}gorgon_sister+marigold+",
#                 f"{GELBOORU_BASE}snake_form+marigold+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}boa_marigold+",
#                 f"{DANBOORU_BASE}marigold_(one_piece)+",
#                 f"{DANBOORU_BASE}gorgon_sister+"
#             ]
#         },
#
#         "marguerite": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}marguerite+",
#                 f"{GELBOORU_BASE}marguerite_(one_piece)+",
#                 f"{GELBOORU_BASE}kuja_warrior+marguerite+",
#                 f"{GELBOORU_BASE}amazon_lily+marguerite+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}marguerite+",
#                 f"{DANBOORU_BASE}marguerite_(one_piece)+",
#                 f"{DANBOORU_BASE}kuja_warrior+"
#             ]
#         },
#
#         "viola": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}viola+",
#                 f"{GELBOORU_BASE}viola_(one_piece)+",
#                 f"{GELBOORU_BASE}violet+one_piece+",
#                 f"{GELBOORU_BASE}princess_viola+",
#                 f"{GELBOORU_BASE}dancing_queen+viola+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}viola+",
#                 f"{DANBOORU_BASE}viola_(one_piece)+",
#                 f"{DANBOORU_BASE}violet_(one_piece)+"
#             ]
#         },
#
#         "rebecca": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}rebecca+",
#                 f"{GELBOORU_BASE}rebecca_(one_piece)+",
#                 f"{GELBOORU_BASE}gladiator_rebecca+",
#                 f"{GELBOORU_BASE}princess_rebecca+",
#                 f"{GELBOORU_BASE}undefeated_woman+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}rebecca+",
#                 f"{DANBOORU_BASE}rebecca_(one_piece)+",
#                 f"{DANBOORU_BASE}gladiator_rebecca+"
#             ]
#         },
#
#         "scarlett": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}scarlett+",
#                 f"{GELBOORU_BASE}scarlett_(one_piece)+",
#                 f"{GELBOORU_BASE}princess_scarlett+",
#                 f"{GELBOORU_BASE}rebecca's_mother+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}scarlett+",
#                 f"{DANBOORU_BASE}scarlett_(one_piece)+",
#                 f"{DANBOORU_BASE}kyros'_wife+"
#             ]
#         },
#
#         "baby_5": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}baby_5+",
#                 f"{GELBOORU_BASE}baby_5_(one_piece)+",
#                 f"{GELBOORU_BASE}baby_five+",
#                 f"{GELBOORU_BASE}arms_arms_fruit+baby_5+",
#                 f"{GELBOORU_BASE}weapon_form+baby_5+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}baby_5+",
#                 f"{DANBOORU_BASE}baby_5_(one_piece)+",
#                 f"{DANBOORU_BASE}arms_arms_fruit+"
#             ]
#         },
#
#         "tashigi": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}tashigi+",
#                 f"{GELBOORU_BASE}tashigi_(one_piece)+",
#                 f"{GELBOORU_BASE}marine_captain+tashigi+",
#                 f"{GELBOORU_BASE}sword_master+tashigi+",
#                 f"{GELBOORU_BASE}g-5+tashigi+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}tashigi+",
#                 f"{DANBOORU_BASE}tashigi_(one_piece)+",
#                 f"{DANBOORU_BASE}marine_captain+"
#             ]
#         },
#
#         "hina": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}hina+",
#                 f"{GELBOORU_BASE}hina_(one_piece)+",
#                 f"{GELBOORU_BASE}black_cage+hina+",
#                 f"{GELBOORU_BASE}marine_captain+hina+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}hina+",
#                 f"{DANBOORU_BASE}hina_(one_piece)+",
#                 f"{DANBOORU_BASE}black_cage+"
#             ]
#         },
#
#         "momousagi": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}momousagi+",
#                 f"{GELBOORU_BASE}gion+",
#                 f"{GELBOORU_BASE}vice_admiral+momousagi+",
#                 f"{GELBOORU_BASE}pink_rabbit+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}momousagi+",
#                 f"{DANBOORU_BASE}gion+",
#                 f"{DANBOORU_BASE}vice_admiral+"
#             ]
#         },
#
#         "tsuru": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}tsuru+",
#                 f"{GELBOORU_BASE}tsuru_(one_piece)+",
#                 f"{GELBOORU_BASE}great_staff_officer+",
#                 f"{GELBOORU_BASE}marine_legend+tsuru+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}tsuru+",
#                 f"{DANBOORU_BASE}tsuru_(one_piece)+",
#                 f"{DANBOORU_BASE}vice_admiral+tsuru+"
#             ]
#         },
#
#         "stussy": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}stussy+",
#                 f"{GELBOORU_BASE}stussy_(one_piece)+",
#                 f"{GELBOORU_BASE}cp0+stussy+",
#                 f"{GELBOORU_BASE}agent+stussy+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}stussy+",
#                 f"{DANBOORU_BASE}stussy_(one_piece)+",
#                 f"{DANBOORU_BASE}cp0+stussy+"
#             ]
#         },
#
#         "koala": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}koala+",
#                 f"{GELBOORU_BASE}koala_(one_piece)+",
#                 f"{GELBOORU_BASE}revolutionary_army+koala+",
#                 f"{GELBOORU_BASE}fishman_karate+koala+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}koala+",
#                 f"{DANBOORU_BASE}koala_(one_piece)+",
#                 f"{DANBOORU_BASE}revolutionary_army+"
#             ]
#         },
#
#         "belo_betty": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}belo_betty+",
#                 f"{GELBOORU_BASE}betty_(one_piece)+",
#                 f"{GELBOORU_BASE}east_army_commander+",
#                 f"{GELBOORU_BASE}pump_pump_fruit+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}belo_betty+",
#                 f"{DANBOORU_BASE}betty_(one_piece)+",
#                 f"{DANBOORU_BASE}revolutionary_commander+"
#             ]
#         },
#
#         "lindbergh": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}lindbergh+",
#                 f"{GELBOORU_BASE}lindbergh_(one_piece)+",
#                 f"{GELBOORU_BASE}north_army_commander+",
#                 f"{GELBOORU_BASE}revolutionary_inventor+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}lindbergh+",
#                 f"{DANBOORU_BASE}lindbergh_(one_piece)+",
#                 f"{DANBOORU_BASE}revolutionary_army+"
#             ]
#         },
#
#         "karasu": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}karasu+",
#                 f"{GELBOORU_BASE}karasu_(one_piece)+",
#                 f"{GELBOORU_BASE}crow_commander+",
#                 f"{GELBOORU_BASE}revolutionary_commander+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}karasu+",
#                 f"{DANBOORU_BASE}karasu_(one_piece)+",
#                 f"{DANBOORU_BASE}revolutionary_army+"
#             ]
#         },
#
#         "bellemere": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}bellemere+",
#                 f"{GELBOORU_BASE}bell-mère+",
#                 f"{GELBOORU_BASE}belle_mere_(one_piece)+",
#                 f"{GELBOORU_BASE}marine_bellemere+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}bellemere+",
#                 f"{DANBOORU_BASE}bell-mère+",
#                 f"{DANBOORU_BASE}belle_mere_(one_piece)+"
#             ]
#         },
#
#         "isuka": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}isuka+",
#                 f"{GELBOORU_BASE}isuka_(one_piece)+",
#                 f"{GELBOORU_BASE}marine_captain+isuka+",
#                 f"{GELBOORU_BASE}smoke_smoke_fruit+isuka+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}isuka+",
#                 f"{DANBOORU_BASE}isuka_(one_piece)+",
#                 f"{DANBOORU_BASE}marine_captain+"
#             ]
#         },
#
#         "ain": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}ain+",
#                 f"{GELBOORU_BASE}ain_(one_piece)+",
#                 f"{GELBOORU_BASE}neo_marines+ain+",
#                 f"{GELBOORU_BASE}modo_modo_no_mi+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}ain+",
#                 f"{DANBOORU_BASE}ain_(one_piece)+",
#                 f"{DANBOORU_BASE}neo_marines+"
#             ]
#         },
#
#         "sadi": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}sadi+",
#                 f"{GELBOORU_BASE}sadi_(one_piece)+",
#                 f"{GELBOORU_BASE}chief_guard+sadi+",
#                 f"{GELBOORU_BASE}impel_down+sadi+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}sadi+",
#                 f"{DANBOORU_BASE}sadi_(one_piece)+",
#                 f"{DANBOORU_BASE}impel_down+"
#             ]
#         },
#
#         "domino": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}domino+",
#                 f"{GELBOORU_BASE}domino_(one_piece)+",
#                 f"{GELBOORU_BASE}vice_chief_guard+",
#                 f"{GELBOORU_BASE}impel_down+domino+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}domino+",
#                 f"{DANBOORU_BASE}domino_(one_piece)+",
#                 f"{DANBOORU_BASE}impel_down+"
#             ]
#         },
#
#         "charlotte_pudding": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}charlotte_pudding+",
#                 f"{GELBOORU_BASE}pudding_(one_piece)+",
#                 f"{GELBOORU_BASE}three_eye_tribe+",
#                 f"{GELBOORU_BASE}charlotte_family+pudding+",
#                 f"{GELBOORU_BASE}minister_of_chocolate+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}charlotte_pudding+",
#                 f"{DANBOORU_BASE}pudding_(one_piece)+",
#                 f"{DANBOORU_BASE}three_eye_tribe+"
#             ]
#         },
#
#         "charlotte_smoothie": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}charlotte_smoothie+",
#                 f"{GELBOORU_BASE}smoothie_(one_piece)+",
#                 f"{GELBOORU_BASE}sweet_commander+smoothie+",
#                 f"{GELBOORU_BASE}minister_of_juice+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}charlotte_smoothie+",
#                 f"{DANBOORU_BASE}smoothie_(one_piece)+",
#                 f"{DANBOORU_BASE}sweet_commander+"
#             ]
#         },
#
#         "charlotte_amande": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}charlotte_amande+",
#                 f"{GELBOORU_BASE}amande_(one_piece)+",
#                 f"{GELBOORU_BASE}minister_of_nuts+",
#                 f"{GELBOORU_BASE}snake_neck+amande+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}charlotte_amande+",
#                 f"{DANBOORU_BASE}amande_(one_piece)+",
#                 f"{DANBOORU_BASE}minister_of_nuts+"
#             ]
#         },
#
#         "charlotte_flampe": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}charlotte_flampe+",
#                 f"{GELBOORU_BASE}flampe_(one_piece)+",
#                 f"{GELBOORU_BASE}special_forces+flampe+",
#                 f"{GELBOORU_BASE}charlotte_family+flampe+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}charlotte_flampe+",
#                 f"{DANBOORU_BASE}flampe_(one_piece)+",
#                 f"{DANBOORU_BASE}special_forces+"
#             ]
#         },
#
#         "conis": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}conis+",
#                 f"{GELBOORU_BASE}conis_(one_piece)+",
#                 f"{GELBOORU_BASE}skypiean+conis+",
#                 f"{GELBOORU_BASE}angel_island+conis+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}conis+",
#                 f"{DANBOORU_BASE}conis_(one_piece)+",
#                 f"{DANBOORU_BASE}skypiean+"
#             ]
#         },
#
#         "kalifa": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}kalifa+",
#                 f"{GELBOORU_BASE}kalifa_(one_piece)+",
#                 f"{GELBOORU_BASE}cp9+kalifa+",
#                 f"{GELBOORU_BASE}bubble_bubble_fruit+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}kalifa+",
#                 f"{DANBOORU_BASE}kalifa_(one_piece)+",
#                 f"{DANBOORU_BASE}cp9+"
#             ]
#         },
#
#         "mozu_and_kiwi": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}mozu+",
#                 f"{GELBOORU_BASE}kiwi+",
#                 f"{GELBOORU_BASE}square_sisters+",
#                 f"{GELBOORU_BASE}franky_family+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}mozu+",
#                 f"{DANBOORU_BASE}kiwi+",
#                 f"{DANBOORU_BASE}square_sisters+"
#             ]
#         },
#
#         "kumadori's_mother": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}kumadori's_mother+",
#                 f"{GELBOORU_BASE}kumadori_mother+",
#                 f"{GELBOORU_BASE}cp9+mother+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}kumadori's_mother+",
#                 f"{DANBOORU_BASE}kumadori_family+"
#             ]
#         },
#
#         "kureha": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}kureha+",
#                 f"{GELBOORU_BASE}kureha_(one_piece)+",
#                 f"{GELBOORU_BASE}dr_kureha+",
#                 f"{GELBOORU_BASE}drum_kingdom+kureha+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}kureha+",
#                 f"{DANBOORU_BASE}kureha_(one_piece)+",
#                 f"{DANBOORU_BASE}dr_kureha+"
#             ]
#         },
#
#         "porche": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}porche+",
#                 f"{GELBOORU_BASE}porche_(one_piece)+",
#                 f"{GELBOORU_BASE}foxy_pirates+porche+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}porche+",
#                 f"{DANBOORU_BASE}porche_(one_piece)+",
#                 f"{DANBOORU_BASE}foxy_pirates+"
#             ]
#         },
#
#         "marguerite": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}marguerite+",
#                 f"{GELBOORU_BASE}marguerite_(one_piece)+",
#                 f"{GELBOORU_BASE}kuja_warrior+marguerite+",
#                 f"{GELBOORU_BASE}amazon_lily+marguerite+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}marguerite+",
#                 f"{DANBOORU_BASE}marguerite_(one_piece)+",
#                 f"{DANBOORU_BASE}kuja_warrior+"
#             ]
#         },
#
#         "spandam's_secretary": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}spandam's_secretary+",
#                 f"{GELBOORU_BASE}enies_lobby+secretary+",
#                 f"{GELBOORU_BASE}tower_of_justice+staff+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}spandam's_secretary+",
#                 f"{DANBOORU_BASE}enies_lobby+secretary+"
#             ]
#         },
#
#         "kaya": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}kaya+",
#                 f"{GELBOORU_BASE}kaya_(one_piece)+",
#                 f"{GELBOORU_BASE}syrup_village+kaya+",
#                 f"{GELBOORU_BASE}mansion_owner+kaya+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}kaya+",
#                 f"{DANBOORU_BASE}kaya_(one_piece)+",
#                 f"{DANBOORU_BASE}syrup_village+"
#             ]
#         },
#
#         "merry": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}merry+",
#                 f"{GELBOORU_BASE}merry_(one_piece)+",
#                 f"{GELBOORU_BASE}butler+merry+",
#                 f"{GELBOORU_BASE}kaya's_butler+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}merry+",
#                 f"{DANBOORU_BASE}merry_(one_piece)+",
#                 f"{DANBOORU_BASE}butler+"
#             ]
#         },
#
#         "chouchou's_owner": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}hocker+",
#                 f"{GELBOORU_BASE}pet_shop_owner+",
#                 f"{GELBOORU_BASE}orange_town+owner+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}hocker+",
#                 f"{DANBOORU_BASE}pet_shop_owner+"
#             ]
#         },
#
#         "jessica": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}jessica+",
#                 f"{GELBOORU_BASE}jessica_(one_piece)+",
#                 f"{GELBOORU_BASE}g8+jessica+",
#                 f"{GELBOORU_BASE}marine_chef+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}jessica+",
#                 f"{DANBOORU_BASE}jessica_(one_piece)+",
#                 f"{DANBOORU_BASE}g8_arc+"
#             ]
#         },
#
#         "henzo's_grandmother": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}henzo's_grandmother+",
#                 f"{GELBOORU_BASE}ruluka+elder+",
#                 f"{GELBOORU_BASE}rainbow_mist+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}henzo's_grandmother+",
#                 f"{DANBOORU_BASE}ruluka+"
#             ]
#         },
#
#         "akibi": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}akibi+",
#                 f"{GELBOORU_BASE}akibi_(one_piece)+",
#                 f"{GELBOORU_BASE}rainbow_mist+akibi+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}akibi+",
#                 f"{DANBOORU_BASE}akibi_(one_piece)+"
#             ]
#         },
#
#         "yuki": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}yuki+",
#                 f"{GELBOORU_BASE}yuki_(one_piece)+",
#                 f"{GELBOORU_BASE}goat_island+yuki+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}yuki+",
#                 f"{DANBOORU_BASE}yuki_(one_piece)+"
#             ]
#         },
#
#         "lily": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}lily+",
#                 f"{GELBOORU_BASE}lily_(one_piece)+",
#                 f"{GELBOORU_BASE}lovely_land+lily+",
#                 f"{GELBOORU_BASE}spa_island+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}lily+",
#                 f"{DANBOORU_BASE}lily_(one_piece)+"
#             ]
#         },
#
#         "shirahoshi": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}shirahoshi+",
#                 f"{GELBOORU_BASE}shirahoshi_(one_piece)+",
#                 f"{GELBOORU_BASE}mermaid_princess+",
#                 f"{GELBOORU_BASE}poseidon+shirahoshi+",
#                 f"{GELBOORU_BASE}giant_mermaid+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}shirahoshi+",
#                 f"{DANBOORU_BASE}shirahoshi_(one_piece)+",
#                 f"{DANBOORU_BASE}mermaid_princess+"
#             ]
#         },
#
#         "otohime": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}otohime+",
#                 f"{GELBOORU_BASE}otohime_(one_piece)+",
#                 f"{GELBOORU_BASE}queen_otohime+",
#                 f"{GELBOORU_BASE}ryugu_queen+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}otohime+",
#                 f"{DANBOORU_BASE}otohime_(one_piece)+",
#                 f"{DANBOORU_BASE}ryugu_queen+"
#             ]
#         },
#
#         "madam_shyarly": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}madam_shyarly+",
#                 f"{GELBOORU_BASE}shyarly_(one_piece)+",
#                 f"{GELBOORU_BASE}fortune_teller+shyarly+",
#                 f"{GELBOORU_BASE}mermaid_cafe+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}madam_shyarly+",
#                 f"{DANBOORU_BASE}shyarly_(one_piece)+",
#                 f"{DANBOORU_BASE}fortune_teller+"
#             ]
#         },
#
#         "ishilly": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}ishilly+",
#                 f"{GELBOORU_BASE}ishilly_(one_piece)+",
#                 f"{GELBOORU_BASE}mermaid_cafe+ishilly+",
#                 f"{GELBOORU_BASE}mermaid_cove+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}ishilly+",
#                 f"{DANBOORU_BASE}ishilly_(one_piece)+",
#                 f"{DANBOORU_BASE}mermaid_cafe+"
#             ]
#         },
#
#         "lilo": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}lilo+",
#                 f"{GELBOORU_BASE}lilo_(one_piece)+",
#                 f"{GELBOORU_BASE}accino_family+",
#                 f"{GELBOORU_BASE}ice_hunter+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}lilo+",
#                 f"{DANBOORU_BASE}lilo_(one_piece)+"
#             ]
#         },
#
#         "daisy": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}daisy+",
#                 f"{GELBOORU_BASE}daisy_(one_piece)+",
#                 f"{GELBOORU_BASE}little_east_blue+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}daisy+",
#                 f"{DANBOORU_BASE}daisy_(one_piece)+"
#             ]
#         },
#
#         "shuzo's_wife": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}shuzo's_wife+",
#                 f"{GELBOORU_BASE}neo_marines+family+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}shuzo's_wife+",
#                 f"{DANBOORU_BASE}neo_marines+"
#             ]
#         },
#
#         "commander_jonathan's_wife": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}jessica+",
#                 f"{GELBOORU_BASE}jessica_(one_piece)+",
#                 f"{GELBOORU_BASE}navarone+jessica+",
#                 f"{GELBOORU_BASE}g8_base+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}jessica+",
#                 f"{DANBOORU_BASE}jessica_(one_piece)+"
#             ]
#         },
#
#         "lina": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}lina+",
#                 f"{GELBOORU_BASE}lina_(one_piece)+",
#                 f"{GELBOORU_BASE}spa_island+",
#                 f"{GELBOORU_BASE}spa_worker+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}lina+",
#                 f"{DANBOORU_BASE}lina_(one_piece)+"
#             ]
#         },
#
#         "komei's_sister": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}komei's_sister+",
#                 f"{GELBOORU_BASE}nebulandia+",
#                 f"{GELBOORU_BASE}marine_family+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}komei's_sister+",
#                 f"{DANBOORU_BASE}nebulandia+"
#             ]
#         },
#
#         "myskina_acier": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}myskina_acier+",
#                 f"{GELBOORU_BASE}silver_mine+",
#                 f"{GELBOORU_BASE}resistance_fighter+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}myskina_acier+",
#                 f"{DANBOORU_BASE}silver_mine+"
#             ]
#         },
#
#         "carmel": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}carmel+",
#                 f"{GELBOORU_BASE}carmel_(one_piece)+",
#                 f"{GELBOORU_BASE}marine_rookie+",
#                 f"{GELBOORU_BASE}training_marine+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}carmel+",
#                 f"{DANBOORU_BASE}carmel_(one_piece)+",
#                 f"{DANBOORU_BASE}marine_rookie+"
#             ]
#         },
#
#         "ishigo_shitemanna": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}ishigo+",
#                 f"{GELBOORU_BASE}ishigo_(one_piece)+",
#                 f"{GELBOORU_BASE}cidre_guild+",
#                 f"{GELBOORU_BASE}guild_brewer+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}ishigo+",
#                 f"{DANBOORU_BASE}ishigo_(one_piece)+",
#                 f"{DANBOORU_BASE}cidre_guild+"
#             ]
#         },
#
#         "bonham": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}bonham+",
#                 f"{GELBOORU_BASE}bonham_(one_piece)+",
#                 f"{GELBOORU_BASE}marine_instructor+",
#                 f"{GELBOORU_BASE}training_officer+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}bonham+",
#                 f"{DANBOORU_BASE}bonham_(one_piece)+",
#                 f"{DANBOORU_BASE}marine_instructor+"
#             ]
#         },
#
#         "udetsuki": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}udetsuki+",
#                 f"{GELBOORU_BASE}udetsuki_(one_piece)+",
#                 f"{GELBOORU_BASE}cidre_guild+executive+",
#                 f"{GELBOORU_BASE}guild_leader+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}udetsuki+",
#                 f"{DANBOORU_BASE}udetsuki_(one_piece)+",
#                 f"{DANBOORU_BASE}cidre_executive+"
#             ]
#         },
#
#         "carmel": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}carmel+",
#                 f"{GELBOORU_BASE}carmel_(one_piece)+",
#                 f"{GELBOORU_BASE}marine_rookie+",
#                 f"{GELBOORU_BASE}training_marine+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}carmel+",
#                 f"{DANBOORU_BASE}carmel_(one_piece)+",
#                 f"{DANBOORU_BASE}marine_rookie+"
#             ]
#         },
#
#         "ishigo_shitemanna": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}ishigo+",
#                 f"{GELBOORU_BASE}ishigo_(one_piece)+",
#                 f"{GELBOORU_BASE}cidre_guild+",
#                 f"{GELBOORU_BASE}guild_brewer+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}ishigo+",
#                 f"{DANBOORU_BASE}ishigo_(one_piece)+",
#                 f"{DANBOORU_BASE}cidre_guild+"
#             ]
#         },
#
#         "bonham": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}bonham+",
#                 f"{GELBOORU_BASE}bonham_(one_piece)+",
#                 f"{GELBOORU_BASE}marine_instructor+",
#                 f"{GELBOORU_BASE}training_officer+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}bonham+",
#                 f"{DANBOORU_BASE}bonham_(one_piece)+",
#                 f"{DANBOORU_BASE}marine_instructor+"
#             ]
#         },
#
#         "udetsuki": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}udetsuki+",
#                 f"{GELBOORU_BASE}udetsuki_(one_piece)+",
#                 f"{GELBOORU_BASE}cidre_guild+executive+",
#                 f"{GELBOORU_BASE}guild_leader+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}udetsuki+",
#                 f"{DANBOORU_BASE}udetsuki_(one_piece)+",
#                 f"{DANBOORU_BASE}cidre_executive+"
#             ]
#         },
#
#         "sengoku's_secretary": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}sengoku's_secretary+",
#                 f"{GELBOORU_BASE}marine_headquarters+secretary+",
#                 f"{GELBOORU_BASE}marineford+staff+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}sengoku's_secretary+",
#                 f"{DANBOORU_BASE}marine_staff+"
#             ]
#         },
#
#         "domino": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}domino+",
#                 f"{GELBOORU_BASE}domino_(one_piece)+",
#                 f"{GELBOORU_BASE}impel_down+guard+",
#                 f"{GELBOORU_BASE}prison_officer+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}domino+",
#                 f"{DANBOORU_BASE}domino_(one_piece)+",
#                 f"{DANBOORU_BASE}impel_down+"
#             ]
#         },
#
#         "tsuru": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}tsuru+",
#                 f"{GELBOORU_BASE}tsuru_(one_piece)+",
#                 f"{GELBOORU_BASE}vice_admiral+tsuru+",
#                 f"{GELBOORU_BASE}marine_legend+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}tsuru+",
#                 f"{DANBOORU_BASE}tsuru_(one_piece)+",
#                 f"{DANBOORU_BASE}vice_admiral+"
#             ]
#         },
#
#         "kairen": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}kairen+",
#                 f"{GELBOORU_BASE}kairen_(one_piece)+",
#                 f"{GELBOORU_BASE}marine_giant+",
#                 f"{GELBOORU_BASE}giant_squad+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}kairen+",
#                 f"{DANBOORU_BASE}kairen_(one_piece)+",
#                 f"{DANBOORU_BASE}marine_giant+"
#             ]
#         },
#
#         "sadi": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}sadi+",
#                 f"{GELBOORU_BASE}sadi_(one_piece)+",
#                 f"{GELBOORU_BASE}chief_guard+sadi+",
#                 f"{GELBOORU_BASE}impel_down+guard+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}sadi+",
#                 f"{DANBOORU_BASE}sadi_(one_piece)+",
#                 f"{DANBOORU_BASE}chief_guard+"
#             ]
#         },
#
#         "sadie-chan": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}sadie-chan+",
#                 f"{GELBOORU_BASE}sadie_(one_piece)+",
#                 f"{GELBOORU_BASE}impel_down+guard+",
#                 f"{GELBOORU_BASE}prison_guard+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}sadie-chan+",
#                 f"{DANBOORU_BASE}sadie_(one_piece)+"
#             ]
#         },
#
#         "saldeath": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}saldeath+",
#                 f"{GELBOORU_BASE}saldeath_(one_piece)+",
#                 f"{GELBOORU_BASE}blugori_commander+",
#                 f"{GELBOORU_BASE}impel_down+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}saldeath+",
#                 f"{DANBOORU_BASE}saldeath_(one_piece)+"
#             ]
#         },
#
#         "charlotte_galette": [f"{GELBOORU_BASE}{tag}" for tag in
#                               CharacterTags.ONE_PIECE_TAGS["charlotte_galette"]["gelbooru"]],
#         # Wano Characters
#
#         # Vegapunk satellites
#         "vegapunk_lilith": [f"{GELBOORU_BASE}{tag}" for tag in
#                             CharacterTags.ONE_PIECE_TAGS["vegapunk_lilith"]["gelbooru"]],
#         "vegapunk_atlas": [f"{GELBOORU_BASE}{tag}" for tag in
#                            CharacterTags.ONE_PIECE_TAGS["vegapunk_atlas"]["gelbooru"]],
#         "vegapunk_york": [f"{GELBOORU_BASE}{tag}" for tag in
#                           CharacterTags.ONE_PIECE_TAGS["vegapunk_york"]["gelbooru"]],
#         "vegapunk_edison": [f"{GELBOORU_BASE}{tag}" for tag in
#                             CharacterTags.ONE_PIECE_TAGS["vegapunk_edison"]["gelbooru"]],
#
#         # Additional Characters
#         "whitey_bay": [f"{GELBOORU_BASE}{tag}" for tag in CharacterTags.ONE_PIECE_TAGS["whitey_bay"]["gelbooru"]],
#         "shakky": [f"{GELBOORU_BASE}{tag}" for tag in CharacterTags.ONE_PIECE_TAGS["shakky"]["gelbooru"]],
#
#         # Additional Characters from CHARACTER_MAPPINGS
#         "ann": [f"{GELBOORU_BASE}ann_%28one_piece%29+"],
#         "aphelandra": [f"{GELBOORU_BASE}aphelandra_%28one_piece%29+"],
#         "baccarat": [f"{GELBOORU_BASE}baccarat_%28one_piece%29+"],
#         "carina": [f"{GELBOORU_BASE}carina_%28one_piece%29+"],
#         "ein": [f"{GELBOORU_BASE}ein_%28one_piece%29+"],
#         "honey_queen": [
#             f"{GELBOORU_BASE}honey_queen+",
#             f"{GELBOORU_BASE}honey queen+"
#         ],
#         "laki": [f"{GELBOORU_BASE}laki_%28one_piece%29+"],
#         "lily_enstomach": [
#             f"{GELBOORU_BASE}lily_enstomach+",
#             f"{GELBOORU_BASE}lily enstomach+"
#         ],
#         "mero": [f"{GELBOORU_BASE}mero_%28one_piece%29+"],
#         "miss_valentine": [
#             f"{GELBOORU_BASE}miss_valentine+",
#             f"{GELBOORU_BASE}miss valentine+"
#         ],
#         "moda": [f"{GELBOORU_BASE}moda_%28one_piece%29+"],
#         "mousse": [f"{GELBOORU_BASE}mousse_%28one_piece%29+"],
#         "nico_olvia": [
#             f"{GELBOORU_BASE}nico_olvia+",
#             f"{GELBOORU_BASE}olvia+"
#         ],
#         "nojiko": [f"{GELBOORU_BASE}nojiko+"],
#         "ro": [f"{GELBOORU_BASE}ro_%28one_piece%29+"],
#         "stella": [f"{GELBOORU_BASE}stella_%28one_piece%29+"],
#         "tama": [f"{GELBOORU_BASE}tama_%28one_piece%29+"],
#         "victoria_cindry": [
#             f"{GELBOORU_BASE}victoria_cindry+",
#             f"{GELBOORU_BASE}cindry+"
#         ],
#         "wanda": [f"{GELBOORU_BASE}wanda_%28one_piece%29+"],
#         "uta": [
#             f"{GELBOORU_BASE}uta_%28one_piece%29+",
#             f"{GELBOORU_BASE}world_diva+",
#             f"{GELBOORU_BASE}shanks_daughter+"
#         ],
#     },
#
#     DOTA2_URLS = {
#         "gelbooru": {
#             # Core Heroes
#             "lina": [f"{GELBOORU_BASE}{tag}+" for tag in ["lina", "lina_(dota)", "slayer"]],
#             "crystal_maiden": [f"{GELBOORU_BASE}{tag}+" for tag in ["crystal_maiden", "rylai", "cm"]],
#             "windrunner": [f"{GELBOORU_BASE}{tag}+" for tag in ["windranger", "windrunner", "lyralei"]],
#             "drow_ranger": [f"{GELBOORU_BASE}{tag}+" for tag in ["drow_ranger", "traxex"]],
#             "templar_assassin": [f"{GELBOORU_BASE}{tag}+" for tag in ["templar_assassin", "lanaya"]],
#
#             # Intelligence Heroes
#             "dark_willow": [f"{GELBOORU_BASE}{tag}+" for tag in ["dark_willow", "mireska"]],
#             "death_prophet": [f"{GELBOORU_BASE}{tag}+" for tag in ["death_prophet", "krobelus"]],
#             "queen_of_pain": [f"{GELBOORU_BASE}{tag}+" for tag in ["queen_of_pain", "akasha"]],
#             "enchantress": [f"{GELBOORU_BASE}{tag}+" for tag in ["enchantress", "aiushtha"]],
#             "winter_wyvern": [f"{GELBOORU_BASE}{tag}+" for tag in ["winter_wyvern", "auroth"]],
#
#             # Strength Heroes
#             "legion_commander": [f"{GELBOORU_BASE}{tag}+" for tag in ["legion_commander", "tresdin"]],
#             "marci": [f"{GELBOORU_BASE}{tag}+" for tag in ["marci", "marci_(dota)"]],
#             "dawnbreaker": [f"{GELBOORU_BASE}{tag}+" for tag in ["dawnbreaker", "valora"]],
#
#             # Agility Heroes
#             "luna": [f"{GELBOORU_BASE}{tag}+" for tag in ["luna_(dota)", "moon_rider"]],
#             "mirana": [f"{GELBOORU_BASE}{tag}+" for tag in ["mirana", "princess_of_the_moon"]],
#             "naga_siren": [f"{GELBOORU_BASE}{tag}+" for tag in ["naga_siren", "slithice"]],
#             "phantom_assassin": [f"{GELBOORU_BASE}{tag}+" for tag in ["phantom_assassin", "mortred"]],
#             "spectre": [f"{GELBOORU_BASE}{tag}+" for tag in ["spectre", "mercurial"]],
#             "vengeful_spirit": [f"{GELBOORU_BASE}{tag}+" for tag in ["vengeful_spirit", "shendelzare"]],
#
#             # Additional Heroes
#             "broodmother": [f"{GELBOORU_BASE}{tag}+" for tag in ["broodmother", "black_arachnia"]],
#             "medusa": [f"{GELBOORU_BASE}{tag}+" for tag in ["medusa_(dota)", "gorgon"]],
#             "snapfire": [f"{GELBOORU_BASE}{tag}+" for tag in ["snapfire", "beatrix"]],
#             "hoodwink": [f"{GELBOORU_BASE}{tag}+" for tag in ["hoodwink", "hoodwink_(dota)"]],
#
#             # Personas
#             "anti_mage_persona": [f"{GELBOORU_BASE}{tag}+" for tag in ["anti_mage_persona", "wei"]],
#             "keeper_of_the_light_persona": [f"{GELBOORU_BASE}{tag}+" for tag in
#                                             ["keeper_of_the_light_persona", "wraith_of_the_wilds"]],
#             "oracle_persona": [f"{GELBOORU_BASE}{tag}+" for tag in ["oracle_persona", "fortune's_tout"]]
#         },
#         "danbooru": {
#             # Core Heroes
#             "lina": [f"{DANBOORU_BASE}{tag}+" for tag in ["lina_(dota)", "the_slayer"]],
#             "crystal_maiden": [f"{DANBOORU_BASE}{tag}+" for tag in ["crystal_maiden", "rylai"]],
#             "windrunner": [f"{DANBOORU_BASE}{tag}+" for tag in ["windranger", "lyralei"]],
#             "drow_ranger": [f"{DANBOORU_BASE}{tag}+" for tag in ["drow_ranger", "traxex"]],
#             "templar_assassin": [f"{DANBOORU_BASE}{tag}+" for tag in ["templar_assassin", "lanaya"]],
#
#             # Intelligence Heroes
#             "dark_willow": [f"{DANBOORU_BASE}{tag}+" for tag in ["dark_willow", "mireska_sunbreeze"]],
#             "death_prophet": [f"{DANBOORU_BASE}{tag}+" for tag in ["death_prophet", "krobelus"]],
#             "queen_of_pain": [f"{DANBOORU_BASE}{tag}+" for tag in ["queen_of_pain", "akasha"]],
#             "enchantress": [f"{DANBOORU_BASE}{tag}+" for tag in ["enchantress", "aiushtha"]],
#             "winter_wyvern": [f"{DANBOORU_BASE}{tag}+" for tag in ["winter_wyvern", "auroth"]],
#
#             # Strength Heroes
#             "legion_commander": [f"{DANBOORU_BASE}{tag}+" for tag in ["legion_commander", "tresdin"]],
#             "marci": [f"{DANBOORU_BASE}{tag}+" for tag in ["marci", "marci_(dota)"]],
#             "dawnbreaker": [f"{DANBOORU_BASE}{tag}+" for tag in ["dawnbreaker", "valora"]],
#
#             # Agility Heroes
#             "luna": [f"{DANBOORU_BASE}{tag}+" for tag in ["luna_(dota)", "moon_rider"]],
#             "mirana": [f"{DANBOORU_BASE}{tag}+" for tag in ["mirana", "princess_of_the_moon"]],
#             "naga_siren": [f"{DANBOORU_BASE}{tag}+" for tag in ["naga_siren", "slithice"]],
#             "phantom_assassin": [f"{DANBOORU_BASE}{tag}+" for tag in ["phantom_assassin", "mortred"]],
#             "spectre": [f"{DANBOORU_BASE}{tag}+" for tag in ["spectre", "mercurial"]],
#             "vengeful_spirit": [f"{DANBOORU_BASE}{tag}+" for tag in ["vengeful_spirit", "shendelzare"]],
#
#             # Additional Heroes
#             "broodmother": [f"{DANBOORU_BASE}{tag}+" for tag in ["broodmother", "black_arachnia"]],
#             "medusa": [f"{DANBOORU_BASE}{tag}+" for tag in ["medusa_(dota)", "gorgon"]],
#             "snapfire": [f"{DANBOORU_BASE}{tag}+" for tag in ["snapfire", "beatrix"]],
#             "hoodwink": [f"{DANBOORU_BASE}{tag}+" for tag in ["hoodwink", "hoodwink_(dota)"]],
#
#             # Personas
#             "anti_mage_persona": [f"{DANBOORU_BASE}{tag}+" for tag in ["anti_mage_persona", "wei"]],
#             "keeper_of_the_light_persona": [f"{DANBOORU_BASE}{tag}+" for tag in ["kotl_persona", "wraith_persona"]],
#             "oracle_persona": [f"{DANBOORU_BASE}{tag}+" for tag in ["oracle_persona", "fortune_tout"]]
#         }
#     }
#
#     NARUTO_URLS = {
#         # Hokage & Main Characters
#         "tsunade": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}tsunade+",
#                 f"{GELBOORU_BASE}tsunade_(naruto)+",
#                 f"{GELBOORU_BASE}senju_tsunade+",
#                 f"{GELBOORU_BASE}godaime_hokage+",
#                 f"{GELBOORU_BASE}princess_tsunade+",
#                 f"{GELBOORU_BASE}lady_tsunade+",
#                 f"{GELBOORU_BASE}legendary_sannin+tsunade+",
#                 f"{GELBOORU_BASE}young_tsunade+",
#                 f"{GELBOORU_BASE}hundred_healings+tsunade+",
#                 f"{GELBOORU_BASE}medical_ninja+tsunade+",
#                 f"{GELBOORU_BASE}hokage_tsunade+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}tsunade+",
#                 f"{DANBOORU_BASE}senju_tsunade+",
#                 f"{DANBOORU_BASE}godaime_hokage+",
#                 f"{DANBOORU_BASE}tsunade_(naruto)+",
#                 f"{DANBOORU_BASE}young_tsunade+",
#                 f"{DANBOORU_BASE}hundred_healings+tsunade+",
#                 f"{DANBOORU_BASE}medical_ninja+tsunade+"
#             ]
#         },
#         "sakura": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}haruno_sakura+",
#                 f"{GELBOORU_BASE}sakura_(naruto)+",
#                 f"{GELBOORU_BASE}uchiha_sakura+",
#                 f"{GELBOORU_BASE}inner_sakura+",
#                 f"{GELBOORU_BASE}adult_sakura+",
#                 f"{GELBOORU_BASE}young_sakura+",
#                 f"{GELBOORU_BASE}hundred_healings_sakura+",
#                 f"{GELBOORU_BASE}medical_ninja+sakura+",
#                 f"{GELBOORU_BASE}team_7+sakura+",
#                 f"{GELBOORU_BASE}boruto_era_sakura+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}haruno_sakura+",
#                 f"{DANBOORU_BASE}sakura_(naruto)+",
#                 f"{DANBOORU_BASE}uchiha_sakura+",
#                 f"{DANBOORU_BASE}inner_sakura+",
#                 f"{DANBOORU_BASE}adult_sakura+",
#                 f"{DANBOORU_BASE}medical_ninja+sakura+"
#             ],
#         },
#         "hinata": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}hyuuga_hinata+",
#                 f"{GELBOORU_BASE}hinata_(naruto)+",
#                 f"{GELBOORU_BASE}uzumaki_hinata+",
#                 f"{GELBOORU_BASE}byakugan_princess+",
#                 f"{GELBOORU_BASE}hinata+byakugan+",
#                 f"{GELBOORU_BASE}young_hinata+",
#                 f"{GELBOORU_BASE}adult_hinata+",
#                 f"{GELBOORU_BASE}the_last_hinata+",
#                 f"{GELBOORU_BASE}boruto_era_hinata+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}hyuuga_hinata+",
#                 f"{DANBOORU_BASE}hinata_(naruto)+",
#                 f"{DANBOORU_BASE}uzumaki_hinata+",
#                 f"{DANBOORU_BASE}byakugan+hinata+",
#                 f"{DANBOORU_BASE}adult_hinata+",
#                 f"{DANBOORU_BASE}the_last_hinata+"
#             ]
#         },
#         "ino": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}yamanaka_ino+",
#                 f"{GELBOORU_BASE}ino_(naruto)+",
#                 f"{GELBOORU_BASE}ino_yamanaka+",
#                 f"{GELBOORU_BASE}young_ino+",
#                 f"{GELBOORU_BASE}adult_ino+",
#                 f"{GELBOORU_BASE}war_arc_ino+",
#                 f"{GELBOORU_BASE}boruto_era_ino+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}yamanaka_ino+",
#                 f"{DANBOORU_BASE}ino_(naruto)+",
#                 f"{DANBOORU_BASE}adult_ino+",
#                 f"{DANBOORU_BASE}young_ino+"
#             ]
#         },
#         "tenten": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}tenten+",
#                 f"{GELBOORU_BASE}tenten_(naruto)+",
#                 f"{GELBOORU_BASE}young_tenten+",
#                 f"{GELBOORU_BASE}adult_tenten+",
#                 f"{GELBOORU_BASE}weapons_specialist+tenten+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}tenten+",
#                 f"{DANBOORU_BASE}tenten_(naruto)+",
#                 f"{DANBOORU_BASE}adult_tenten+"
#             ]
#         },
#
#         "kurenai": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}yuuhi_kurenai+",
#                 f"{GELBOORU_BASE}kurenai_(naruto)+",
#                 f"{GELBOORU_BASE}sarutobi_kurenai+",
#                 f"{GELBOORU_BASE}young_kurenai+",
#                 f"{GELBOORU_BASE}pregnant_kurenai+",
#                 f"{GELBOORU_BASE}genjutsu_master+kurenai+",
#                 f"{GELBOORU_BASE}team_8_leader+kurenai+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}yuuhi_kurenai+",
#                 f"{DANBOORU_BASE}kurenai_(naruto)+",
#                 f"{DANBOORU_BASE}genjutsu_master+",
#                 f"{DANBOORU_BASE}pregnant_kurenai+"
#             ]
#         },
#
#         "anko": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}mitarashi_anko+",
#                 f"{GELBOORU_BASE}anko_(naruto)+",
#                 f"{GELBOORU_BASE}cursed_seal+anko+",
#                 f"{GELBOORU_BASE}young_anko+",
#                 f"{GELBOORU_BASE}snake_mistress+anko+",
#                 f"{GELBOORU_BASE}boruto_era_anko+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}mitarashi_anko+",
#                 f"{DANBOORU_BASE}anko_(naruto)+",
#                 f"{DANBOORU_BASE}young_anko+",
#                 f"{DANBOORU_BASE}snake_techniques+anko+"
#             ]
#         },
#         "shizune": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}shizune+",
#                 f"{GELBOORU_BASE}shizune_(naruto)+",
#                 f"{GELBOORU_BASE}medical_ninja+shizune+",
#                 f"{GELBOORU_BASE}young_shizune+",
#                 f"{GELBOORU_BASE}hokage_assistant+shizune+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}shizune+",
#                 f"{DANBOORU_BASE}shizune_(naruto)+",
#                 f"{DANBOORU_BASE}medical_ninja+shizune+"
#             ]
#         },
#
#         "sarada": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}uchiha_sarada+",
#                 f"{GELBOORU_BASE}sarada_(naruto)+",
#                 f"{GELBOORU_BASE}sarada+sharingan+",
#                 f"{GELBOORU_BASE}young_sarada+",
#                 f"{GELBOORU_BASE}teen_sarada+",
#                 f"{GELBOORU_BASE}genin_sarada+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}uchiha_sarada+",
#                 f"{DANBOORU_BASE}sarada_(naruto)+",
#                 f"{DANBOORU_BASE}sharingan+sarada+"
#             ]
#         },
#
#         "himawari": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}uzumaki_himawari+",
#                 f"{GELBOORU_BASE}himawari_(naruto)+",
#                 f"{GELBOORU_BASE}himawari+byakugan+",
#                 f"{GELBOORU_BASE}young_himawari+",
#                 f"{GELBOORU_BASE}teen_himawari+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}uzumaki_himawari+",
#                 f"{DANBOORU_BASE}himawari_(naruto)+",
#                 f"{DANBOORU_BASE}byakugan+himawari+"
#             ]
#         },
#
#         "chocho": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}akimichi_chocho+",
#                 f"{GELBOORU_BASE}chocho_(naruto)+",
#                 f"{GELBOORU_BASE}butterfly_mode+chocho+",
#                 f"{GELBOORU_BASE}young_chocho+",
#                 f"{GELBOORU_BASE}teen_chocho+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}akimichi_chocho+",
#                 f"{DANBOORU_BASE}chocho_(naruto)+",
#                 f"{DANBOORU_BASE}butterfly_mode+chocho+"
#             ]
#         },
#
#         "temari": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}temari+",
#                 f"{GELBOORU_BASE}temari_(naruto)+",
#                 f"{GELBOORU_BASE}nara_temari+",
#                 f"{GELBOORU_BASE}wind_techniques+temari+",
#                 f"{GELBOORU_BASE}young_temari+",
#                 f"{GELBOORU_BASE}adult_temari+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}temari+",
#                 f"{DANBOORU_BASE}temari_(naruto)+",
#                 f"{DANBOORU_BASE}nara_temari+"
#             ]
#         },
#
#         "mei": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}terumi_mei+",
#                 f"{GELBOORU_BASE}mei_(naruto)+",
#                 f"{GELBOORU_BASE}mizukage+mei+",
#                 f"{GELBOORU_BASE}young_mei+",
#                 f"{GELBOORU_BASE}lava_release+mei+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}terumi_mei+",
#                 f"{DANBOORU_BASE}mei_(naruto)+",
#                 f"{DANBOORU_BASE}mizukage+mei+"
#             ]
#         },
#
#         "konan": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}konan+",
#                 f"{GELBOORU_BASE}konan_(naruto)+",
#                 f"{GELBOORU_BASE}angel_form+konan+",
#                 f"{GELBOORU_BASE}paper_techniques+konan+",
#                 f"{GELBOORU_BASE}young_konan+",
#                 f"{GELBOORU_BASE}akatsuki_konan+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}konan+",
#                 f"{DANBOORU_BASE}konan_(naruto)+",
#                 f"{DANBOORU_BASE}paper_angel+",
#                 f"{DANBOORU_BASE}akatsuki_member+konan+"
#             ]
#         },
#
#         "guren": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}guren+",
#                 f"{GELBOORU_BASE}guren_(naruto)+",
#                 f"{GELBOORU_BASE}crystal_release+guren+",
#                 f"{GELBOORU_BASE}crystal_style+guren+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}guren+",
#                 f"{DANBOORU_BASE}guren_(naruto)+",
#                 f"{DANBOORU_BASE}crystal_style+"
#             ]
#         },
#
#         "kaguya": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}ootsutsuki_kaguya+",
#                 f"{GELBOORU_BASE}kaguya_(naruto)+",
#                 f"{GELBOORU_BASE}rabbit_goddess+",
#                 f"{GELBOORU_BASE}rinne_sharingan+kaguya+",
#                 f"{GELBOORU_BASE}byakugan+kaguya+",
#                 f"{GELBOORU_BASE}goddess_form+kaguya+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}ootsutsuki_kaguya+",
#                 f"{DANBOORU_BASE}kaguya_(naruto)+",
#                 f"{DANBOORU_BASE}rabbit_goddess+",
#                 f"{DANBOORU_BASE}rinne_sharingan+kaguya+"
#             ]
#         },
#
#
#     },
#
#
#     DRAGON_BALL_URLS = {
#         "bulma": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}bulma+",
#                 f"{GELBOORU_BASE}bulma_(dragon_ball)+",
#                 f"{GELBOORU_BASE}bulma_briefs+",
#                 f"{GELBOORU_BASE}capsule_corp+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}bulma+",
#                 f"{DANBOORU_BASE}bulma_(dragon_ball)+",
#                 f"{DANBOORU_BASE}briefs_family+",
#                 f"{DANBOORU_BASE}scientist+"
#             ]
#         },
#
#         "android_18": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}android_18+",
#                 f"{GELBOORU_BASE}lazuli+",
#                 f"{GELBOORU_BASE}cyborg_18+",
#                 f"{GELBOORU_BASE}c18+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}android_18+",
#                 f"{DANBOORU_BASE}c-18+",
#                 f"{DANBOORU_BASE}infinite_energy+"
#             ]
#         },
#
#         "chi_chi": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}chi-chi+",
#                 f"{GELBOORU_BASE}chi-chi_(dragon_ball)+",
#                 f"{GELBOORU_BASE}ox_princess+",
#                 f"{GELBOORU_BASE}son_family+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}chi-chi+",
#                 f"{DANBOORU_BASE}son_chi-chi+",
#                 f"{DANBOORU_BASE}ox_princess+"
#             ]
#         },
#
#         "caulifla": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}caulifla+",
#                 f"{GELBOORU_BASE}universe_6_saiyan+",
#                 f"{GELBOORU_BASE}super_saiyan+caulifla+",
#                 f"{GELBOORU_BASE}kefla_component+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}caulifla+",
#                 f"{DANBOORU_BASE}universe_six+",
#                 f"{DANBOORU_BASE}super_saiyan+"
#             ]
#         },
#
#         "kale": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}kale+",
#                 f"{GELBOORU_BASE}kale_(dragon_ball)+",
#                 f"{GELBOORU_BASE}legendary_super_saiyan+",
#                 f"{GELBOORU_BASE}berserker_form+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}kale+",
#                 f"{DANBOORU_BASE}universe_six_broly+",
#                 f"{DANBOORU_BASE}legendary_saiyan+"
#             ]
#         },
#
#         "android_21": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}android_21+",
#                 f"{GELBOORU_BASE}majin_android_21+",
#                 f"{GELBOORU_BASE}lab_coat_21+",
#                 f"{GELBOORU_BASE}dragon_ball_fighters+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}android_21+",
#                 f"{DANBOORU_BASE}a21+",
#                 f"{DANBOORU_BASE}majin_form+"
#             ]
#         },
#
#         "cheelai": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}cheelai+",
#                 f"{GELBOORU_BASE}broly_movie+",
#                 f"{GELBOORU_BASE}frieza_force+",
#                 f"{GELBOORU_BASE}dragon_ball_super+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}cheelai+",
#                 f"{DANBOORU_BASE}broly_movie+",
#                 f"{DANBOORU_BASE}frieza_force+"
#             ]
#         },
#
#         "towa": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}towa+",
#                 f"{GELBOORU_BASE}towa_(dragon_ball)+",
#                 f"{GELBOORU_BASE}demon_scientist+",
#                 f"{GELBOORU_BASE}time_breaker+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}towa+",
#                 f"{DANBOORU_BASE}demon_realm+",
#                 f"{DANBOORU_BASE}time_breaker+"
#             ]
#         },
#
#         "chronoa": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}supreme_kai_of_time+",
#                 f"{GELBOORU_BASE}chronoa+",
#                 f"{GELBOORU_BASE}time_patrol+",
#                 f"{GELBOORU_BASE}xenoverse+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}chronoa+",
#                 f"{DANBOORU_BASE}supreme_kai_of_time+",
#                 f"{DANBOORU_BASE}time_patrol+"
#             ]
#         },
#
#         "videl": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}videl+",
#                 f"{GELBOORU_BASE}videl_(dragon_ball)+",
#                 f"{GELBOORU_BASE}great_saiyawoman+",
#                 f"{GELBOORU_BASE}son_family+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}videl+",
#                 f"{DANBOORU_BASE}great_saiyaman_saga+",
#                 f"{DANBOORU_BASE}satan_city+"
#             ]
#         },
#
#         "launch": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}launch+",
#                 f"{GELBOORU_BASE}launch_(dragon_ball)+",
#                 f"{GELBOORU_BASE}blonde_launch+",
#                 f"{GELBOORU_BASE}blue_launch+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}launch+",
#                 f"{DANBOORU_BASE}personality_switch+",
#                 f"{DANBOORU_BASE}kame_house+"
#             ]
#         },
#
#         "marron": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}marron+",
#                 f"{GELBOORU_BASE}marron_(dragon_ball)+",
#                 f"{GELBOORU_BASE}krillin_family+",
#                 f"{GELBOORU_BASE}kame_house+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}marron+",
#                 f"{DANBOORU_BASE}krillin_daughter+",
#                 f"{DANBOORU_BASE}android_18_family+"
#             ]
#         },
#
#         "pan": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}pan+",
#                 f"{GELBOORU_BASE}pan_(dragon_ball)+",
#                 f"{GELBOORU_BASE}gt_pan+",
#                 f"{GELBOORU_BASE}quarter_saiyan+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}pan+",
#                 f"{DANBOORU_BASE}son_family+",
#                 f"{DANBOORU_BASE}gt_era+"
#             ]
#         },
#
#         "bulla": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}bulla+",
#                 f"{GELBOORU_BASE}bra_(dragon_ball)+",
#                 f"{GELBOORU_BASE}vegeta_family+",
#                 f"{GELBOORU_BASE}capsule_corp+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}bulla+",
#                 f"{DANBOORU_BASE}brief_family+",
#                 f"{DANBOORU_BASE}saiyan_princess+"
#             ]
#         },
#
#         "vados": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}vados+",
#                 f"{GELBOORU_BASE}universe_6_angel+",
#                 f"{GELBOORU_BASE}champa_attendant+",
#                 f"{GELBOORU_BASE}whis_sister+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}vados+",
#                 f"{DANBOORU_BASE}angel_attendant+",
#                 f"{DANBOORU_BASE}universe_6+"
#             ]
#         },
#     },
#
#     ATTACK_ON_TITAN_URLS = {
#         "mikasa": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}mikasa_ackerman+",
#                 f"{GELBOORU_BASE}mikasa+(shingeki_no_kyojin)+",
#                 f"{GELBOORU_BASE}ackerman+mikasa+",
#                 f"{GELBOORU_BASE}survey_corps+mikasa+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}mikasa_ackerman+",
#                 f"{DANBOORU_BASE}mikasa+(attack_on_titan)+",
#                 f"{DANBOORU_BASE}ackerman_clan+",
#                 f"{DANBOORU_BASE}survey_corps+"
#             ]
#         },
#
#         "annie": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}annie_leonhart+",
#                 f"{GELBOORU_BASE}female_titan+",
#                 f"{GELBOORU_BASE}warrior+annie+",
#                 f"{GELBOORU_BASE}crystal_form+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}annie_leonhardt+",
#                 f"{DANBOORU_BASE}female_type_titan+",
#                 f"{DANBOORU_BASE}warrior_unit+"
#             ]
#         },
#
#         "historia": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}historia_reiss+",
#                 f"{GELBOORU_BASE}christa_lenz+",
#                 f"{GELBOORU_BASE}queen+historia+",
#                 f"{GELBOORU_BASE}royal_blood+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}historia_reiss+",
#                 f"{DANBOORU_BASE}krista_lenz+",
#                 f"{DANBOORU_BASE}queen_historia+"
#             ]
#         },
#
#         "pieck": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}pieck_finger+",
#                 f"{GELBOORU_BASE}cart_titan+",
#                 f"{GELBOORU_BASE}warrior_pieck+",
#                 f"{GELBOORU_BASE}marley_soldier+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}pieck+",
#                 f"{DANBOORU_BASE}cart_titan+",
#                 f"{DANBOORU_BASE}warrior_unit+"
#             ]
#         },
#
#         "gabi": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}gabi_braun+",
#                 f"{GELBOORU_BASE}warrior_candidate+",
#                 f"{GELBOORU_BASE}marley_soldier+gabi+",
#                 f"{GELBOORU_BASE}braun_family+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}gabi+",
#                 f"{DANBOORU_BASE}warrior_cadet+",
#                 f"{DANBOORU_BASE}marley_warrior+"
#             ]
#         },
#
#         "hitch": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}hitch_dreyse+",
#                 f"{GELBOORU_BASE}military_police+",
#                 f"{GELBOORU_BASE}stohess_guard+",
#                 f"{GELBOORU_BASE}mp_brigade+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}hitch+",
#                 f"{DANBOORU_BASE}mp_brigade+",
#                 f"{DANBOORU_BASE}military_police+"
#             ]
#         },
#
#         "traute": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}traute_caven+",
#                 f"{GELBOORU_BASE}anti_personnel+",
#                 f"{GELBOORU_BASE}kenny_squad+",
#                 f"{GELBOORU_BASE}interior_police+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}traute+",
#                 f"{DANBOORU_BASE}interior_police+",
#                 f"{DANBOORU_BASE}anti_personnel+"
#             ]
#         },
#     },
#
#     DEMON_SLAYER_URLS = {
#         "shinobu": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}kochou_shinobu+",
#                 f"{GELBOORU_BASE}insect_hashira+",
#                 f"{GELBOORU_BASE}butterfly_mansion+",
#                 f"{GELBOORU_BASE}demon_slayer_corps+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}kochou_shinobu+",
#                 f"{DANBOORU_BASE}insect_pillar+",
#                 f"{DANBOORU_BASE}hashira+"
#             ]
#         },
#
#         "kanao": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}tsuyuri_kanao+",
#                 f"{GELBOORU_BASE}flower_breathing+",
#                 f"{GELBOORU_BASE}butterfly_estate+",
#                 f"{GELBOORU_BASE}demon_hunter+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}tsuyuri_kanao+",
#                 f"{DANBOORU_BASE}flower_breath+",
#                 f"{DANBOORU_BASE}butterfly_mansion+"
#             ]
#         },
#
#         "mitsuri": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}kanroji_mitsuri+",
#                 f"{GELBOORU_BASE}love_hashira+",
#                 f"{GELBOORU_BASE}love_breathing+",
#                 f"{GELBOORU_BASE}demon_slayer_corps+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}kanroji_mitsuri+",
#                 f"{DANBOORU_BASE}love_pillar+",
#                 f"{DANBOORU_BASE}love_breathing+"
#             ]
#         },
#
#         "daki": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}daki+",
#                 f"{GELBOORU_BASE}upper_six+",
#                 f"{GELBOORU_BASE}oiran+",
#                 f"{GELBOORU_BASE}entertainment_district+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}daki+",
#                 f"{DANBOORU_BASE}upper_moon_six+",
#                 f"{DANBOORU_BASE}twelve_kizuki+"
#             ]
#         },
#
#         "nakime": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}nakime+",
#                 f"{GELBOORU_BASE}biwa_demon+",
#                 f"{GELBOORU_BASE}infinity_castle+",
#                 f"{GELBOORU_BASE}fortress_demon+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}nakime+",
#                 f"{DANBOORU_BASE}biwa_demon+",
#                 f"{DANBOORU_BASE}infinity_fortress+"
#             ]
#         },
#
#         "kanae": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}kochou_kanae+",
#                 f"{GELBOORU_BASE}flower_hashira+",
#                 f"{GELBOORU_BASE}butterfly_mansion+",
#                 f"{GELBOORU_BASE}demon_slayer_corps+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}kochou_kanae+",
#                 f"{DANBOORU_BASE}flower_hashira+",
#                 f"{DANBOORU_BASE}butterfly_estate+"
#             ]
#         },
#
#         "aoi": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}aoi_kanzaki+",
#                 f"{GELBOORU_BASE}butterfly_mansion+",
#                 f"{GELBOORU_BASE}medical_corps+",
#                 f"{GELBOORU_BASE}demon_slayer_support+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}aoi_kanzaki+",
#                 f"{DANBOORU_BASE}butterfly_mansion+",
#                 f"{DANBOORU_BASE}medical_staff+"
#             ]
#         },
#
#         "hinatsuru": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}hinatsuru+",
#                 f"{GELBOORU_BASE}uzui_wife+",
#                 f"{GELBOORU_BASE}kunoichi+",
#                 f"{GELBOORU_BASE}shinobi_wife+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}hinatsuru+",
#                 f"{DANBOORU_BASE}uzui_clan+",
#                 f"{DANBOORU_BASE}ninja_wife+"
#             ]
#         },
#
#         "makio": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}makio+",
#                 f"{GELBOORU_BASE}uzui_wife+",
#                 f"{GELBOORU_BASE}kunoichi+",
#                 f"{GELBOORU_BASE}entertainment_district+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}makio+",
#                 f"{DANBOORU_BASE}uzui_clan+",
#                 f"{DANBOORU_BASE}shinobi_wife+"
#             ]
#         },
#
#         "suma": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}suma+",
#                 f"{GELBOORU_BASE}uzui_wife+",
#                 f"{GELBOORU_BASE}kunoichi+",
#                 f"{GELBOORU_BASE}entertainment_district+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}suma+",
#                 f"{DANBOORU_BASE}uzui_clan+",
#                 f"{DANBOORU_BASE}ninja_wife+"
#             ]
#         },
#
#         "rengoku_mother": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}ruka_rengoku+",
#                 f"{GELBOORU_BASE}rengoku_family+",
#                 f"{GELBOORU_BASE}kyojuro_mother+",
#                 f"{GELBOORU_BASE}demon_slayer_family+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}ruka_rengoku+",
#                 f"{DANBOORU_BASE}rengoku_family+",
#                 f"{DANBOORU_BASE}hashira_family+"
#             ]
#         },
#
#         "amane": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}amane_ubuyashiki+",
#                 f"{GELBOORU_BASE}demon_slayer_master_wife+",
#                 f"{GELBOORU_BASE}ubuyashiki_family+",
#                 f"{GELBOORU_BASE}noble_family+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}amane_ubuyashiki+",
#                 f"{DANBOORU_BASE}ubuyashiki_family+",
#                 f"{DANBOORU_BASE}corps_master_wife+"
#             ]
#         },
#
#         "nichika": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}nichika_ubuyashiki+",
#                 f"{GELBOORU_BASE}ubuyashiki_daughter+",
#                 f"{GELBOORU_BASE}demon_slayer_family+",
#                 f"{GELBOORU_BASE}noble_daughter+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}nichika_ubuyashiki+",
#                 f"{DANBOORU_BASE}ubuyashiki_family+",
#                 f"{DANBOORU_BASE}corps_master_daughter+"
#             ]
#         },
#
#         "hinaki": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}hinaki_ubuyashiki+",
#                 f"{GELBOORU_BASE}ubuyashiki_daughter+",
#                 f"{GELBOORU_BASE}demon_slayer_family+",
#                 f"{GELBOORU_BASE}noble_daughter+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}hinaki_ubuyashiki+",
#                 f"{DANBOORU_BASE}ubuyashiki_family+",
#                 f"{DANBOORU_BASE}corps_master_daughter+"
#             ]
#         },
#
#         "kotoha": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}kotoha+",
#                 f"{GELBOORU_BASE}swordsmith_village+",
#                 f"{GELBOORU_BASE}village_resident+",
#                 f"{GELBOORU_BASE}demon_slayer_support+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}kotoha+",
#                 f"{DANBOORU_BASE}swordsmith_village+",
#                 f"{DANBOORU_BASE}village_resident+"
#             ]
#         },
#
#         "muzan_wife": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}muzan_wife+",
#                 f"{GELBOORU_BASE}kibutsuji_family+",
#                 f"{GELBOORU_BASE}human_disguise+",
#                 f"{GELBOORU_BASE}demon_slayer_character+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}muzan_wife+",
#                 f"{DANBOORU_BASE}kibutsuji_family+",
#                 f"{DANBOORU_BASE}human_disguise+"
#             ]
#         },
#
#         "susamaru": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}susamaru+",
#                 f"{GELBOORU_BASE}temari_demon+",
#                 f"{GELBOORU_BASE}demon_slayer_demon+",
#                 f"{GELBOORU_BASE}ball_demon+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}susamaru+",
#                 f"{DANBOORU_BASE}temari_demon+",
#                 f"{DANBOORU_BASE}demon_character+"
#             ]
#         },
#
#         "mukago": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}mukago+",
#                 f"{GELBOORU_BASE}spider_demon+",
#                 f"{GELBOORU_BASE}spider_family+",
#                 f"{GELBOORU_BASE}natagumo_mountain+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}mukago+",
#                 f"{DANBOORU_BASE}spider_family+",
#                 f"{DANBOORU_BASE}demon_spider+"
#             ]
#         },
#
#         "kacho": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}kacho+",
#                 f"{GELBOORU_BASE}butterfly_mansion+",
#                 f"{GELBOORU_BASE}medical_corps+",
#                 f"{GELBOORU_BASE}support_staff+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}kacho+",
#                 f"{DANBOORU_BASE}butterfly_mansion+",
#                 f"{DANBOORU_BASE}medical_staff+"
#             ]
#         },
#
#         "kiyo": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}kiyo+",
#                 f"{GELBOORU_BASE}butterfly_mansion+",
#                 f"{GELBOORU_BASE}medical_support+",
#                 f"{GELBOORU_BASE}healing_staff+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}kiyo+",
#                 f"{DANBOORU_BASE}butterfly_mansion+",
#                 f"{DANBOORU_BASE}support_staff+"
#             ]
#         },
#
#         "sumi": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}sumi+",
#                 f"{GELBOORU_BASE}butterfly_mansion+",
#                 f"{GELBOORU_BASE}medical_support+",
#                 f"{GELBOORU_BASE}quiet_helper+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}sumi+",
#                 f"{DANBOORU_BASE}butterfly_mansion+",
#                 f"{DANBOORU_BASE}medical_staff+"
#             ]
#         },
#
#         "teiko": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}teiko+",
#                 f"{GELBOORU_BASE}entertainment_district+",
#                 f"{GELBOORU_BASE}gyutaro_victim+",
#                 f"{GELBOORU_BASE}historical_character+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}teiko+",
#                 f"{DANBOORU_BASE}yuukaku+",
#                 f"{DANBOORU_BASE}flashback_character+"
#             ]
#         }
#     },
#
#     JUJUTSU_KAISEN_URLS = {
#         "nobara": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}kugisaki_nobara+",
#                 f"{GELBOORU_BASE}hammer_nail+",
#                 f"{GELBOORU_BASE}straw_doll_technique+",
#                 f"{GELBOORU_BASE}first_year_student+",
#                 f"{GELBOORU_BASE}jujutsu_kaisen+nobara+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}kugisaki_nobara+",
#                 f"{DANBOORU_BASE}hammer_nail+",
#                 f"{DANBOORU_BASE}first_year+",
#                 f"{DANBOORU_BASE}straw_doll+"
#             ]
#         },
#
#         "maki": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}zenin_maki+",
#                 f"{GELBOORU_BASE}hr_user+",
#                 f"{GELBOORU_BASE}cursed_tools+maki+",
#                 f"{GELBOORU_BASE}heavenly_restriction+",
#                 f"{GELBOORU_BASE}jujutsu_kaisen+maki+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}zenin_maki+",
#                 f"{DANBOORU_BASE}heavenly_restriction+",
#                 f"{DANBOORU_BASE}cursed_tools+",
#                 f"{DANBOORU_BASE}second_year+"
#             ]
#         },
#
#         "miwa": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}kasumi_miwa+",
#                 f"{GELBOORU_BASE}simple_domain+",
#                 f"{GELBOORU_BASE}kyoto_student+",
#                 f"{GELBOORU_BASE}sword_user+",
#                 f"{GELBOORU_BASE}jujutsu_kaisen+miwa+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}kasumi_miwa+",
#                 f"{DANBOORU_BASE}kyoto_student+",
#                 f"{DANBOORU_BASE}simple_domain+",
#                 f"{DANBOORU_BASE}swordsman+"
#             ]
#         },
#
#         "mai": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}zenin_mai+",
#                 f"{GELBOORU_BASE}construction+mai+",
#                 f"{GELBOORU_BASE}kyoto_student+mai+",
#                 f"{GELBOORU_BASE}twins+maki+",
#                 f"{GELBOORU_BASE}jujutsu_kaisen+mai+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}zenin_mai+",
#                 f"{DANBOORU_BASE}kyoto_student+",
#                 f"{DANBOORU_BASE}construction_technique+",
#                 f"{DANBOORU_BASE}maki_twin+"
#             ]
#         },
#
#         "momo": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}nishimiya_momo+",
#                 f"{GELBOORU_BASE}broom_flight+",
#                 f"{GELBOORU_BASE}kyoto_student+momo+",
#                 f"{GELBOORU_BASE}second_year+momo+",
#                 f"{GELBOORU_BASE}jujutsu_kaisen+momo+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}nishimiya_momo+",
#                 f"{DANBOORU_BASE}kyoto_student+",
#                 f"{DANBOORU_BASE}broom_user+",
#                 f"{DANBOORU_BASE}second_year+"
#             ]
#         },
#
#         "rika": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}orimoto_rika+",
#                 f"{GELBOORU_BASE}cursed_spirit+",
#                 f"{GELBOORU_BASE}queen_of_curses+",
#                 f"{GELBOORU_BASE}yuta_curse+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}orimoto_rika+",
#                 f"{DANBOORU_BASE}special_grade_curse+",
#                 f"{DANBOORU_BASE}yuta_okkotsu+"
#             ]
#         },
#
#         "uraume": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}uraume+",
#                 f"{GELBOORU_BASE}frost_human+",
#                 f"{GELBOORU_BASE}sukuna_servant+",
#                 f"{GELBOORU_BASE}heian_sorcerer+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}uraume+",
#                 f"{DANBOORU_BASE}ice_technique+",
#                 f"{DANBOORU_BASE}ancient_sorcerer+"
#             ]
#         },
#
#         "takako": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}uro_takako+",
#                 f"{GELBOORU_BASE}thin_ice+",
#                 f"{GELBOORU_BASE}sky_manipulation+",
#                 f"{GELBOORU_BASE}culling_game+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}uro_takako+",
#                 f"{DANBOORU_BASE}curved_sky+",
#                 f"{DANBOORU_BASE}heian_sorcerer+"
#             ]
#         },
#
#         "mei_mei": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}mei_mei+",
#                 f"{GELBOORU_BASE}crow_user+",
#                 f"{GELBOORU_BASE}grade_1_sorcerer+",
#                 f"{GELBOORU_BASE}bird_manipulation+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}mei_mei+",
#                 f"{DANBOORU_BASE}crow_technique+",
#                 f"{DANBOORU_BASE}mercenary_sorcerer+"
#             ]
#         },
#
#         "tsumiki": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}fushiguro_tsumiki+",
#                 f"{GELBOORU_BASE}megumi_sister+",
#                 f"{GELBOORU_BASE}culling_game+",
#                 f"{GELBOORU_BASE}vessel+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}fushiguro_tsumiki+",
#                 f"{DANBOORU_BASE}coma_patient+",
#                 f"{DANBOORU_BASE}megumi_family+"
#             ]
#         },
#
#         "utahime": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}iori_utahime+",
#                 f"{GELBOORU_BASE}singing_voice+",
#                 f"{GELBOORU_BASE}kyoto_teacher+",
#                 f"{GELBOORU_BASE}jujutsu_instructor+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}iori_utahime+",
#                 f"{DANBOORU_BASE}kyoto_staff+",
#                 f"{DANBOORU_BASE}singing_technique+"
#             ]
#         },
#
#         "yuki": {
#             "gelbooru": [
#                 f"{GELBOORU_BASE}tsukumo_yuki+",
#                 f"{GELBOORU_BASE}special_grade+",
#                 f"{GELBOORU_BASE}wandering_sorcerer+",
#                 f"{GELBOORU_BASE}curse_researcher+"
#             ],
#             "danbooru": [
#                 f"{DANBOORU_BASE}tsukumo_yuki+",
#                 f"{DANBOORU_BASE}special_grade_sorcerer+",
#                 f"{DANBOORU_BASE}curse_investigator+"
#             ]
#         }
#     },
#
#     SPY_X_FAMILY_URLS = {
#         "gelbooru": {
#             "yor": [f"{GELBOORU_BASE}yor_forger+"],
#             "anya": [f"{GELBOORU_BASE}anya_%28spy_x_family%29+"],
#             "sylvia": [f"{GELBOORU_BASE}sylvia_sherwood+"],
#             "fiona": [f"{GELBOORU_BASE}fiona_frost+"],
#             "becky": [f"{GELBOORU_BASE}becky_blackbell+"],
#             "sharon": [f"{GELBOORU_BASE}sharon_%28spy_x_family%29+"],
#             "melinda": [f"{GELBOORU_BASE}melinda_desmond+"],
#             "camilla": [f"{GELBOORU_BASE}camilla_%28spy_x_family%29+"],
#             "karen": [f"{GELBOORU_BASE}karen_gloomy+"],
#             "martha": [f"{GELBOORU_BASE}martha_%28spy_x_family%29+"],
#             # Additional characters
#             "lady_in_black": [f"{GELBOORU_BASE}lady_in_black_%28spy_x_family%29+"],
#             "elena": [f"{GELBOORU_BASE}elena_%28spy_x_family%29+"],
#             "sandra": [f"{GELBOORU_BASE}sandra_%28spy_x_family%29+"],
#             "millie": [f"{GELBOORU_BASE}millie_%28spy_x_family%29+"]
#         },
#         "danbooru": {
#             # Mirror structure with danbooru base URL
#         }
#     },
#
#
#     POKEMON_URLS = {
#         "gelbooru": {
#             "misty": [f"{GELBOORU_BASE}misty_%28pokemon%29+"],
#             "may": [f"{GELBOORU_BASE}may_%28pokemon%29+"],
#             "dawn": [f"{GELBOORU_BASE}dawn_%28pokemon%29+"],
#             "serena": [f"{GELBOORU_BASE}serena_%28pokemon%29+"],
#             "iris": [f"{GELBOORU_BASE}iris_%28pokemon%29+"],
#             "lillie": [f"{GELBOORU_BASE}lillie_%28pokemon%29+"],
#             "cynthia": [f"{GELBOORU_BASE}cynthia_%28pokemon%29+"],
#             "diantha": [f"{GELBOORU_BASE}diantha_%28pokemon%29+"],
#             "lusamine": [f"{GELBOORU_BASE}lusamine_%28pokemon%29+"],
#             "sabrina": [f"{GELBOORU_BASE}sabrina_%28pokemon%29+"],
#             "erika": [f"{GELBOORU_BASE}erika_%28pokemon%29+"],
#             "whitney": [f"{GELBOORU_BASE}whitney_%28pokemon%29+"],
#             "jasmine": [f"{GELBOORU_BASE}jasmine_%28pokemon%29+"],
#             "clair": [f"{GELBOORU_BASE}clair_%28pokemon%29+"],
#             "flannery": [f"{GELBOORU_BASE}flannery_%28pokemon%29+"],
#             "winona": [f"{GELBOORU_BASE}winona_%28pokemon%29+"],
#             "roxanne": [f"{GELBOORU_BASE}roxanne_%28pokemon%29+"],
#             "gardenia": [f"{GELBOORU_BASE}gardenia_%28pokemon%29+"],
#             "candice": [f"{GELBOORU_BASE}candice_%28pokemon%29+"],
#             "fantina": [f"{GELBOORU_BASE}fantina_%28pokemon%29+"],
#             "elesa": [f"{GELBOORU_BASE}elesa_%28pokemon%29+"],
#             "skyla": [f"{GELBOORU_BASE}skyla_%28pokemon%29+"],
#             "nessa": [f"{GELBOORU_BASE}nessa_%28pokemon%29+"],
#             "marnie": [f"{GELBOORU_BASE}marnie_%28pokemon%29+"],
#             "sonia": [f"{GELBOORU_BASE}sonia_%28pokemon%29+"],
#             "professor_juniper": [f"{GELBOORU_BASE}professor_juniper+"],
#             "nurse_joy": [f"{GELBOORU_BASE}joy_%28pokemon%29+"],
#             "officer_jenny": [f"{GELBOORU_BASE}officer_jenny+"],
#             "jessie": [f"{GELBOORU_BASE}jessie_%28pokemon%29+"],
#             "rosa": [f"{GELBOORU_BASE}rosa_%28pokemon%29+"],
#             # Additional characters
#             "gloria": [f"{GELBOORU_BASE}gloria_%28pokemon%29+"],
#             "leaf": [f"{GELBOORU_BASE}leaf_%28pokemon%29+"],
#             "hilda": [f"{GELBOORU_BASE}hilda_%28pokemon%29+"],
#             "courtney": [f"{GELBOORU_BASE}courtney_%28pokemon%29+"],
#             "mars": [f"{GELBOORU_BASE}mars_%28pokemon%29+"],
#             "jupiter": [f"{GELBOORU_BASE}jupiter_%28pokemon%29+"],
#             "shelly": [f"{GELBOORU_BASE}shelly_%28pokemon%29+"],
#             "melony": [f"{GELBOORU_BASE}melony_%28pokemon%29+"],
#             "klara": [f"{GELBOORU_BASE}klara_%28pokemon%29+"],
#             "oleana": [f"{GELBOORU_BASE}oleana_%28pokemon%29+"],
#             "bea": [f"{GELBOORU_BASE}bea_%28pokemon%29+"],
#             "karen": [f"{GELBOORU_BASE}karen_%28pokemon%29+"],
#             "lorelei": [f"{GELBOORU_BASE}lorelei_%28pokemon%29+"],
#             "acerola": [f"{GELBOORU_BASE}acerola_%28pokemon%29+"]
#         },
#         "danbooru": {
#             # Mirror structure with danbooru base URL
#         }
#     },
#
#     DOTA2_URLS = {
#         "gelbooru": {
#             # Core Heroes
#             "lina": [f"{GELBOORU_BASE}lina_%28dota%29+"],
#             "crystal_maiden": [f"{GELBOORU_BASE}crystal_maiden+"],
#             "windrunner": [
#                 f"{GELBOORU_BASE}windranger_%28dota%29+",
#                 f"{GELBOORU_BASE}windrunner_%28dota%29+"
#             ],
#             "drow_ranger": [f"{GELBOORU_BASE}drow_ranger+"],
#             "templar_assassin": [f"{GELBOORU_BASE}templar_assassin_%28dota%29+"],
#             "phantom_assassin": [f"{GELBOORU_BASE}phantom_assassin_%28dota%29+"],
#
#             # Intelligence Heroes
#             "dark_willow": [f"{GELBOORU_BASE}dark_willow+"],
#             "death_prophet": [f"{GELBOORU_BASE}death_prophet_%28dota%29+"],
#             "enchantress": [
#                 f"{GELBOORU_BASE}enchantress_%28dota%29+",
#                 f"{GELBOORU_BASE}enchantress_%28dota_2%29+"
#             ],
#             "queen_of_pain": [f"{GELBOORU_BASE}queen_of_pain_%28dota%29+"],
#             "winter_wyvern": [f"{GELBOORU_BASE}winter_wyvern+"],
#
#             # Strength Heroes
#             "legion_commander": [f"{GELBOORU_BASE}legion_commander_%28dota%29+"],
#             "marci": [f"{GELBOORU_BASE}marci_%28dota%29+"],
#             "dawnbreaker": [
#                 f"{GELBOORU_BASE}dawnbreaker_%28dota%29+",
#                 f"{GELBOORU_BASE}dawnbreaker_%28dota_2%29+"
#             ],
#
#             # Agility Heroes
#             "luna": [f"{GELBOORU_BASE}luna_%28dota%29+"],
#             "mirana": [f"{GELBOORU_BASE}mirana_%28dota%29+"],
#             "naga_siren": [f"{GELBOORU_BASE}naga_siren_%28dota%29+"],
#             "vengeful_spirit": [f"{GELBOORU_BASE}vengeful_spirit_%28dota_2%29+"],
#
#             # Additional Characters
#             "keeper_of_the_light_persona": [f"{GELBOORU_BASE}keeper_of_the_light_persona+"],
#             "oracle_persona": [f"{GELBOORU_BASE}oracle_persona+"],
#             "anti_mage_persona": [f"{GELBOORU_BASE}anti_mage_persona+"]
#         },
#         "danbooru": {
#             # Mirror structure with danbooru base URLs
#         }
#     },
#
#     ONE_PIECE_URLS = {
#         "gelbooru": {
#             "nami": {
#                 "gelbooru": [
#                     f"{GELBOORU_BASE}nami+",
#                     f"{GELBOORU_BASE}nami_(one_piece)+",
#                     f"{GELBOORU_BASE}cat_burglar_nami+",
#                     f"{GELBOORU_BASE}weather_witch+",
#                     f"{GELBOORU_BASE}climatact+nami+",
#                     f"{GELBOORU_BASE}post_timeskip_nami+",
#                     f"{GELBOORU_BASE}pre_timeskip_nami+",
#                     f"{GELBOORU_BASE}wano_nami+"
#                 ],
#                 "danbooru": [
#                     f"{DANBOORU_BASE}nami+",
#                     f"{DANBOORU_BASE}nami_(one_piece)+",
#                     f"{DANBOORU_BASE}cat_burglar+",
#                     f"{DANBOORU_BASE}weather_control+nami+"
#                 ]
#             },
#
#             "robin": {
#                 "gelbooru": [
#                     f"{GELBOORU_BASE}nico_robin+",
#                     f"{GELBOORU_BASE}robin_(one_piece)+",
#                     f"{GELBOORU_BASE}devil_child+",
#                     f"{GELBOORU_BASE}hana_hana_no_mi+",
#                     f"{GELBOORU_BASE}post_timeskip_robin+",
#                     f"{GELBOORU_BASE}pre_timeskip_robin+",
#                     f"{GELBOORU_BASE}wano_robin+"
#                 ],
#                 "danbooru": [
#                     f"{DANBOORU_BASE}nico_robin+",
#                     f"{DANBOORU_BASE}robin_(one_piece)+",
#                     f"{DANBOORU_BASE}hana_hana_no_mi+"
#                 ]
#             },
#
#             "yamato": {
#                 "gelbooru": [
#                     f"{GELBOORU_BASE}yamato+",
#                     f"{GELBOORU_BASE}yamato_(one_piece)+",
#                     f"{GELBOORU_BASE}oni_princess+",
#                     f"{GELBOORU_BASE}hybrid_form+yamato+",
#                     f"{GELBOORU_BASE}ice_oni+yamato+"
#                 ],
#                 "danbooru": [
#                     f"{DANBOORU_BASE}yamato_(one_piece)+",
#                     f"{DANBOORU_BASE}oni_princess+",
#                     f"{DANBOORU_BASE}hybrid_form+yamato+"
#                 ]
#             },
#
#             "vivi": [f"{GELBOORU_BASE}nefertari_vivi+"],
#             "carrot": [
#                 f"{GELBOORU_BASE}carrot_%28one_piece%29+",
#                 f"{GELBOORU_BASE}carrot_(one_piece)"
#             ],
#
#             # Charlotte Family
#              "charlotte_flampe": [f"{GELBOORU_BASE}charlotte_flampe+"],
#             "charlotte_galette": [f"{GELBOORU_BASE}charlotte_galette+"],
#             "charlotte_amande": [f"{GELBOORU_BASE}charlotte_amande+"],
#             "charlotte_praline": [f"{GELBOORU_BASE}charlotte_praline+"],
#
#             # Wano Characters
#             "kouzuki_toki": [f"{GELBOORU_BASE}kouzuki_toki+"],
#             "kikunojo": [f"{GELBOORU_BASE}kikunojo_%28one_piece%29+"],
#             "ulti": [f"{GELBOORU_BASE}ulti_%28one_piece%29+"],
#
#             # Marines and World Government
#             "tashigi": [f"{GELBOORU_BASE}tashigi+"],
#             "hina": [f"{GELBOORU_BASE}hina_%28one_piece%29+"],
#             "isuka": [
#                 f"{GELBOORU_BASE}isuka_%28one_piece%29+",
#                 f"{GELBOORU_BASE}isuka_(one_piece)"
#             ],
#             "ain": [f"{GELBOORU_BASE}ain_%28one_piece%29+"],
#             "gion": [f"{GELBOORU_BASE}gion_%28one_piece%29+"],
#             "stussy": [f"{GELBOORU_BASE}stussy_%28one_piece%29+"],
#
#             # Vegapunk Satellites
#             "vegapunk_lilith": [f"{GELBOORU_BASE}vegapunk_lilith+"],
#             "vegapunk_atlas": [f"{GELBOORU_BASE}vegapunk_atlas+"],
#             "vegapunk_york": [f"{GELBOORU_BASE}vegapunk_york+"],
#             "vegapunk_edison": [f"{GELBOORU_BASE}vegapunk_edison+"],
#             "vegapunk_pythagoras": [f"{GELBOORU_BASE}vegapunk_pythagoras+"],
#             "vegapunk_shaka": [f"{GELBOORU_BASE}vegapunk_shaka+"],
#
#             # Other Major Characters
#             "vinsmoke_reiju": [f"{GELBOORU_BASE}vinsmoke_reiju+"],
#             "perona": [f"{GELBOORU_BASE}perona+"],
#             "jewelry_bonney": [f"{GELBOORU_BASE}jewelry_bonney+"],
#             "alvida": [f"{GELBOORU_BASE}alvida_%28one_piece%29+"],
#
#             # Additional Characters
#             "whitey_bay": [f"{GELBOORU_BASE}whitey_bay+"],
#             "sugar": [f"{GELBOORU_BASE}sugar_%28one_piece%29+"],
#             "monet": [f"{GELBOORU_BASE}monet_%28one_piece%29+"],
#             "shirahoshi": [f"{GELBOORU_BASE}shirahoshi+"],
#             "shakky": [f"{GELBOORU_BASE}shakky+"],
#             "makino": [f"{GELBOORU_BASE}makino_%28one_piece%29+"]
#         },
#         "danbooru": {
#             # Mirror structure with danbooru base URLs
#         }
#     }
#
#     DOTA2_URLS = {
#         "gelbooru": {
#             # Core Heroes
#             "lina": [f"{GELBOORU_BASE}lina_%28dota%29+"],
#             "crystal_maiden": [f"{GELBOORU_BASE}crystal_maiden+"],
#             "windrunner": [
#                 f"{GELBOORU_BASE}windranger_%28dota%29+",
#                 f"{GELBOORU_BASE}windrunner_%28dota%29+"
#             ],
#             "drow_ranger": [f"{GELBOORU_BASE}drow_ranger+"],
#             "templar_assassin": [f"{GELBOORU_BASE}templar_assassin_%28dota%29+"],
#             "phantom_assassin": [f"{GELBOORU_BASE}phantom_assassin_%28dota%29+"],
#
#             # Intelligence Heroes
#             "dark_willow": [f"{GELBOORU_BASE}dark_willow+"],
#             "death_prophet": [f"{GELBOORU_BASE}death_prophet_%28dota%29+"],
#             "enchantress": [
#                 f"{GELBOORU_BASE}enchantress_%28dota%29+",
#                 f"{GELBOORU_BASE}enchantress_%28dota_2%29+"
#             ],
#             "queen_of_pain": [f"{GELBOORU_BASE}queen_of_pain_%28dota%29+"],
#             "winter_wyvern": [f"{GELBOORU_BASE}winter_wyvern+"],
#
#             # Strength Heroes
#             "legion_commander": [f"{GELBOORU_BASE}legion_commander_%28dota%29+"],
#             "marci": [f"{GELBOORU_BASE}marci_%28dota%29+"],
#             "dawnbreaker": [
#                 f"{GELBOORU_BASE}dawnbreaker_%28dota%29+",
#                 f"{GELBOORU_BASE}dawnbreaker_%28dota_2%29+"
#             ],
#
#             # Agility Heroes
#             "luna": [f"{GELBOORU_BASE}luna_%28dota%29+"],
#             "mirana": [f"{GELBOORU_BASE}mirana_%28dota%29+"],
#             "naga_siren": [f"{GELBOORU_BASE}naga_siren_%28dota%29+"],
#             "vengeful_spirit": [f"{GELBOORU_BASE}vengeful_spirit_%28dota_2%29+"],
#
#             # Additional Characters
#             "keeper_of_the_light_persona": [f"{GELBOORU_BASE}keeper_of_the_light_persona+"],
#             "oracle_persona": [f"{GELBOORU_BASE}oracle_persona+"],
#             "anti_mage_persona": [f"{GELBOORU_BASE}anti_mage_persona+"]
#         },
#         "danbooru": {
#             # Mirror structure with danbooru base URLs
#         }
#     }
#
#     LOL_URLS = {
#         "gelbooru": {
#             # Popular Champions
#             "ahri": [f"{GELBOORU_BASE}ahri_%28league_of_legends%29+"],
#             "lux": [f"{GELBOORU_BASE}lux_%28league_of_legends%29+"],
#             "jinx": [f"{GELBOORU_BASE}jinx_%28league_of_legends%29+"],
#             "miss_fortune": [f"{GELBOORU_BASE}miss_fortune_%28league_of_legends%29+"],
#             "kaisa": [f"{GELBOORU_BASE}kai%27sa+"],
#
#             # Mid Lane
#             "katarina": [f"{GELBOORU_BASE}katarina_%28league_of_legends%29+"],
#             "leblanc": [f"{GELBOORU_BASE}leblanc_%28league_of_legends%29+"],
#             "lissandra": [f"{GELBOORU_BASE}lissandra_%28league_of_legends%29+"],
#             "orianna": [f"{GELBOORU_BASE}orianna_%28league_of_legends%29+"],
#             "syndra": [f"{GELBOORU_BASE}syndra+"],
#             "zoe": [f"{GELBOORU_BASE}zoe_%28league_of_legends%29+"],
#
#             # Bottom Lane
#             "ashe": [f"{GELBOORU_BASE}ashe_%28league_of_legends%29+"],
#             "caitlyn": [f"{GELBOORU_BASE}caitlyn_%28league_of_legends%29+"],
#             "senna": [f"{GELBOORU_BASE}senna_%28league_of_legends%29+"],
#             "seraphine": [f"{GELBOORU_BASE}seraphine_%28league_of_legends%29+"],
#             "xayah": [f"{GELBOORU_BASE}xayah+"],
#
#             # Top Lane
#             "fiora": [f"{GELBOORU_BASE}fiora_%28league_of_legends%29+"],
#             "irelia": [f"{GELBOORU_BASE}irelia+"],
#             "riven": [f"{GELBOORU_BASE}riven_%28league_of_legends%29+"],
#
#             # Jungle
#             "evelynn": [f"{GELBOORU_BASE}evelynn_%28league_of_legends%29+"],
#             "elise": [f"{GELBOORU_BASE}elise_%28league_of_legends%29+"],
#             "nidalee": [f"{GELBOORU_BASE}nidalee+"],
#
#             # Support
#             "janna": [f"{GELBOORU_BASE}janna_%28league_of_legends%29+"],
#             "lulu": [f"{GELBOORU_BASE}lulu_%28league_of_legends%29+"],
#             "nami": [f"{GELBOORU_BASE}nami_%28league_of_legends%29+"],
#             "soraka": [f"{GELBOORU_BASE}soraka_%28league_of_legends%29+"],
#             "yuumi": [f"{GELBOORU_BASE}yuumi_%28league_of_legends%29+"],
#
#             # New/Recent Champions
#             "bel_veth": [f"{GELBOORU_BASE}bel%27veth+"],
#             "nilah": [f"{GELBOORU_BASE}nilah_%28league_of_legends%29+"],
#             "zeri": [f"{GELBOORU_BASE}zeri_%28league_of_legends%29+"],
#             "renata": [f"{GELBOORU_BASE}renata_glasc+"],
#             "vex": [f"{GELBOORU_BASE}vex_%28league_of_legends%29+"],
#             "gwen": [f"{GELBOORU_BASE}gwen_%28league_of_legends%29+"],
#
#             # Additional Champions
#             "akali": [f"{GELBOORU_BASE}akali+"],
#             "anivia": [f"{GELBOORU_BASE}anivia+"],
#             "annie": [f"{GELBOORU_BASE}annie_%28league_of_legends%29+"],
#             "cassiopeia": [f"{GELBOORU_BASE}cassiopeia_%28league_of_legends%29+"],
#             "diana": [f"{GELBOORU_BASE}diana_%28league_of_legends%29+"],
#             "karma": [f"{GELBOORU_BASE}karma_%28league_of_legends%29+"],
#             "kayle": [f"{GELBOORU_BASE}kayle_%28league_of_legends%29+"],
#             "kindred": [f"{GELBOORU_BASE}kindred_%28league_of_legends%29+"],
#             "leona": [f"{GELBOORU_BASE}leona_%28league_of_legends%29+"],
#             "lillia": [f"{GELBOORU_BASE}lillia_%28league_of_legends%29+"],
#             "morgana": [f"{GELBOORU_BASE}morgana_%28league_of_legends%29+"],
#             "neeko": [f"{GELBOORU_BASE}neeko_%28league_of_legends%29+"],
#             "qiyana": [f"{GELBOORU_BASE}qiyana_%28league_of_legends%29+"],
#             "rell": [f"{GELBOORU_BASE}rell_%28league_of_legends%29+"],
#             "samira": [f"{GELBOORU_BASE}samira_%28league_of_legends%29+"],
#             "sejuani": [f"{GELBOORU_BASE}sejuani+"],
#             "shyvana": [f"{GELBOORU_BASE}shyvana+"],
#             "sivir": [f"{GELBOORU_BASE}sivir+"],
#             "sona": [f"{GELBOORU_BASE}sona_%28league_of_legends%29+"],
#             "taliyah": [f"{GELBOORU_BASE}taliyah+"],
#             "tristana": [f"{GELBOORU_BASE}tristana_%28league_of_legends%29+"],
#             "vayne": [f"{GELBOORU_BASE}vayne_%28league_of_legends%29+"]
#         },
#         "danbooru": {
#             # Mirror structure with danbooru base URLs
#         }
#     },
#
#     HATSUNE_MIKU_URLS = {
#         "gelbooru": {
#             # Main Crypton Vocaloids
#             "miku": [
#                 f"{GELBOORU_BASE}hatsune_miku+",
#                 f"{GELBOORU_BASE}miku_%28vocaloid%29+"
#             ],
#             "meiko": [f"{GELBOORU_BASE}meiko_%28vocaloid%29+"],
#             "rin": [
#                 f"{GELBOORU_BASE}kagamine_rin+",
#                 f"{GELBOORU_BASE}rin_%28vocaloid%29+"
#             ],
#             "luka": [
#                 f"{GELBOORU_BASE}megurine_luka+",
#                 f"{GELBOORU_BASE}luka_%28vocaloid%29+"
#             ],
#
#             # Other Popular Vocaloids
#             "gumi": [
#                 f"{GELBOORU_BASE}gumi+",
#                 f"{GELBOORU_BASE}megpoid_gumi+"
#             ],
#             "ia": [
#                 f"{GELBOORU_BASE}ia_%28vocaloid%29+",
#                 f"{GELBOORU_BASE}aria_on_the_planetes+"
#             ],
#
#             # UTAUs and Derivatives
#             "teto": [f"{GELBOORU_BASE}kasane_teto+"],
#             "neru": [
#                 f"{GELBOORU_BASE}akita_neru+",
#                 f"{GELBOORU_BASE}neru_%28vocaloid%29+"
#             ],
#             "haku": [
#                 f"{GELBOORU_BASE}yowane_haku+",
#                 f"{GELBOORU_BASE}haku_%28vocaloid%29+"
#             ],
#
#             # Newer Vocaloids
#             "una": [f"{GELBOORU_BASE}otomachi_una+"],
#             "cul": [f"{GELBOORU_BASE}cul_%28vocaloid%29+"],
#             "lily": [f"{GELBOORU_BASE}lily_%28vocaloid%29+"],
#             "miki": [
#                 f"{GELBOORU_BASE}sf-a2_miki+",
#                 f"{GELBOORU_BASE}miki_%28vocaloid%29+"
#             ],
#             "yukari": [f"{GELBOORU_BASE}yuzuki_yukari+"],
#
#             # Additional Characters
#             "mayu": [f"{GELBOORU_BASE}mayu_%28vocaloid%29+"],
#             "flower": [f"{GELBOORU_BASE}v_flower+"],
#             "mew": [f"{GELBOORU_BASE}mew_%28vocaloid%29+"],
#             "iroha": [f"{GELBOORU_BASE}nekomura_iroha+"],
#             "seeu": [f"{GELBOORU_BASE}seeu+"],
#             "galaco": [f"{GELBOORU_BASE}galaco+"],
#             "lenka": [f"{GELBOORU_BASE}lenka_%28vocaloid%29+"]
#         },
#         "danbooru": {
#             # Mirror structure with danbooru base URLs
#         }
#     }
#
#     LYCORIS_RECOIL_URLS = {
#         "gelbooru": {
#             "chisato": [f"{GELBOORU_BASE}nishikigi_chisato+"],
#             "takina": [f"{GELBOORU_BASE}inoue_takina+"],
#             "mizuki": [f"{GELBOORU_BASE}nakahara_mizuki+"],
#             "kurumi": [f"{GELBOORU_BASE}kurumi_%28lycoris_recoil%29+"],
#             "sakura": [f"{GELBOORU_BASE}otome_sakura+"],
#             "himegama": [f"{GELBOORU_BASE}himegama_%28lycoris_recoil%29+"],
#             "mika": [f"{GELBOORU_BASE}mika_%28lycoris_recoil%29+"],
#             "robota": [f"{GELBOORU_BASE}robota_%28lycoris_recoil%29+"],
#             "erika": [f"{GELBOORU_BASE}karuizawa_erika+"],
#             "shiori": [f"{GELBOORU_BASE}shiori_%28lycoris_recoil%29+"],
#             "fuki": [f"{GELBOORU_BASE}fuki_%28lycoris_recoil%29+"],
#             "yoshimatsu": [f"{GELBOORU_BASE}yoshimatsu_%28lycoris_recoil%29+"]
#         },
#         "danbooru": {
#             # Mirror structure with danbooru base URLs
#         }
#     }
#
#     KONOSUBA_URLS = {
#         "gelbooru": {
#             "aqua": [f"{GELBOORU_BASE}aqua_%28konosuba%29+"],
#             "megumin": [f"{GELBOORU_BASE}megumin+"],
#             "darkness": [f"{GELBOORU_BASE}darkness_%28konosuba%29+"],
#             "wiz": [f"{GELBOORU_BASE}wiz_%28konosuba%29+"],
#             "yunyun": [f"{GELBOORU_BASE}yunyun_%28konosuba%29+"],
#             "chris": [f"{GELBOORU_BASE}chris_%28konosuba%29+"],
#             "luna": [f"{GELBOORU_BASE}luna_%28konosuba%29+"],
#             "sena": [f"{GELBOORU_BASE}sena_%28konosuba%29+"],
#             "wolbach": [f"{GELBOORU_BASE}wolbach+"],
#             "iris": [f"{GELBOORU_BASE}iris_%28konosuba%29+"],
#             "komekko": [f"{GELBOORU_BASE}komekko+"],
#             "cecily": [f"{GELBOORU_BASE}cecily_%28konosuba%29+"],
#             "arue": [f"{GELBOORU_BASE}arue_%28konosuba%29+"],
#             "claire": [f"{GELBOORU_BASE}claire_%28konosuba%29+"],
#             "sylvia": [f"{GELBOORU_BASE}sylvia_%28konosuba%29+"],
#             "lean": [f"{GELBOORU_BASE}lean_%28konosuba%29+"],
#             "yuiyui": [f"{GELBOORU_BASE}yuiyui_%28konosuba%29+"],
#             # Additional characters
#             "eris": [f"{GELBOORU_BASE}eris_%28konosuba%29+"],
#             "lynn": [f"{GELBOORU_BASE}lynn_%28konosuba%29+"],
#             "alice": [f"{GELBOORU_BASE}alice_%28konosuba%29+"],
#             "funifura": [f"{GELBOORU_BASE}funifura+"],
#             "dodonko": [f"{GELBOORU_BASE}dodonko+"],
#             "serena": [f"{GELBOORU_BASE}serena_%28konosuba%29+"]
#         },
#         "danbooru": {
#             # Mirror structure with danbooru base URLs
#         }
#     },


def main():
    """Main entry point for the scraper"""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('scraper.log'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)

    try:
        # Setup configuration
        config = ScraperConfig(
            base_save_path="./hentai",
            request_timeout=30,
            download_delay=2,
            page_delay=1,
            chunk_size=8192,
            filename_length=6,
            headless=False,
            nsfw_threshold=0.5,
        )

        logger.info(f"Starting scraper with config: {config}")

        # Initialize threaded scraper
        threaded_gelbooru_scraper = ThreadedGelbooruScraper(config)

        # Initialize and setup scraper
        # scraper = HentaiScraper(config)
        # scraper.setup()

        #gelbooru_scraper = GelbooruScraper(config)
        # danbooru_scraper = DanbooruScraper(config)

        # https://danbooru.donmai.us/

        urls = {
            # ONE PIECE
            # "monkey_d_luffy": "https://gelbooru.com/index.php?page=post&s=list&tags=monkey_d_luffy",
            # "roronoa_zoro": "https://gelbooru.com/index.php?page=post&s=list&tags=roronoa_zoro",
            "nami": "https://gelbooru.com/index.php?page=post&s=list&tags=nami_(one_piece)",
            # "vinsmoke_sanji": "https://gelbooru.com/index.php?page=post&s=list&tags=vinsmoke_sanji",
            "nico_robin": "https://gelbooru.com/index.php?page=post&s=list&tags=nico_robin",
            # "uta": "https://gelbooru.com/index.php?page=post&s=list&tags=uta_(one_piece)",
            # "rebecca": "https://gelbooru.com/index.php?page=post&s=list&tags=rebecca_(one_piece)",
            # 'viola': "https://gelbooru.com/index.php?page=post&s=list&tags=viola_%28one_piece%29",  # Need to add
            # "carrot": "https://gelbooru.com/index.php?page=post&s=list&tags=carrot_(one_piece)",
            # "jewelry_bonney": "https://gelbooru.com/index.php?page=post&s=list&tags=jewelry_bonney",
            # "baby_5": "https://gelbooru.com/index.php?page=post&s=list&tags=baby_5",
            # "boa_hancock": "https://gelbooru.com/index.php?page=post&s=list&tags=boa_hancock",
            # "nefertari_vivi": "https://gelbooru.com/index.php?page=post&s=list&tags=nefertari_vivi",
            # "vinsmoke_reiju": "https://gelbooru.com/index.php?page=post&s=list&tags=vinsmoke_reiju",
            # "charlotte_linlin": "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_linlin",
            # "shimotsuki_kuina": "https://gelbooru.com/index.php?page=post&s=list&tags=shimotsuki_kuina",
            # "charlotte_smoothie": "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_smoothie",
            # "shirahoshi": "https://gelbooru.com/index.php?page=post&s=list&tags=shirahoshi",
            # "kouzuki_hiyori": "https://gelbooru.com/index.php?page=post&s=list&tags=kouzuki_hiyori",
            # "catarina_devon": "https://gelbooru.com/index.php?page=post&s=list&tags=catarina_devon",
            # "perona": "https://gelbooru.com/index.php?page=post&s=list&tags=perona",
            # "charlotte_flampe": "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_flampe",
            # "kouzuki_toki": "https://gelbooru.com/index.php?page=post&s=list&tags=kouzuki_toki",
            # "alvida": "https://gelbooru.com/index.php?page=post&s=list&tags=alvida_(one_piece)",
            # "kikunojo": "https://gelbooru.com/index.php?page=post&s=list&tags=kikunojo_(one_piece)",
            # "vegapunk_lilith": "https://gelbooru.com/index.php?page=post&s=list&tags=vegapunk_lilith",
            # "kaya": "https://gelbooru.com/index.php?page=post&s=list&tags=kaya_(one_piece)",
            # "monet": "https://gelbooru.com/index.php?page=post&s=list&tags=monet_(one_piece)",
            # "wanda": "https://gelbooru.com/index.php?page=post&s=list&tags=wanda_(one_piece)",
            # "nico_olvia": "https://gelbooru.com/index.php?page=post&s=list&tags=nico_olvia",
            # "nojiko": "https://gelbooru.com/index.php?page=post&s=list&tags=nojiko",
            # "charlotte_pudding": "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_pudding",
            # "vegapunk_atlas": "https://gelbooru.com/index.php?page=post&s=list&tags=vegapunk_atlas",
            # "vegapunk_york": "https://gelbooru.com/index.php?page=post&s=list&tags=vegapunk_york",
            # "stussy": "https://gelbooru.com/index.php?page=post&s=list&tags=stussy_(one_piece)",
            # "tashigi": "https://gelbooru.com/index.php?page=post&s=list&tags=tashigi",
            # "hina": "https://gelbooru.com/index.php?page=post&s=list&tags=hina_(one_piece)",
            # "isuka": "https://gelbooru.com/index.php?page=post&s=list&tags=isuka_(one_piece)",

            # DOTA 2
            # "lina": "https://gelbooru.com/index.php?page=post&s=list&tags=lina_%28dota_2%29+",
            # "lina": "https://gelbooru.com/index.php?page=post&s=list&tags=lina_%28dota%29+",
            # "crystal_maiden": "https://gelbooru.com/index.php?page=post&s=list&tags=crystal_maiden",
            # "windrunner": "https://gelbooru.com/index.php?page=post&s=list&tags=windranger_(dota)",
            # "marci": "https://gelbooru.com/index.php?page=post&s=list&tags=marci_(dota)",
            # "dark_willow": "https://gelbooru.com/index.php?page=post&s=list&tags=dark_willow",
            # "mirana": "https://gelbooru.com/index.php?page=post&s=list&tags=mirana_(dota)",
            # "broodmother": "https://gelbooru.com/index.php?page=post&s=list&tags=broodmother_(dota)",
            # "dawnbreaker": "https://gelbooru.com/index.php?page=post&s=list&tags=dawnbreaker_(dota)",
            # "death_prophet": "https://gelbooru.com/index.php?page=post&s=list&tags=death_prophet_(dota)",
            # "enchantress": "https://gelbooru.com/index.php?page=post&s=list&tags=enchantress_(dota)",
            # "legion_commander": "https://gelbooru.com/index.php?page=post&s=list&tags=legion_commander_(dota)",
            # "luna": "https://gelbooru.com/index.php?page=post&s=list&tags=luna_(dota)",
            # "naga_siren": "https://gelbooru.com/index.php?page=post&s=list&tags=naga_siren_(dota)",
            # "phantom_assassin": "https://gelbooru.com/index.php?page=post&s=list&tags=phantom_assassin_(dota)",
            # "queen_of_pain": "https://gelbooru.com/index.php?page=post&s=list&tags=queen_of_pain_(dota)",
            # "snapfire": "https://gelbooru.com/index.php?page=post&s=list&tags=snapfire",
            # "spectre": "https://gelbooru.com/index.php?page=post&s=list&tags=spectre_(dota)",
            # "templar_assassin": "https://gelbooru.com/index.php?page=post&s=list&tags=templar_assassin_(dota)",
            # "vengeful_spirit": "https://gelbooru.com/index.php?page=post&s=list&tags=vengeful_spirit_(dota_2)",

            # NARUTO
            "tsunade_senju": "https://gelbooru.com/index.php?page=post&s=list&tags=tsunade",
            "sakura_haruno": "https://gelbooru.com/index.php?page=post&s=list&tags=haruno_sakura",
            "hinata_hyuga": "https://gelbooru.com/index.php?page=post&s=list&tags=hyuuga_hinata",
            "tenten": "https://gelbooru.com/index.php?page=post&s=list&tags=tenten",
            "temari": "https://gelbooru.com/index.php?page=post&s=list&tags=temari",
            "kushina_uzumaki": "https://gelbooru.com/index.php?page=post&s=list&tags=uzumaki_kushina",
            "sarada_uchiha": "https://gelbooru.com/index.php?page=post&s=list&tags=uchiha_sarada",
            "himawari_uzumaki": "https://gelbooru.com/index.php?page=post&s=list&tags=uzumaki_himawari",
            "ino_yamanaka": "https://gelbooru.com/index.php?page=post&s=list&tags=yamanaka_ino",
            "kurenai_yuhi": "https://gelbooru.com/index.php?page=post&s=list&tags=yuuhi_kurenai",
            # Note: Different spelling
            "anko_mitarashi": "https://gelbooru.com/index.php?page=post&s=list&tags=mitarashi_anko",
            "shizune": "https://gelbooru.com/index.php?page=post&s=list&tags=shizune_(naruto)",
            "karin_uzumaki": "https://gelbooru.com/index.php?page=post&s=list&tags=karin_(naruto)",
            "konan": "https://gelbooru.com/index.php?page=post&s=list&tags=konan_(naruto)",
            "mei_terumi": "https://gelbooru.com/index.php?page=post&s=list&tags=terumi_mei",  # Note: Name order swapped
            "samui": "https://gelbooru.com/index.php?page=post&s=list&tags=samui_(naruto)",
            "karui": "https://gelbooru.com/index.php?page=post&s=list&tags=karui_(naruto)",
            "mabui": "https://gelbooru.com/index.php?page=post&s=list&tags=mabui_(naruto)",
            "yugao_uzuki": "https://gelbooru.com/index.php?page=post&s=list&tags=uzuki_yuugao",
            # Note: Different spelling
            "tsume_inuzuka": "https://gelbooru.com/index.php?page=post&s=list&tags=inuzuka_tsume",
            "hana_inuzuka": "https://gelbooru.com/index.php?page=post&s=list&tags=inuzuka_hana",
            "natsu_hyuga": "https://gelbooru.com/index.php?page=post&s=list&tags=hyuuga_natsu",
            "yakumo_kurama": "https://gelbooru.com/index.php?page=post&s=list&tags=kurama_yakumo",
            "tsunami": "https://gelbooru.com/index.php?page=post&s=list&tags=tsunami_(naruto)",
            "ayame": "https://gelbooru.com/index.php?page=post&s=list&tags=ichiraku_ayame",
            "yugito_nii": "https://gelbooru.com/index.php?page=post&s=list&tags=nii_yugito",
            "fuu": "https://gelbooru.com/index.php?page=post&s=list&tags=fuu_(naruto)",
            "hokuto": "https://gelbooru.com/index.php?page=post&s=list&tags=hokuto_(naruto)",
            "hanabi_hyuga": "https://gelbooru.com/index.php?page=post&s=list&tags=hyuuga_hanabi",
            "moegi": "https://gelbooru.com/index.php?page=post&s=list&tags=kazamatsuri_moegi",
            "sumire_kakei": "https://gelbooru.com/index.php?page=post&s=list&tags=kakei_sumire",
            "chocho_akimichi": "https://gelbooru.com/index.php?page=post&s=list&tags=akimichi_chouchou", # Note: Different spelling
            "mirai_sarutobi": "https://gelbooru.com/index.php?page=post&s=list&tags=sarutobi_mirai",
            "wasabi_izuno": "https://gelbooru.com/index.php?page=post&s=list&tags=izuno_wasabi",
            "namida_suzumeno": "https://gelbooru.com/index.php?page=post&s=list&tags=namida",# Note: URL uses first name only

            # FAIRY TAIL
            "lucy_heartfilia": "https://gelbooru.com/index.php?page=post&s=list&tags=lucy_heartfilia",
            "erza_scarlet": "https://gelbooru.com/index.php?page=post&s=list&tags=erza_scarlet",
            "wendy_marvell": "https://gelbooru.com/index.php?page=post&s=list&tags=wendy_marvell",
            "juvia_lockser": "https://gelbooru.com/index.php?page=post&s=list&tags=juvia_lockser",
            "levy_mcgarden": "https://gelbooru.com/index.php?page=post&s=list&tags=levy_mcgarden",
            "mirajane_strauss": "https://gelbooru.com/index.php?page=post&s=list&tags=mirajane_strauss",
            "lisanna_strauss": "https://gelbooru.com/index.php?page=post&s=list&tags=lisanna_strauss",
            "cana_alberona": "https://gelbooru.com/index.php?page=post&s=list&tags=cana_alberona",
            "evergreen": "https://gelbooru.com/index.php?page=post&s=list&tags=evergreen_(fairy_tail)",
            "bisca_connell": "https://gelbooru.com/index.php?page=post&s=list&tags=bisca_mulan",
            # Note: URL uses different name
            "laki_olietta": "https://gelbooru.com/index.php?page=post&s=list&tags=laki_olietta",
            "kinana": "https://gelbooru.com/index.php?page=post&s=list&tags=kinana_(fairy_tail)",
            "mavis_vermillion": "https://gelbooru.com/index.php?page=post&s=list&tags=mavis_vermilion",
            # Note: Different spelling
            "meredy": "https://gelbooru.com/index.php?page=post&s=list&tags=meredy_(fairy_tail)",
            "ultear_milkovich": "https://gelbooru.com/index.php?page=post&s=list&tags=ultear_milkovich",
            "yukino_agria": "https://gelbooru.com/index.php?page=post&s=list&tags=yukino_agria",
            "minerva_orlando": "https://gelbooru.com/index.php?page=post&s=list&tags=minerva_orlando",
            "kagura_mikazuchi": "https://gelbooru.com/index.php?page=post&s=list&tags=kagura_mikazuchi",
            "milliana": "https://gelbooru.com/index.php?page=post&s=list&tags=millianna",  # Note: Different spelling
            "flare_corona": "https://gelbooru.com/index.php?page=post&s=list&tags=flare_corona",
            "jenny_realight": "https://gelbooru.com/index.php?page=post&s=list&tags=jenny_realight",
            "sherry_blendy": "https://gelbooru.com/index.php?page=post&s=list&tags=sherry_blendy",
            "chelia_blendy": "https://gelbooru.com/index.php?page=post&s=list&tags=chelia_blendy",
            "sorano_agria": "https://gelbooru.com/index.php?page=post&s=list&tags=sorano_aguria", # Note: Different spelling
            "brandish_mu": "https://gelbooru.com/index.php?page=post&s=list&tags=brandish_mew", # Note: Different spelling
            "dimaria_yesta": "https://gelbooru.com/index.php?page=post&s=list&tags=dimaria_yesta",
            "irene_belserion": "https://gelbooru.com/index.php?page=post&s=list&tags=irene_belserion",
            "hisui_fiore": "https://gelbooru.com/index.php?page=post&s=list&tags=hisui_e._fiore", # Note: Different format

            # DRAGON BALL
            "bulma_briefs": "https://gelbooru.com/index.php?page=post&s=list&tags=bulma",
            "chi_chi": "https://gelbooru.com/index.php?page=post&s=list&tags=chi-chi_(dragon_ball)",
            "videl_satan": "https://ja.gelbooru.com/index.php?page=post&s=list&tags=videl",
            "pan": "https://gelbooru.com/index.php?page=post&s=list&tags=pan_(dragon_ball)",
            "android_18": "https://gelbooru.com/index.php?page=post&s=list&tags=android_18",
            "bulla_briefs": "https://gelbooru.com/index.php?page=post&s=list&tags=bra_(dragon_ball)",
            # Note: Uses alternate name
            "launch": "https://gelbooru.com/index.php?page=post&s=list&tags=launch_(dragon_ball)",
            "marron": "https://gelbooru.com/index.php?page=post&s=list&tags=marron_(dragon_ball)",
            "mai": "https://gelbooru.com/index.php?page=post&s=list&tags=mai_(dragon_ball)",
            "ranfan": "https://gelbooru.com/index.php?page=post&s=list&tags=ranfan",
            "vados": "https://gelbooru.com/index.php?page=post&s=list&tags=vados_(dragon_ball)",
            "caulifla": "https://gelbooru.com/index.php?page=post&s=list&tags=caulifla",
            "kale": "https://gelbooru.com/index.php?page=post&s=list&tags=kale_(dragon_ball)",
            "ribrianne": "https://gelbooru.com/index.php?page=post&s=list&tags=ribrianne",
            "oceanus_shenron": "https://gelbooru.com/index.php?page=post&s=list&tags=oceanus_shenron",
            "gine": "https://gelbooru.com/index.php?page=post&s=list&tags=gine",
            "fasha": "https://gelbooru.com/index.php?page=post&s=list&tags=fasha",
            "zangya": "https://gelbooru.com/index.php?page=post&s=list&tags=zangya",
            "towa": "https://gelbooru.com/index.php?page=post&s=list&tags=towa_(dragon_ball)",
            "chronoa": "https://gelbooru.com/index.php?page=post&s=list&tags=supreme_kai_of_time",
            "arale_norimaki": "https://gelbooru.com/index.php?page=post&s=list&tags=norimaki_arale",

            # ATTACK ON TITAN
            "mikasa_ackerman": "https://gelbooru.com/index.php?page=post&s=list&tags=mikasa_ackerman",
            "annie_leonhart": "https://gelbooru.com/index.php?page=post&s=list&tags=annie_leonhardt",
            # Note: Different spelling
            "historia_reiss": "https://gelbooru.com/index.php?page=post&s=list&tags=historia_reiss",
            "sasha_braus": "https://gelbooru.com/index.php?page=post&s=list&tags=sasha_braus",
            "hange_zoe": "https://gelbooru.com/index.php?page=post&s=list&tags=hange_zoe",
            "ymir": "https://gelbooru.com/index.php?page=post&s=list&tags=ymir_(shingeki_no_kyojin)",
            "pieck_finger": "https://gelbooru.com/index.php?page=post&s=list&tags=pieck",
            "gabi_braun": "https://gelbooru.com/index.php?page=post&s=list&tags=gabi_braun",
            "frieda_reiss": "https://gelbooru.com/index.php?page=post&s=list&tags=frieda_reiss",
            "carla_yeager": "https://gelbooru.com/index.php?page=post&s=list&tags=carla_yeager",
            "dina_fritz": "https://gelbooru.com/index.php?page=post&s=list&tags=dina_fritz",
            "petra_ral": "https://gelbooru.com/index.php?page=post&s=list&tags=petra_ral",
            "rico_brzenska": "https://gelbooru.com/index.php?page=post&s=list&tags=rico_brzenska",
            "yelena": "https://gelbooru.com/index.php?page=post&s=list&tags=yelena_(shingeki_no_kyojin)",
            "kiyomi_azumabito": "https://gelbooru.com/index.php?page=post&s=list&tags=kiyomi_azumabito",
            "louise": "https://gelbooru.com/index.php?page=post&s=list&tags=louise_(shingeki_no_kyojin)",
            "nifa": "https://gelbooru.com/index.php?page=post&s=list&tags=nifa_(shingeki_no_kyojin)",
            "lynne": "https://gelbooru.com/index.php?page=post&s=list&tags=lynne_(shingeki_no_kyojin)",
            "ilse_langnar": "https://gelbooru.com/index.php?page=post&s=list&tags=ilse_langner",
            # Note: Different spelling
            "nanaba": "https://gelbooru.com/index.php?page=post&s=list&tags=nanaba",

            # 'one_piece': "https://gelbooru.com/index.php?page=post&s=list&tags=one_piece",

            # 'dota_2': "https://gelbooru.com/index.php?page=post&s=list&tags=dota_2+",
            # 'dota_2': "https://gelbooru.com/index.php?page=post&s=list&tags=dota_(series)+",

            # 'dota_2_girls': "https://gelbooru.com/index.php?page=post&s=view&id=2447831",

            # Demon Slayer
            "nezuko_kamado": "https://gelbooru.com/index.php?page=post&s=list&tags=kamado_nezuko",
            "kanao_tsuyuri": "https://gelbooru.com/index.php?page=post&s=list&tags=tsuyuri_kanao",
            "shinobu_kocho": "https://gelbooru.com/index.php?page=post&s=list&tags=kochou_shinobu",
            "kanae_kocho": "https://gelbooru.com/index.php?page=post&s=list&tags=kochou_kanae",
            "mitsuri_kanroji": "https://gelbooru.com/index.php?page=post&s=list&tags=kanroji_mitsuri",
            "daki": "https://gelbooru.com/index.php?page=post&s=list&tags=daki_%28kimetsu_no_yaiba%29",
            "tamayo": "https://gelbooru.com/index.php?page=post&s=list&tags=tamayo_%28kimetsu_no_yaiba%29&pid=42",
            "makio": "https://gelbooru.com/index.php?page=post&s=list&tags=makio_%28kimetsu_no_yaiba%29",
            "suma": "https://gelbooru.com/index.php?page=post&s=list&tags=suma_%28kimetsu_no_yaiba%29",
            "hinatsuru": "https://gelbooru.com/index.php?page=post&s=list&tags=hinatsuru_%28kimetsu_no_yaiba%29",
            "aoi_kanzaki": "https://gelbooru.com/index.php?page=post&s=list&tags=kanzaki_aoi_%28kimetsu_no_yaiba%29",
            "kiyo_terauchi": "https://gelbooru.com/index.php?page=post&s=list&tags=terauchi_kiyo",
            "sumi_nakahara": "https://gelbooru.com/index.php?page=post&s=list&tags=nakahara_sumi",
            "naho_takada": "https://gelbooru.com/index.php?page=post&s=list&tags=takada_naho",
            "goto": "https://gelbooru.com/index.php?page=post&s=list&tags=goto_%28kimetsu_no_yaiba%29",
            "amane": "https://gelbooru.com/index.php?page=post&s=list&tags=ubuyashiki_amane",
            "mukago": "https://gelbooru.com/index.php?page=post&s=list&tags=mukago_%28kimetsu_no_yaiba%29",
            "ruka": "https://gelbooru.com/index.php?page=post&s=list&tags=rengoku_ruka",
            "hinaki_ubuyashiki": "https://gelbooru.com/index.php?page=post&s=list&tags=ubuyashiki_hinaki",
            "nichika_ubuyashiki": "https://gelbooru.com/index.php?page=post&s=list&tags=ubuyashiki_nichika",
            "kuina_ubuyashiki": "https://gelbooru.com/index.php?page=post&s=list&tags=ubuyashiki_kuina",

            # Jujutsu Kaisen
            "nobara_kugisaki": "https://gelbooru.com/index.php?page=post&s=list&tags=kugisaki_nobara",
            "maki_zenin": "https://gelbooru.com/index.php?page=post&s=list&tags=zen%27in_maki",
            "mei_mei": "https://gelbooru.com/index.php?page=post&s=list&tags=mei_mei_%28jujutsu_kaisen%29",
            "kasumi_miwa": "https://gelbooru.com/index.php?page=post&s=list&tags=miwa_kasumi",
            "momo_nishimiya": "https://gelbooru.com/index.php?page=post&s=list&tags=nishimiya_momo",
            "mai_zenin": "https://gelbooru.com/index.php?page=post&s=list&tags=zenin_mai",
            "yuki_tsukumo": "https://gelbooru.com/index.php?page=post&s=list&tags=tsukumo_yuki_%28jujutsu_kaisen%29",
            "rika": "https://gelbooru.com/index.php?page=post&s=list&tags=orimoto_rika",
            "utahime_iori": "https://gelbooru.com/index.php?page=post&s=list&tags=iori_utahime",
            "tsumiki_fushiguro": "https://gelbooru.com/index.php?page=post&s=list&tags=fushiguro_tsumiki",
            "manami_suda": "https://gelbooru.com/index.php?page=post&s=list&tags=suda_manami_%28jujutsu_kaisen%29",
            "saori_rokujo": "https://gelbooru.com/index.php?page=post&s=list&tags=saori_%28jujutsu_kaisen%29",
            "shoko_ieiri": "https://gelbooru.com/index.php?page=post&s=list&tags=ieiri_shoko",
            "mimiko_hasaba": "https://gelbooru.com/index.php?page=post&s=list&tags=mimiko_%28jujutsu_kaisen%29",
            "nanako_hasaba": "https://gelbooru.com/index.php?page=post&s=list&tags=nanako_%28jujutsu_kaisen%29",

            # Cowboy Bebop
            "faye_valentine": "https://gelbooru.com/index.php?page=post&s=list&tags=faye_valentine",
            "edward_wong": "https://gelbooru.com/index.php?page=post&s=list&tags=edward_wong_hau_pepelu_tivrusky_iv",
            "julia": "https://gelbooru.com/index.php?page=post&s=list&tags=julia_%28cowboy_bebop%29",
            "meifa_puzi": "https://gelbooru.com/index.php?page=post&s=list&tags=meifa_puzi",
            "judy": "https://gelbooru.com/index.php?page=post&s=list&tags=Judy_%28Cowboy_Bebop%29",
            "anastasia": "https://gelbooru.com/index.php?page=post&s=list&tags=bebop_%28cowboy_bebop%29",
            "alisa": "hhttps://gelbooru.com/index.php?page=post&s=list&tags=alisa_%28cowboy_bebop%29",
            # "victoria_terraforming": "https://gelbooru.com/index.php?page=post&s=list&tags=victoria_terraforming%28cowboy_bebop%29",
            # "stella_bonnaro": "https://api.example.com/images/cowboy_bebop/stella_main.jpg",
            # "coffee": "https://api.example.com/images/cowboy_bebop/coffee_main.jpg",
            "katrina_solensan": "https://gelbooru.com/index.php?page=post&s=list&tags=katerina_solensan",

            # Spy x Family
            "yor_forger": "https://gelbooru.com/index.php?page=post&s=list&tags=yor_forger",
            "anya_forger": "https://gelbooru.com/index.php?page=post&s=list&tags=anya_%28spy_x_family%29+",
            "sylvia_sherwood": "https://gelbooru.com/index.php?page=post&s=list&tags=sylvia_sherwood",
            "fiona_frost": "https://gelbooru.com/index.php?page=post&s=list&tags=fiona_frost",
            "becky_blackbell": "https://gelbooru.com/index.php?page=post&s=list&tags=becky_blackbell",
            "sharon": "https://gelbooru.com/index.php?page=post&s=list&tags=sharon_%28spy_x_family%29",
            "melinda_desmond": "https://gelbooru.com/index.php?page=post&s=list&tags=melinda_desmond",
            "camilla": "https://gelbooru.com/index.php?page=post&s=list&tags=camilla_%28spy_x_family%29",
            # "karen_gloomy": "https://api.example.com/images/spy_x_family/karen_main.jpg",
            "dominic": "https://gelbooru.com/index.php?page=post&s=list&tags=dominic_%28spy_x_family%29",
            "martha": "https://gelbooru.com/index.php?page=post&s=list&tags=martha_%28spy_x_family%29",

            # One Punch Man
            "fubuki": "https://gelbooru.com/index.php?page=post&s=list&tags=fubuki_%28one-punch_man%29",
            "tatsumaki": "https://gelbooru.com/index.php?page=post&s=list&tags=Tatsumaki",
            "psykos": "https://gelbooru.com/index.php?page=post&s=list&tags=psykos",
            "suiko": "https://gelbooru.com/index.php?page=post&s=list&tags=suiko_%28one-punch_man%29",
            "lin_lin": "https://gelbooru.com/index.php?page=post&s=list&tags=lin_lin_%28one-punch_man%29",
            "lily": "https://gelbooru.com/index.php?page=post&s=list&tags=sansetsukon_no_lily",
            "do_s": "https://gelbooru.com/index.php?page=post&s=list&tags=kaijin_hime_do-s",
            "mosquito_girl": "https://gelbooru.com/index.php?page=post&s=list&tags=mosquito_girl",
            "captain_mizuki": "https://gelbooru.com/index.php?page=post&s=list&tags=captain_mizuki",
            "shadow_ring": "https://gelbooru.com/index.php?page=post&s=list&tags=shadow_ring_%28one-punch_man%29",
            "zenko": "https://gelbooru.com/index.php?page=post&s=list&tags=zenko_%28one-punch_man%29",
            # "madame_shibabawa": "https://api.example.com/images/one_punch_man/madame_shibabawa_main.jpg",
            # "goddess_glasses": "https://api.example.com/images/one_punch_man/goddess_glasses_main.jpg",
            # "swim": "https://api.example.com/images/one_punch_man/swim_main.jpg",
            # "pai": "https://api.example.com/images/one_punch_man/pai_main.jpg",

            # League of Legends
            "ahri": "https://gelbooru.com/index.php?page=post&s=list&tags=ahri_%28league_of_legends%29", # https://gelbooru.com/index.php?page=post&s=list&tags=ahri
            "lux": "https://gelbooru.com/index.php?page=post&s=list&tags=lux_%28league_of_legends%29",
            "jinx": "https://gelbooru.com/index.php?page=post&s=list&tags=jinx_%28league_of_legends%29",
            "vi": "https://gelbooru.com/index.php?page=post&s=list&tags=vi_%28league_of_legends%29",
            "caitlyn": "https://gelbooru.com/index.php?page=post&s=list&tags=caitlyn_%28league_of_legends%29",
            "leona": "https://gelbooru.com/index.php?page=post&s=list&tags=leona_%28league_of_legends%29",
            "diana": "https://gelbooru.com/index.php?page=post&s=list&tags=diana_%28league_of_legends%29",
            "ashe": "https://gelbooru.com/index.php?page=post&s=list&tags=ashe_%28league_of_legends%29",
            "katarina": "https://gelbooru.com/index.php?page=post&s=list&tags=katarina_%28league_of_legends%29",
            "miss_fortune": "https://gelbooru.com/index.php?page=post&s=list&tags=miss_fortune_%28league_of_legends%29",
            "akali": "https://gelbooru.com/index.php?page=post&s=list&tags=akali",
            "anivia": "https://gelbooru.com/index.php?page=post&s=list&tags=anivia",
            "annie": "https://gelbooru.com/index.php?page=post&s=list&tags=annie_%28league_of_legends%29",
            "bel_veth": "https://gelbooru.com/index.php?page=post&s=list&tags=bel%27veth",
            "briar": "https://gelbooru.com/index.php?page=post&s=list&tags=briar_%28league_of_legends%29",
            "cassiopeia": "https://gelbooru.com/index.php?page=post&s=list&tags=cassiopeia_%28league_of_legends%29",
            "elise": "https://gelbooru.com/index.php?page=post&s=list&tags=elise_%28league_of_legends%29",
            "evelynn": "https://gelbooru.com/index.php?page=post&s=list&tags=evelynn_%28league_of_legends%29",
            "fiora": "https://gelbooru.com/index.php?page=post&s=list&tags=fiora_%28league_of_legends%29&pid=84",
            "gwen": "https://gelbooru.com/index.php?page=post&s=list&tags=gwen_%28league_of_legends%29",
            "illaoi": "https://gelbooru.com/index.php?page=post&s=list&tags=illaoi",
            "irelia": "https://gelbooru.com/index.php?page=post&s=list&tags=irelia",
            "janna": "https://gelbooru.com/index.php?page=post&s=list&tags=janna_%28league_of_legends%29",
            "kai_sa": "https://gelbooru.com/index.php?page=post&s=list&tags=kai%27sa",
            "kalista": "https://gelbooru.com/index.php?page=post&s=list&tags=kalista",
            "karma": "https://gelbooru.com/index.php?page=post&s=list&tags=karma_%28league_of_legends%29",
            "kindred": "https://gelbooru.com/index.php?page=post&s=list&tags=kindred_%28league_of_legends%29",
            "leblanc": "https://gelbooru.com/index.php?page=post&s=list&tags=leblanc_%28league_of_legends%29",
            "lillia": "https://gelbooru.com/index.php?page=post&s=list&tags=lillia_%28league_of_legends%29",
            "lissandra": "https://gelbooru.com/index.php?page=post&s=list&tags=lissandra_%28league_of_legends%29",
            "morgana": "https://gelbooru.com/index.php?page=post&s=list&tags=morgana_%28league_of_legends%29",
            "lol_nami": "https://gelbooru.com/index.php?page=post&s=list&tags=nami_(league_of_legends)",  # Renamed key for LoL Nami
            "neeko": "https://gelbooru.com/index.php?page=post&s=list&tags=neeko_%28league_of_legends%29",
            "nidalee": "https://gelbooru.com/index.php?page=post&s=list&tags=nidalee",
            "nilah": "https://gelbooru.com/index.php?page=post&s=list&tags=nilah_%28league_of_legends%29",
            "orianna": "https://gelbooru.com/index.php?page=post&s=list&tags=orianna_%28league_of_legends%29",
            "poppy": "https://gelbooru.com/index.php?page=post&s=list&tags=poppy_%28league_of_legends%29",
            "qiyana": "https://gelbooru.com/index.php?page=post&s=list&tags=qiyana_%28league_of_legends%29",
            "rell": "https://gelbooru.com/index.php?page=post&s=list&tags=rell_%28league_of_legends%29",
            "riven": "https://gelbooru.com/index.php?page=post&s=list&tags=riven_%28league_of_legends%29",
            "samira": "https://gelbooru.com/index.php?page=post&s=list&tags=league_of_legends",
            "senna": "https://gelbooru.com/index.php?page=post&s=list&tags=senna_%28league_of_legends%29",
            "seraphine": "https://gelbooru.com/index.php?page=post&s=list&tags=seraphine_%28league_of_legends%29",
            "sejuani": "https://gelbooru.com/index.php?page=post&s=list&tags=sejuani",
            "shyvana": "https://gelbooru.com/index.php?page=post&s=list&tags=shyvana",
            "sivir": "https://gelbooru.com/index.php?page=post&s=list&tags=sivir",
            "sona": "https://gelbooru.com/index.php?page=post&s=list&tags=sona_%28league_of_legends%29",
            "soraka": "https://gelbooru.com/index.php?page=post&s=list&tags=soraka_%28league_of_legends%29",
            "syndra": "https://gelbooru.com/index.php?page=post&s=list&tags=syndra",
            "taliyah": "https://gelbooru.com/index.php?page=post&s=list&tags=taliyah",
            "tristana": "https://gelbooru.com/index.php?page=post&s=list&tags=tristana_%28league_of_legends%29",
            "vayne": "https://gelbooru.com/index.php?page=post&s=list&tags=vayne_%28league_of_legends%29",
            "vex": "https://gelbooru.com/index.php?page=post&s=list&tags=vex_%28league_of_legends%29",
            "xayah": "https://gelbooru.com/index.php?page=post&s=list&tags=xayah",
            "yuumi": "https://gelbooru.com/index.php?page=post&s=list&tags=yuumi_%28league_of_legends%29",
            "zeri": "https://gelbooru.com/index.php?page=post&s=list&tags=zeri_%28league_of_legends%29",
            "zoe": "https://gelbooru.com/index.php?page=post&s=list&tags=zoe_%28league_of_legends%29",
            "zyra": "https://gelbooru.com/index.php?page=post&s=list&tags=zyra+league_of_legends",

            # Hunter x Hunter
            "biscuit_krueger": "https://gelbooru.com/index.php?page=post&s=list&tags=biscuit_krueger",
            "palm_siberia": "https://gelbooru.com/index.php?page=post&s=list&tags=palm_siberia",
            "machi": "https://gelbooru.com/index.php?page=post&s=list&tags=machi_%28hunter_x_hunter%29",
            "shizuku": "https://gelbooru.com/index.php?page=post&s=list&tags=shizuku_%28hunter_x_hunter%29",
            "canary": "https://gelbooru.com/index.php?page=post&s=list&tags=canary_%28hunter_x_hunter%29",
            "neferpitou": "https://gelbooru.com/index.php?page=post&s=list&tags=neferpitou",
            "komugi": "https://gelbooru.com/index.php?page=post&s=list&tags=komugi_%28hunter_x_hunter%29",
            "pakunoda": "https://gelbooru.com/index.php?page=post&s=list&tags=pakunoda",
            "melody": "https://gelbooru.com/index.php?page=post&s=list&tags=melody_(hunter_x_hunter)",
            "zazan": "https://gelbooru.com/index.php?page=post&s=list&tags=zazan_%28hunter_x_hunter%29",
            "eliza": "https://gelbooru.com/index.php?page=post&s=list&tags=eliza_%28hunter_x_hunter%29",
            "amane": "https://gelbooru.com/index.php?page=post&s=list&tags=amane_%28hunter_x_hunter%29",
            "tsubone": "https://gelbooru.com/index.php?page=post&s=list&tags=tsubone_%28hunter_x_hunter%29",
            "kalluto_zoldyck": "https://gelbooru.com/index.php?page=post&s=list&tags=kalluto_zoldyck",
            "kikyo_zoldyck": "https://gelbooru.com/index.php?page=post&s=list&tags=kikyou_zoldyck",
            "alluka_zoldyck": "https://gelbooru.com/index.php?page=post&s=list&tags=alluka_zoldyck",
            "cheadle_yorkshire": "https://gelbooru.com/index.php?page=post&s=list&tags=cheadle_yorkshire",
            "menchi": "https://gelbooru.com/index.php?page=post&s=list&tags=menchi_%28hunter_x_hunter%29",
            "ponzu": "https://gelbooru.com/index.php?page=post&s=list&tags=ponzu",

            # Fullmetal Alchemist
            "winry_rockbell": "https://api.example.com/images/fma/winry_main.jpg",
            "riza_hawkeye": "https://gelbooru.com/index.php?page=post&s=list&tags=winry_rockbell",
            "olivier_armstrong": "https://gelbooru.com/index.php?page=post&s=list&tags=olivier_mira_armstrong",
            "izumi_curtis": "https://gelbooru.com/index.php?page=post&s=list&tags=izumi_curtis",
            "mei_chang": "https://gelbooru.com/index.php?page=post&s=list&tags=may_chang",
            "maria_ross": "https://gelbooru.com/index.php?page=post&s=list&tags=maria_ross",
            "gracia_hughes": "https://gelbooru.com/index.php?page=post&s=list&tags=gracia_hughes",
            "elicia_hughes": "https://gelbooru.com/index.php?page=post&s=list&tags=elicia_hughes",
            "lan_fan": "https://gelbooru.com/index.php?page=post&s=list&tags=lan_fan",
            "paninya": "https://gelbooru.com/index.php?page=post&s=list&tags=paninya_%28fma%29",
            "sheska": "https://gelbooru.com/index.php?page=post&s=list&tags=sheska_%28fma%29",
            "rose_thomas": "https://gelbooru.com/index.php?page=post&s=list&tags=rose_thomas",
            "catherine_armstrong": "https://gelbooru.com/index.php?page=post&s=list&tags=catherine_elle_armstrong",
            "martel": "https://gelbooru.com/index.php?page=post&s=list&tags=martel_%28fma%29",
            "trisha_elric": "https://gelbooru.com/index.php?page=post&s=list&tags=trisha_elric",
            "pinako_rockbell": "https://gelbooru.com/index.php?page=post&s=list&tags=pinako_rockbell",
            "lust": "https://gelbooru.com/index.php?page=post&s=list&tags=lust_%28fma%29",
            "dante": "https://gelbooru.com/index.php?page=post&s=list&tags=dante_%28fma%29",
            "clara": "https://gelbooru.com/index.php?page=post&s=list&tags=clara_(fma)",

            # My Hero Academia
            "ochaco_uraraka": "https://gelbooru.com/index.php?page=post&s=list&tags=uraraka_ochako",
            "tsuyu_asui": "https://gelbooru.com/index.php?page=post&s=list&tags=asui_tsuyu",
            "momo_yaoyorozu": "https://gelbooru.com/index.php?page=post&s=list&tags=yaoyorozu_momo",
            "kyoka_jirou": "https://gelbooru.com/index.php?page=post&s=list&tags=sameyama_jiro",
            "toru_hagakure": "https://gelbooru.com/index.php?page=post&s=list&tags=hagakure_tooru",
            "mina_ashido": "https://gelbooru.com/index.php?page=post&s=list&tags=mina_ashido",
            "yu_takeyama": "https://gelbooru.com/index.php?page=post&s=list&tags=mount_lady",
            "nemuri_kayama": "https://gelbooru.com/index.php?page=post&s=list&tags=midnight_%28boku_no_hero_academia%29",
            "rumi_usagiyama": "https://gelbooru.com/index.php?page=post&s=list&tags=mirko",
            "ryuko_tatsuma": "https://gelbooru.com/index.php?page=post&s=list&tags=ryuukyuu",
            "nejire_hado": "https://gelbooru.com/index.php?page=post&s=list&tags=hadou_nejire",
            "shino_sosaki": "https://gelbooru.com/index.php?page=post&s=list&tags=mandalay_%28boku_no_hero_academia%29",
            "ryuko_tsuchikawa": "https://gelbooru.com/index.php?page=post&s=list&tags=pixie-bob_%28boku_no_hero_academia%29",
            "tomoko_shiretoko": "https://gelbooru.com/index.php?page=post&s=list&tags=ragdoll_%28boku_no_hero_academia%29",
            "itsuka_kendo": "https://gelbooru.com/index.php?page=post&s=list&tags=kendou_itsuka",
            "pony_tsunotori": "https://gelbooru.com/index.php?page=post&s=list&tags=tsunotori_pony",
            "kinoko_komori": "https://gelbooru.com/index.php?page=post&s=list&tags=komori_kinoko",
            "yui_kodai": "https://gelbooru.com/index.php?page=post&s=list&tags=kodai_yui",
            "reiko_yanagi": "https://gelbooru.com/index.php?page=post&s=list&tags=yanagi_reiko",
            "setsuna_tokage": "https://gelbooru.com/index.php?page=post&s=list&tags=tokage_setsuna",
            "melissa_shield": "https://gelbooru.com/index.php?page=post&s=list&tags=melissa_shield",
            "inko_midoriya": "https://gelbooru.com/index.php?page=post&s=list&tags=midoriya_inko",
            "fuyumi_todoroki": "https://gelbooru.com/index.php?page=post&s=list&tags=todoroki_fuyumi",
            "eri": "https://gelbooru.com/index.php?page=post&s=list&tags=eri_%28boku_no_hero_academia%29",
            "nnana_shimuraana": "https://gelbooru.com/index.php?page=post&s=list&tags=shimura_nana",
            "himiko_toga": "https://gelbooru.com/index.php?page=post&s=list&tags=toga_himiko",

            # Jojos Bizarre Adventure
            "jolyne_cujoh": "https://gelbooru.com/index.php?page=post&s=list&tags=kujo_jolyne",
            "lisa_lisa": "https://gelbooru.com/index.php?page=post&s=list&tags=lisa_lisa",
            "erina_pendleton": "https://gelbooru.com/index.php?page=post&s=list&tags=erina_pendleton",
            "trish_una": "https://gelbooru.com/index.php?page=post&s=list&tags=trish_una",
            "suzi_q": "https://gelbooru.com/index.php?page=post&s=list&tags=suzi_q",
            "holly_kujo": "https://gelbooru.com/index.php?page=post&s=list&tags=kuujou_holly",
            "yukako_yamagishi": "https://gelbooru.com/index.php?page=post&s=list&tags=yamagishi_yukako",
            "reimi_sugimoto": "https://gelbooru.com/index.php?page=post&s=list&tags=sugimoto_reimi",
            "hot_pants": "https://gelbooru.com/index.php?page=post&s=list&tags=hot_pants_%28sbr%29",
            "lucy_steel": "https://gelbooru.com/index.php?page=post&s=list&tags=lucy_steel",
            "yasuho_hirose": "https://gelbooru.com/index.php?page=post&s=list&tags=hirose_yasuho",
            "hermes_costello": "https://gelbooru.com/index.php?page=post&s=list&tags=ermes_costello",
            "foo_fighters": "https://gelbooru.com/index.php?page=post&s=list&tags=foo_fighters_%28jojo%29",
            "ermes_costello": "https://gelbooru.com/index.php?page=post&s=list&tags=ermes_costello",
            "gwess": "https://gelbooru.com/index.php?page=post&s=list&tags=gwess",
            "mariah": "https://gelbooru.com/index.php?page=post&s=list&tags=mariah_%28jojo%29",
            "midler": "https://gelbooru.com/index.php?page=post&s=list&tags=midler",
            "anne": "https://gelbooru.com/index.php?page=post&s=list&tags=runaway_girl_%28jojo%29",
            "tomoko_higashikata": "https://gelbooru.com/index.php?page=post&s=list&tags=higashikata_tomoko",

            # Pokemon
            "misty_waterflower": "https://gelbooru.com/index.php?page=post&s=list&tags=misty_%28pokemon%29",
            "may_maple": "https://gelbooru.com/index.php?page=post&s=list&tags=may_%28pokemon%29",
            "dawn_berlitz": "https://gelbooru.com/index.php?page=post&s=list&tags=dawn_%28pokemon%29+",
            "serena": "https://gelbooru.com/index.php?page=post&s=list&tags=serena_%28pokemon%29",
            "iris": "https://ja.gelbooru.com/index.php?page=post&s=list&tags=iris_%28pokemon%29",
            "lillie": "https://gelbooru.com/index.php?page=post&s=list&tags=lillie_%28pokemon%29",
            "cynthia": "https://gelbooru.com/index.php?page=post&s=list&tags=cynthia_%28pokemon%29",
            "diantha": "https://gelbooru.com/index.php?page=post&s=list&tags=diantha_%28pokemon%29",
            "lusamine": "https://gelbooru.com/index.php?page=post&s=list&tags=lusamine_%28pokemon%29",
            "sabrina": "https://gelbooru.com/index.php?page=post&s=list&tags=lusamine_%28pokemon%29",
            "erika": "https://gelbooru.com/index.php?page=post&s=list&tags=erika_%28pokemon%29",
            "whitney": "https://gelbooru.com/index.php?page=post&s=list&tags=whitney_%28pokemon%29",
            "jasmine": "https://gelbooru.com/index.php?page=post&s=list&tags=jasmine_%28pokemon%29",
            "clair": "https://gelbooru.com/index.php?page=post&s=list&tags=clair_%28pokemon%29",
            "flannery": "https://gelbooru.com/index.php?page=post&s=list&tags=flannery_%28pokemon%29",
            "winona": "https://gelbooru.com/index.php?page=post&s=list&tags=winona_%28pokemon%29",
            "roxanne": "https://gelbooru.com/index.php?page=post&s=list&tags=roxanne_%28pokemon%29",
            "gardenia": "https://gelbooru.com/index.php?page=post&s=list&tags=gardenia_%28pokemon%29",
            "candice": "https://gelbooru.com/index.php?page=post&s=list&tags=candice_%28pokemon%29",
            "fantina": "https://gelbooru.com/index.php?page=post&s=list&tags=fantina_%28pokemon%29",
            "elesa": "https://gelbooru.com/index.php?page=post&s=list&tags=elesa_%28pokemon%29",
            "skyla": "https://gelbooru.com/index.php?page=post&s=list&tags=skyla_%28pokemon%29",
            "korrina": "https://gelbooru.com/index.php?page=post&s=list&tags=korrina_%28pokemon%29",
            "valerie": "https://gelbooru.com/index.php?page=post&s=list&tags=valerie_%28pokemon%29",
            "olympia": "https://gelbooru.com/index.php?page=post&s=list&tags=olympia_%28pokemon%29",
            "mallow": "https://gelbooru.com/index.php?page=post&s=list&tags=mallow_%28pokemon%29",
            "lana": "https://gelbooru.com/index.php?page=post&s=list&tags=lana_%28pokemon%29",
            "lanas_mother": "https://gelbooru.com/index.php?page=post&s=list&tags=lana%27s_mother_%28pokemon%29",
            "nessa": "https://gelbooru.com/index.php?page=post&s=list&tags=nessa_%28pokemon%29",
            "marnie": "https://gelbooru.com/index.php?page=post&s=list&tags=marnie_%28pokemon%29",
            "sonia": "https://gelbooru.com/index.php?page=post&s=list&tags=sonia_%28pokemon%29+",
            "professor_juniper": "https://gelbooru.com/index.php?page=post&s=list&tags=professor_juniper",
            "nurse_joy": "https://gelbooru.com/index.php?page=post&s=list&tags=joy_%28pokemon%29",
            "officer_jenny": "https://gelbooru.com/index.php?page=post&s=list&tags=officer_jenny",
            "jessie": "https://gelbooru.com/index.php?page=post&s=list&tags=jessie_%28pokemon%29&pid=420",
            "bonnie": "https://gelbooru.com/index.php?page=post&s=list&tags=bonnie_%28pokemon%29+",
            "rosa": "https://gelbooru.com/index.php?page=post&s=list&tags=rosa_%28pokemon%29+",

            # Hatsune Miku
            "hatsune_miku": "https://gelbooru.com/index.php?page=post&s=list&tags=hatsune_miku",
            "meiko": "https://gelbooru.com/index.php?page=post&s=list&tags=meiko_%28vocaloid%29+",
            "kagamine_rin": "https://gelbooru.com/index.php?page=post&s=list&tags=kagamine_rin",
            "megurine_luka": "https://gelbooru.com/index.php?page=post&s=list&tags=vocaloid+hatsune_miku+megurine_luka",
            "megpoid_gumi": "https://gelbooru.com/index.php?page=post&s=list&tags=gumi",
            "kasane_teto": "https://gelbooru.com/index.php?page=post&s=list&tags=kasane_teto",
            "akita_neru": "https://gelbooru.com/index.php?page=post&s=list&tags=akita_neru+hatsune_miku",
            "yowane_haku": "https://gelbooru.com/index.php?page=post&s=list&tags=yowane_haku",
            "otomachi_una": "https://gelbooru.com/index.php?page=post&s=list&tags=otomachi_una",
            "ia": "https://gelbooru.com/index.php?page=post&s=list&tags=IA_%28vocaloid%29",
            "cul": "https://gelbooru.com/index.php?page=post&s=list&tags=cul",
            "lily": "https://gelbooru.com/index.php?page=post&s=list&tags=lily_%28vocaloid%29",
            "sf_a2_miki": "https://gelbooru.com/index.php?page=post&s=list&tags=sf-a2_miki",
            "yuzuki_yukari": "https://gelbooru.com/index.php?page=post&s=list&tags=chigasaki_yukari",

            # Konosuba
            "aqua": "https://gelbooru.com/index.php?page=post&s=list&tags=aqua_%28konosuba%29",
            "megumin": "https://gelbooru.com/index.php?page=post&s=list&tags=megumin+",
            "lalatina_dustiness": "https://gelbooru.com/index.php?page=post&s=list&tags=darkness_%28konosuba%29+",
            "wiz": "https://gelbooru.com/index.php?page=post&s=list&tags=wiz_%28konosuba%29+",
            "yunyun": "https://gelbooru.com/index.php?page=post&s=list&tags=yunyun_%28konosuba%29+",
            "chris": "https://gelbooru.com/index.php?page=post&s=list&tags=chris_%28konosuba%29+",
            "luna": "https://gelbooru.com/index.php?page=post&s=list&tags=luna_%28konosuba%29+",
            "sena": "https://gelbooru.com/index.php?page=post&s=list&tags=sena_%28konosuba%29+",
            "wolbach": "https://gelbooru.com/index.php?page=post&s=list&tags=wolbach",
            "iris": "https://gelbooru.com/index.php?page=post&s=list&tags=iris_%28konosuba%29+",
            "komekko": "https://gelbooru.com/index.php?page=post&s=list&tags=komekko",
            "cecily": "https://gelbooru.com/index.php?page=post&s=list&tags=cecily_%28konosuba%29+",
            "arue": "https://gelbooru.com/index.php?page=post&s=list&tags=arue_%28konosuba%29+",
            "claire": "https://gelbooru.com/index.php?page=post&s=list&tags=claire_%28konosuba%29+",
            "sylvia": "https://gelbooru.com/index.php?page=post&s=list&tags=sylvia_%28konosuba%29+",
            "lean": "https://gelbooru.com/index.php?page=post&s=list&tags=lean_%28konosuba%29+",
            "verdia": "https://gelbooru.com/index.php?page=post&s=list&tags=verdia+",
            "hans": "https://gelbooru.com/index.php?page=post&s=list&tags=hans_%28konosuba%29+",
            "yuiyui": "https://gelbooru.com/index.php?page=post&s=list&tags=yuiyui_%28konosuba%29+",

            # Lycoris Recoil
            "chisato_nishikigi": "https://gelbooru.com/index.php?page=post&s=list&tags=nishikigi_chisato",
            "takina_inoue": "https://gelbooru.com/index.php?page=post&s=list&tags=inoue_takina",
            "mizuki_nakahara": "https://gelbooru.com/index.php?page=post&s=list&tags=nakahara_mizuki",
            "kurumi_shinonome": "https://gelbooru.com/index.php?page=post&s=list&tags=kurumi_%28lycoris_recoil%29+",
            # "erika_karuizawa": "https://api.example.com/images/lycoris_recoil/erika_main.jpg",
            "sakura_otome": "https://gelbooru.com/index.php?page=post&s=list&tags=otome_sakura",
            "fuki_himegama": "https://gelbooru.com/index.php?page=post&s=list&tags=himegama_%28lycoris_recoil%29",
            "mika": "https://gelbooru.com/index.php?page=post&s=list&tags=mika_%28lycoris_recoil%29",
            "robota": "https://gelbooru.com/index.php?page=post&s=list&tags=robota_%28lycoris_recoil%29",
            # "lucy": "https://api.example.com/images/lycoris_recoil/lucy_main.jpg",
        }

        threaded_gelbooru_scraper.process_urls(urls, max_pages=380)

        # Get URLs for each scraper
        # gelbooru_urls = URLs.URLS["gelbooru"]
        # danbooru_urls = URLs.URLS["danbooru"]

        # Process URLs for each scraper
        # gelbooru_scraper.process_urls(gelbooru_urls)
        # danbooru_scraper.process_urls(danbooru_urls)

        # scraper.download_batch(urls)
        # threaded_gelbooru_scraper.process_urls(urls, max_pages=380, max_workers=4)

    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")

    except Exception as e:
        logger.error(f"Scraping failed: {str(e)}")
        raise
    finally:
        logger.info("Scraping completed")



if __name__ == "__main__":
    main()

