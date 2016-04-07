# General settings for url building and sending requests
BASE_URL = 'https://play.google.com/store/apps'
HEADERS = {
	'origin': 'https://play.google.com',
	'user-agent':
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) '
		'AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/48.0.2564.116 Safari/537.36',
	'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
}

VERIFY_SSL = True

DEBUG = True

NUM_COLLECTIONS = 20
NUM_RESULTS = 60  # Max = 120

# App Categories
CATEGORIES = {
	"ANDROID_WEAR": {"url": "/store/apps/category/ANDROID_WEAR", "category_id": "ANDROID_WEAR", "name": "Android Wear"},
	"BOOKS_AND_REFERENCE": {"url": "/store/apps/category/BOOKS_AND_REFERENCE", "category_id": "BOOKS_AND_REFERENCE", "name": "Books & Reference"},
	"BUSINESS": {"url": "/store/apps/category/BUSINESS", "category_id": "BUSINESS", "name": "Business"},
	"COMICS": {"url": "/store/apps/category/COMICS", "category_id": "COMICS", "name": "Comics"},
	"COMMUNICATION": {"url": "/store/apps/category/COMMUNICATION", "category_id": "COMMUNICATION", "name": "Communication"},
	"EDUCATION": {"url": "/store/apps/category/EDUCATION", "category_id": "EDUCATION", "name": "Education"},
	"ENTERTAINMENT": {"url": "/store/apps/category/ENTERTAINMENT", "category_id": "ENTERTAINMENT", "name": "Entertainment"},
	"FINANCE": {"url": "/store/apps/category/FINANCE", "category_id": "FINANCE", "name": "Finance"},
	"HEALTH_AND_FITNESS": {"url": "/store/apps/category/HEALTH_AND_FITNESS", "category_id": "HEALTH_AND_FITNESS", "name": "Health & Fitness"},
	"LIBRARIES_AND_DEMO": {"url": "/store/apps/category/LIBRARIES_AND_DEMO", "category_id": "LIBRARIES_AND_DEMO", "name": "Libraries & Demo"},
	"LIFESTYLE": {"url": "/store/apps/category/LIFESTYLE", "category_id": "LIFESTYLE", "name": "Lifestyle"},
	"APP_WALLPAPER": {"url": "/store/apps/category/APP_WALLPAPER", "category_id": "APP_WALLPAPER", "name": "Live Wallpaper"},
	"MEDIA_AND_VIDEO": {"url": "/store/apps/category/MEDIA_AND_VIDEO", "category_id": "MEDIA_AND_VIDEO", "name": "Media & Video"},
	"MEDICAL": {"url": "/store/apps/category/MEDICAL", "category_id": "MEDICAL", "name": "Medical"},
	"MUSIC_AND_AUDIO": {"url": "/store/apps/category/MUSIC_AND_AUDIO", "category_id": "MUSIC_AND_AUDIO", "name": "Music & Audio"},
	"NEWS_AND_MAGAZINES": {"url": "/store/apps/category/NEWS_AND_MAGAZINES", "category_id": "NEWS_AND_MAGAZINES", "name": "News & Magazines"},
	"PERSONALIZATION": {"url": "/store/apps/category/PERSONALIZATION", "category_id": "PERSONALIZATION", "name": "Personalization"},
	"PHOTOGRAPHY": {"url": "/store/apps/category/PHOTOGRAPHY", "category_id": "PHOTOGRAPHY", "name": "Photography"},
	"PRODUCTIVITY": {"url": "/store/apps/category/PRODUCTIVITY", "category_id": "PRODUCTIVITY", "name": "Productivity"},
	"SHOPPING": {"url": "/store/apps/category/SHOPPING", "category_id": "SHOPPING", "name": "Shopping"},
	"SOCIAL": {"url": "/store/apps/category/SOCIAL", "category_id": "SOCIAL", "name": "Social"},
	"SPORTS": {"url": "/store/apps/category/SPORTS", "category_id": "SPORTS", "name": "Sports"},
	"TOOLS": {"url": "/store/apps/category/TOOLS", "category_id": "TOOLS", "name": "Tools"},
	"TRANSPORTATION": {"url": "/store/apps/category/TRANSPORTATION", "category_id": "TRANSPORTATION", "name": "Transportation"},
	"TRAVEL_AND_LOCAL": {"url": "/store/apps/category/TRAVEL_AND_LOCAL", "category_id": "TRAVEL_AND_LOCAL", "name": "Travel & Local"},
	"WEATHER": {"url": "/store/apps/category/WEATHER", "category_id": "WEATHER", "name": "Weather"},
	"APP_WIDGETS": {"url": "/store/apps/category/APP_WIDGETS", "category_id": "APP_WIDGETS", "name": "Widgets"},
	"GAME_ACTION": {"url": "/store/apps/category/GAME_ACTION", "category_id": "GAME_ACTION", "name": "Action"},
	"GAME_ADVENTURE": {"url": "/store/apps/category/GAME_ADVENTURE", "category_id": "GAME_ADVENTURE", "name": "Adventure"},
	"GAME_ARCADE": {"url": "/store/apps/category/GAME_ARCADE", "category_id": "GAME_ARCADE", "name": "Arcade"},
	"GAME_BOARD": {"url": "/store/apps/category/GAME_BOARD", "category_id": "GAME_BOARD", "name": "Board"},
	"GAME_CARD": {"url": "/store/apps/category/GAME_CARD", "category_id": "GAME_CARD", "name": "Card"},
	"GAME_CASINO": {"url": "/store/apps/category/GAME_CASINO", "category_id": "GAME_CASINO", "name": "Casino"},
	"GAME_CASUAL": {"url": "/store/apps/category/GAME_CASUAL", "category_id": "GAME_CASUAL", "name": "Casual"},
	"GAME_EDUCATIONAL": {"url": "/store/apps/category/GAME_EDUCATIONAL", "category_id": "GAME_EDUCATIONAL", "name": "Educational"},
	"GAME_MUSIC": {"url": "/store/apps/category/GAME_MUSIC", "category_id": "GAME_MUSIC", "name": "Music"},
	"GAME_PUZZLE": {"url": "/store/apps/category/GAME_PUZZLE", "category_id": "GAME_PUZZLE", "name": "Puzzle"},
	"GAME_RACING": {"url": "/store/apps/category/GAME_RACING", "category_id": "GAME_RACING", "name": "Racing"},
	"GAME_ROLE_PLAYING": {"url": "/store/apps/category/GAME_ROLE_PLAYING", "category_id": "GAME_ROLE_PLAYING", "name": "Role Playing"},
	"GAME_SIMULATION": {"url": "/store/apps/category/GAME_SIMULATION", "category_id": "GAME_SIMULATION", "name": "Simulation"},
	"GAME_SPORTS": {"url": "/store/apps/category/GAME_SPORTS", "category_id": "GAME_SPORTS", "name": "Sports"},
	"GAME_STRATEGY": {"url": "/store/apps/category/GAME_STRATEGY", "category_id": "GAME_STRATEGY", "name": "Strategy"},
	"GAME_TRIVIA": {"url": "/store/apps/category/GAME_TRIVIA", "category_id": "GAME_TRIVIA", "name": "Trivia"},
	"GAME_WORD": {"url": "/store/apps/category/GAME_WORD", "category_id": "GAME_WORD", "name": "Word"},
	"FAMILY?age=AGE_RANGE1": {"url": "/store/apps/category/FAMILY?age=AGE_RANGE1", "category_id": "FAMILY?age=AGE_RANGE1", "name": "Ages 5 & Under"},
	"FAMILY?age=AGE_RANGE2": {"url": "/store/apps/category/FAMILY?age=AGE_RANGE2", "category_id": "FAMILY?age=AGE_RANGE2", "name": "Ages 6-8"},
	"FAMILY?age=AGE_RANGE3": {"url": "/store/apps/category/FAMILY?age=AGE_RANGE3", "category_id": "FAMILY?age=AGE_RANGE3", "name": "Ages 9 & Up"},
	"FAMILY_ACTION": {"url": "/store/apps/category/FAMILY_ACTION", "category_id": "FAMILY_ACTION", "name": "Action & Adventure"},
	"FAMILY_BRAINGAMES": {"url": "/store/apps/category/FAMILY_BRAINGAMES", "category_id": "FAMILY_BRAINGAMES", "name": "Brain Games"},
	"FAMILY_CREATE": {"url": "/store/apps/category/FAMILY_CREATE", "category_id": "FAMILY_CREATE", "name": "Creativity"},
	"FAMILY_EDUCATION": {"url": "/store/apps/category/FAMILY_EDUCATION", "category_id": "FAMILY_EDUCATION", "name": "Education"},
	"FAMILY_MUSICVIDEO": {"url": "/store/apps/category/FAMILY_MUSICVIDEO", "category_id": "FAMILY_MUSICVIDEO", "name": "Music & Video"},
	"FAMILY_PRETEND": {"url": "/store/apps/category/FAMILY_PRETEND", "category_id": "FAMILY_PRETEND", "name": "Pretend Play"}
}

BASE_COLLECTIONS = {
	'Top New Free': 'topselling_new_free',
	'Top New Paid': 'topselling_new_paid',
	'Top Free': 'topselling_free',
	'Top Paid': 'topselling_paid',
	'Top Grossing': 'topgrossing',
	'Trending': 'movers_shakers'
}
