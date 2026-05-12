from numpy.f2py.crackfortran import c
import json
import random
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from pprint import pprint
from typing import Dict, List

import ollama
import requests
import wikipediaapi
from bs4 import BeautifulSoup

@dataclass
class Data:
    page: str
    score: int

    def __repr__(self):
        return f"Data(page={self.page!r}, score={self.score})"

GAME_DATA = {'football': {'Campeonato_Brasileiro_Série_A': [Data(page='Club_Athletico_Paranaense', score=11871),
                                                Data(page='Esporte_Clube_Bahia', score=12103),
                                                Data(page='Botafogo_FR', score=24271),
                                                Data(page='Sport_Club_Corinthians_Paulista', score=13),
                                                Data(page='Coritiba_Foot_Ball_Club', score=7891),
                                                Data(page='Cruzeiro_EC', score=21362),
                                                Data(page='CR_Flamengo', score=49937),
                                                Data(page='Fluminense_FC', score=28248),
                                                Data(page='SC_Internacional', score=27996),
                                                Data(page='Mirassol_Futebol_Clube', score=6860),
                                                Data(page='SE_Palmeiras', score=29463),
                                                Data(page='Red_Bull_Bragantino', score=10486),
                                                Data(page='Clube_do_Remo', score=6768),
                                                Data(page='Santos_FC', score=44688),
                                                Data(page='CR_Vasco_da_Gama', score=25261)],
              'Brazil_Clubs': [Data(page='CR_Flamengo', score=49937),
                               Data(page='Fluminense_FC', score=28248),
                               Data(page='Botafogo_de_Futebol_e_Regatas', score=6),
                               Data(page='CR_Vasco_da_Gama', score=25261),
                               Data(page='America_Football_Club_(Rio_de_Janeiro)', score=5180),
                               Data(page='Volta_Redonda_Futebol_Clube', score=1),
                               Data(page='Sport_Club_Corinthians_Paulista', score=13),
                               Data(page='SE_Palmeiras', score=29463),
                               Data(page='Santos_FC', score=44688),
                               Data(page='Guarani_Futebol_Clube', score=3),
                               Data(page='Red_Bull_Bragantino', score=10486),
                               Data(page='Botafogo_Futebol_Clube_(SP)', score=3091),
                               Data(page='Cruzeiro_Esporte_Clube', score=13),
                               Data(page='Tombense_Futebol_Clube', score=846),
                               Data(page='Tupi_Football_Club', score=313),
                               Data(page='Sport_Club_Internacional', score=14),
                               Data(page='Esporte_Clube_Juventude', score=6429),
                               Data(page='Sociedade_Esportiva_e_Recreativa_Caxias_do_Sul', score=1248),
                               Data(page='Ypiranga_Futebol_Clube', score=967),
                               Data(page='Club_Athletico_Paranaense', score=11871),
                               Data(page='Coritiba_Foot_Ball_Club', score=7891),
                               Data(page='Londrina_Esporte_Clube', score=2042),
                               Data(page='Sport_Club_do_Recife', score=5102),
                               Data(page='Santa_Cruz_Futebol_Clube', score=3697),
                               Data(page='Central_Sport_Club', score=331),
                               Data(page='Esporte_Clube_Bahia', score=12103),
                               Data(page='Fluminense_de_Feira_Futebol_Clube', score=268),
                               Data(page='Sociedade_Desportiva_Juazeirense', score=290),
                               Data(page='Fortaleza_Esporte_Clube', score=5868),
                               Data(page='Floresta_Esporte_Clube', score=707),
                               Data(page='Figueirense_Futebol_Clube', score=2),
                               Data(page='Joinville_Esporte_Clube', score=1206),
                               Data(page='Brusque_Futebol_Clube', score=1616),
                               Data(page='Vila_Nova_Futebol_Clube', score=2421),
                               Data(page='Centro_Sportivo_Alagoano', score=1628),
                               Data(page='Clube_de_Regatas_Brasil', score=2276),
                               Data(page='ABC_Futebol_Clube', score=1309),
                               Data(page='Paysandu_Sport_Club', score=2833),
                               Data(page='Clube_do_Remo', score=6768),
                               Data(page='Manaus_Futebol_Clube', score=638)],
              'Campeonato_Brasileiro_Série_B': [Data(page='Athletic_Club_(MG)', score=3533),
                                                Data(page='Botafogo_Futebol_Clube_(SP)', score=3091),
                                                Data(page='Clube_de_Regatas_Brasil', score=2276),
                                                Data(page='Fortaleza_Esporte_Clube', score=5868),
                                                Data(page='Esporte_Clube_Juventude', score=6429),
                                                Data(page='Londrina_Esporte_Clube', score=2042),
                                                Data(page='Sport_Club_do_Recife', score=5102),
                                                Data(page='Vila_Nova_Futebol_Clube', score=2421)],
              'Global_Football_Teams': [Data(page='Argentina_national_football_team', score=119907),
                                        Data(page='Bolivia_national_football_team', score=24394),
                                        Data(page='Brazil_national_football_team', score=145140),
                                        Data(page='Chile_national_football_team', score=20749),
                                        Data(page='Colombia_national_football_team', score=41949),
                                        Data(page='Ecuador_national_football_team', score=33171),
                                        Data(page='Paraguay_national_football_team', score=32119),
                                        Data(page='Peru_national_football_team', score=13156),
                                        Data(page='Uruguay_national_football_team', score=52653),
                                        Data(page='Venezuela_national_football_team', score=11249),
                                        Data(page='Austria_national_football_team', score=33531),
                                        Data(page='Belgium_national_football_team', score=55107),
                                        Data(page='Croatia_national_football_team', score=55663),
                                        Data(page='Czech_Republic_national_football_team', score=56216),
                                        Data(page='Denmark_national_football_team', score=31792),
                                        Data(page='England_national_football_team', score=143455),
                                        Data(page='France_national_football_team', score=143456),
                                        Data(page='Germany_national_football_team', score=120701),
                                        Data(page='Hungary_national_football_team', score=21692),
                                        Data(page='Italy_national_football_team', score=171771),
                                        Data(page='Netherlands_national_football_team', score=76003),
                                        Data(page='Norway_national_football_team', score=54477),
                                        Data(page='Poland_national_football_team', score=34668),
                                        Data(page='Portugal_national_football_team', score=98411),
                                        Data(page='Scotland_national_football_team', score=47054),
                                        Data(page='Serbia_national_football_team', score=23172),
                                        Data(page='Spain_national_football_team', score=113022),
                                        Data(page="Sweden_men's_national_football_team", score=68429),
                                        Data(page='Switzerland_national_football_team', score=38013),
                                        Data(page='Turkey_national_football_team', score=64590),
                                        Data(page='Ukraine_national_football_team', score=16554),
                                        Data(page='Algeria_national_football_team', score=30315),
                                        Data(page='Cameroon_national_football_team', score=17331),
                                        Data(page='Egypt_national_football_team', score=32688),
                                        Data(page='Ghana_national_football_team', score=45771),
                                        Data(page='Ivory_Coast_national_football_team', score=38167),
                                        Data(page='Morocco_national_football_team', score=52362),
                                        Data(page='Nigeria_national_football_team', score=28856),
                                        Data(page='Senegal_national_football_team', score=33857),
                                        Data(page='South_Africa_national_football_team', score=5),
                                        Data(page='Tunisia_national_football_team', score=25226),
                                        Data(page='Australia_national_football_team', score=6),
                                        Data(page='Iran_national_football_team', score=46533),
                                        Data(page='Japan_national_football_team', score=87647),
                                        Data(page='Qatar_national_football_team', score=29346),
                                        Data(page='Saudi_Arabia_national_football_team', score=34674),
                                        Data(page='South_Korea_national_football_team', score=53090),
                                        Data(page="Canada_men's_national_soccer_team", score=53422),
                                        Data(page='Costa_Rica_national_football_team', score=14848),
                                        Data(page='Mexico_national_football_team', score=83426),
                                        Data(page="United_States_men's_national_soccer_team", score=91725)]},
 'games': {'Category:Role-playing_video_games': [Data(page='Chrono_Trigger', score=33827),
                                                 Data(page='Dark_Souls', score=35708),
                                                 Data(page='Deus_Ex', score=17052),
                                                 Data(page='Diablo', score=1281),
                                                 Data(page='EarthBound', score=25909),
                                                 Data(page='Fallout', score=82),
                                                 Data(page='Final_Fantasy_VI', score=24403),
                                                 Data(page='Final_Fantasy_VII', score=45939),
                                                 Data(page='Kingdom_Hearts', score=51187),
                                                 Data(page='The_Legend_of_Zelda:_Breath_of_the_Wild', score=43772),
                                                 Data(page='Mass_Effect_2', score=9078),
                                                 Data(page='Monster_Hunter:_World', score=12188),
                                                 Data(page='Paper_Mario:_The_Thousand-Year_Door', score=14991),
                                                 Data(page='Persona_5', score=47028),
                                                 Data(page='Secret_of_Mana', score=11210),
                                                 Data(page='Star_Wars:_Knights_of_the_Old_Republic', score=21367),
                                                 Data(page='Undertale', score=39104),
                                                 Data(page='Xenoblade_Chronicles', score=22694),
                                                 Data(page='Yakuza:_Like_a_Dragon', score=14605),
                                                 Data(page='Suikoden_II', score=4237)],
           'Category:Puzzle_video_games': [Data(page='Baba_Is_You', score=6392),
                                           Data(page='Bejeweled', score=381),
                                           Data(page='The_Legend_of_Zelda:_Tears_of_the_Kingdom', score=41257),
                                           Data(page='Lumines', score=1936),
                                           Data(page='Myst', score=23591),
                                           Data(page='Picross_3D', score=930),
                                           Data(page='Portal', score=2145),
                                           Data(page='Portal_2', score=17380),
                                           Data(page='Professor_Layton_and_the_Curious_Village', score=5092),
                                           Data(page='Puyo_Puyo_Tetris', score=2116),
                                           Data(page='Puzzle_Bobble', score=5346),
                                           Data(page='Return_of_the_Obra_Dinn', score=16646),
                                           Data(page='Snakebird', score=2),
                                           Data(page="Stephen's_Sausage_Roll", score=1902),
                                           Data(page='Tetris', score=48508),
                                           Data(page='Tetris_Effect', score=3540),
                                           Data(page='Thomas_Was_Alone', score=1503),
                                           Data(page='World_of_Goo', score=2933)],
           'Category:Simulation_video_games': [Data(page='Animal_Crossing:_New_Horizons', score=21655),
                                               Data(page='Cities:_Skylines', score=12314),
                                               Data(page='Disney_Dreamlight_Valley', score=9484),
                                               Data(page='Dwarf_Fortress', score=17267),
                                               Data(page='Euro_Truck_Simulator_2', score=26731),
                                               Data(page='Farming_Simulator_22', score=1),
                                               Data(page='Flight_Unlimited', score=582),
                                               Data(page='Goat_Simulator', score=8407),
                                               Data(page='Harvest_Moon:_Back_to_Nature', score=3469),
                                               Data(page='Kerbal_Space_Program', score=47099),
                                               Data(page='Microsoft_Flight_Simulator', score=13688),
                                               Data(page='Planet_Coaster', score=3376),
                                               Data(page='PowerWash_Simulator', score=6128),
                                               Data(page='Railroad_Tycoon_II', score=1503),
                                               Data(page='RimWorld', score=11331),
                                               Data(page='RollerCoaster_Tycoon', score=15394),
                                               Data(page='Space_Engineers', score=1980),
                                               Data(page='Stardew_Valley', score=35973),
                                               Data(page='The_Sims_4', score=20205),
                                               Data(page='Theme_Hospital', score=3717),
                                               Data(page='Two_Point_Hospital', score=2505),
                                               Data(page='Viscera_Cleanup_Detail', score=980)],
           'Category:Adventure_games': [Data(page='The_Stanley_Parable', score=19882),
                                        Data(page='Life_Is_Strange', score=52880),
                                        Data(page='The_Walking_Dead_(video_game)', score=15893),
                                        Data(page='Grim_Fandango', score=10856),
                                        Data(page="Monkey_Island_2:_LeChuck's_Revenge", score=3920),
                                        Data(page='The_Curse_of_Monkey_Island', score=5045),
                                        Data(page='The_Longest_Journey', score=4046),
                                        Data(page='Dreamfall:_The_Longest_Journey', score=2588),
                                        Data(page='Syberia', score=3876),
                                        Data(page='The_Book_of_Unwritten_Tales', score=523),
                                        Data(page='Broken_Sword:_The_Shadow_of_the_Templars', score=6450),
                                        Data(page='Gabriel_Knight:_Sins_of_the_Fathers', score=2580),
                                        Data(page="King's_Quest_VI:_Heir_Today,_Gone_Tomorrow", score=3),
                                        Data(page='Police_Quest:_In_Pursuit_of_the_Death_Angel', score=1538),
                                        Data(page='Quest_for_Glory:_So_You_Want_to_Be_a_Hero', score=1130),
                                        Data(page='Leisure_Suit_Larry_in_the_Land_of_the_Lounge_Lizards', score=4887),
                                        Data(page='The_Last_Express', score=2213),
                                        Data(page='To_the_Moon', score=2237),
                                        Data(page='What_Remains_of_Edith_Finch', score=20527),
                                        Data(page='Firewatch', score=15264),
                                        Data(page='Kentucky_Route_Zero', score=5225),
                                        Data(page='Disco_Elysium', score=58839),
                                        Data(page='Thimbleweed_Park', score=2381)],
           'Category:Strategy_video_games': [Data(page='StarCraft', score=18410),
                                             Data(page='StarCraft_II:_Wings_of_Liberty', score=7636),
                                             Data(page='Warcraft_III:_Reign_of_Chaos', score=15024),
                                             Data(page='Command_&_Conquer:_Red_Alert', score=12817),
                                             Data(page='Command_&_Conquer:_Tiberian_Sun', score=5301),
                                             Data(page='Age_of_Empires_II:_The_Age_of_Kings', score=4),
                                             Data(page='Age_of_Mythology', score=8953),
                                             Data(page='Rise_of_Nations', score=5305),
                                             Data(page='Empire_Earth', score=3943),
                                             Data(page='Sins_of_a_Solar_Empire', score=1962),
                                             Data(page='Homeworld', score=5276),
                                             Data(page='Dune_II', score=9236),
                                             Data(page='Total_Annihilation', score=4802),
                                             Data(page='Supreme_Commander', score=325),
                                             Data(page='Company_of_Heroes', score=3616),
                                             Data(page='World_in_Conflict', score=4193),
                                             Data(page="Tom_Clancy's_EndWar", score=3160),
                                             Data(page='Halo_Wars', score=6027),
                                             Data(page='Civilization_V', score=7043),
                                             Data(page='Civilization_VI', score=12284),
                                             Data(page='Master_of_Orion_II:_Battle_at_Antares', score=1344),
                                             Data(page='Master_of_Magic', score=1362),
                                             Data(page='Alpha_Centauri', score=68358),
                                             Data(page='Endless_Legend', score=1021),
                                             Data(page='Endless_Space_2', score=1005),
                                             Data(page='Stellaris', score=314),
                                             Data(page='Crusader_Kings_III', score=14379),
                                             Data(page='Europa_Universalis_IV', score=6483),
                                             Data(page='Hearts_of_Iron_IV', score=18532),
                                             Data(page='Victoria_3', score=6478),
                                             Data(page='Total_War:_Shogun_2', score=4593),
                                             Data(page='XCOM:_Enemy_Unknown', score=8409),
                                             Data(page='XCOM_2', score=8036),
                                             Data(page='Into_the_Breach', score=3996),
                                             Data(page='Fire_Emblem:_Three_Houses', score=14269),
                                             Data(page='Advance_Wars', score=7139)]},
 'tech': {'Programming_languages': [Data(page='C_(programming_language)', score=133299),
                                    Data(page='C_Sharp_(programming_language)', score=25141),
                                    Data(page='Java_(programming_language)', score=42373),
                                    Data(page='JavaScript', score=65229),
                                    Data(page='Python_(programming_language)', score=117790),
                                    Data(page='PHP', score=32953),
                                    Data(page='Ruby_(programming_language)', score=12849),
                                    Data(page='Swift_(programming_language)', score=14900),
                                    Data(page='Go_(programming_language)', score=36046),
                                    Data(page='Rust_(programming_language)', score=54513),
                                    Data(page='Kotlin', score=14164),
                                    Data(page='TypeScript', score=23175),
                                    Data(page='Dart_(programming_language)', score=8683),
                                    Data(page='Scala_(programming_language)', score=8995),
                                    Data(page='R_(programming_language)', score=38166),
                                    Data(page='Lua', score=23688),
                                    Data(page='Perl', score=15214),
                                    Data(page='Haskell', score=13266),
                                    Data(page='Erlang_(programming_language)', score=9334),
                                    Data(page='Elixir_(programming_language)', score=9079),
                                    Data(page='Clojure', score=9291),
                                    Data(page='Lisp_(programming_language)', score=32445),
                                    Data(page='Scheme_(programming_language)', score=7504),
                                    Data(page='OCaml', score=12650),
                                    Data(page='F_Sharp_(programming_language)', score=11622),
                                    Data(page='Fortran', score=25522),
                                    Data(page='COBOL', score=28810),
                                    Data(page='Ada_(programming_language)', score=15248),
                                    Data(page='Pascal_(programming_language)', score=13211),
                                    Data(page='Delphi_(software)', score=8806),
                                    Data(page='Assembly_language', score=33079),
                                    Data(page='SQL', score=30455),
                                    Data(page='Bash_(Unix_shell)', score=25209),
                                    Data(page='PowerShell', score=14706),
                                    Data(page='Julia_(programming_language)', score=10926),
                                    Data(page='MATLAB', score=16665),
                                    Data(page='Scratch_(programming_language)', score=56674),
                                    Data(page='Prolog', score=9879),
                                    Data(page='Smalltalk', score=11189),
                                    Data(page='Objective-C', score=9449),
                                    Data(page='Visual_Basic_(.NET)', score=6999),
                                    Data(page='ActionScript', score=3322),
                                    Data(page='Lua', score=23688),
                                    Data(page='AWK', score=6078),
                                    Data(page='APL_(programming_language)', score=7759),
                                    Data(page='Simula', score=2930),
                                    Data(page='Logo_(programming_language)', score=6636)],
          'software': [Data(page='1Password', score=5949),
                       Data(page='9GAG', score=11),
                       Data(page='Adblock_Plus', score=2709),
                       Data(page='AllTrails', score=1318),
                       Data(page='Amazon_Prime_Video', score=82949),
                       Data(page='Amazon_Music', score=4005),
                       Data(page='Audible_(service)', score=6494),
                       Data(page='AutoCAD', score=15200),
                       Data(page='Avast_Antivirus', score=4160),
                       Data(page='Babbel', score=2281),
                       Data(page='BBC_iPlayer', score=12607),
                       Data(page='BitTorrent_(software)', score=2254),
                       Data(page='Bitwarden', score=8846),
                       Data(page='Blogger_(service)', score=8319),
                       Data(page='CamScanner', score=1759),
                       Data(page='CapCut', score=107631),
                       Data(page='ChatGPT_(mobile_app)', score=1),
                       Data(page='Chess.com', score=24646),
                       Data(page='Crunchyroll', score=34927),
                       Data(page='Discord', score=95932),
                       Data(page='Disney+', score=63831),
                       Data(page='DeepL_Translator', score=19431),
                       Data(page='DuckDuckGo', score=169396),
                       Data(page='Duolingo', score=25810),
                       Data(page='ES_File_Explorer', score=1296),
                       Data(page='Evernote', score=4664),
                       Data(page='FaceApp', score=3036),
                       Data(page='Facebook', score=725869),
                       Data(page='Firefox_for_Android', score=2400),
                       Data(page='Fitbit', score=11522),
                       Data(page='Flickr', score=11059),
                       Data(page='Flipboard', score=1652),
                       Data(page='Gboard', score=4065),
                       Data(page='Google_Assistant', score=7830),
                       Data(page='Google_Earth', score=127905),
                       Data(page='Google_Gemini', score=115466),
                       Data(page='Google_Maps', score=227765),
                       Data(page='HBO_Max', score=80339),
                       Data(page='Hulu', score=51747),
                       Data(page='IBeer', score=1),
                       Data(page='Instagram', score=1056427),
                       Data(page='Jamboard', score=1655),
                       Data(page='Kodi_(software)', score=6849),
                       Data(page='Krita', score=9316),
                       Data(page='Last.fm', score=31006),
                       Data(page='Lyft', score=8954),
                       Data(page='Malwarebytes_(software)', score=5766),
                       Data(page='Mercado_Libre', score=10607),
                       Data(page='Microsoft_Copilot', score=63108),
                       Data(page='Microsoft_Teams', score=81753),
                       Data(page='Musical.ly', score=12755),
                       Data(page='MX_Player', score=19276),
                       Data(page='MyFitnessPal', score=3561),
                       Data(page='Myspace', score=42232),
                       Data(page='Netflix', score=226176),
                       Data(page='Notion_(productivity_software)', score=17134),
                       Data(page='Obsidian_(software)', score=33506),
                       Data(page='OkCupid', score=5065),
                       Data(page='OneDrive', score=11637),
                       Data(page='OpenTable', score=3375),
                       Data(page='Pandora_(service)', score=6899)],
          'Software_companies': [Data(page='Adobe_Inc.', score=32725),
                                 Data(page='Alphabet_Inc.', score=88175),
                                 Data(page='Amazon_(company)', score=175538),
                                 Data(page='Apple_Inc.', score=292769),
                                 Data(page='Asana,_Inc.', score=8083),
                                 Data(page='Autodesk', score=15855),
                                 Data(page='Automattic', score=4961),
                                 Data(page='Backblaze', score=1815),
                                 Data(page='BMC_Software', score=3890),
                                 Data(page='Box,_Inc.', score=5975),
                                 Data(page='Cadence_Design_Systems', score=9955),
                                 Data(page='Citrix_Systems', score=6076),
                                 Data(page='Cloudera', score=4537),
                                 Data(page='Cloudflare', score=34931),
                                 Data(page='Coursera', score=11694),
                                 Data(page='Datadog', score=11322),
                                 Data(page='Google', score=543482),
                                 Data(page='Intuit', score=18556),
                                 Data(page='Microsoft', score=164753),
                                 Data(page='Oracle_Corporation', score=158096),
                                 Data(page='Docker,_Inc.', score=4385),
                                 Data(page='Docusign', score=10124),
                                 Data(page='Dropbox', score=13109),
                                 Data(page='ElevenLabs', score=28882),
                                 Data(page='Epic_Systems', score=22180),
                                 Data(page='Esri', score=5850),
                                 Data(page='F5,_Inc.', score=5168),
                                 Data(page='Fastly', score=3834),
                                 Data(page='HashiCorp', score=10287),
                                 Data(page='Hewlett_Packard_Enterprise', score=15741),
                                 Data(page='HP_Inc.', score=23123),
                                 Data(page='HubSpot', score=12183),
                                 Data(page='IBM', score=73747),
                                 Data(page='Intel', score=52692),
                                 Data(page='ITA_Software', score=778),
                                 Data(page='Jamf', score=2537),
                                 Data(page='Joyent', score=1103),
                                 Data(page='JW_Player', score=2052),
                                 Data(page='MathWorks', score=5283),
                                 Data(page='McAfee', score=15613),
                                 Data(page='MongoDB_Inc.', score=3896),
                                 Data(page='Mozilla_Corporation', score=6069),
                                 Data(page='New_Relic', score=198144),
                                 Data(page='Okta,_Inc.', score=11086),
                                 Data(page='Palantir', score=261155),
                                 Data(page='Panic_Inc.', score=2873),
                                 Data(page='PARC_(company)', score=7701),
                                 Data(page='Perforce', score=3661),
                                 Data(page='Perplexity_AI', score=97651),
                                 Data(page='Plex', score=13895),
                                 Data(page='Pluralsight', score=2769),
                                 Data(page='PreSonus', score=1265),
                                 Data(page='Puppet_(software)', score=2603),
                                 Data(page='Qualtrics', score=26446),
                                 Data(page='Red_Hat', score=19180)],
          'programming_concepts': [Data(page='Bubble_sort', score=10849),
                                   Data(page='Quicksort', score=19132),
                                   Data(page='Insertion_sort', score=10564),
                                   Data(page='Merge_sort', score=13027),
                                   Data(page='Binary_search_algorithm', score=21),
                                   Data(page="Dijkstra's_algorithm", score=44238),
                                   Data(page='A*_search_algorithm', score=22588),
                                   Data(page='Big_O_notation', score=33095),
                                   Data(page='Time_complexity', score=14216),
                                   Data(page='Space_complexity', score=1555),
                                   Data(page='Dynamic_programming', score=14137),
                                   Data(page='Greedy_algorithm', score=7339),
                                   Data(page='Inheritance_(object-oriented_programming)', score=3359),
                                   Data(page='Polymorphism_(computer_science)', score=6274),
                                   Data(page='Encapsulation_(computer_programming)', score=4559),
                                   Data(page='Abstraction_(computer_science)', score=3507),
                                   Data(page='Class_(computer_programming)', score=4),
                                   Data(page='Object_(computer_science)', score=2070),
                                   Data(page='Method_(computer_programming)', score=1699),
                                   Data(page='Interface_(object-oriented_programming)', score=1416),
                                   Data(page='Constructor_(object-oriented_programming)', score=1215),
                                   Data(page='Destructor_(computer_science)', score=1),
                                   Data(page='Instance_variable', score=318),
                                   Data(page='Method_overriding', score=591),
                                   Data(page='Method_overloading', score=1),
                                   Data(page='Associative_array', score=3329),
                                   Data(page='Array_(data_structure)', score=5462),
                                   Data(page='Linked_list', score=5978),
                                   Data(page='Stack_(abstract_data_type)', score=11041),
                                   Data(page='Queue_(abstract_data_type)', score=3699),
                                   Data(page='Set_(abstract_data_type)', score=1413),
                                   Data(page='Binary_tree', score=8398),
                                   Data(page='B-tree', score=13586),
                                   Data(page='Hash_table', score=15222),
                                   Data(page='Graph_(abstract_data_type)', score=2970),
                                   Data(page='Heap_(data_structure)', score=11799),
                                   Data(page='Recursion_(computer_science)', score=4313),
                                   Data(page='Closure_(computer_programming)', score=6060),
                                   Data(page='Functional_programming', score=14131),
                                   Data(page='Object-oriented_programming', score=27227),
                                   Data(page='Asynchronous_I/O', score=1573),
                                   Data(page='Multithreading_(computer_architecture)', score=2961),
                                   Data(page='Concurrency_(computer_science)', score=3196),
                                   Data(page='Deadlock_(computer_science)', score=6677),
                                   Data(page='Garbage_collection_(computer_science)', score=8573),
                                   Data(page='Memory_leak', score=3283),
                                   Data(page='Application_programming_interface', score=66),
                                   Data(page='Regular_expression', score=43055),
                                   Data(page='Dependency_injection', score=11625),
                                   Data(page='Compiler', score=15697),
                                   Data(page='Interpreter_(computing)', score=6395),
                                   Data(page='Virtual_machine', score=11329)]}}

