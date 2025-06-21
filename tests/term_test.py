import term
import pytest

def test_term():
    assert term.compile_term("(And (Or (Title/Abstract complication) (Title/Abstract adverse events)) (Or (Title/Abstract esophageal stenting) (Title/Abstract stent placement for esophageal cancer)))") == "(('complication'[Title/Abstract] OR 'adverse events'[Title/Abstract]) AND ('esophageal stenting'[Title/Abstract] OR 'stent placement for esophageal cancer'[Title/Abstract]))"
    assert term.compile_term("(Title/Abstract esophageal\\ stenting)")=="'esophageal stenting'[Title/Abstract]"
    assert term.compile_term("(Title/Abstract esophageal stenting\\(cancer\\))")=="'esophageal stenting(cancer)'[Title/Abstract]"
    with pytest.raises(Exception):
        term.compile_term("")
    with pytest.raises(Exception):
        term.compile_term("(")
    with pytest.raises(Exception):
        term.compile_term("(Plain A")
    with pytest.raises(Exception):
        term.compile_term("(Plain (And))")
    with pytest.raises(Exception):
        term.compile_term("((And) A)")
    with pytest.raises(Exception):
        term.compile_term("(Title/Abstract (And))")
    with pytest.raises(Exception):
        term.compile_term("(Title/Abstract \\A)")
    with pytest.raises(Exception):
        term.compile_term("(Title/Abstract \\")