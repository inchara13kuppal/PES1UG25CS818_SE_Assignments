
import pytest

from marathon_registration import (
    entry_fee,
    start_wave,
    finisher_status
)


# ENTRY FEE: All decision branches

def test_unknown_race():
    with pytest.raises(ValueError):
        entry_fee("invalid", 30, False, False)


def test_age_below_12():
    with pytest.raises(ValueError):
        entry_fee("5k", 11, False, False)


def test_age_12_allowed():
    assert entry_fee("5k", 12, False, False) == 500


def test_half_race_age_below_18():
    with pytest.raises(ValueError):
        entry_fee("half", 17, False, False)


def test_half_race_age_18_allowed():
    assert entry_fee("half", 18, False, False) == 1200


def test_full_race_age_below_18():
    with pytest.raises(ValueError):
        entry_fee("full", 17, False, False)


def test_full_race_age_18_allowed():
    assert entry_fee("full", 18, False, False) == 1800


def test_early_bird_true():
    assert entry_fee("10k", 30, True, False) == 600


def test_early_bird_false():
    assert entry_fee("10k", 30, False, False) == 800


def test_senior_true():
    assert entry_fee("5k", 65, False, False) == 250


def test_senior_false():
    assert entry_fee("5k", 64, False, False) == 500


def test_tshirt_true():
    assert entry_fee("5k", 30, False, True) == 800


def test_tshirt_false():
    assert entry_fee("5k", 30, False, False) == 500


# START WAVE: All decision branches

def test_no_time():
    assert start_wave(None, "full") == "D"


def test_full_race_wave_a():
    assert start_wave(180, "full") == "A"


def test_full_race_wave_b():
    assert start_wave(200, "full") == "B"


def test_full_race_wave_c():
    assert start_wave(241, "full") == "C"


def test_non_full_race_wave_a():
    assert start_wave(90, "10k") == "A"


def test_non_full_race_wave_b():
    assert start_wave(120, "10k") == "B"


def test_non_full_race_wave_c():
    assert start_wave(121, "10k") == "C"


# FINISHER STATUS: All decision branches

def test_missed_checkpoint_disqualification():
    assert finisher_status(400, "full", 1) == "DSQ"


def test_no_missed_checkpoint():
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
