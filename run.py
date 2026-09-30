# ============================================================
# 🌍 UNREAL PLACES ENGINE — FULL AUTOMATION ENGINE
# AUTO-MUSIC FINDER + GLASS OVERLAY TYPOGRAPHY + ULTRA 4K
# ============================================================

import os
import glob
import random
import requests
import subprocess

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
VIDEOS_DIR = "videos"
OUTPUT_DIR = "output"
MUSIC_DIR = "music"

os.makedirs(VIDEOS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)


# ============================================================
# 🌎 REAL WORLD LOCATIONS & FANTASY WORLDS POOL
# ============================================================

UNREAL_PLACES_POOL = [
    # 🇨🇭 SWITZERLAND
    {"country": "SWITZERLAND", "flag": "🇨🇭", "query": "Lauterbrunnen Valley waterfalls Switzerland 4k cinematic"},
    {"country": "SWITZERLAND", "flag": "🇨🇭", "query": "Grindelwald Switzerland Alps drone 4k"},
    {"country": "SWITZERLAND", "flag": "🇨🇭", "query": "Oeschinen Lake Switzerland turquoise 4k"},
    {"country": "SWITZERLAND", "flag": "🇨🇭", "query": "Blausee Switzerland crystal lake 4k"},
    {"country": "SWITZERLAND", "flag": "🇨🇭", "query": "Lake Lucerne Swiss Alps 4k"},
    {"country": "SWITZERLAND", "flag": "🇨🇭", "query": "Matterhorn Zermatt sunrise 4k"},
    {"country": "SWITZERLAND", "flag": "🇨🇭", "query": "Aletsch Glacier Switzerland aerial 4k"},
    {"country": "SWITZERLAND", "flag": "🇨🇭", "query": "Jungfrau Switzerland clouds 4k"},
    {"country": "SWITZERLAND", "flag": "🇨🇭", "query": "Engelberg Switzerland mountain valley 4k"},
    {"country": "SWITZERLAND", "flag": "🇨🇭", "query": "Lago di Saoseo Switzerland hidden lake 4k"},
    {"country": "SWITZERLAND", "flag": "🇨🇭", "query": "Val Verzasca Switzerland emerald river 4k"},
    {"country": "SWITZERLAND", "flag": "🇨🇭", "query": "Saxon Switzerland mountain landscape 4k"},

    # 🇳🇴 NORWAY
    {"country": "NORWAY", "flag": "🇳🇴", "query": "Lofoten Islands Reine Norway drone 4k"},
    {"country": "NORWAY", "flag": "🇳🇴", "query": "Geirangerfjord Norway waterfalls 4k"},
    {"country": "NORWAY", "flag": "🇳🇴", "query": "Trolltunga Norway sunrise 4k"},
    {"country": "NORWAY", "flag": "🇳🇴", "query": "Preikestolen Norway fjord 4k"},
    {"country": "NORWAY", "flag": "🇳🇴", "query": "Kjerag Norway mountains 4k"},
    {"country": "NORWAY", "flag": "🇳🇴", "query": "Senja Norway dramatic coastline 4k"},
    {"country": "NORWAY", "flag": "🇳🇴", "query": "Loen Norway mountains clouds 4k"},
    {"country": "NORWAY", "flag": "🇳🇴", "query": "Flam Norway fjord valley 4k"},
    {"country": "NORWAY", "flag": "🇳🇴", "query": "Vesteralen Norway islands 4k"},
    {"country": "NORWAY", "flag": "🇳🇴", "query": "Northern Norway northern lights mountains 4k"},
    {"country": "NORWAY", "flag": "🇳🇴", "query": "Hardangerfjord Norway spring waterfalls 4k"},
    {"country": "NORWAY", "flag": "🇳🇴", "query": "Jotunheimen National Park Norway 4k"},

    # 🇮🇸 ICELAND
    {"country": "ICELAND", "flag": "🇮🇸", "query": "Reynisfjara black sand beach Iceland 4k"},
    {"country": "ICELAND", "flag": "🇮🇸", "query": "Skogafoss Iceland waterfall 4k"},
    {"country": "ICELAND", "flag": "🇮🇸", "query": "Seljalandsfoss Iceland waterfall 4k"},
    {"country": "ICELAND", "flag": "🇮🇸", "query": "Kirkjufell Iceland northern lights 4k"},
    {"country": "ICELAND", "flag": "🇮🇸", "query": "Jokulsarlon glacier lagoon 4k"},
    {"country": "ICELAND", "flag": "ICELAND diamond beach ice chunks 4k"},
    {"country": "ICELAND", "flag": "🇮🇸", "query": "Iceland Highlands volcanic landscape 4k"},
    {"country": "ICELAND", "flag": "🇮🇸", "query": "Iceland blue lagoon aerial 4k"},
    {"country": "ICELAND", "flag": "🇮🇸", "query": "Svartifoss Iceland basalt waterfall 4k"},
    {"country": "ICELAND", "flag": "🇮🇸", "query": "Fjaðrárgljúfur canyon Iceland 4k"},
    {"country": "ICELAND", "flag": "🇮🇸", "query": "Vestrahorn Iceland mountain beach 4k"},
    {"country": "ICELAND", "flag": "🇮🇸", "query": "Landmannalaugar Iceland colorful mountains 4k"},

    # 🇯🇵 JAPAN
    {"country": "JAPAN", "flag": "🇯🇵", "query": "Arashiyama bamboo forest Kyoto 4k"},
    {"country": "JAPAN", "flag": "🇯🇵", "query": "Mount Fuji cherry blossoms 4k"},
    {"country": "JAPAN", "flag": "🇯🇵", "query": "Kawaguchiko Mount Fuji sunrise 4k"},
    {"country": "JAPAN", "flag": "🇯🇵", "query": "Shirakawa Go village snow 4k"},
    {"country": "JAPAN", "flag": "🇯🇵", "query": "Nachi waterfall Japan 4k"},
    {"country": "JAPAN", "flag": "🇯🇵", "query": "Yakushima ancient forest 4k"},
    {"country": "JAPAN", "flag": "🇯🇵", "query": "Hokkaido lavender fields 4k"},
    {"country": "JAPAN", "flag": "🇯🇵", "query": "Japanese autumn forest mountain 4k"},
    {"country": "JAPAN", "flag": "🇯🇵", "query": "Kamikochi Japan mountain valley 4k"},
    {"country": "JAPAN", "flag": "🇯🇵", "query": "Oirase stream forest Japan 4k"},
    {"country": "JAPAN", "flag": "🇯🇵", "query": "Hitachi seaside park flowers 4k"},
    {"country": "JAPAN", "flag": "🇯🇵", "query": "Nakasendo Japan mountain village 4k"},

    # 🇨🇳 CHINA
    {"country": "CHINA", "flag": "🇨🇳", "query": "Zhangjiajie Avatar mountains drone 4k"},
    {"country": "CHINA", "flag": "🇨🇳", "query": "Huangshan Yellow Mountain sea clouds 4k"},
    {"country": "CHINA", "flag": "🇨🇳", "query": "Jiuzhaigou Valley turquoise lakes 4k"},
    {"country": "CHINA", "flag": "🇨🇳", "query": "Guilin Li River karst mountains 4k"},
    {"country": "CHINA", "flag": "🇨🇳", "query": "Zhangye Rainbow Mountains China 4k"},
    {"country": "CHINA", "flag": "🇨🇳", "query": "Tianzi Mountain China clouds 4k"},
    {"country": "CHINA", "flag": "🇨🇳", "query": "Fanjingshan China clouds 4k"},
    {"country": "CHINA", "flag": "🇨🇳", "query": "Yunnan rice terraces China 4k"},
    {"country": "CHINA", "flag": "🇨🇳", "query": "Tibet Himalayas lake mountains 4k"},
    {"country": "CHINA", "flag": "🇨🇳", "query": "Huanglong colorful pools China 4k"},
    {"country": "CHINA", "flag": "🇨🇳", "query": "Three Gorges China aerial 4k"},
    {"country": "CHINA", "flag": "🇨🇳", "query": "Wulingyuan China mist mountains 4k"},

    # 🇫🇴 FAROE ISLANDS
    {"country": "FAROE ISLANDS", "flag": "🇫🇴", "query": "Gasadalur waterfall Faroe Islands 4k"},
    {"country": "FAROE ISLANDS", "flag": "🇫🇴", "query": "Drangarnir Faroe Islands cliffs 4k"},
    {"country": "FAROE ISLANDS", "flag": "🇫🇴", "query": "Saksun Faroe Islands village 4k"},
    {"country": "FAROE ISLANDS", "flag": "🇫🇴", "query": "Mykines Faroe Islands cliffs 4k"},
    {"country": "FAROE ISLANDS", "flag": "🇫🇴", "query": "Kalsoy Faroe Islands mountains 4k"},
    {"country": "FAROE ISLANDS", "flag": "🇫🇴", "query": "Faroe Islands ocean cliffs fog 4k"},

    # 🇮🇹 ITALY
    {"country": "ITALY", "flag": "🇮🇹", "query": "Dolomites Seceda ridge sunrise 4k"},
    {"country": "ITALY", "flag": "🇮🇹", "query": "Tre Cime di Lavaredo 4k"},
    {"country": "ITALY", "flag": "🇮🇹", "query": "Lake Braies Dolomites 4k"},
    {"country": "ITALY", "flag": "🇮🇹", "query": "Lake Como mountains drone 4k"},
    {"country": "ITALY", "flag": "🇮🇹", "query": "Amalfi Coast drone 4k"},
    {"country": "ITALY", "flag": "🇮🇹", "query": "Cinque Terre coastline 4k"},
    {"country": "ITALY", "flag": "🇮🇹", "query": "Tuscany hills sunrise 4k"},
    {"country": "ITALY", "flag": "🇮🇹", "query": "Sardinia turquoise coastline 4k"},
    {"country": "ITALY", "flag": "🇮🇹", "query": "Lake Garda Italy mountains 4k"},
    {"country": "ITALY", "flag": "🇮🇹", "query": "Gran Paradiso Italy mountains 4k"},

    # 🇮🇩 INDONESIA
    {"country": "INDONESIA", "flag": "🇮🇩", "query": "Bali Tegalalang rice terraces 4k"},
    {"country": "INDONESIA", "flag": "🇮🇩", "query": "Mount Bromo sunrise 4k"},
    {"country": "INDONESIA", "flag": "🇮🇩", "query": "Kelingking Beach Nusa Penida 4k"},
    {"country": "INDONESIA", "flag": "🇮🇩", "query": "Raja Ampat islands drone 4k"},
    {"country": "INDONESIA", "flag": "🇮🇩", "query": "Komodo National Park aerial 4k"},
    {"country": "INDONESIA", "flag": "🇮🇩", "query": "Ijen crater blue fire 4k"},
    {"country": "INDONESIA", "flag": "🇮🇩", "query": "Sekumpul waterfall Bali 4k"},
    {"country": "INDONESIA", "flag": "🇮🇩", "query": "Munduk Bali jungle waterfall 4k"},
    {"country": "INDONESIA", "flag": "🇮🇩", "query": "Mount Rinjani Lombok 4k"},
    {"country": "INDONESIA", "flag": "🇮🇩", "query": "Flores Kelimutu lakes 4k"},
    {"country": "INDONESIA", "flag": "🇮🇩", "query": "Nusa Penida hidden beach 4k"},

    # 🇳🇿 NEW ZEALAND
    {"country": "NEW ZEALAND", "flag": "🇳🇿", "query": "Milford Sound New Zealand 4k"},
    {"country": "NEW ZEALAND", "flag": "🇳🇿", "query": "Mount Cook New Zealand 4k"},
    {"country": "NEW ZEALAND", "flag": "🇳🇿", "query": "Lake Tekapo New Zealand 4k"},
    {"country": "NEW ZEALAND", "flag": "🇳🇿", "query": "Lake Pukaki Mount Cook 4k"},
    {"country": "NEW ZEALAND", "flag": "🇳🇿", "query": "Roy's Peak Wanaka 4k"},
    {"country": "NEW ZEALAND", "flag": "🇳🇿", "query": "Franz Josef Glacier 4k"},
    {"country": "NEW ZEALAND", "flag": "🇳🇿", "query": "Fiordland National Park 4k"},
    {"country": "NEW ZEALAND", "flag": "🇳🇿", "query": "Abel Tasman turquoise coast 4k"},
    {"country": "NEW ZEALAND", "flag": "🇳🇿", "query": "Milford Sound waterfalls mist 4k"},
    {"country": "NEW ZEALAND", "flag": "🇳🇿", "query": "Aoraki Mount Cook sunrise 4k"},

    # 🇻🇳 VIETNAM
    {"country": "VIETNAM", "flag": "🇻🇳", "query": "Ha Long Bay Vietnam 4k"},
    {"country": "VIETNAM", "flag": "🇻🇳", "query": "Ninh Binh Trang An 4k"},
    {"country": "VIETNAM", "flag": "🇻🇳", "query": "Ban Gioc waterfall Vietnam 4k"},
    {"country": "VIETNAM", "flag": "🇻🇳", "query": "Sapa rice terraces 4k"},
    {"country": "VIETNAM", "flag": "🇻🇳", "query": "Phong Nha cave Vietnam 4k"},
    {"country": "VIETNAM", "flag": "🇻🇳", "query": "Da Lat Vietnam waterfalls 4k"},
    {"country": "VIETNAM", "flag": "🇻🇳", "query": "Cat Ba island Vietnam 4k"},
    {"country": "VIETNAM", "flag": "🇻🇳", "query": "Ha Giang mountain road Vietnam 4k"},

    # 🇵🇹 PORTUGAL
    {"country": "PORTUGAL", "flag": "🇵🇹", "query": "Madeira island cliffs ocean 4k"},
    {"country": "PORTUGAL", "flag": "🇵🇹", "query": "Madeira levada misty forest 4k"},
    {"country": "PORTUGAL", "flag": "🇵🇹", "query": "Pico do Arieiro Madeira clouds 4k"},
    {"country": "PORTUGAL", "flag": "🇵🇹", "query": "Azores Sete Cidades lake 4k"},
    {"country": "PORTUGAL", "flag": "🇵🇹", "query": "Azores volcanic landscape 4k"},
    {"country": "PORTUGAL", "flag": "🇵🇹", "query": "Benagil cave Portugal 4k"},
    {"country": "PORTUGAL", "flag": "🇵🇹", "query": "Madeira hidden waterfall 4k"},

    # 🇺🇸 USA
    {"country": "USA", "flag": "🇺🇸", "query": "Antelope Canyon sunbeam 4k"},
    {"country": "USA", "flag": "🇺🇸", "query": "Grand Canyon sunrise 4k"},
    {"country": "USA", "flag": "🇺🇸", "query": "Yosemite Valley waterfall 4k"},
    {"country": "USA", "flag": "🇺🇸", "query": "Zion National Park cliffs 4k"},
    {"country": "USA", "flag": "🇺🇸", "query": "Bryce Canyon hoodoos 4k"},
    {"country": "USA", "flag": "🇺🇸", "query": "Horseshoe Bend Arizona 4k"},
    {"country": "USA", "flag": "🇺🇸", "query": "Yellowstone Grand Prismatic Spring 4k"},
    {"country": "USA", "flag": "🇺🇸", "query": "Glacier National Park Montana 4k"},
    {"country": "USA", "flag": "🇺🇸", "query": "Hawaii Na Pali Coast 4k"},
    {"country": "USA", "flag": "🇺🇸", "query": "Hawaii black sand beach 4k"},
    {"country": "USA", "flag": "🇺🇸", "query": "Alaska glacier mountains 4k"},
    {"country": "USA", "flag": "🇺🇸", "query": "Grand Teton National Park 4k"},
    {"country": "USA", "flag": "🇺🇸", "query": "Olympic rainforest Washington 4k"},
    {"country": "USA", "flag": "🇺🇸", "query": "Nā Pali Coast Kauai drone 4k"},
    {"country": "USA", "flag": "🇺🇸", "query": "Bryce Canyon Milky Way 4k"},
    {"country": "USA", "flag": "🇺🇸", "query": "Death Valley moving dunes 4k"},

    # 🇨🇦 CANADA
    {"country": "CANADA", "flag": "🇨🇦", "query": "Lake Louise Banff 4k"},
    {"country": "CANADA", "flag": "🇨🇦", "query": "Moraine Lake Canada 4k"},
    {"country": "CANADA", "flag": "🇨🇦", "query": "Jasper National Park 4k"},
    {"country": "CANADA", "flag": "🇨🇦", "query": "Canadian Rockies turquoise lake 4k"},
    {"country": "CANADA", "flag": "🇨🇦", "query": "Yoho National Park waterfall 4k"},
    {"country": "CANADA", "flag": "🇨🇦", "query": "Vancouver Island rainforest 4k"},
    {"country": "CANADA", "flag": "🇨🇦", "query": "Athabasca Glacier 4k"},
    {"country": "CANADA", "flag": "🇨🇦", "query": "Emerald Lake Canada 4k"},
    {"country": "CANADA", "flag": "🇨🇦", "query": "Spirit Island Jasper Canada 4k"},

    # 🇫🇷 FRANCE
    {"country": "FRANCE", "flag": "🇫🇷", "query": "Chamonix Mont Blanc 4k"},
    {"country": "FRANCE", "flag": "🇫🇷", "query": "Annecy Lake Alps 4k"},
    {"country": "FRANCE", "flag": "🇫🇷", "query": "Verdon Gorge France 4k"},
    {"country": "FRANCE", "flag": "🇫🇷", "query": "Corsica turquoise coast 4k"},
    {"country": "FRANCE", "flag": "🇫🇷", "query": "Calanques Marseille France 4k"},
    {"country": "FRANCE", "flag": "🇫🇷", "query": "Pyrenees mountain valley 4k"},

    # 🇪🇸 SPAIN
    {"country": "SPAIN", "flag": "🇪🇸", "query": "Mallorca dramatic coast 4k"},
    {"country": "SPAIN", "flag": "🇪🇸", "query": "Tenerife Mount Teide 4k"},
    {"country": "SPAIN", "flag": "🇪🇸", "query": "Picos de Europa Spain 4k"},
    {"country": "SPAIN", "flag": "🇪🇸", "query": "Gran Canaria mountains 4k"},
    {"country": "SPAIN", "flag": "🇪🇸", "query": "Gaztelugatxe Basque coast 4k"},
    {"country": "SPAIN", "flag": "🇪🇸", "query": "Andalusia white villages mountains 4k"},

    # 🇬🇷 GREECE
    {"country": "GREECE", "flag": "🇬🇷", "query": "Santorini caldera sunset 4k"},
    {"country": "GREECE", "flag": "🇬🇷", "query": "Milos Greece turquoise beaches 4k"},
    {"country": "GREECE", "flag": "🇬🇷", "query": "Zakynthos Navagio beach 4k"},
    {"country": "GREECE", "flag": "🇬🇷", "query": "Meteora Greece mountains 4k"},
    {"country": "GREECE", "flag": "🇬🇷", "query": "Balos Lagoon Crete 4k"},
    {"country": "GREECE", "flag": "🇬🇷", "query": "Melissani Cave Greece 4k"},

    # 🇸🇮 SLOVENIA
    {"country": "SLOVENIA", "flag": "🇸🇮", "query": "Lake Bled Slovenia 4k"},
    {"country": "SLOVENIA", "flag": "🇸🇮", "query": "Lake Bohinj Slovenia 4k"},
    {"country": "SLOVENIA", "flag": "🇸🇮", "query": "Soca Valley Slovenia 4k"},
    {"country": "SLOVENIA", "flag": "🇸🇮", "query": "Vintgar Gorge Slovenia 4k"},
    {"country": "SLOVENIA", "flag": "🇸🇮", "query": "Triglav National Park 4k"},

    # 🇲🇪 MONTENEGRO
    {"country": "MONTENEGRO", "flag": "🇲🇪", "query": "Bay of Kotor Montenegro 4k"},
    {"country": "MONTENEGRO", "flag": "🇲🇪", "query": "Durmitor National Park 4k"},
    {"country": "MONTENEGRO", "flag": "🇲🇪", "query": "Tara Canyon Montenegro 4k"},
    {"country": "MONTENEGRO", "flag": "🇲🇪", "query": "Sveti Stefan Montenegro aerial 4k"},

    # 🇹🇷 TURKEY
    {"country": "TURKEY", "flag": "🇹🇷", "query": "Cappadocia balloons sunrise 4k"},
    {"country": "TURKEY", "flag": "🇹🇷", "query": "Pamukkale Turkey aerial 4k"},
    {"country": "TURKEY", "flag": "🇹🇷", "query": "Oludeniz turquoise lagoon 4k"},
    {"country": "TURKEY", "flag": "🇹🇷", "query": "Mount Ararat Turkey 4k"},
    {"country": "TURKEY", "flag": "🇹🇷", "query": "Butterfly Valley Turkey 4k"},
    {"country": "TURKEY", "flag": "🇹🇷", "query": "Saklikent Canyon Turkey 4k"},

    # 🇬🇪 GEORGIA
    {"country": "GEORGIA", "flag": "🇬🇪", "query": "Kazbegi Georgia mountains 4k"},
    {"country": "GEORGIA", "flag": "🇬🇪", "query": "Gergeti Trinity Church mountains 4k"},
    {"country": "GEORGIA", "flag": "🇬🇪", "query": "Svaneti Georgia mountain villages 4k"},
    {"country": "GEORGIA", "flag": "🇬🇪", "query": "Martvili Canyon Georgia 4k"},
    {"country": "GEORGIA", "flag": "🇬🇪", "query": "Prometheus Cave Georgia 4k"},

    # 🇳🇵 NEPAL
    {"country": "NEPAL", "flag": "🇳🇵", "query": "Everest Himalayas sunrise 4k"},
    {"country": "NEPAL", "flag": "🇳🇵", "query": "Annapurna mountain range 4k"},
    {"country": "NEPAL", "flag": "🇳🇵", "query": "Gokyo Lakes Nepal 4k"},
    {"country": "NEPAL", "flag": "🇳🇵", "query": "Himalayan mountain valley clouds 4k"},
    {"country": "NEPAL", "flag": "🇳🇵", "query": "Langtang Valley Nepal 4k"},

    # 🇮🇳 INDIA
    {"country": "INDIA", "flag": "🇮🇳", "query": "Ladakh Himalayas India 4k"},
    {"country": "INDIA", "flag": "🇮🇳", "query": "Valley of Flowers India 4k"},
    {"country": "INDIA", "flag": "🇮🇳", "query": "Meghalaya waterfalls India 4k"},
    {"country": "INDIA", "flag": "🇮🇳", "query": "Kerala backwaters aerial 4k"},
    {"country": "INDIA", "flag": "🇮🇳", "query": "Spiti Valley India 4k"},
    {"country": "INDIA", "flag": "🇮🇳", "query": "Zanskar Valley India 4k"},
    {"country": "INDIA", "flag": "🇮🇳", "query": "Munnar tea plantations 4k"},

    # 🇵🇭 PHILIPPINES
    {"country": "PHILIPPINES", "flag": "🇵🇭", "query": "Palawan turquoise lagoons 4k"},
    {"country": "PHILIPPINES", "flag": "🇵🇭", "query": "El Nido Philippines drone 4k"},
    {"country": "PHILIPPINES", "flag": "🇵🇭", "query": "Coron Palawan lakes 4k"},
    {"country": "PHILIPPINES", "flag": "🇵🇭", "query": "Bohol Chocolate Hills 4k"},
    {"country": "PHILIPPINES", "flag": "🇵🇭", "query": "Siargao island Philippines 4k"},
    {"country": "PHILIPPINES", "flag": "🇵🇭", "query": "Siquijor waterfalls Philippines 4k"},

    # 🇹🇭 THAILAND
    {"country": "THAILAND", "flag": "🇹🇭", "query": "Phi Phi Islands Thailand 4k"},
    {"country": "THAILAND", "flag": "🇹🇭", "query": "Krabi limestone cliffs 4k"},
    {"country": "THAILAND", "flag": "🇹🇭", "query": "Phang Nga Bay Thailand 4k"},
    {"country": "THAILAND", "flag": "🇹🇭", "query": "Koh Lipe Thailand turquoise 4k"},
    {"country": "THAILAND", "flag": "🇹🇭", "query": "Erawan Waterfalls Thailand 4k"},

    # 🇦🇺 AUSTRALIA
    {"country": "AUSTRALIA", "flag": "🇦🇺", "query": "Great Barrier Reef aerial 4k"},
    {"country": "AUSTRALIA", "flag": "🇦🇺", "query": "Whitehaven Beach drone 4k"},
    {"country": "AUSTRALIA", "flag": "🇦🇺", "query": "Twelve Apostles Australia 4k"},
    {"country": "AUSTRALIA", "flag": "🇦🇺", "query": "Blue Mountains Australia 4k"},
    {"country": "AUSTRALIA", "flag": "🇦🇺", "query": "Tasmania wilderness 4k"},
    {"country": "AUSTRALIA", "flag": "🇦🇺", "query": "Uluru sunrise 4k"},
    {"country": "AUSTRALIA", "flag": "🇦🇺", "query": "Daintree rainforest 4k"},
    {"country": "AUSTRALIA", "flag": "🇦🇺", "query": "Wineglass Bay Tasmania 4k"},

    # 🇿🇦 SOUTH AFRICA
    {"country": "SOUTH AFRICA", "flag": "🇿🇦", "query": "Table Mountain Cape Town 4k"},
    {"country": "SOUTH AFRICA", "flag": "🇿🇦", "query": "Drakensberg mountains 4k"},
    {"country": "SOUTH AFRICA", "flag": "🇿🇦", "query": "Blyde River Canyon 4k"},
    {"country": "SOUTH AFRICA", "flag": "🇿🇦", "query": "Garden Route South Africa 4k"},
    {"country": "SOUTH AFRICA", "flag": "🇿🇦", "query": "Wild Coast South Africa 4k"},

    # 🇳🇦 NAMIBIA
    {"country": "NAMIBIA", "flag": "🇳🇦", "query": "Sossusvlei red dunes 4k"},
    {"country": "NAMIBIA", "flag": "🇳🇦", "query": "Deadvlei Namibia 4k"},
    {"country": "NAMIBIA", "flag": "🇳🇦", "query": "Namib desert aerial 4k"},
    {"country": "NAMIBIA", "flag": "🇳🇦", "query": "Skeleton Coast Namibia 4k"},
    {"country": "NAMIBIA", "flag": "🇳🇦", "query": "Spitzkoppe Namibia 4k"},

    # 🇲🇦 MOROCCO
    {"country": "MOROCCO", "flag": "🇲🇦", "query": "Sahara desert Morocco dunes 4k"},
    {"country": "MOROCCO", "flag": "🇲🇦", "query": "Atlas Mountains Morocco 4k"},
    {"country": "MOROCCO", "flag": "🇲🇦", "query": "Ait Ben Haddou desert landscape 4k"},
    {"country": "MOROCCO", "flag": "🇲🇦", "query": "Dades Gorge Morocco 4k"},
    {"country": "MOROCCO", "flag": "🇲🇦", "query": "Todra Gorge Morocco 4k"},
    {"country": "MOROCCO", "flag": "🇲🇦", "query": "Chefchaouen mountains Morocco 4k"},

    # 🇯🇴 JORDAN
    {"country": "JORDAN", "flag": "🇯🇴", "query": "Wadi Rum Jordan desert 4k"},
    {"country": "JORDAN", "flag": "🇯🇴", "query": "Wadi Rum red canyon 4k"},
    {"country": "JORDAN", "flag": "🇯🇴", "query": "Dead Sea Jordan aerial 4k"},
    {"country": "JORDAN", "flag": "🇯🇴", "query": "Dana Biosphere Jordan 4k"},

    # 🇲🇽 MEXICO
    {"country": "MEXICO", "flag": "🇲🇽", "query": "Sumidero Canyon Mexico 4k"},
    {"country": "MEXICO", "flag": "🇲🇽", "query": "Cenote Mexico turquoise cave 4k"},
    {"country": "MEXICO", "flag": "🇲🇽", "query": "Copper Canyon Mexico 4k"},
    {"country": "MEXICO", "flag": "🇲🇽", "query": "Bacalar lagoon Mexico 4k"},
    {"country": "MEXICO", "flag": "🇲🇽", "query": "Hierve el Agua Mexico 4k"},
    {"country": "MEXICO", "flag": "🇲🇽", "query": "Holbox Mexico turquoise water 4k"},

    # 🇵🇪 PERU
    {"country": "PERU", "flag": "🇵🇪", "query": "Machu Picchu clouds sunrise 4k"},
    {"country": "PERU", "flag": "🇵🇪", "query": "Rainbow Mountain Peru 4k"},
    {"country": "PERU", "flag": "🇵🇪", "query": "Huacachina desert oasis 4k"},
    {"country": "PERU", "flag": "🇵🇪", "query": "Colca Canyon Peru 4k"},
    {"country": "PERU", "flag": "🇵🇪", "query": "Laguna Humantay Peru 4k"},
    {"country": "PERU", "flag": "🇵🇪", "query": "Ausangate Peru mountains 4k"},

    # 🇧🇴 BOLIVIA
    {"country": "BOLIVIA", "flag": "🇧🇴", "query": "Salar de Uyuni mirror Bolivia 4k"},
    {"country": "BOLIVIA", "flag": "🇧🇴", "query": "Laguna Colorada Bolivia 4k"},
    {"country": "BOLIVIA", "flag": "🇧🇴", "query": "Bolivia high altitude volcano lake 4k"},
    {"country": "BOLIVIA", "flag": "🇧🇴", "query": "Eduardo Avaroa Bolivia landscape 4k"},

    # 🇨🇱 CHILE
    {"country": "CHILE", "flag": "🇨🇱", "query": "Torres del Paine Chile 4k"},
    {"country": "CHILE", "flag": "🇨🇱", "query": "Atacama Desert Chile 4k"},
    {"country": "CHILE", "flag": "🇨🇱", "query": "Marble Caves Chile 4k"},
    {"country": "CHILE", "flag": "🇨🇱", "query": "Patagonia Chile mountains 4k"},
    {"country": "CHILE", "flag": "🇨🇱", "query": "Valle de la Luna Chile 4k"},
    {"country": "CHILE", "flag": "🇨🇱", "query": "General Carrera Lake Chile 4k"},

    # 🇦🇷 ARGENTINA
    {"country": "ARGENTINA", "flag": "🇦🇷", "query": "Patagonia Argentina mountains 4k"},
    {"country": "ARGENTINA", "flag": "🇦🇷", "query": "Perito Moreno Glacier 4k"},
    {"country": "ARGENTINA", "flag": "🇦🇷", "query": "Iguazu Falls Argentina 4k"},
    {"country": "ARGENTINA", "flag": "🇦🇷", "query": "Mount Fitz Roy Patagonia 4k"},
    {"country": "ARGENTINA", "flag": "🇦🇷", "query": "Quebrada de Humahuaca Argentina 4k"},

    # 🇧🇷 BRAZIL
    {"country": "BRAZIL", "flag": "🇧🇷", "query": "Lençóis Maranhenses Brazil lagoons 4k"},
    {"country": "BRAZIL", "flag": "🇧🇷", "query": "Iguazu Falls Brazil aerial 4k"},
    {"country": "BRAZIL", "flag": "🇧🇷", "query": "Amazon rainforest aerial 4k"},
    {"country": "BRAZIL", "flag": "🇧🇷", "query": "Fernando de Noronha Brazil 4k"},
    {"country": "BRAZIL", "flag": "🇧🇷", "query": "Chapada Diamantina Brazil 4k"},
    {"country": "BRAZIL", "flag": "🇧🇷", "query": "Jalapao Brazil golden dunes 4k"},

    # 🇨🇴 COLOMBIA
    {"country": "COLOMBIA", "flag": "🇨🇴", "query": "Cocora Valley Colombia giant palms 4k"},
    {"country": "COLOMBIA", "flag": "🇨🇴", "query": "Guatape Colombia mountains lake 4k"},
    {"country": "COLOMBIA", "flag": "🇨🇴", "query": "Caño Cristales Colombia rainbow river 4k"},
    {"country": "COLOMBIA", "flag": "🇨🇴", "query": "Tayrona National Park Colombia 4k"},
    {"country": "COLOMBIA", "flag": "🇨🇴", "query": "Lost City Colombia jungle 4k"},

    # 🇪🇨 ECUADOR
    {"country": "ECUADOR", "flag": "🇪🇨", "query": "Galapagos Islands Ecuador 4k"},
    {"country": "ECUADOR", "flag": "🇪🇨", "query": "Cotopaxi volcano Ecuador 4k"},
    {"country": "ECUADOR", "flag": "🇪🇨", "query": "Quilotoa crater lake Ecuador 4k"},
    {"country": "ECUADOR", "flag": "🇪🇨", "query": "Amazon Ecuador rainforest 4k"},

    # 🇨🇷 COSTA RICA
    {"country": "COSTA RICA", "flag": "🇨🇷", "query": "Costa Rica rainforest waterfall 4k"},
    {"country": "COSTA RICA", "flag": "🇨🇷", "query": "Arenal volcano Costa Rica 4k"},
    {"country": "COSTA RICA", "flag": "🇨🇷", "query": "Manuel Antonio Costa Rica 4k"},
    {"country": "COSTA RICA", "flag": "🇨🇷", "query": "Rio Celeste Costa Rica blue river 4k"},

    # 🇳🇵 / 🇧🇹 HIMALAYAN WORLD
    {"country": "BHUTAN", "flag": "🇧🇹", "query": "Tiger Nest Bhutan mountains 4k"},
    {"country": "BHUTAN", "flag": "🇧🇹", "query": "Bhutan Himalayan valley clouds 4k"},
    {"country": "BHUTAN", "flag": "🇧🇹", "query": "Punakha Bhutan valley 4k"},
    {"country": "PAKISTAN", "flag": "🇵🇰", "query": "Hunza Valley Pakistan 4k"},
    {"country": "PAKISTAN", "flag": "🇵🇰", "query": "Skardu Pakistan mountains 4k"},
    {"country": "PAKISTAN", "flag": "🇵🇰", "query": "Attabad Lake Pakistan turquoise 4k"},
    {"country": "PAKISTAN", "flag": "🇵🇰", "query": "Fairy Meadows Pakistan 4k"},

    # 🇰🇿 CENTRAL ASIA
    {"country": "KAZAKHSTAN", "flag": "🇰🇿", "query": "Charyn Canyon Kazakhstan 4k"},
    {"country": "KAZAKHSTAN", "flag": "🇰🇿", "query": "Kolsai Lakes Kazakhstan 4k"},
    {"country": "KAZAKHSTAN", "flag": "🇰🇿", "query": "Kaindy Lake Kazakhstan submerged forest 4k"},
    {"country": "KYRGYZSTAN", "flag": "🇰🇬", "query": "Issyk Kul Kyrgyzstan mountains 4k"},
    {"country": "KYRGYZSTAN", "flag": "🇰🇬", "query": "Ala Archa Kyrgyzstan 4k"},
    {"country": "KYRGYZSTAN", "flag": "🇰🇬", "query": "Song Kul Kyrgyzstan 4k"},
    {"country": "TAJIKISTAN", "flag": "🇹🇯", "query": "Pamir Mountains Tajikistan 4k"},
    {"country": "TAJIKISTAN", "flag": "🇹🇯", "query": "Seven Lakes Tajikistan 4k"},
    {"country": "UZBEKISTAN", "flag": "🇺🇿", "query": "Chimgan Mountains Uzbekistan 4k"},
    {"country": "UZBEKISTAN", "flag": "🇺🇿", "query": "Charvak Lake Uzbekistan mountains 4k"},
    {"country": "UZBEKISTAN", "flag": "🇺🇿", "query": "Zaamin National Park Uzbekistan 4k"},

    # 🏝 ISLAND PARADISE
    {"country": "MALDIVES", "flag": "🇲🇻", "query": "Maldives turquoise islands aerial 4k"},
    {"country": "SEYCHELLES", "flag": "🇸🇨", "query": "Seychelles granite rocks turquoise water 4k"},
    {"country": "MAURITIUS", "flag": "🇲🇺", "query": "Mauritius underwater waterfall illusion 4k"},
    {"country": "FIJI", "flag": "🇫🇯", "query": "Fiji tropical islands drone 4k"},
    {"country": "PALAU", "flag": "🇵🇼", "query": "Palau Rock Islands aerial 4k"},
    {"country": "FRENCH POLYNESIA", "flag": "🇵🇫", "query": "Bora Bora lagoon aerial 4k"},
    {"country": "FRENCH POLYNESIA", "flag": "🇵🇫", "query": "Moorea island mountains 4k"},
    {"country": "SAMOA", "flag": "🇼🇸", "query": "Samoa To Sua ocean trench 4k"},
    {"country": "PALAU", "flag": "🇵🇼", "query": "Palau jellyfish lake 4k"},
    {"country": "BAHAMAS", "flag": "🇧🇸", "query": "Bahamas turquoise water aerial 4k"},

    # 🧊 EXTREME PLACES
    {"country": "GREENLAND", "flag": "🇬🇱", "query": "Greenland giant icebergs aerial 4k"},
    {"country": "GREENLAND", "flag": "🇬🇱", "query": "Greenland fjord ice mountains 4k"},
    {"country": "SVALBARD", "flag": "🇳🇴", "query": "Svalbard Arctic glaciers 4k"},
    {"country": "SVALBARD", "flag": "🇳🇴", "query": "Svalbard polar landscape 4k"},
    {"country": "ANTARCTICA", "flag": "🇦🇶", "query": "Antarctica ice mountains aerial 4k"},
    {"country": "ANTARCTICA", "flag": "🇦🇶", "query": "Antarctica blue ice caves 4k"},
    {"country": "ANTARCTICA", "flag": "🇦🇶", "query": "Antarctica iceberg ocean cinematic 4k"},

    # 🌲 FOREST / WATERFALL
    {"country": "CANADA", "flag": "🇨🇦", "query": "hidden Canadian rainforest waterfall 4k"},
    {"country": "USA", "flag": "🇺🇸", "query": "hidden forest waterfall Oregon 4k"},
    {"country": "BRAZIL", "flag": "🇧🇷", "query": "Amazon hidden waterfall jungle 4k"},
    {"country": "JAPAN", "flag": "🇯🇵", "query": "ancient Japanese forest waterfall 4k"},
    {"country": "NEW ZEALAND", "flag": "🇳🇿", "query": "New Zealand hidden rainforest waterfall 4k"},
    {"country": "INDONESIA", "flag": "🇮🇩", "query": "hidden Indonesian jungle waterfall 4k"},
    {"country": "COSTA RICA", "flag": "🇨🇷", "query": "hidden Costa Rica jungle waterfall 4k"},
    {"country": "VIETNAM", "flag": "🇻🇳", "query": "hidden Vietnam jungle waterfall 4k"},
    {"country": "PHILIPPINES", "flag": "🇵🇭", "query": "hidden Philippines jungle waterfall 4k"},
    {"country": "THAILAND", "flag": "🇹🇭", "query": "hidden Thailand jungle waterfall 4k"},

    # 🤖 AI / FANTASY WORLD
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated impossible floating island waterfall cinematic 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated giant floating mountains above clouds 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated endless turquoise waterfall valley 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated magical glowing forest lake 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated crystal mountain landscape 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated giant waterfall inside canyon 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated floating jungle islands clouds 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated blue bioluminescent forest 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated fantasy ocean cliffs sunset 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated impossible rainbow mountains 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated giant tree island floating sky 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated hidden paradise valley waterfalls 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated glowing blue waterfall night 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated fantasy crystal cave lake 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated massive waterfall above clouds 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated ancient jungle ruins waterfall 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated giant moon alien landscape 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated pink mountains turquoise lake 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated emerald valley giant cliffs 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated fantasy island endless ocean 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated waterfall from floating island 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated golden desert turquoise river 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated giant crystal canyon 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated hidden valley aurora 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated giant flowers mountain valley 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated fantasy glacier glowing blue 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated floating waterfall mountains 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated giant canyon ocean waterfall 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated magical valley under two moons 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated impossible ocean cliff city nature 4k"},
    {"country": "AI WORLD", "flag": "🤖", "query": "AI generated surreal forest with giant waterfall 4k"},

    # 👽 ALIEN PLANETS
    {"country": "ALIEN WORLD", "flag": "👽", "query": "alien planet mountains giant moons cinematic 4k"},
    {"country": "ALIEN WORLD", "flag": "👽", "query": "alien planet ocean cliffs cinematic 4k"},
    {"country": "ALIEN WORLD", "flag": "👽", "query": "alien jungle glowing plants cinematic 4k"},
    {"country": "ALIEN WORLD", "flag": "👽", "query": "alien desert giant planet sky 4k"},
    {"country": "ALIEN WORLD", "flag": "👽", "query": "alien waterfall landscape cinematic 4k"},
    {"country": "ALIEN WORLD", "flag": "👽", "query": "alien crystal mountains blue atmosphere 4k"},
    {"country": "ALIEN WORLD", "flag": "👽", "query": "alien ocean bioluminescent island 4k"},
    {"country": "ALIEN WORLD", "flag": "👽", "query": "alien valley aurora giant moon 4k"},
    {"country": "ALIEN WORLD", "flag": "👽", "query": "alien forest giant trees mist 4k"},
    {"country": "ALIEN WORLD", "flag": "👽", "query": "alien floating islands clouds 4k"},
    {"country": "ALIEN WORLD", "flag": "👽", "query": "alien turquoise lake impossible mountains 4k"},
    {"country": "ALIEN WORLD", "flag": "👽", "query": "alien planet giant waterfall canyon 4k"},

    # 🌌 COSMIC NATURE
    {"country": "COSMIC WORLD", "flag": "🌌", "query": "cosmic mountains galaxy sky cinematic 4k"},
    {"country": "COSMIC WORLD", "flag": "🌌", "query": "forest under Milky Way giant galaxy 4k"},
    {"country": "COSMIC WORLD", "flag": "🌌", "query": "waterfall under northern lights galaxy 4k"},
    {"country": "COSMIC WORLD", "flag": "🌌", "query": "surreal ocean galaxy reflection 4k"},
    {"country": "COSMIC WORLD", "flag": "🌌", "query": "giant planet above mountain valley 4k"},
    {"country": "COSMIC WORLD", "flag": "🌌", "query": "galaxy reflected in turquoise mountain lake 4k"},
    {"country": "COSMIC WORLD", "flag": "🌌", "query": "cosmic waterfall under Milky Way 4k"},
    {"country": "COSMIC WORLD", "flag": "🌌", "query": "giant moon above endless ocean cliffs 4k"},
]