wiki = wikipediaapi.Wikipedia(
    user_agent="MeuJogoDeFutebol/1.0 (contato@email.com)", language="pt"
)

def get_neighbours(seed):
    num_links = 25
    page = wiki.page(seed)
    relevant_links = []
    for section in page.sections:
        print(section.title)
        # Verifica se o título da seção é um dos que queremos
        if section.title in target_sections:
            # Pega os links que aparecem no texto desta seção
            # (Usando a lógica de comparação de texto que vimos antes)
            section_links = [l for l in page.links if l in section.text]
            relevant_links.extend(section_links)
    all_links = relevant_links
    print(all_links)
    selected_links = random.sample(all_links, min(num_links, len(all_links)))
    selected_links = [a for a in selected_links if len(a.split()) < 4]
    result = []
    for link in selected_links:
        result.append(evaluate(link))
    result = list(zip(selected_links, result))
    pprint(result)
    top_two = sorted(result, key=lambda x: x[1], reverse=True)[:2]
    return top_two

import requests
import random
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass

@dataclass
class Item:
    name: str
    page: str
    score: int

@dataclass
class Data:
    page: str
    score: int

def get_first_caption(page_title: str, seed) -> str:
    if seed == "football":
        url = "https://pt.wikipedia.org/w/api.php"
    else:
        url ="https://en.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": page_title,
        "prop": "text",
        "format": "json",
        "redirects": 1  # Automatically follow redirects
    }
    headers = {
        "User-Agent": "trendmine/1.0 (your@email.com)"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            return ""

        data = response.json()
        if "error" in data:
            return ""

        html = data["parse"]["text"]["*"]
        soup = BeautifulSoup(html, "html.parser")

        # Look for caption in infoboxes or tables
        infobox = soup.find("table", class_="infobox")

        if infobox:
            # A. Tenta o <caption> primeiro (como você já fazia)
            caption = infobox.find("caption")
            if caption:
                return caption.get_text(strip=True)

            # B. Se não houver caption, busca o cabeçalho principal da Infobox
            # Geralmente é um <th> com a classe 'infobox-above' ou 'infobox-title'
            infobox_title = infobox.find(["th", "td"], class_=["infobox-above", "infobox-title"])
            if infobox_title:
                return infobox_title.get_text(strip=True)

            # C. Fallback: Pega o primeiro <th> da tabela se for largo (colspan)
            # Útil para páginas que não seguem o padrão estrito
            first_th = infobox.find("th")
            if first_th:
                return first_th.get_text(strip=True)
        # Fallback: if no caption, return the page title cleaned up
        caption = soup.find("caption")
        if caption:
            return caption.get_text(strip=True)
        return page_title.replace("_", " ")
    except Exception:
        return page_title.replace("_", " ")

def get_pageviews(wikipedia_name: str,seed, days: int = 30) -> int:
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)

    # Wikimedia API requires underscores instead of spaces
    slug = wikipedia_name.replace(" ", "_")

    if seed == "football":
        u= "pt"
    else:
        u="en"
    url = (
        f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"
        f"/{u}.wikipedia/all-access/all-agents"
        f"/{slug}"
        f"/daily"
        f"/{start.strftime('%Y%m%d')}00/{end.strftime('%Y%m%d')}00"
    )

    try:
        response = requests.get(url, headers={"User-Agent": "trendmine/1.0 (your@email.com)"})
        if response.status_code != 200:
            return 0

        data = response.json()
        return sum(item["views"] for item in data.get("items", []))
    except Exception:
        return 0

