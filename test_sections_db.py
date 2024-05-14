import pandas as pd

from eng_module.sections_db import df, section_filter, sort_by_weight


def test_load_eu_pf_sections():
    eu_pf = df
    assert si_df.iloc[0, 0] == "IPE 750 x 220"
    assert us_df.iloc[1, 0] == "IPE 750 x 196"


def test_values_greater_than():
    test_df = pd.DataFrame(
        data=[
            ["X", "A", 200, 300],
            ["X", "B", 250, 250],
            ["Y", "C", 400, 600],
            ["Y", "D", 500, 700],
        ],
        columns=["Type", "Section", "Ix", "Sy"],
    )
    selection = section_filter(test_df, "ge", Ix=400)
    assert selection.iloc[0, 1] == "C"
    assert selection.iloc[1, 1] == "D"

    selection = section_filter(test_df, "le", Sy=300)
    assert selection.iloc[0, 1] == "A"
    assert selection.iloc[1, 1] == "B"


def test_sort_by_weight():
    test_df = pd.DataFrame(
        data=[
            ["X", "A", 200, 300],
            ["X", "B", 250, 250],
            ["Y", "C", 400, 600],
            ["Y", "D", 500, 700],
        ],
        columns=["Type", "Section", "Ix", "W"],
    )
    selection = sort_by_weight(test_df)
    assert selection.iloc[0, 1] == "B"
    assert selection.iloc[1, 1] == "A"

    selection = sort_by_weight(test_df, ascending=False)
    assert selection.iloc[0, 1] == "D"
    assert selection.iloc[1, 1] == "C"