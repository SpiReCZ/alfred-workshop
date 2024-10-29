from .text_utils import remove_preceding_text, remove_trigger_word, find_trigger_word, text_to_voice_command


def test_remove_preceding_text():
    assert remove_preceding_text("tohle by bylo fajn.      Sním o slonovi", "Sním") == "Sním o slonovi"
    assert remove_preceding_text("Sním o slonovi", "Sním") == "Sním o slonovi"
    assert remove_preceding_text("OhniSním o slonovi", "Sním") == "Sním o slonovi"

def test_remove_trigger_word():
    assert remove_trigger_word("Sním o slonovi", "sním") == "o slonovi"
    assert remove_trigger_word("Sním o slonovi", "Sním o") == "slonovi"
    assert remove_trigger_word("Sním o slonovi", "slonovi") == "Sním o"

def test_find_trigger_word():
    trigger_words_list = {
        "calibrate": ["kalibruj", "kalibrace", "kalibrovat"],
        "loop": ["opakuj", "opakovat", "opakuj to"],
        "dream": ["sním o"]
    }
    found = find_trigger_word("kalbruj to hodně", trigger_words_list)
    assert found[0] == "calibrate"
    assert found[1] == "kalbruj"


    found = find_trigger_word("kalbrujmeskalsj tohle moc", trigger_words_list)
    assert found[0] == "calibrate"
    assert found[1] == "kalbrujmeskalsj"

    found = find_trigger_word("tohle moc nefunguje", trigger_words_list)
    assert found[0] == None
    assert found[1] == None

    found = find_trigger_word("Sním o stromě který je veliký", trigger_words_list)
    assert found[0] == "dream"
    assert found[1] == "Sním o"

    found = find_trigger_word("Sníh o stromě který je veliký", trigger_words_list)
    assert found[0] == "dream"
    assert found[1] == "Sníh o"

    found = find_trigger_word("Snim o stromě který je veliký", trigger_words_list)
    assert found[0] == "dream"
    assert found[1] == "Snim o"

    found = find_trigger_word("Min o stromě který je veliký", trigger_words_list)
    assert found[0] == None
    assert found[1] == None


def test_find_and_remove_preceding_anf_trigger_word():
    trigger_words_list = {
        "calibrate": ["kalibruj", "kalibrace", "kalibrovat"],
        "loop": ["opakuj", "opakovat", "opakuj to"],
        "dream": ["sním o"]
    }
    haystack = "moc dobrý to je. Sníh o stromě který je veliký"
    found = find_trigger_word(haystack, trigger_words_list)
    removed = remove_preceding_text(haystack, found[1])
    removed = remove_trigger_word(removed, found[1])
    assert removed == "stromě který je veliký"