# Example target_sections structure for the function to work
# target_sections = {"football": {"teams": ["Sport_Club_do_Recife", "Clube_Náutico_Capibaribe"]}}
from wiki.db import get_view_count

import unicodedata

def remove_accents(input_str):
    if not input_str:
        return ""

    # 1. Normalize to "NFD" (Normalization Form Decomposition)
    # This turns 'é' into ('e' + 'combining acute accent')
    nfkd_form = unicodedata.normalize('NFD', input_str)

    # 2. Filter out the non-spacing mark characters (the accents)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])
def get_query(seed: str, keys ) -> Item:
    """
    Selects a random item from target_sections[seed],
    fetches its display name and pageview score.
    """
    if seed not in trivia_categories:
        raise ValueError(f"Seed '{seed}' not found in target sections.")

    # Get a random category/key from the seed
    random_key = random.choice(keys)

    # Get a random wikipedia slug from that category
    wikipedia_slug = random.choice(GAME_DATA[seed][random_key])
    score = wikipedia_slug.score
    name = wikipedia_slug.page.replace("_", " ")
 #   name = get_first_caption(wikipedia_slug, seed)
 #   score = get_pageviews(wikipedia_slug, seed)
    item = Item(
        name=name,
        page=wikipedia_slug.page,
        score=score
    )

    return item
