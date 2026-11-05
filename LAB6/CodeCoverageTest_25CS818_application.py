
import pytest

from marathon_registration import (
    entry_fee,
    start_wave,
    finisher_status
)


# ---------------- ENTRY FEE TESTS ----------------

def test_entry_fee_unknown_race():
    with pytest.raises(ValueError, match="unknown race"):
        entry_fee("ultra", 30, False, False)


def test_entry_fee_under_12():
    with pytest.raises(ValueError, match="too young"):
        entry_fee("5k", 11, False, False)


def test_entry_fee_under_18_for_half():
    with pytest.raises(ValueError, match="too young for this distance"):
        entry_fee("half", 17, False, False)


def test_entry_fee_under_18_for_full():
    with pytest.raises(ValueError, match="too young for this distance"):
        entry_fee("full", 17, False, False)


def test_entry_fee_early_bird():
    assert entry_fee("10k", 30, True, False) == 600


def test_entry_fee_senior_discount():
    assert entry_fee("5k", 65, False, False) == 250


def test_entry_fee_tshirt():
    assert entry_fee("5k", 30, False, True) == 800


def test_entry_fee_all_discounts_and_tshirt():
    assert entry_fee("10k", 65, True, True) == 600


# ---------------- START WAVE TESTS ----------------

def test_start_wave_no_time():
    assert start_wave(None, "full") == "D"


def test_start_wave_full_wave_a():
    assert start_wave(180, "full") == "A"


def test_start_wave_full_wave_b():
    assert start_wave(200, "full") == "B"


def test_start_wave_full_wave_c():
    assert start_wave(241, "full") == "C"


def test_start_wave_other_race_wave_a():
    assert start_wave(90, "10k") == "A"


def test_start_wave_other_race_wave_b():
    assert start_wave(120, "10k") == "B"


def test_start_wave_other_race_wave_c():
    assert start_wave(121, "10k") == "C"


# ---------------- FINISHER STATUS TESTS ----------------

def test_finisher_disqualified():
    assert finisher_status(60, "full", 1) == "DSQ"


def test_full_race_finisher():
    assert finisher_status(360, "full", 0) == "finisher"


def test_full_race_dnf():
    assert finisher_status(361, "full", 0) == "DNF"


def test_half_race_finisher():
    assert finisher_status(180, "half", 0) == "finisher"


def test_half_race_dnf():
    assert finisher_status(181, "half", 0) == "DNF"


def test_other_race_finisher():
    assert finisher_status(90, "5k", 0) == "finisher"


def test_other_race_dnf():
    assert finisher_status(91, "10k", 0) == "DNF"