# ============================================================
# 🎨 CINEMATIC STYLES & ATMOSPHERES
# ============================================================

CINEMATIC_STYLES = [
    "cinematic", "ultra realistic", "photorealistic", "epic aerial drone",
    "slow cinematic drone", "golden hour", "sunrise", "sunset", "misty morning",
    "dramatic clouds", "after rain", "foggy atmosphere", "moonlight", "blue hour",
    "soft sunlight", "volumetric lighting", "8k nature documentary",
    "travel documentary", "high detail landscape"
]

CAMERA_STYLES = [
    "drone flyover", "slow aerial reveal", "wide establishing shot",
    "low angle cinematic shot", "high altitude aerial view", "slow forward camera movement",
    "smooth orbit camera", "mountain reveal", "waterfall reveal", "ocean reveal",
    "valley reveal", "vertical cinematic push in"
]

ATMOSPHERES = [
    "soft morning mist", "dramatic clouds", "light fog", "sun rays through clouds",
    "floating clouds", "fresh rain atmosphere", "crystal clear sky", "golden sunlight",
    "soft blue atmosphere", "cinematic haze", "volumetric sun rays", "light atmospheric fog"
]

def enhance_query(base_query):
    style = random.choice(CINEMATIC_STYLES)
    camera = random.choice(CAMERA_STYLES)
    atmosphere = random.choice(ATMOSPHERES)
    return (
        f"{base_query}, {style}, {camera}, {atmosphere}, "
        f"ultra detailed, natural colors, high quality, 4k"
    )