def save_to_json(section: str,
    teams: Dict[str, List[str]], output_path: Path = Path("data/teams.json")
):
    array:List[DataItem]= []
    for team in teams[section]:
        team = team.replace(' ', '_')
        name = get_first_caption(team)
        if name == "":
            print("error at ",team)
            continue
        score = get_pageviews(team)
        data = DataItem(name=name, page=team, score=score)  # ← fixed constructor
        array.append(data)  # ← was append() with no arg

    # ← new_dict.json_dump doesn't exist; convert dataclasses to dicts first
    serializable =  [ asdict(team) for team in array]

    write_to_file(section, serializable, output_path)

def write_to_file(name, data, output_path: Path = Path("data/teams copy.json")):
    existing = {}
    if output_path.exists():
        with open(output_path, "r", encoding="utf-8") as f:
            existing = json.load(f)
    existing[name] = data
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved to '{output_path}'")


def evaluate(query: str) -> float:
    messages = [
        {
            "role": "system",
            "content": "Your job is to classify if a given input is related to Soccer. Answer ONLY with a value between 0 to 1. Provide exactly one score per line. Do not add any extra text, letters, or explanation.",
        },
        {"role": "user", "content": query},
    ]
    response = ollama.chat(
        # model="hf.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF:Q3_K_M",
        model="qwen2.5:1.5b",
        messages=messages,
        options={
            "num_ctx": 128,  # SHRINK THE SCRATCHPAD: Only reserve RAM for 512 tokens
            "temperature": 0.1,  # Make it strictly logical, no creative rambling
        },
    )
    print(response)
    response_text = response["message"]["content"]
    print(response_text)
    try:
        return float(response_text)
    except ValueError:
        return 0.0

    scores = []
    response_lines = response_text.strip().split("\n")
    for line in response_lines:
        try:
            scores.append(float(line.strip()))
        except ValueError:
            scores.append(0.01)

    while len(scores) < len(queries):
        scores.append(0.02)
    return scores[: len(queries)]


    # neighbours = get_neighbours(TEAMS[0])
    # pprint(neighbours)


