import json
from datetime import datetime
from database import SessionLocal
from models.team import Team
from models.match import Match


teams_data = [
    {"name": "Mexico", "code": "MEX", "group": "A"},
    {"name": "South Africa", "code": "RSA", "group": "A"},
    {"name": "South Korea", "code": "KOR", "group": "A"},
    {"name": "Czech Republic", "code": "CZE", "group": "A"},
    {"name": "Canada", "code": "CAN", "group": "B"},
    {"name": "Bosnia & Herzegovina", "code": "BIH", "group": "B"},
    {"name": "Qatar", "code": "QAT", "group": "B"},
    {"name": "Switzerland", "code": "SUI", "group": "B"},
    {"name": "Brazil", "code": "BRA", "group": "C"},
    {"name": "Morocco", "code": "MAR", "group": "C"},
    {"name": "Haiti", "code": "HAI", "group": "C"},
    {"name": "Scotland", "code": "SCO", "group": "C"},
    {"name": "USA", "code": "USA", "group": "D"},
    {"name": "Paraguay", "code": "PAR", "group": "D"},
    {"name": "Australia", "code": "AUS", "group": "D"},
    {"name": "Turkey", "code": "TUR", "group": "D"},
    {"name": "Germany", "code": "GER", "group": "E"},
    {"name": "Curaçao", "code": "CUW", "group": "E"},
    {"name": "Ivory Coast", "code": "CIV", "group": "E"},
    {"name": "Ecuador", "code": "ECU", "group": "E"},
    {"name": "Netherlands", "code": "NED", "group": "F"},
    {"name": "Japan", "code": "JPN", "group": "F"},
    {"name": "Sweden", "code": "SWE", "group": "F"},
    {"name": "Tunisia", "code": "TUN", "group": "F"},
    {"name": "Belgium", "code": "BEL", "group": "G"},
    {"name": "Egypt", "code": "EGY", "group": "G"},
    {"name": "Iran", "code": "IRN", "group": "G"},
    {"name": "New Zealand", "code": "NZL", "group": "G"},
    {"name": "Spain", "code": "ESP", "group": "H"},
    {"name": "Cape Verde", "code": "CPV", "group": "H"},
    {"name": "Saudi Arabia", "code": "KSA", "group": "H"},
    {"name": "Uruguay", "code": "URU", "group": "H"},
    {"name": "France", "code": "FRA", "group": "I"},
    {"name": "Senegal", "code": "SEN", "group": "I"},
    {"name": "Iraq", "code": "IRQ", "group": "I"},
    {"name": "Norway", "code": "NOR", "group": "I"},
    {"name": "Argentina", "code": "ARG", "group": "J"},
    {"name": "Algeria", "code": "ALG", "group": "J"},
    {"name": "Austria", "code": "AUT", "group": "J"},
    {"name": "Jordan", "code": "JOR", "group": "J"},
    {"name": "Portugal", "code": "POR", "group": "K"},
    {"name": "DR Congo", "code": "COD", "group": "K"},
    {"name": "Uzbekistan", "code": "UZB", "group": "K"},
    {"name": "Colombia", "code": "COL", "group": "K"},
    {"name": "England", "code": "ENG", "group": "L"},
    {"name": "Croatia", "code": "CRO", "group": "L"},
    {"name": "Ghana", "code": "GHA", "group": "L"},
    {"name": "Panama", "code": "PAN", "group": "L"},
]


def seed_teams(db):
    for team_info in teams_data:
        team = Team(
            name=team_info["name"],
            code=team_info["code"],
            group=team_info["group"],
        )
        db.add(team)
    db.commit()
    print("Teams seeded!")

def convert_stage(round_name):
    if round_name.startswith("Matchday"):
        return "group"
    mapping = {
        "Round of 32": "round32",
        "Round of 16": "round16",
        "Quarter-finals": "quarter",
        "Semi-finals": "semi",
        "Third place": "third",
        "Final": "final",
    }
    return mapping.get(round_name, "unknown")


def parse_match_date(date_str, time_str):
    time_only = time_str.split(" ")[0]
    return datetime.fromisoformat(f"{date_str}T{time_only}:00")


def seed_matches(db):
    teams = db.query(Team).all()
    teams_by_name = {t.name: t.id for t in teams}

    with open("data/matches.json", "r") as f:
        data = json.load(f)
    matches_data = data["matches"]

    print(f"Seeding {len(matches_data)} matches...")
    for m in matches_data:
        home_id = teams_by_name.get(m["team1"])
        away_id = teams_by_name.get(m["team2"])

        if home_id is None or away_id is None:
            print(f"⚠️ Skipping match: {m['team1']} vs {m['team2']} (team not found)")
            continue

        new_match = Match(
            team_home_id=home_id,
            team_away_id=away_id,
            date=parse_match_date(m["date"], m["time"]),
            stage=convert_stage(m["round"]),
        )
        db.add(new_match)

    db.commit()
    print("Matches seeded!")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        # seed_teams(db)  # déjà fait, à décommenter pour une nouvelle BDD
        seed_matches(db)
    finally:
        db.close()
