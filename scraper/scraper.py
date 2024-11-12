import sqlite3

import requests
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
from nudenet import NudeDetector
import urllib

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
            "bonney": ["jewelry bonney" , "jewelry_bonney", "bonney"],
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
            "chi_chi": ["chi chi", "chi_chi", "chi-chi"],
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

        "konosuba": {
            "aqua": ["aqua", "aqua_(konosuba)", "goddess_aqua", "useless_goddess"],
            "megumin": ["megumin", "megumin_(konosuba)", "explosion_girl", "crimson_demon_megumin"],
            "darkness": ["darkness", "darkness_(konosuba)", "dustiness_ford_lalatina", "lalatina", "crusader_darkness"],
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
            "chisato": ["chisato nishikigi", "chisato_nishikigi", "chisato", "nishikigi"],
            "takina": ["takina inoue", "takina_inoue", "takina"],
            "mizuki": ["mizuki nakahara", "mizuki_nakahara", "mizuki"],
            "kurumi": ["kurumi shinonome", "kurumi_shinonome", "walnut", "kurumi"],
            "erika": ["erika karuizawa", "erika_karuizawa", "erika"],
            "sakura": ["sakura otome", "sakura_otome", "sakura"],
            "himegama": ["fuki himegama", "fuki_himegama", "himegama"],
            "mika": ["mika"],
            "robota": ["robota"],
            "lucy": ["lucy"]
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
    nsfw_threshold: float = 0.0
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
    """Handles NSFW content detection"""

    def __init__(self, threshold: float = 0.0):
        self.threshold = threshold
        self._setup_logging()
        self._setup_detector()

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('nsfw_detector.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _setup_detector(self):
        try:
            from nudenet import NudeDetector
            self.detector = NudeDetector()
            self.logger.info("NSFW detector initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize NSFW detector: {str(e)}")
            raise

    def check_gif(self, gif_path: Path) -> Tuple[bool, float]:
        """
        Check if a GIF contains NSFW content by analyzing frames

        Returns:
            Tuple[bool, float]: (is_nsfw, max_confidence)
        """
        try:
            from PIL import Image
            import tempfile

            # Open the GIF
            gif = Image.open(str(gif_path))
            max_score = 0.0
            frames_checked = 0
            frame_scores = []

            # Create temporary directory for frame extraction
            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    # Process every nth frame (e.g., every 5th frame)
                    while gif:
                        if frames_checked % 5 == 0:  # Check every 5th frame
                            # Save current frame
                            frame_path = Path(temp_dir) / f"frame_{frames_checked}.png"
                            gif.save(str(frame_path))

                            # Check frame for NSFW content
                            is_frame_nsfw, frame_score = self.check_image(frame_path)
                            frame_scores.append(frame_score)
                            max_score = max(max_score, frame_score)

                            # Early exit if we find definite NSFW content
                            if frame_score > self.threshold * 1.5:
                                return True, frame_score

                        frames_checked += 1
                        try:
                            gif.seek(gif.tell() + 1)
                        except EOFError:
                            break

                    # Calculate final results
                    avg_score = sum(frame_scores) / len(frame_scores) if frame_scores else 0
                    is_nsfw = (
                            max_score > self.threshold or
                            avg_score > self.threshold * 0.8 or
                            len([s for s in frame_scores if s > self.threshold]) >= 2
                    )

                    self.logger.debug(
                        f"GIF analysis results for {gif_path}:\n"
                        f"Max score: {max_score:.2f}\n"
                        f"Avg score: {avg_score:.2f}\n"
                        f"Frames checked: {frames_checked}\n"
                        f"NSFW frames: {len([s for s in frame_scores if s > self.threshold])}"
                    )

                    return is_nsfw, max_score

                except Exception as e:
                    self.logger.error(f"Error processing GIF frames: {str(e)}")
                    return True, 1.0  # Err on side of caution

        except Exception as e:
            self.logger.error(f"Error analyzing GIF {gif_path}: {str(e)}")
            return True, 1.0  # Err on side of caution

    def check_content(self, file_path: Path) -> Tuple[bool, float]:
        """
        Universal checker that handles both static images and GIFs

        Returns:
            Tuple[bool, float]: (is_nsfw, confidence)
        """
        try:
            # Determine if file is a GIF
            from PIL import Image
            with Image.open(str(file_path)) as img:
                is_gif = getattr(img, "is_animated", False)

            if is_gif:
                return self.check_gif(file_path)
            else:
                return self.check_image(file_path)

        except Exception as e:
            self.logger.error(f"Error determining file type: {str(e)}")
            return True, 1.0  # Err on side of caution

    def check_image(self, image_path: Path) -> Tuple[bool, float]:
        """
        Enhanced NSFW detection with better sensitivity

        Returns:
            Tuple[bool, float]: (is_nsfw, confidence)
        """
        try:
            detections = self.detector.detect(str(image_path))

            if not detections:
                return False, 0.0

            # Calculate scores
            scores = [det.get('score', 0) for det in detections]
            max_score = max(scores) if scores else 0
            avg_score = sum(scores) / len(scores) if scores else 0

            # Count significant detections
            significant_detections = sum(1 for score in scores if score > 0.3)

            # Check for multiple detections
            is_nsfw = (
                    max_score > self.threshold or  # Any single strong detection
                    avg_score > self.threshold * 0.8 or  # High average confidence
                    significant_detections >= 2 or  # Multiple moderate detections
                    len(detections) >= 3  # Multiple body parts detected
            )

            if is_nsfw:
                self.logger.debug(
                    f"NSFW content in {image_path}:\n"
                    f"Max score: {max_score:.2f}\n"
                    f"Avg score: {avg_score:.2f}\n"
                    f"Significant detections: {significant_detections}\n"
                    f"Total detections: {len(detections)}\n"
                    f"Raw detections: {detections}"
                )

            return is_nsfw, max_score

        except Exception as e:
            self.logger.error(f"Error checking image {image_path}: {str(e)}")
            self.logger.error(f"Raw detections: {detections}")
            return True, 1.0  # Err on side of caution

class HentaiScraper:
    def __init__(self, config: ScraperConfig):
        self.config = config
        self.nsfw_detector = NSFWDetector(threshold=config.nsfw_threshold)
        self._setup_logging()
        self._setup_browser()
        self.setup()

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
        """Extract character name from URL and create appropriate path."""
        try:
            # Extract tags from source page URL
            if 'tags=' in source_page:
                tags = source_page.split('tags=')[-1].split('&')[0]
                tags = urllib.parse.unquote(tags)  # Decode URL-encoded characters

                # Parse character name from tags
                if '(' in tags and ')' in tags:
                    # Handle tags like "uta_(one_piece)"
                    character_tags = [tag for tag in tags.split() if '(' in tag and ')' in tag]
                    if character_tags:
                        character = character_tags[0]
                        series = character.split('(')[1].rstrip(')')
                        character_name = character.split('(')[0].rstrip('_')
                        return Path(series) / character_name

            # Default to raw directory if no character info found
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

    def _get_character_path(self, url: str, source_page: str) -> Path:
        """Extract character name from URL and create appropriate path."""
        try:
            # Extract tags from source page URL
            if 'tags=' in source_page:
                tags = source_page.split('tags=')[-1].split('&')[0]
                tags = urllib.parse.unquote(tags)  # Decode URL-encoded characters

                # Parse character name from tags
                if '(' in tags and ')' in tags:
                    # Handle tags like "uta_(one_piece)"
                    character_tags = [tag for tag in tags.split() if '(' in tag and ')' in tag]
                    if character_tags:
                        character = character_tags[0]
                        series = character.split('(')[1].rstrip(')')
                        character_name = character.split('(')[0].rstrip('_')
                        return Path(series) / character_name

            # Default to raw directory if no character info found
            return Path('raw')
        except Exception as e:
            self.logger.error(f"Error parsing character path: {str(e)}")
            return Path('raw')

    def process_urls(self, urls: Dict[str, str], max_pages: int = 380):
        """Process multiple URLs and download images with improved error handling."""
        processed_count = 0

        try:
            for search_term, base_url in urls.items():
                self.logger.info(f"Processing search term: {search_term}")

                for page_num in range(max_pages):
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
                        self.logger.error(f"Timeout on page {page_num + 1}")
                        continue
                    except Exception as e:
                        self.logger.error(f"Error processing page {page_num + 1}: {str(e)}")
                        continue

        except Exception as e:
            self.logger.error(f"Fatal error in process_urls: {str(e)}")
        finally:
            self.logger.info(f"Processed {processed_count} images successfully")
            try:
                self.browser.quit()
            except Exception as e:
                self.logger.error(f"Error closing browser: {str(e)}")

def main():
    """Main entry point for the scraper"""
    try:
        # Setup logging first
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper.log'),
                logging.StreamHandler()
            ]
        )
        logger = logging.getLogger(__name__)

        # Setup configuration with proper initialization
        config = ScraperConfig(
            base_save_path="./hentai",  # This will be converted to Path in __post_init__
            request_timeout=30,
            download_delay=2,
            page_delay=1,
            chunk_size=8192,
            filename_length=6,
            headless=False,
            nsfw_threshold=0.0,
        )

        # Log configuration
        logger.info(f"Starting scraper with config: {config}")

        # Initialize and setup scraper
        scraper = HentaiScraper(config)
        scraper.setup()

        # https://danbooru.donmai.us/

        urls = {
                # 'uta': 'https://gelbooru.com/index.php?page=post&s=list&tags=uta_%28one_piece%29',
                # 'rebecca': 'https://gelbooru.com/index.php?page=post&s=list&tags=rebecca_%28one_piece%29+',
                # 'carrot': "https://gelbooru.com/index.php?page=post&s=list&tags=carrot_%28one_piece%29+",
                # 'bonney': "https://gelbooru.com/index.php?page=post&s=list&tags=jewelry_bonney+",
                # 'baby_5': "https://gelbooru.com/index.php?page=post&s=list&tags=baby_5+",
                # 'robin': "https://gelbooru.com/index.php?page=post&s=list&tags=nico_robin+",
                # 'nami': "https://gelbooru.com/index.php?page=post&s=list&tags=nami_%28one_piece%29",
                # 'nami': "https://gelbooru.com/index.php?page=post&s=list&tags=nami_(one_piece)+",
                # 'boa_hancock': "https://gelbooru.com/index.php?page=post&s=list&tags=boa_hancock+",
                # 'robin': "https://gelbooru.com/index.php?page=post&s=list&tags=nico_robin_(cosplay)",
                # 'robin': "https://gelbooru.com/index.php?page=post&s=list&tags=nico_robin_(alabasta)",
                # 'vivi': "https://gelbooru.com/index.php?page=post&s=list&tags=nefertari_vivi+",
                # 'vinsmoke_reiju': "https://gelbooru.com/index.php?page=post&s=list&tags=vinsmoke_reiju+",
                # 'charlotte_linlin': "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_linlin+",
                # 'kuina': "https://gelbooru.com/index.php?page=post&s=view&id=10840090&tags=kuina+",
                # 'kuina': "https://gelbooru.com/index.php?page=post&s=view&id=10840088&tags=kuina+",
                # 'kuina': "https://gelbooru.com/index.php?page=post&s=view&id=10840087&tags=kuina+",
                # 'charlotte_smoothie': "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_smoothie+",
                # 'shirahoshi': "https://gelbooru.com/index.php?page=post&s=list&tags=shirahoshi",
                # 'kouzuki_hiyori': "https://gelbooru.com/index.php?page=post&s=list&tags=kouzuki_hiyori",
                # 'catarina_devon': "https://gelbooru.com/index.php?page=post&s=list&tags=catarina_devon",
                # 'perona': "https://gelbooru.com/index.php?page=post&s=list&tags=perona",
                # 'charlotte_flampe': "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_flampe",
                # 'kouzuki_toki': "https://gelbooru.com/index.php?page=post&s=list&tags=kouzuki_toki",
                # 'alvida': "https://gelbooru.com/index.php?page=post&s=list&tags=alvida_(one_piece)",
                # 'kikunojo': "https://gelbooru.com/index.php?page=post&s=list&tags=kikunojo_(one_piece)",
                # 'vegapunk_lilith': "https://gelbooru.com/index.php?page=post&s=list&tags=vegapunk_lilith",
                # 'kaya': "https://gelbooru.com/index.php?page=post&s=list&tags=kaya_(one_piece)",
                # 'lily': "https://gelbooru.com/index.php?page=post&s=view&id=4939575&tags=lily_(one_piece)",
                # 'monet': "https://gelbooru.com/index.php?page=post&s=list&tags=monet_(one_piece)",
                # 'wanda': "https://gelbooru.com/index.php?page=post&s=list&tags=wanda_(one_piece)",
                # 'rebecca': "https://gelbooru.com/index.php?page=post&s=list&tags=rebecca_(one_piece)",
                # 'nico_olvia': "https://gelbooru.com/index.php?page=post&s=list&tags=nico_olvia",
                # 'nojiko': "https://gelbooru.com/index.php?page=post&s=list&tags=nojiko",
                # 'charlotte_pudding': "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_pudding",
                # 'charlotte_prim': "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_prim",
                # 'charlotte_poire': "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_poire",
                # 'charlotte_anana': "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_anana",
                # 'charlotte_amande': "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_amande",
                # 'charlotte_meukle': "https://gelbooru.com/index.php?page=post&s=list&tags=charlotte_meukle",
                # 'carrot': "https://gelbooru.com/index.php?page=post&s=list&tags=carrot_(one_piece)",
                # 'bellett': "https://gelbooru.com/index.php?page=post&s=list&tags=bellett",
                # 'bellemere': "https://gelbooru.com/index.php?page=post&s=list&tags=bellemere",
                # 'baby_5': "https://gelbooru.com/index.php?page=post&s=list&tags=baby_5",
                # 'vegapunk_atlas': "https://gelbooru.com/index.php?page=post&s=list&tags=vegapunk_atlas",
                # 'vegapunk_york': "https://gelbooru.com/index.php?page=post&s=list&tags=vegapunk_york",
                # 'gion': "https://gelbooru.com/index.php?page=post&s=list&tags=gion_(one_piece)",
                # 'stussy': "https://gelbooru.com/index.php?page=post&s=list&tags=stussy_(one_piece)",
                # 'uta': "https://gelbooru.com/index.php?page=post&s=list&tags=uta_(one_piece)",
                # 'isuka': "https://gelbooru.com/index.php?page=post&s=view&id=8003494&tags=isuka_(one_piece)",
                # 'isuka': "https://gelbooru.com/index.php?page=post&s=view&id=7661332&tags=isuka_(one_piece)",
                # 'tashigi': "https://gelbooru.com/index.php?page=post&s=list&tags=tashigi",
                # 'hina': "https://gelbooru.com/index.php?page=post&s=list&tags=hina_(one_piece)",
                # 'kujaku': "https://gelbooru.com/index.php?page=post&s=list&tags=kujaku_(one_piece)",
                # 'hibari': "https://gelbooru.com/index.php?page=post&s=list&tags=hibari_(one_piece)+",
                # 'doll': "https://gelbooru.com/index.php?page=post&s=list&tags=doll_(one_piece)",
                # 'viola': "https://gelbooru.com/index.php?page=post&s=list&tags=viola_%28one_piece%29", # Need to add
                # 'one_piece': "https://gelbooru.com/index.php?page=post&s=list&tags=one_piece",
                # 'marci': "https://gelbooru.com/index.php?page=post&s=list&tags=marci_(dota)",
                # 'dark_willow': "https://gelbooru.com/index.php?page=post&s=list&tags=dark_willow",
                # 'mirana': "https://gelbooru.com/index.php?page=post&s=list&tags=mirana_(dota)+",
                # 'crystal_maiden': "https://gelbooru.com/index.php?page=post&s=list&tags=crystal_maiden+",
                # 'dota_2': "https://gelbooru.com/index.php?page=post&s=list&tags=dota_2+",
                # 'dota_2': "https://gelbooru.com/index.php?page=post&s=list&tags=dota_(series)+",
                # 'broodmother': "https://gelbooru.com/index.php?page=post&s=list&tags=broodmother_(dota)+",
                # 'dawnbreaker': "https://gelbooru.com/index.php?page=post&s=list&tags=dawnbreaker_(dota)+",
                # 'dawnbreaker': "https://gelbooru.com/index.php?page=post&s=list&tags=dawnbreaker_(dota_2)+",
                # 'death_prophet': "https://gelbooru.com/index.php?page=post&s=list&tags=death_prophet_(dota)+",
                # 'enchantress': "https://gelbooru.com/index.php?page=post&s=list&tags=enchantress_(dota)+",
                # 'enchantress': "https://gelbooru.com/index.php?page=post&s=list&tags=enchantress_(dota_2)+",
                # 'legion_commander': "https://gelbooru.com/index.php?page=post&s=list&tags=legion_commander_(dota)+",
                # 'luna': "https://gelbooru.com/index.php?page=post&s=list&tags=luna_(dota)",
                # 'dota_2_girls': "https://gelbooru.com/index.php?page=post&s=view&id=2447831",
                # 'marci': "https://gelbooru.com/index.php?page=post&s=list&tags=marci_(dota)+",
                # 'naga_siren': "https://gelbooru.com/index.php?page=post&s=list&tags=naga_siren_(dota)+",
                # 'phantom_assassin': "https://gelbooru.com/index.php?page=post&s=list&tags=phantom_assassin_(dota)+",
                # 'queen_of_pain': "https://gelbooru.com/index.php?page=post&s=list&tags=queen_of_pain_(dota)+",
                # 'snapfire': "https://gelbooru.com/index.php?page=post&s=list&tags=snapfire",
                # 'spectre': "https://gelbooru.com/index.php?page=post&s=list&tags=spectre_(dota)",
                # 'templar_assassin': "https://gelbooru.com/index.php?page=post&s=list&tags=templar_assassin_(dota)+",
                # 'vengeful_spirit': "https://gelbooru.com/index.php?page=post&s=list&tags=vengeful_spirit_(dota_2)+",
                # 'windranger': "https://gelbooru.com/index.php?page=post&s=list&tags=windranger_(dota)+",
                # 'winter_wyrven': "https://gelbooru.com/index.php?page=post&s=list&tags=winter_wyrven+",
                # "lucy": "https://gelbooru.com/index.php?page=post&s=list&tags=lucy_heartfilia",
                # "erza": "https://gelbooru.com/index.php?page=post&s=list&tags=erza_scarlet",
                # "wendy": "https://gelbooru.com/index.php?page=post&s=list&tags=wendy_marvell",
                # "juvia": "https://gelbooru.com/index.php?page=post&s=list&tags=juvia_lockser",
                # "levy": "https://gelbooru.com/index.php?page=post&s=list&tags=levy_mcgarden",
                # "mirajane": "https://gelbooru.com/index.php?page=post&s=list&tags=mirajane_strauss",
                # "lisanna": "https://gelbooru.com/index.php?page=post&s=list&tags=lisanna_strauss",
                # "cana": "https://gelbooru.com/index.php?page=post&s=list&tags=cana_alberona",
                # "evergreen": "https://gelbooru.com/index.php?page=post&s=list&tags=evergreen_%28fairy_tail%29",
                # "bisca": "https://gelbooru.com/index.php?page=post&s=list&tags=bisca_mulan",
                # "laki": "https://gelbooru.com/index.php?page=post&s=list&tags=laki_olietta",
                # "kinana": "https://gelbooru.com/index.php?page=post&s=list&tags=kinana_%28fairy_tail%29",
                # "mavis": "https://gelbooru.com/index.php?page=post&s=list&tags=mavis_vermilion",
                # "meredy": "https://gelbooru.com/index.php?page=post&s=list&tags=meredy_%28fairy_tail%29",
                # "ultear": "https://gelbooru.com/index.php?page=post&s=list&tags=ultear_milkovich",
                # "yukino": "https://gelbooru.com/index.php?page=post&s=list&tags=yukino_agria",
                # "minerva": "https://gelbooru.com/index.php?page=post&s=list&tags=minerva_orlando",
                # "kagura": "https://gelbooru.com/index.php?page=post&s=list&tags=kagura_mikazuchi",
                # "milliana": "https://gelbooru.com/index.php?page=post&s=list&tags=millianna",
                # "flare": "https://gelbooru.com/index.php?page=post&s=list&tags=flare_corona",
                # "jenny": "https://gelbooru.com/index.php?page=post&s=list&tags=jenny_realight",
                # "sherry": "https://gelbooru.com/index.php?page=post&s=list&tags=sherry_blendy",
                # "chelia": "https://gelbooru.com/index.php?page=post&s=list&tags=chelia_blendy",
                # "sorano": "https://gelbooru.com/index.php?page=post&s=list&tags=sorano_aguria",
                # "brandish": "https://gelbooru.com/index.php?page=post&s=list&tags=brandish_mew",
                # "dimaria": "https://gelbooru.com/index.php?page=post&s=list&tags=dimaria_yesta",
                # "irene": "https://gelbooru.com/index.php?page=post&s=list&tags=irene_belserion",
                # "hisui": "https://gelbooru.com/index.php?page=post&s=list&tags=hisui_e._fiore",
                # "bulma": "https://gelbooru.com/index.php?page=post&s=list&tags=bulma",
                # "chi_chi": "https://gelbooru.com/index.php?page=post&s=list&tags=chi-chi_%28dragon_ball%29",
                # "videl": "https://ja.gelbooru.com/index.php?page=post&s=list&tags=videl",
                # "pan": "https://gelbooru.com/index.php?page=post&s=list&tags=pan_%28dragon_ball%29",
                # "android_18": "https://gelbooru.com/index.php?page=post&s=list&tags=android_18",
                # "bulla": "https://gelbooru.com/index.php?page=post&s=list&tags=bra_%28dragon_ball%29",
                # "launch": "https://gelbooru.com/index.php?page=post&s=list&tags=launch_(dragon_ball)",
                # "marron": "https://gelbooru.com/index.php?page=post&s=list&tags=marron_%28dragon_ball%29",
                # "mai": "https://gelbooru.com/index.php?page=post&s=list&tags=mai_%28dragon_ball%29",
                # "ranfan": "https://gelbooru.com/index.php?page=post&s=list&tags=ranfan",
                # "vados": "https://gelbooru.com/index.php?page=post&s=list&tags=vados_%28dragon_ball%29",
                # "caulifla": "https://gelbooru.com/index.php?page=post&s=list&tags=caulifla",
                # "kale": "https://gelbooru.com/index.php?page=post&s=list&tags=kale_%28dragon_ball%29",
                # "ribrianne": "https://gelbooru.com/index.php?page=post&s=list&tags=ribrianne",
                # "oceanus": "https://gelbooru.com/index.php?page=post&s=list&tags=oceanus_shenron",
                # "gine": "https://gelbooru.com/index.php?page=post&s=list&tags=gine",
                # "fasha": "https://gelbooru.com/index.php?page=post&s=list&tags=fasha",
                # "zangya": "https://gelbooru.com/index.php?page=post&s=list&tags=zangya",
                # "towa": "https://gelbooru.com/index.php?page=post&s=list&tags=towa_%28dragon_ball%29",
                # "supreme_kai_of_time": "https://gelbooru.com/index.php?page=post&s=list&tags=supreme_kai_of_time",
                # "arale": "https://gelbooru.com/index.php?page=post&s=list&tags=norimaki_arale",
                # "mikasa": "https://gelbooru.com/index.php?page=post&s=list&tags=mikasa_ackerman",
                # "annie": "https://gelbooru.com/index.php?page=post&s=list&tags=annie_leonhardt",
                # "historia": "https://gelbooru.com/index.php?page=post&s=list&tags=historia_reiss",
                # "sasha": "https://gelbooru.com/index.php?page=post&s=list&tags=sasha_braus",
                # "hange": "https://gelbooru.com/index.php?page=post&s=list&tags=hange_zoe",
                # "ymir": "https://gelbooru.com/index.php?page=post&s=list&tags=ymir_%28shingeki_no_kyojin%29",
                # "pieck": "https://gelbooru.com/index.php?page=post&s=list&tags=pieck",
                # "gabi": "https://gelbooru.com/index.php?page=post&s=list&tags=gabi_braun",
                # "frieda": "https://gelbooru.com/index.php?page=post&s=list&tags=frieda_reiss",
                # "carla": "https://gelbooru.com/index.php?page=post&s=list&tags=carla_yeager",
                # "dina": "https://gelbooru.com/index.php?page=post&s=list&tags=dina_fritz",
                # "petra": "https://gelbooru.com/index.php?page=post&s=list&tags=petra_ral",
                # "rico": "https://gelbooru.com/index.php?page=post&s=list&tags=rico_brzenska",
                # "yelena": "https://gelbooru.com/index.php?page=post&s=list&tags=yelena_%28shingeki_no_kyojin%29",
                # "kiyomi": "https://gelbooru.com/index.php?page=post&s=list&tags=kiyomi_azumabito",
                # "louise": "https://gelbooru.com/index.php?page=post&s=list&tags=louise_%28shingeki_no_kyojin%29",
                # "nifa": "https://gelbooru.com/index.php?page=post&s=list&tags=nifa_%28shingeki_no_kyojin%29",
                # "lynne": "https://gelbooru.com/index.php?page=post&s=list&tags=lynne_%28shingeki_no_kyojin%29",
                # "ilse": "https://gelbooru.com/index.php?page=post&s=list&tags=ilse_langner",
                # "nanaba": "https://gelbooru.com/index.php?page=post&s=list&tags=nanaba",
                # "tsunade": "https://gelbooru.com/index.php?page=post&s=list&tags=tsunade",
                # "sakura": "https://gelbooru.com/index.php?page=post&s=list&tags=haruno_sakura",
                # "hinata": "https://gelbooru.com/index.php?page=post&s=list&tags=hyuuga_hinata",
                # "tenten": "https://gelbooru.com/index.php?page=post&s=list&tags=tenten",
                # "temari": "https://gelbooru.com/index.php?page=post&s=list&tags=temari",
                # "kushina": "https://gelbooru.com/index.php?page=post&s=list&tags=uzumaki_kushina",
                # "sarada": "https://gelbooru.com/index.php?page=post&s=list&tags=uchiha_sarada",
                # "himawari": "https://gelbooru.com/index.php?page=post&s=list&tags=uzumaki_himawari",
                # "ino": "https://gelbooru.com/index.php?page=post&s=list&tags=yamanaka_ino",
                # "kurenai": "https://gelbooru.com/index.php?page=post&s=list&tags=yuuhi_kurenai",
                # "anko": "https://gelbooru.com/index.php?page=post&s=list&tags=mitarashi_anko",
                # "shizune": "https://gelbooru.com/index.php?page=post&s=list&tags=shizune_%28naruto%29",
                # "karin": "https://gelbooru.com/index.php?page=post&s=list&tags=karin_%28naruto%29",
                # "konan": "https://gelbooru.com/index.php?page=post&s=list&tags=konan_%28naruto%29",
                # "mei": "https://gelbooru.com/index.php?page=post&s=list&tags=terumi_mei",
                # "samui": "https://gelbooru.com/index.php?page=post&s=list&tags=samui_%28naruto%29",
                # "karui": "https://gelbooru.com/index.php?page=post&s=list&tags=karui_%28naruto%29",
                # "mabui": "https://gelbooru.com/index.php?page=post&s=list&tags=mabui_%28naruto%29",
                # "yugao": "https://gelbooru.com/index.php?page=post&s=list&tags=uzuki_yuugao",
                # "tsume": "https://gelbooru.com/index.php?page=post&s=list&tags=inuzuka_tsume",
                # "hana": "https://gelbooru.com/index.php?page=post&s=list&tags=inuzuka_hana",
                # "natsu": "https://gelbooru.com/index.php?page=post&s=list&tags=hyuuga_natsu",
                # "yakumo": "https://gelbooru.com/index.php?page=post&s=list&tags=kurama_yakumo",
                # "tsunami": "https://gelbooru.com/index.php?page=post&s=list&tags=tsunami_%28naruto%29",
                # "ayame": "https://gelbooru.com/index.php?page=post&s=list&tags=ichiraku_ayame",
                # "yugito": "https://gelbooru.com/index.php?page=post&s=list&tags=nii_yugito&pid=0",
                # "fuu": "https://gelbooru.com/index.php?page=post&s=list&tags=fuu_%28naruto%29",
                # "hokuto": "https://gelbooru.com/index.php?page=post&s=list&tags=hokuto_%28naruto%29",
                # "hanabi": "https://gelbooru.com/index.php?page=post&s=list&tags=hyuuga_hanabi",
                # "moegi": "https://gelbooru.com/index.php?page=post&s=list&tags=kazamatsuri_moegi",
                # "sumire": "https://gelbooru.com/index.php?page=post&s=list&tags=kakei_sumire",
                # "chocho": "https://gelbooru.com/index.php?page=post&s=list&tags=akimichi_chouchou",
                # "mirai": "https://gelbooru.com/index.php?page=post&s=list&tags=sarutobi_mirai",
                # "wasabi": "https://gelbooru.com/index.php?page=post&s=list&tags=izuno_wasabi",
                # "namida": "https://gelbooru.com/index.php?page=post&s=list&tags=namida",
                # "nezuko": "https://gelbooru.com/index.php?page=post&s=list&tags=kamado_nezuko",
                # "kanao": "https://gelbooru.com/index.php?page=post&s=list&tags=tsuyuri_kanao",
                # "shinobu": "https://gelbooru.com/index.php?page=post&s=list&tags=kochou_shinobu",
                "kanae": "https://gelbooru.com/index.php?page=post&s=list&tags=kochou_kanae",
                "mitsuri": "https://gelbooru.com/index.php?page=post&s=list&tags=kanroji_mitsuri",
                "daki": "https://gelbooru.com/index.php?page=post&s=list&tags=daki_%28kimetsu_no_yaiba%29",
                "tamayo": "https://gelbooru.com/index.php?page=post&s=list&tags=tamayo_%28kimetsu_no_yaiba%29&pid=42",
                "makio": "https://gelbooru.com/index.php?page=post&s=list&tags=makio_%28kimetsu_no_yaiba%29",
                "suma": "https://gelbooru.com/index.php?page=post&s=list&tags=suma_%28kimetsu_no_yaiba%29",
                "hinatsuru": "https://gelbooru.com/index.php?page=post&s=list&tags=hinatsuru_%28kimetsu_no_yaiba%29",
                "aoi": "https://gelbooru.com/index.php?page=post&s=list&tags=kanzaki_aoi_%28kimetsu_no_yaiba%29",
                "kiyo": "https://gelbooru.com/index.php?page=post&s=list&tags=terauchi_kiyo",
                "sumi": "https://gelbooru.com/index.php?page=post&s=list&tags=nakahara_sumi",
                "naho": "https://gelbooru.com/index.php?page=post&s=list&tags=takada_naho",
                "goto": "https://gelbooru.com/index.php?page=post&s=list&tags=goto_%28kimetsu_no_yaiba%29",
                "amane": "https://gelbooru.com/index.php?page=post&s=list&tags=ubuyashiki_amane",
                "mukago": "https://gelbooru.com/index.php?page=post&s=list&tags=mukago_%28kimetsu_no_yaiba%29",
                "ruka": "https://gelbooru.com/index.php?page=post&s=list&tags=rengoku_ruka",
                "hinaki": "https://gelbooru.com/index.php?page=post&s=list&tags=ubuyashiki_hinaki",
                "nichika": "https://gelbooru.com/index.php?page=post&s=list&tags=ubuyashiki_nichika",
                "kuina": "https://gelbooru.com/index.php?page=post&s=list&tags=ubuyashiki_kuina",
                "nobara": "https://gelbooru.com/index.php?page=post&s=list&tags=kugisaki_nobara",
                "maki": "https://gelbooru.com/index.php?page=post&s=list&tags=zen%27in_maki",
                "mei_mei": "https://gelbooru.com/index.php?page=post&s=list&tags=mei_mei_%28jujutsu_kaisen%29",
                "miwa": "https://gelbooru.com/index.php?page=post&s=list&tags=miwa_kasumi",
                "momo": "https://gelbooru.com/index.php?page=post&s=list&tags=nishimiya_momo",
                "mai": "https://gelbooru.com/index.php?page=post&s=list&tags=zenin_mai",
                "yuki": "https://gelbooru.com/index.php?page=post&s=list&tags=tsukumo_yuki_%28jujutsu_kaisen%29",
                "rika": "https://gelbooru.com/index.php?page=post&s=list&tags=orimoto_rika",
                "utahime": "https://gelbooru.com/index.php?page=post&s=list&tags=iori_utahime",
                "tsumiki": "https://gelbooru.com/index.php?page=post&s=list&tags=fushiguro_tsumiki",
                "manami": "https://gelbooru.com/index.php?page=post&s=list&tags=suda_manami_%28jujutsu_kaisen%29",
                "saori": "https://gelbooru.com/index.php?page=post&s=list&tags=saori_%28jujutsu_kaisen%29",
                "shoko": "https://gelbooru.com/index.php?page=post&s=list&tags=ieiri_shoko",
                "mimiko": "https://gelbooru.com/index.php?page=post&s=list&tags=mimiko_%28jujutsu_kaisen%29",
                "nanako": "https://gelbooru.com/index.php?page=post&s=list&tags=nanako_%28jujutsu_kaisen%29",
                "faye": "https://gelbooru.com/index.php?page=post&s=list&tags=faye_valentine",
                "ed": "https://gelbooru.com/index.php?page=post&s=list&tags=edward_wong_hau_pepelu_tivrusky_iv",
                "julia": "https://gelbooru.com/index.php?page=post&s=list&tags=julia_%28cowboy_bebop%29",
                "meifa": "https://gelbooru.com/index.php?page=post&s=list&tags=meifa_puzi",
                "judy": "https://gelbooru.com/index.php?page=post&s=list&tags=Judy_%28Cowboy_Bebop%29",
                "annie": "https://gelbooru.com/index.php?page=post&s=list&tags=bebop_%28cowboy_bebop%29",
                "alisa": "hhttps://gelbooru.com/index.php?page=post&s=list&tags=alisa_%28cowboy_bebop%29",
                # "vip": "https://gelbooru.com/index.php?page=post&s=list&tags=cowboy_bebop",
                # "stella": "https://api.example.com/images/cowboy_bebop/stella_main.jpg",
                # "coffee": "https://api.example.com/images/cowboy_bebop/coffee_main.jpg",
                "katrina": "https://gelbooru.com/index.php?page=post&s=list&tags=katerina_solensan",
                "yor": "https://gelbooru.com/index.php?page=post&s=list&tags=yor_forger",
                "anya": "https://gelbooru.com/index.php?page=post&s=list&tags=anya_%28spy_x_family%29+",
                "sylvia": "https://gelbooru.com/index.php?page=post&s=list&tags=sylvia_sherwood",
                "fiona": "https://gelbooru.com/index.php?page=post&s=list&tags=fiona_frost",
                "becky": "https://gelbooru.com/index.php?page=post&s=list&tags=becky_blackbell",
                "sharon": "https://gelbooru.com/index.php?page=post&s=list&tags=sharon_%28spy_x_family%29",
                "melinda": "https://gelbooru.com/index.php?page=post&s=list&tags=melinda_desmond",
                "camilla": "https://gelbooru.com/index.php?page=post&s=list&tags=camilla_%28spy_x_family%29",
                # "karen": "https://api.example.com/images/spy_x_family/karen_main.jpg",
                "dominic": "https://gelbooru.com/index.php?page=post&s=list&tags=dominic_%28spy_x_family%29",
                "martha": "https://gelbooru.com/index.php?page=post&s=list&tags=martha_%28spy_x_family%29",
                "fubuki": "https://gelbooru.com/index.php?page=post&s=list&tags=fubuki_%28one-punch_man%29",
                "tatsumaki": "https://gelbooru.com/index.php?page=post&s=list&tags=Tatsumaki",
                "psykos": "https://gelbooru.com/index.php?page=post&s=list&tags=psykos",
                "suiko": "https://gelbooru.com/index.php?page=post&s=list&tags=suiko_%28one-punch_man%29",
                "lin_lin": "https://gelbooru.com/index.php?page=post&s=list&tags=lin_lin_%28one-punch_man%29",
                "lily": "https://gelbooru.com/index.php?page=post&s=list&tags=sansetsukon_no_lily",
                "do_s": "https://gelbooru.com/index.php?page=post&s=list&tags=kaijin_hime_do-s",
                "mosquito_girl": "https://gelbooru.com/index.php?page=post&s=list&tags=mosquito_girl",
                "mizuki": "https://gelbooru.com/index.php?page=post&s=list&tags=captain_mizuki",
                "shadow_ring": "https://gelbooru.com/index.php?page=post&s=list&tags=shadow_ring_%28one-punch_man%29",
                "zenko": "https://gelbooru.com/index.php?page=post&s=list&tags=zenko_%28one-punch_man%29",
                # "madame_shibabawa": "https://api.example.com/images/one_punch_man/madame_shibabawa_main.jpg",
                # "goddess_glasses": "https://api.example.com/images/one_punch_man/goddess_glasses_main.jpg",
                # "swim": "https://api.example.com/images/one_punch_man/swim_main.jpg",
                # "pai": "https://api.example.com/images/one_punch_man/pai_main.jpg",
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
                "gwen": "https://api.example.com/images/lol/gwen_main.jpg",
                "illaoi": "https://api.example.com/images/lol/illaoi_main.jpg",
                "irelia": "https://api.example.com/images/lol/irelia_main.jpg",
                "janna": "https://api.example.com/images/lol/janna_main.jpg",
                "kai_sa": "https://api.example.com/images/lol/kai_sa_main.jpg",
                "kalista": "https://api.example.com/images/lol/kalista_main.jpg",
                "karma": "https://api.example.com/images/lol/karma_main.jpg",
                "kindred": "https://api.example.com/images/lol/kindred_main.jpg",
                "leblanc": "https://api.example.com/images/lol/leblanc_main.jpg",
                "lillia": "https://api.example.com/images/lol/lillia_main.jpg",
                "lissandra": "https://api.example.com/images/lol/lissandra_main.jpg",
                "morgana": "https://api.example.com/images/lol/morgana_main.jpg",
                "nami": "https://api.example.com/images/lol/nami_main.jpg",
                "neeko": "https://api.example.com/images/lol/neeko_main.jpg",
                "nidalee": "https://api.example.com/images/lol/nidalee_main.jpg",
                "nilah": "https://api.example.com/images/lol/nilah_main.jpg",
                "orianna": "https://api.example.com/images/lol/orianna_main.jpg",
                "poppy": "https://api.example.com/images/lol/poppy_main.jpg",
                "qiyana": "https://api.example.com/images/lol/qiyana_main.jpg",
                "rell": "https://api.example.com/images/lol/rell_main.jpg",
                "riven": "https://api.example.com/images/lol/riven_main.jpg",
                "samira": "https://api.example.com/images/lol/samira_main.jpg",
                "senna": "https://api.example.com/images/lol/senna_main.jpg",
                "seraphine": "https://api.example.com/images/lol/seraphine_main.jpg",
                "sejuani": "https://api.example.com/images/lol/sejuani_main.jpg",
                "shyvana": "https://api.example.com/images/lol/shyvana_main.jpg",
                "sivir": "https://api.example.com/images/lol/sivir_main.jpg",
                "sona": "https://api.example.com/images/lol/sona_main.jpg",
                "soraka": "https://api.example.com/images/lol/soraka_main.jpg",
                "syndra": "https://api.example.com/images/lol/syndra_main.jpg",
                "taliyah": "https://api.example.com/images/lol/taliyah_main.jpg",
                "tristana": "https://api.example.com/images/lol/tristana_main.jpg",
                "vayne": "https://api.example.com/images/lol/vayne_main.jpg",
                "vex": "https://api.example.com/images/lol/vex_main.jpg",
                "xayah": "https://api.example.com/images/lol/xayah_main.jpg",
                "yuumi": "https://api.example.com/images/lol/yuumi_main.jpg",
                "zeri": "https://api.example.com/images/lol/zeri_main.jpg",
                "zoe": "https://api.example.com/images/lol/zoe_main.jpg",
                "zyra": "https://api.example.com/images/lol/zyra_main.jpg",
                "biscuit": "https://api.example.com/images/hunter_x_hunter/biscuit_main.jpg",
                "palm": "https://api.example.com/images/hunter_x_hunter/palm_main.jpg",
                "machi": "https://api.example.com/images/hunter_x_hunter/machi_main.jpg",
                "shizuku": "https://api.example.com/images/hunter_x_hunter/shizuku_main.jpg",
                "canary": "https://api.example.com/images/hunter_x_hunter/canary_main.jpg",
                "neferpitou": "https://api.example.com/images/hunter_x_hunter/neferpitou_main.jpg",
                "komugi": "https://api.example.com/images/hunter_x_hunter/komugi_main.jpg",
                "pakunoda": "https://api.example.com/images/hunter_x_hunter/pakunoda_main.jpg",
                "melody": "https://api.example.com/images/hunter_x_hunter/melody_main.jpg",
                "zazan": "https://api.example.com/images/hunter_x_hunter/zazan_main.jpg",
                "eliza": "https://api.example.com/images/hunter_x_hunter/eliza_main.jpg",
                "amane": "https://api.example.com/images/hunter_x_hunter/amane_main.jpg",
                "tsubone": "https://api.example.com/images/hunter_x_hunter/tsubone_main.jpg",
                "kalluto": "https://api.example.com/images/hunter_x_hunter/kalluto_main.jpg",
                "kikyo": "https://api.example.com/images/hunter_x_hunter/kikyo_main.jpg",
                "alluka": "https://api.example.com/images/hunter_x_hunter/alluka_main.jpg",
                "cheadle": "https://api.example.com/images/hunter_x_hunter/cheadle_main.jpg",
                "menchi": "https://api.example.com/images/hunter_x_hunter/menchi_main.jpg",
                "ponzu": "https://api.example.com/images/hunter_x_hunter/ponzu_main.jpg",
                "winry": "https://api.example.com/images/fma/winry_main.jpg",
                "riza": "https://api.example.com/images/fma/riza_main.jpg",
                "olivier": "https://api.example.com/images/fma/olivier_main.jpg",
                "izumi": "https://api.example.com/images/fma/izumi_main.jpg",
                "mei": "https://api.example.com/images/fma/mei_main.jpg",
                "maria": "https://api.example.com/images/fma/maria_main.jpg",
                "gracia": "https://api.example.com/images/fma/gracia_main.jpg",
                "elicia": "https://api.example.com/images/fma/elicia_main.jpg",
                "lan_fan": "https://api.example.com/images/fma/lan_fan_main.jpg",
                "paninya": "https://api.example.com/images/fma/paninya_main.jpg",
                "sheska": "https://api.example.com/images/fma/sheska_main.jpg",
                "rose": "https://api.example.com/images/fma/rose_main.jpg",
                "catherine": "https://api.example.com/images/fma/catherine_main.jpg",
                "martel": "https://api.example.com/images/fma/martel_main.jpg",
                "trisha": "https://api.example.com/images/fma/trisha_main.jpg",
                "pinako": "https://api.example.com/images/fma/pinako_main.jpg",
                "lust": "https://api.example.com/images/fma/lust_main.jpg",
                "dante": "https://api.example.com/images/fma/dante_main.jpg",
                "clara": "https://api.example.com/images/fma/clara_main.jpg",
                "uraraka": "https://api.example.com/images/mha/uraraka_main.jpg",
                "asui": "https://api.example.com/images/mha/asui_main.jpg",
                "yaoyorozu": "https://api.example.com/images/mha/yaoyorozu_main.jpg",
                "jirou": "https://api.example.com/images/mha/jirou_main.jpg",
                "hagakure": "https://api.example.com/images/mha/hagakure_main.jpg",
                "ashido": "https://api.example.com/images/mha/ashido_main.jpg",
                "mount_lady": "https://api.example.com/images/mha/mount_lady_main.jpg",
                "midnight": "https://api.example.com/images/mha/midnight_main.jpg",
                "mirko": "https://api.example.com/images/mha/mirko_main.jpg",
                "ryuku": "https://api.example.com/images/mha/ryuku_main.jpg",
                "nejire": "https://api.example.com/images/mha/nejire_main.jpg",
                "mandalay": "https://api.example.com/images/mha/mandalay_main.jpg",
                "pixie_bob": "https://api.example.com/images/mha/pixie_bob_main.jpg",
                "ragdoll": "https://api.example.com/images/mha/ragdoll_main.jpg",
                "kendo": "https://api.example.com/images/mha/kendo_main.jpg",
                "tsunotori": "https://api.example.com/images/mha/tsunotori_main.jpg",
                "komori": "https://api.example.com/images/mha/komori_main.jpg",
                "kodai": "https://api.example.com/images/mha/kodai_main.jpg",
                "yanagi": "https://api.example.com/images/mha/yanagi_main.jpg",
                "tokage": "https://api.example.com/images/mha/tokage_main.jpg",
                "melissa": "https://api.example.com/images/mha/melissa_main.jpg",
                "inko": "https://api.example.com/images/mha/inko_main.jpg",
                "fuyumi": "https://api.example.com/images/mha/fuyumi_main.jpg",
                "eri": "https://api.example.com/images/mha/eri_main.jpg",
                "nana": "https://api.example.com/images/mha/nana_main.jpg",
                "toga": "https://api.example.com/images/mha/toga_main.jpg",
                "jolyne": "https://api.example.com/images/jojo/jolyne_main.jpg",
                "lisa_lisa": "https://api.example.com/images/jojo/lisa_lisa_main.jpg",
                "erina": "https://api.example.com/images/jojo/erina_main.jpg",
                "trish": "https://api.example.com/images/jojo/trish_main.jpg",
                "suzi_q": "https://api.example.com/images/jojo/suzi_q_main.jpg",
                "holly": "https://api.example.com/images/jojo/holly_main.jpg",
                "yukako": "https://api.example.com/images/jojo/yukako_main.jpg",
                "reimi": "https://api.example.com/images/jojo/reimi_main.jpg",
                "hot_pants": "https://api.example.com/images/jojo/hot_pants_main.jpg",
                "lucy": "https://api.example.com/images/jojo/lucy_main.jpg",
                "yasuho": "https://api.example.com/images/jojo/yasuho_main.jpg",
                "hermes": "https://api.example.com/images/jojo/hermes_main.jpg",
                "foo_fighters": "https://api.example.com/images/jojo/foo_fighters_main.jpg",
                "ermes": "https://api.example.com/images/jojo/ermes_main.jpg",
                "gwess": "https://api.example.com/images/jojo/gwess_main.jpg",
                "mariah": "https://api.example.com/images/jojo/mariah_main.jpg",
                "midler": "https://api.example.com/images/jojo/midler_main.jpg",
                "anne": "https://api.example.com/images/jojo/anne_main.jpg",
                "tomoko": "https://api.example.com/images/jojo/tomoko_main.jpg",
                "misty": "https://api.example.com/images/pokemon/misty_main.jpg",
                "may": "https://api.example.com/images/pokemon/may_main.jpg",
                "dawn": "https://api.example.com/images/pokemon/dawn_main.jpg",
                "serena": "https://api.example.com/images/pokemon/serena_main.jpg",
                "iris": "https://api.example.com/images/pokemon/iris_main.jpg",
                "lillie": "https://api.example.com/images/pokemon/lillie_main.jpg",
                "cynthia": "https://api.example.com/images/pokemon/cynthia_main.jpg",
                "diantha": "https://api.example.com/images/pokemon/diantha_main.jpg",
                "lusamine": "https://api.example.com/images/pokemon/lusamine_main.jpg",
                "sabrina": "https://api.example.com/images/pokemon/sabrina_main.jpg",
                "erika": "https://api.example.com/images/pokemon/erika_main.jpg",
                "whitney": "https://api.example.com/images/pokemon/whitney_main.jpg",
                "jasmine": "https://api.example.com/images/pokemon/jasmine_main.jpg",
                "clair": "https://api.example.com/images/pokemon/clair_main.jpg",
                "flannery": "https://api.example.com/images/pokemon/flannery_main.jpg",
                "winona": "https://api.example.com/images/pokemon/winona_main.jpg",
                "roxanne": "https://api.example.com/images/pokemon/roxanne_main.jpg",
                "gardenia": "https://api.example.com/images/pokemon/gardenia_main.jpg",
                "candice": "https://api.example.com/images/pokemon/candice_main.jpg",
                "fantina": "https://api.example.com/images/pokemon/fantina_main.jpg",
                "elesa": "https://api.example.com/images/pokemon/elesa_main.jpg",
                "skyla": "https://api.example.com/images/pokemon/skyla_main.jpg",
                "korrina": "https://api.example.com/images/pokemon/korrina_main.jpg",
                "valerie": "https://api.example.com/images/pokemon/valerie_main.jpg",
                "olympia": "https://api.example.com/images/pokemon/olympia_main.jpg",
                "mallow": "https://api.example.com/images/pokemon/mallow_main.jpg",
                "lana": "https://api.example.com/images/pokemon/lana_main.jpg",
                "nessa": "https://api.example.com/images/pokemon/nessa_main.jpg",
                "marnie": "https://api.example.com/images/pokemon/marnie_main.jpg",
                "sonia": "https://api.example.com/images/pokemon/sonia_main.jpg",
                "professor_juniper": "https://api.example.com/images/pokemon/professor_juniper_main.jpg",
                "nurse_joy": "https://api.example.com/images/pokemon/nurse_joy_main.jpg",
                "officer_jenny": "https://api.example.com/images/pokemon/officer_jenny_main.jpg",
                "jessie": "https://api.example.com/images/pokemon/jessie_main.jpg",
                "bonnie": "https://api.example.com/images/pokemon/bonnie_main.jpg",
                "rosa": "https://api.example.com/images/pokemon/rosa_main.jpg",
                "miku": "https://api.example.com/images/vocaloid/miku_main.jpg",
                "meiko": "https://api.example.com/images/vocaloid/meiko_main.jpg",
                "rin": "https://api.example.com/images/vocaloid/rin_main.jpg",
                "luka": "https://api.example.com/images/vocaloid/luka_main.jpg",
                "gumi": "https://api.example.com/images/vocaloid/gumi_main.jpg",
                "teto": "https://api.example.com/images/vocaloid/teto_main.jpg",
                "neru": "https://api.example.com/images/vocaloid/neru_main.jpg",
                "haku": "https://api.example.com/images/vocaloid/haku_main.jpg",
                "una": "https://api.example.com/images/vocaloid/una_main.jpg",
                "ia": "https://api.example.com/images/vocaloid/ia_main.jpg",
                "cul": "https://api.example.com/images/vocaloid/cul_main.jpg",
                "lily": "https://api.example.com/images/vocaloid/lily_main.jpg",
                "miki": "https://api.example.com/images/vocaloid/miki_main.jpg",
                "yukari": "https://api.example.com/images/vocaloid/yukari_main.jpg",
                "aqua": "https://api.example.com/images/konosuba/aqua_main.jpg",
                "megumin": "https://api.example.com/images/konosuba/megumin_main.jpg",
                "darkness": "https://api.example.com/images/konosuba/darkness_main.jpg",
                "wiz": "https://api.example.com/images/konosuba/wiz_main.jpg",
                "yunyun": "https://api.example.com/images/konosuba/yunyun_main.jpg",
                "chris": "https://api.example.com/images/konosuba/chris_main.jpg",
                "luna": "https://api.example.com/images/konosuba/luna_main.jpg",
                "sena": "https://api.example.com/images/konosuba/sena_main.jpg",
                "wolbach": "https://api.example.com/images/konosuba/wolbach_main.jpg",
                "iris": "https://api.example.com/images/konosuba/iris_main.jpg",
                "komekko": "https://api.example.com/images/konosuba/komekko_main.jpg",
                "cecily": "https://api.example.com/images/konosuba/cecily_main.jpg",
                "arue": "https://api.example.com/images/konosuba/arue_main.jpg",
                "claire": "https://api.example.com/images/konosuba/claire_main.jpg",
                "sylvia": "https://api.example.com/images/konosuba/sylvia_main.jpg",
                "lean": "https://api.example.com/images/konosuba/lean_main.jpg",
                "verdia": "https://api.example.com/images/konosuba/verdia_main.jpg",
                "hans": "https://api.example.com/images/konosuba/hans_main.jpg",
                "yuiyui": "https://api.example.com/images/konosuba/yuiyui_main.jpg",
                "chisato": "https://api.example.com/images/lycoris_recoil/chisato_main.jpg",
                "takina": "https://api.example.com/images/lycoris_recoil/takina_main.jpg",
                "mizuki": "https://api.example.com/images/lycoris_recoil/mizuki_main.jpg",
                "kurumi": "https://api.example.com/images/lycoris_recoil/kurumi_main.jpg",
                "erika": "https://api.example.com/images/lycoris_recoil/erika_main.jpg",
                "sakura": "https://api.example.com/images/lycoris_recoil/sakura_main.jpg",
                "himegama": "https://api.example.com/images/lycoris_recoil/himegama_main.jpg",
                "mika": "https://api.example.com/images/lycoris_recoil/mika_main.jpg",
                "robota": "https://api.example.com/images/lycoris_recoil/robota_main.jpg",
                "lucy": "https://api.example.com/images/lycoris_recoil/lucy_main.jpg",
            }

        scraper.process_urls(urls, max_pages=380)

    # scraper.download_batch(urls)
    except KeyboardInterrupt:
        logging.info("Scraping interrupted by user")
    except Exception as e:
        logging.error(f"Scraping failed: {str(e)}")
        raise
    finally:
        logging.info("Scraping completed")



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