_recent_queries = []

def get_unique_place():
    global _recent_queries
    for _ in range(100):
        place = random.choice(UNREAL_PLACES_POOL)
        enhanced = enhance_query(place["query"])
        if enhanced not in _recent_queries:
            _recent_queries.append(enhanced)
            if len(_recent_queries) > 100:
                _recent_queries.pop(0)
            return {
                "country": place["country"],
                "flag": place["flag"],
                "query": enhanced
            }
    p = random.choice(UNREAL_PLACES_POOL)
    return {"country": p["country"], "flag": p["flag"], "query": p["query"]}

# ============================================================
# 🎵 AFTOMATIK MUSIQA TOPISH VA O'RNATISH (AUTO-FETCHER)
# ============================================================

def get_audio_file():
    """Faylni topadi, yo'q bo'lsa YouTube yoki zaxiradan avtomat yuklaydi"""
    tracks = glob.glob("**/*.mp3", recursive=True)
    for t in tracks:
        if os.path.getsize(t) > 20000:
            print(f"[AUDIO TANLANDI]: {t}")
            return os.path.abspath(t)

    target_audio = os.path.join(MUSIC_DIR, "auto_trend_beat.mp3")
    print("\n--- Repoda audio topilmadi. Avtomat musiqa yuklanmoqda... ---")

    # 1-usul: Namunaviy video audiosini yt-dlp orqali toza ajratib olish
    try:
        url = "https://youtube.com/shorts/EfF97vJdqIQ"
        cmd = [
            "yt-dlp", "-x", "--audio-format", "mp3", "--audio-quality", "0",
            "-o", target_audio, url
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(target_audio) and os.path.getsize(target_audio) > 10000:
            print("[AUDIO MUVAFFAQIYAT]: Trenddagi musiqa to'g'ridan-to'g'ri yuklandi!")
            return os.path.abspath(target_audio)
    except Exception as e:
        print(f"[OGOHLANTIRISH]: yt-dlp yuklay olmadi ({e}), zaxira havola ishlatilmoqda...")

    # 2-usul: Zaxira serverdan xuddi shu Trap/Bass trekni yuklash
    try:
        backup_url = "https://cdn.pixabay.com/download/audio/2022/11/06/audio_c937ecfa86.mp3?filename=trap-future-bass-royalty-free-music-125633.mp3"
        r = requests.get(backup_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        with open(target_audio, "wb") as f:
            f.write(r.content)
        print("[AUDIO MUVAFFAQIYAT]: Zaxira audio yuklab olindi!")
        return os.path.abspath(target_audio)
    except Exception as e:
        print(f"[XATO]: Musiqa yuklanmadi: {e}")
        # Shoshilinch zaxira (jimjitlik bo'lmasligi uchun)
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "sine=frequency=100:duration=60",
            target_audio
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return os.path.abspath(target_audio)

# ============================================================
# 🎬 4K YUKLASH VA ULTRA SIFATLI MONTAJ
# ============================================================

def download_crisp_4k_clip(query, idx):
    file_path = os.path.join(VIDEOS_DIR, f"clip_{idx}.mp4")
    if not PEXELS_API_KEY:
        print("[XATO]: PEXELS_API_KEY topilmadi!")
        return None

    try:
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=5&orientation=landscape"
        r = requests.get(url, headers={"Authorization": PEXELS_API_KEY}, timeout=20).json()
        videos = r.get("videos", [])
        if videos:
            files = videos[0].get("video_files", [])
            best = max(files, key=lambda x: (x.get("width", 0) * x.get("height", 0)))
            resp = requests.get(best.get("link"), stream=True, timeout=60)
            with open(file_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
            print(f"[YUKLANDI - 4K]: {query[:40]}...")
            return file_path
    except Exception as e:
        print(f"[XATO]: {e}")
    return None

def build_crisp_synced_short(short_index, spots, audio_path):
    output_file = os.path.join(OUTPUT_DIR, f"Short_{short_index}_UltraCrisp.mp4")
    print(f"\n--- Shorts #{short_index} avtomatik montaj qilinmoqda ---")

    # 1. Boshlang'ich Hook (2.2s - 'SAIL' zarbasigacha to'g'ri keladi)
    hook_video = f"hook_{short_index}.mp4"
    hook_text_filter = (
        "drawtext=text='PLACES ON EARTH THAT\\nDON’T FEEL REAL 🤯':"
        "fontcolor=white:fontsize=56:x=(w-text_w)/2:y=(h-text_h)/2:"
        "line_spacing=24:box=1:boxcolor=black@0.7:boxborderw=30:"
        "shadowcolor=black@0.9:shadowx=5:shadowy=5"
    )
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1080x1920:d=2.2:r=30",
        "-vf", hook_text_filter,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", hook_video
    ], check=True)

    temp_files = [hook_video]
    concat_list = f"concat_{short_index}.txt"

    with open(concat_list, "w") as f:
        f.write(f"file '{os.path.abspath(hook_video)}'\n")

        for i, spot in enumerate(spots):
            raw_clip = download_crisp_4k_clip(spot["query"], f"{short_index}_{i}")
            if not raw_clip:
                continue

            # Qora ekranda davlat kartochkasi (0.8s)
            card_video = f"card_{short_index}_{i}.mp4"
            country_display = f"📍 {spot['country']} {spot['flag']}"
            card_font_size = 50 if len(spot["country"]) > 13 else 64
            
            card_filter = (
                f"drawtext=text='{country_display}':"
                f"fontcolor=white:fontsize={card_font_size}:x=(w-text_w)/2:y=(h-text_h)/2:"
                "box=1:boxcolor=black@0.75:boxborderw=32:"
                "shadowcolor=black@0.9:shadowx=6:shadowy=6"
            )
            subprocess.run([
                "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1080x1920:d=0.8:r=30",
                "-vf", card_filter,
                "-c:v", "libx264", "-pix_fmt", "yuv420p", card_video
            ], check=True)
            temp_files.append(card_video)

            # VIDEO KADR USTIDA CHIROYLIK MATN (Glassmorphism overlay) + ULTRA 4K FILTR
            proc_clip = f"proc_{short_index}_{i}.mp4"
            overlay_font_size = 44 if len(spot["country"]) > 13 else 52
            
            # Kadrning pastki qismida estetik yarim shaffof zamonaviy panel
            clip_filter = (
                "scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop=1080:1920,"
                "unsharp=5:5:1.2:5:5:0.0,"
                "eq=contrast=1.14:saturation=1.28:brightness=0.02,"
                f"drawtext=text='📍 {spot['country']} {spot['flag']}':"
                f"fontcolor=white:fontsize={overlay_font_size}:x=(w-text_w)/2:y=h-320:"
                "box=1:boxcolor=black@0.55:boxborderw=24:"
                "shadowcolor=black@0.85:shadowx=4:shadowy=4,fps=30"
            )
            subprocess.run([
                "ffmpeg", "-y", "-i", raw_clip, "-t", "3.2",
                "-vf", clip_filter,
                "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-pix_fmt", "yuv420p",
                proc_clip
            ], check=True)
            temp_files.append(proc_clip)

            f.write(f"file '{os.path.abspath(card_video)}'\n")
            f.write(f"file '{os.path.abspath(proc_clip)}'\n")

    # Kadrlar oqimini birlashtirish
    temp_merged = f"merged_{short_index}.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", temp_merged
    ], check=True)

    # OVOZNI TO'LIQ VA SOXTASIZ BIRIKTIRISH (-map buyrug'i)
    subprocess.run([
        "ffmpeg", "-y",
        "-i", temp_merged,
        "-i", audio_path,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "320k",
        "-shortest",
        output_file
    ], check=True)

    for tf in temp_files + [concat_list, temp_merged]:
        if os.path.exists(tf):
            os.remove(tf)

    print(f"[TAYYOR ULTRA HD]: {output_file}")

# ============================================================
# 🚀 MAIN RUN
# ============================================================

if __name__ == "__main__":
    audio = get_audio_file()

    for s_idx in range(1, 5):
        selected_spots = [get_unique_place() for _ in range(5)]
        build_crisp_synced_short(s_idx, selected_spots, audio)

    print("\n=== BARCHA NOYOB LOKATSIYALAR ASOSIDA 4 TA ULTRA SHORTS TAYYORLANDI ===")