def complex_refinery(raw_title):
    """
    A complex refinery that uses Regex to transform raw Wikipedia
    titles into clean, searchable Google Trends terms.
    """
    # 1. Remove disambiguation parentheses: "Neymar (futebolista)" -> "Neymar"
    # It handles nested or multiple parentheses
    clean = re.sub(r"\s*\([^)]*\)", "", raw_title)

    # 2. Remove "Category:" or "Categoria:" prefixes
    clean = re.sub(r"^(Category|Categoria):", "", clean, flags=re.IGNORECASE)

    # 3. Strip leading/trailing whitespace and underscores
    clean = clean.replace("_", " ").strip()

    # 4. Complexity Check: If the title is too long (likely a description, not an entity),
    # we truncate it to the first 4 words to keep it "searchable."
    words = clean.split()
    if len(words) > 4:
        clean = " ".join(words[:4])

    return clean


def stochastic_data_miner():
    """
    Random Walk Algorithm:
    1. Jump to a random page.
    2. Extract its categories to find a 'Theme'.
    3. Pick a neighbor from that theme for a fair battle.
    """
    try:
        # Step 1: Stochastic Jump
        random_page_title = wikipedia.random(pages=1)
        page = wikipedia.page(random_page_title, auto_suggest=False)

        # Step 2: Extract Categories (Filtering out 'Hidden' or 'Maintenance' categories)
        # We look for categories that don't contain "Artigos" or "!Esboços"
        valid_themes = [
            c for c in page.categories if "Artigos" not in c and "!" not in c
        ]

        if not valid_themes:
            return stochastic_data_miner()  # Retry if no good theme found

        chosen_theme = random.choice(valid_themes)
        clean_theme = complex_refinery(chosen_theme)

        # Step 3: Get 'Neighbors' from the Category
        cat_page = wikipedia.page(chosen_theme, auto_suggest=False)
        neighbors = cat_page.links

        if len(neighbors) < 2:
            return stochastic_data_miner()

        # Step 4: Refine the Final Entities
        competitors = random.sample(neighbors, 2)
        entity_a = complex_refinery(competitors[0])
        entity_b = complex_refinery(competitors[1])

        return {
            "theme": clean_theme,
            "competitor_a": entity_a,
            "competitor_b": entity_b,
            "seed_origin": random_page_title,
        }

    except Exception:
        # Catching DisambiguationError or PageError and recursing
        return stochastic_data_miner()

