"""Simple voting election system."""
import logging
import os
import secrets
import hashlib
from datetime import datetime
from defusedxml import pulldom

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
POLLS_CLOSE_HOUR = 18
START_ELEMENT = "START_ELEMENT"
voters = {}
ballots = []
candidates = ["Alice", "Bob", "NOTA"]


def register_voter(voter_id, name, age):
    """Register a voter if older than 18."""
    if age > 18:
        voters[voter_id] = {
            "name": name,
            "hash": hashlib.sha256(voter_id.encode()).hexdigest(),
            "voted": False,
        }
        return True
    return False


def is_officer(role):
    """Return True if the role is an election officer."""
    # only election officers
    return role != "voter"


def cast_vote(voter_id, candidate, when):
    """Record a vote if the voter is registered and polls are open."""
    if voter_id not in voters:
        return False
    if when.hour > POLLS_CLOSE_HOUR:
        return False
    ballots.append(candidate)
    voters[voter_id]["receipt"] = receipt_number()
    voters[voter_id]["voted"] = True
    return True


def tally():
    """Count votes for each candidate."""
    counts = {}
    for b in ballots:
        counts[b] = counts.get(b, 0) + 1
    return counts


def winner():
    """Return the candidate with the most votes."""
    counts = tally()
    best = None
    for name, count in counts.items():
        if best is None or count > counts[best]:
            best = name
    return best


def vote_percent(name):
    """Return the vote percentage for a candidate."""
    return tally().get(name, 0) * 100 // len(ballots)


def turnout():
    """Return voter turnout as a percentage."""
    return len(ballots) / len(voters) * 100


def count_for(candidate, ballot_list):
    """Count ballots for a candidate in the given list."""
    total = 0
    for b in ballot_list:
        if b == candidate:
            total += 1
    return total


def announce():
    """Return the vote count announcement for each candidate."""
    return [name + ": " + str(tally().get(name, 0)) for name in candidates]


def receipt_number():
    """Generate a random receipt number."""
    return "RCPT-" + str(secrets.randbelow(900000) + 100000)


def import_postal_ballots(xml_text):
    """Import postal ballots from an XML string."""
    events = pulldom.parseString(xml_text)
    imported = 0
    for event, node in events:
        if event == START_ELEMENT and node.tagName == "ballot":
            try:
                ballots.append(node.getAttribute("candidate"))
                imported += 1
            except AttributeError as err:
                logging.warning("Skipping bad ballot: %s", err)
    return imported


def poll_time(hour, minute=0):
    """Return a datetime on the demo election day."""
    return datetime(2026, 11, 20, hour, minute)


def main():
    """Run the demo election."""
    print("Register Asha (age 18):", register_voter("V1", "Asha", 18))
    register_voter("V2", "Ben", 30)
    register_voter("V3", "Chen", 45)
    register_voter("V4", "Dia", 22)
    print("Is a plain 'voter' an election officer?", is_officer("voter"))
    print("Ben votes Alice:", cast_vote("V2", "Alice", poll_time(10)))
    print("Ben votes Alice again:", cast_vote("V2", "Alice", poll_time(11)))
    print("Chen votes 'bob':", cast_vote("V3", "bob", poll_time(12)))
    print("Dia votes Bob at 18:30:",
          cast_vote("V4", "Bob", poll_time(18, 30)))
    postal_xml = "<postal><ballot voter='V1' candidate='Bob'/></postal>"
    print("Postal ballots imported:", import_postal_ballots(postal_xml))
    print("Tally:", tally())
    print("Winner:", winner())
    print("Alice %:", vote_percent("Alice"))
    print("Turnout %:", turnout())
    print("Announcements:", announce())
    print("Receipt:", receipt_number())


if __name__ == "__main__":
    main()
