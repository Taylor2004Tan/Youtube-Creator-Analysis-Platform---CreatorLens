from flask import Blueprint, jsonify
from services.youtube import YouTubeService
from config import YOUTUBE_API_KEY

categories_bp = Blueprint("categories", __name__)

def _get_youtube_service():
    return YouTubeService(YOUTUBE_API_KEY)

# ----------------------------------------------------------------------- #
#  Curated seed data — 15+ top creators per category
#  Stored as handles; resolved on-demand via /api/resolve/<handle>
# ----------------------------------------------------------------------- #
CATEGORIES: dict[str, list[dict]] = {
    "Technology": [
        {"name": "MKBHD",               "handle": "mkbhd",                "desc": "Premium tech reviews & gadgets"},
        {"name": "Linus Tech Tips",      "handle": "LinusTechTips",        "desc": "PC hardware, builds & reviews"},
        {"name": "Unbox Therapy",        "handle": "unboxtherapy",         "desc": "Viral product unboxings"},
        {"name": "JerryRigEverything",   "handle": "JerryRigEverything",   "desc": "Durability tests & teardowns"},
        {"name": "Dave2D",               "handle": "Dave2D",               "desc": "Laptop & productivity tech"},
        {"name": "Gamers Nexus",         "handle": "GamersNexus",          "desc": "In-depth PC hardware benchmarks"},
        {"name": "Network Chuck",        "handle": "NetworkChuck",         "desc": "Networking & cybersecurity"},
        {"name": "Fireship",             "handle": "Fireship",             "desc": "100-second coding tutorials"},
        {"name": "TechLinked",           "handle": "TechLinked",           "desc": "Daily tech news"},
        {"name": "Hardware Canucks",     "handle": "HardwareCanucks",      "desc": "Canadian PC hardware reviews"},
        {"name": "Tom Scott",            "handle": "TomScott",             "desc": "Fascinating technology stories"},
        {"name": "Techquickie",          "handle": "Techquickie",          "desc": "Quick tech explainers"},
        {"name": "Hardware Unboxed",     "handle": "HardwareUnboxed",      "desc": "GPU & CPU deep dives"},
        {"name": "Two Minute Papers",    "handle": "TwoMinutePapers",      "desc": "AI research explained simply"},
        {"name": "Wendover Productions", "handle": "WendoverProductions",  "desc": "Technology & logistics explainers"},
        {"name": "Linus Tech Tips 2",    "handle": "LinusMediaGroup",      "desc": "Behind the scenes at LMG"},
    ],
    "Gaming": [
        {"name": "PewDiePie",        "handle": "PewDiePie",      "desc": "Gaming & commentary icon"},
        {"name": "Markiplier",       "handle": "markiplier",     "desc": "Let's plays & horror gaming"},
        {"name": "jacksepticeye",    "handle": "jacksepticeye",  "desc": "High-energy gaming commentary"},
        {"name": "VanossGaming",     "handle": "VanossGaming",   "desc": "Multiplayer gaming & comedy"},
        {"name": "DanTDM",           "handle": "DanTDM",         "desc": "Family-friendly gaming"},
        {"name": "Dream",            "handle": "Dream",          "desc": "Minecraft speedruns & challenges"},
        {"name": "Ninja",            "handle": "Ninja",          "desc": "Competitive Fortnite gameplay"},
        {"name": "Pokimane",         "handle": "pokimane",       "desc": "Gaming & variety streaming"},
        {"name": "xQc",              "handle": "xQcOW",          "desc": "Variety gaming & reactions"},
        {"name": "TimTheTatman",     "handle": "TimTheTatman",   "desc": "FPS gaming & variety content"},
        {"name": "Shroud",           "handle": "shroud",         "desc": "Elite competitive FPS gameplay"},
        {"name": "MrBeast Gaming",   "handle": "MrBeastGaming",  "desc": "Gaming challenges & giveaways"},
        {"name": "SSundee",          "handle": "SSundee",        "desc": "Minecraft & Among Us content"},
        {"name": "CoryxKenshin",     "handle": "CoryxKenshin",   "desc": "Horror & anime gaming commentary"},
        {"name": "The Act Man",      "handle": "TheActMan",      "desc": "In-depth game reviews & rants"},
        {"name": "InternetCity",     "handle": "Valkyrae",       "desc": "Games & streaming personality"},
    ],
    "Education": [
        {"name": "Khan Academy",          "handle": "khanacademy",          "desc": "Free world-class education"},
        {"name": "Crash Course",          "handle": "crashcourse",          "desc": "In-depth educational series"},
        {"name": "TED-Ed",                "handle": "TEDEd",                "desc": "Animated educational lessons"},
        {"name": "Veritasium",            "handle": "veritasium",           "desc": "Science & engineering explainers"},
        {"name": "Kurzgesagt",            "handle": "kurzgesagt",           "desc": "Animated science & philosophy"},
        {"name": "3Blue1Brown",           "handle": "3blue1brown",          "desc": "Beautiful mathematics visualised"},
        {"name": "SmarterEveryDay",       "handle": "SmarterEveryDay",      "desc": "Science through real experiments"},
        {"name": "Vsauce",                "handle": "Vsauce",               "desc": "Mind-bending science questions"},
        {"name": "CGP Grey",              "handle": "CGPGrey",              "desc": "Complex topics made simple"},
        {"name": "Tom Scott",             "handle": "TomScott",             "desc": "Fascinating real-world stories"},
        {"name": "MinutePhysics",         "handle": "minutephysics",        "desc": "Physics in under a minute"},
        {"name": "AsapSCIENCE",           "handle": "AsapSCIENCE",          "desc": "Science of everyday life"},
        {"name": "SciShow",               "handle": "SciShow",              "desc": "Weekly science news"},
        {"name": "Mark Rober",            "handle": "MarkRober",            "desc": "Engineering & science projects"},
        {"name": "Wendover Productions",  "handle": "WendoverProductions",  "desc": "How the world really works"},
        {"name": "Real Engineering",      "handle": "RealEngineering",      "desc": "Engineering explainer videos"},
    ],
    "Lifestyle": [
        {"name": "Emma Chamberlain", "handle": "emmachamberlain",  "desc": "Lifestyle, fashion & travel vlogs"},
        {"name": "David Dobrik",     "handle": "DavidDobrik",      "desc": "Pranks, vlogs & surprises"},
        {"name": "Yes Theory",       "handle": "YesTheory",        "desc": "Seeking discomfort & adventure"},
        {"name": "Casey Neistat",    "handle": "casey",            "desc": "NYC vlogs & cinematic filmmaking"},
        {"name": "Nas Daily",        "handle": "NasDaily",         "desc": "One-minute inspiring stories"},
        {"name": "Vlog Brothers",    "handle": "vlogbrothers",     "desc": "Educational vlogs & world events"},
        {"name": "Peter McKinnon",   "handle": "PeterMcKinnon",    "desc": "Photography & creative vlogs"},
        {"name": "Matt D'Avella",    "handle": "MattDAvella",      "desc": "Minimalism & documentary style"},
        {"name": "Kara and Nate",    "handle": "karaandnate",      "desc": "Full-time travel vlogging"},
        {"name": "GaryVee",          "handle": "garyvee",          "desc": "Entrepreneurship & hustle culture"},
        {"name": "Airrack",          "handle": "airrack",          "desc": "Big stunts & viral challenges"},
        {"name": "Dhar Mann",        "handle": "DharMann",         "desc": "Inspirational life lessons"},
        {"name": "Nathaniel Drew",   "handle": "nathanieldrew",    "desc": "Self-improvement & travel"},
        {"name": "Sadhguru",         "handle": "SadhguruJV",       "desc": "Spirituality & inner wellbeing"},
        {"name": "LADbible",         "handle": "ladbible",         "desc": "Viral lifestyle & entertainment"},
        {"name": "Mark Manson",      "handle": "IAmMarkManson",    "desc": "Life advice & philosophy"},
    ],
    "Finance": [
        {"name": "Graham Stephan",    "handle": "GrahamStephan",       "desc": "Real estate & personal finance"},
        {"name": "Andrei Jikh",       "handle": "AndreiJikh",           "desc": "Investing & financial freedom"},
        {"name": "Meet Kevin",        "handle": "MeetKevin",            "desc": "Stocks, real estate & news"},
        {"name": "Humphrey Yang",     "handle": "humphreytalks",        "desc": "Personal finance made simple"},
        {"name": "Minority Mindset",  "handle": "MinorityMindset",      "desc": "Financial literacy & wealth"},
        {"name": "Nate O'Brien",      "handle": "NateOBrien",           "desc": "Minimalism & personal finance"},
        {"name": "The Plain Bagel",   "handle": "ThePlainBagel",        "desc": "Clear Canadian finance education"},
        {"name": "Two Cents",         "handle": "TwoCentsPBS",          "desc": "PBS personal finance series"},
        {"name": "WhiteBoard Finance","handle": "WhiteboardFinance",    "desc": "Investing strategies on whiteboards"},
        {"name": "Ryan Scribner",     "handle": "RyanScribner",         "desc": "Investing & passive income"},
        {"name": "Charlie Chang",     "handle": "charliechangshow",     "desc": "Finance & tech investing"},
        {"name": "Erin Talks Money",  "handle": "ErinTalksMoney",       "desc": "Budgeting & financial planning"},
        {"name": "Jarrad Morrow",     "handle": "JarradMorrow",         "desc": "Index funds & long-term investing"},
        {"name": "ClearValue Tax",    "handle": "ClearValueTax",        "desc": "Tax education & accounting"},
        {"name": "Our Rich Journey",  "handle": "OurRichJourney",       "desc": "FIRE movement & early retirement"},
        {"name": "Investopedia",      "handle": "Investopedia",         "desc": "Finance terms & market explainers"},
    ],
    "Health & Fitness": [
        {"name": "Athlean-X",               "handle": "athleanx",                   "desc": "Science-based strength training"},
        {"name": "Mind Pump TV",            "handle": "MindPumpTV",                 "desc": "No-BS fitness & health advice"},
        {"name": "Jeff Nippard",            "handle": "JeffNippard",               "desc": "Evidence-based bodybuilding"},
        {"name": "Jeremy Ethier",           "handle": "JeremyEthier",              "desc": "Science-backed workout tips"},
        {"name": "Eugene Teo",              "handle": "EugeneTeo",                 "desc": "Movement quality & strength"},
        {"name": "Renaissance Periodization","handle": "RenaissancePeriodization", "desc": "Dr. Mike's training science"},
        {"name": "Thomas DeLauer",          "handle": "ThomasDeLauer",             "desc": "Keto & intermittent fasting"},
        {"name": "Stephanie Buttermore",    "handle": "StephanieButtermore",       "desc": "All-in journey & fitness research"},
        {"name": "Alan Thrall",             "handle": "AlanThrall",                "desc": "Powerlifting & strength training"},
        {"name": "Scott Herman Fitness",    "handle": "ScottHermanFitness",        "desc": "Bodybuilding & nutrition"},
        {"name": "Fitness Blender",         "handle": "FitnessBlender",            "desc": "Free full-length workout videos"},
        {"name": "Yoga With Adriene",       "handle": "YogaWithAdriene",           "desc": "Accessible yoga for everyone"},
        {"name": "Blogilates",              "handle": "blogilates",                "desc": "Pop pilates & fitness lifestyle"},
        {"name": "James Smith PT",          "handle": "JamesSmithPT",              "desc": "Anti-BS fitness & diet advice"},
        {"name": "Gravity Transformation",  "handle": "GravityTransformation",     "desc": "Fat loss & muscle building"},
        {"name": "Doctor Mike",             "handle": "DoctorMikeVideos",           "desc": "Real doctor reacts & health advice"},
    ],
}

CATEGORY_ICONS: dict[str, str] = {
    "Technology":      "💻",
    "Gaming":          "🎮",
    "Education":       "🎓",
    "Lifestyle":       "✨",
    "Finance":         "💰",
    "Health & Fitness":"💪",
}


@categories_bp.route("/api/categories")
def get_categories():
    cats = [
        {"name": k, "icon": CATEGORY_ICONS.get(k, "📁"), "count": len(v)}
        for k, v in CATEGORIES.items()
    ]
    return jsonify({"categories": cats})


@categories_bp.route("/api/categories/<category_name>")
def get_category_creators(category_name: str):
    if category_name not in CATEGORIES:
        return jsonify({"error": "Category not found"}), 404
    return jsonify({
        "category": category_name,
        "icon": CATEGORY_ICONS.get(category_name, "📁"),
        "creators": CATEGORIES[category_name],
    })


@categories_bp.route("/api/resolve/<handle>")
def resolve_handle(handle: str):
    """Resolve a YouTube @handle to full channel info."""
    try:
        channel = _get_youtube_service().get_channel_by_handle(handle.lstrip("@"))
        if not channel:
            return jsonify({"error": "Channel not found"}), 404
        return jsonify(channel)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