def flatten(path: Path) -> Path:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    flattened = [item for section in data.values() for item in section]

    # dedup by "page", keeping first occurrence
    seen = set()
    deduped = []
    for item in flattened:
        if item["page"] not in seen:
            seen.add(item["page"])
            deduped.append(item)

    output_path = path.with_stem(path.stem + "_flattened")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(deduped, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved to '{output_path}' ({len(flattened) - len(deduped)} duplicates removed)")
    return output_path


from wiki.db import connect
def get_bulk_scores(titles_set):
    """
    Fetches all view counts in a single query to save the HDD.
    """
    scores_map = {}
    if not titles_set:
        return scores_map

    # Ensure titles are formatted with underscores for the DB
    formatted_titles = list(titles_set)
    placeholders = ', '.join(['%s'] * len(formatted_titles))

    query = f"""
    SELECT p.page_title, COALESCE(v.view_count, 0)
    FROM page p
    LEFT JOIN page_views v ON p.page_id = v.page_id
    WHERE p.page_title IN ({placeholders})
      AND p.page_namespace = 0;
    """

    try:
        # Use utf8mb4 to handle those Brazilian team accents correctly!
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(query, formatted_titles)

        for (title, count) in cursor.fetchall():
            # Convert back to string since DB returns VARBINARY/bytes
            scores_map[title.decode('utf-8') if isinstance(title, bytes) else title] = count

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'conn' in locals(): conn.close()

    return scores_map

def transform_to_data_struct(nested_dict ):
    # 1. Flatten all titles into a unique set to avoid double lookups
    all_titles = set()
    for cat in nested_dict.values():
        for subcat_titles in cat.values():
            all_titles.update(subcat_titles)

    # 2. Get all scores in one single HDD "sweep"
    print(f"Fetching scores for {len(all_titles)} titles...")
    scores_lookup = get_bulk_scores(all_titles)

    # 3. Build the new structure
    final_struct = {}
    for cat_name, subcategories in nested_dict.items():
        final_struct[cat_name] = {}
        for sub_name, titles in subcategories.items():
            final_struct[cat_name][sub_name] = [
                Data(page=t, score=scores_lookup.get(t, 0))
                for t in titles
            ]
    return final_struct

def transform_to_nested_data(nested_dict: dict[str, dict[str, list[str]]]) -> dict[str, dict[str, list[Data]]]:
    # 1. Flatten all titles for a single HDD seek
    all_titles = set()
    for  title, sub_content in nested_dict.items():
        # Check if the content is a dict (nested) or a list (flat)
        if isinstance(sub_content, dict):
            for titles in sub_content.values():
                all_titles.update(titles)

    # 2. Bulk Database Lookup (No changes here, this part is solid)
    print(f"Searching for {len(all_titles)} titles on HDD...")
    scores_lookup = {}
    placeholders = ', '.join(['%s'] * len(all_titles))
    query = f"""
    SELECT p.page_title, COALESCE(v.view_count, 0)
    FROM page p
    LEFT JOIN page_views v ON p.page_id = v.page_id
    WHERE p.page_title IN ({placeholders}) AND p.page_namespace = 0
    """

    try:
        conn = connect() # Assuming your connect() function works
        cursor = conn.cursor()
        cursor.execute(query, list(all_titles))
        for (title, count) in cursor.fetchall():
            if count == 0:
                continue
            # You can keep the 'continue if 0' logic,
            # but usually it's better to keep the 0s so your struct stays full
            t_str = title.decode('utf-8') if isinstance(title, bytes) else title
            scores_lookup[t_str] = count
    except Exception as e:
        print(f"DB Error: {e}")
    finally:
        if 'conn' in locals(): conn.close()

    # 3. Rebuild the structure safely
    final_output = {}
    for category, sub_content in nested_dict.items():
        if isinstance(sub_content, dict):
            final_output[category] = {}
            for description, titles in sub_content.items():
                final_output[category][description] = []
                for t in titles:
                    score = scores_lookup.get(t, 0)
                    if score!=0:
                        final_output[category][description].append(Data(t, score))
        else:
            # This handles the case where it's NOT a dict of dicts
            final_output[category] = [
                Data(page=t, score=scores_lookup.get(t, 0))
                for t in sub_content
            ]
    return final_output

def find_the_culprit(data, path=""):
    if isinstance(data, dict):
        for k, v in data.items():
            find_the_culprit(v, f"{path} -> {k}")
    elif isinstance(data, list):
        for i, v in enumerate(data):
            if isinstance(v, dict):
                print(f"Found a dict at: {path} -> index {i}")
            else:
                find_the_culprit(v, f"{path} -> index {i}")

find_the_culprit(trivia_categories)
if __name__ == "__main__":
    processed_games = transform_to_nested_data(trivia_categories)
  #  processed_games = transform_to_nested_data(trivia_categories)
    print("GAME_DATA = ", end="")
    pprint(processed_games, width=120, sort_dicts=False)
   # from users import TEAMS
   # item= get_query()
   # pprint(item)
    # write_to_file("bob", [asdict(DataItem(name="bob", page="booob", score=2))])
    # save_to_json("Brasileirão - Série B",teams)
    # flatten(Path("data/teams.json"))
