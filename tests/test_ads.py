import os
import pytest

import bibmanager.bib_manager as bm
import bibmanager.ads_manager as am
import bibmanager.config_manager as cm
import bibmanager.utils as u


def test_key_update_journal_year():
    # Case of journal does not matter:
    assert am.key_update("BeaulieuEtal2010ArXiVGJ436b", "2011ApJ...731...16B",
               "2010arXiv1007.0324B") == "BeaulieuEtal2011apjGJ436b"
    assert am.key_update("BeaulieuEtal2010arXivGJ436b", "2011ApJ...731...16B",
               "2010arXiv1007.0324B") == "BeaulieuEtal2011apjGJ436b"
    assert am.key_update("BeaulieuEtal2010arxivGJ436b", "2011ApJ...731...16B",
               "2010arXiv1007.0324B") == "BeaulieuEtal2011apjGJ436b"


def test_key_update_year():
    assert am.key_update("BeaulieuEtal2010apjGJ436b", "2011ApJ...731...16B",
               "2010arXiv1007.0324B") == "BeaulieuEtal2011apjGJ436b"
    # Year does not get updated if it does not match:
    assert am.key_update("BeaulieuEtal2009arxivGJ436b", "2011ApJ...731...16B",
               "2010arXiv1007.0324B") == "BeaulieuEtal2009apjGJ436b"


def test_key_update_journal():
    assert am.key_update("BeaulieuEtal2011arxivGJ436b", "2011ApJ...731...16B",
               "2011arXiv1007.0324B") == "BeaulieuEtal2011apjGJ436b"


@pytest.mark.skip(reason="Can I test this without monkeypatching the request?")
def test_search(ads_entries, mock_init):
    cm.set("ads_token", os.environ.get("ADS_TOKEN"))
    querry = 'author:"^mayor" year:1995 property:refereed'
    results, nmatch = am.search(querry)
    assert nmatch == 1
    assert results == [ads_entries['mayor']]


@pytest.mark.skip(reason="Can I test this without monkeypatching the request?")
def test_search_limit_cache(ads_entries):
    cm.set("ads_token", os.environ.get("ADS_TOKEN"))
    querry = 'author:"^fortney, j" year:2000-2018 property:refereed'
    results, nmatch = am.search(querry, start=0, cache_rows=2)
    # There are 26 matches:
    assert nmatch == 26
    # But requested only two entries:
    assert len(results) == 2
    assert results == [ads_entries['fortney2018'], ads_entries['fortney2016']]


@pytest.mark.skip(reason="Can I test this without monkeypatching the request?")
def test_search_start(ads_entries):
    cm.set("ads_token", os.environ.get("ADS_TOKEN"))
    querry = 'author:"^fortney, j" year:2000-2018 property:refereed'
    results, nmatch = am.search(querry, start=2, cache_rows=2)
    # There are 26 matches:
    assert nmatch == 26
    # But requested only two entries:
    assert len(results) == 2
    # But results start from third match:
    assert results == [ads_entries['fortney2013'], ads_entries['fortney2012']]


@pytest.mark.skip(reason="Can I test this without monkeypatching the request?")
def test_search_unauthorized():
    cm.set("ads_token", "None")
    querry = 'author:"^fortney, j" year:2000-2018 property:refereed'
    with pytest.raises(ValueError, match="Invalid ADS request: Unauthorized," \
                                         " check you have a valid ADS token."):
        results, nmatch = am.search(querry)


def test_display_all(capsys, ads_entries):
    results = [ads_entries['fortney2018'], ads_entries['fortney2016']]
    start  = 0
    index  = 0
    rows   = 2
    nmatch = 2
    am.display(results, start, index, rows, nmatch, short=True)
    captured = capsys.readouterr()
    assert captured.out == f"""
Title: A deeper look at Jupiter
Authors: Fortney, Jonathan
adsurl: https://ui.adsabs.harvard.edu/\\#abs/2018Natur.555..168F
{u.BOLD}bibcode{u.END}: 2018Natur.555..168F

Title: The Hunt for Planet Nine: Atmosphere, Spectra, Evolution, and
    Detectability
Authors: Fortney, Jonathan J.; et al.
adsurl: https://ui.adsabs.harvard.edu/\\#abs/2016ApJ...824L..25F
{u.BOLD}bibcode{u.END}: 2016ApJ...824L..25F

Showing entries 1--2 out of 2 matches.\n"""


def test_display_first_batch(capsys, ads_entries):
    results = [ads_entries['fortney2018'], ads_entries['fortney2016'],
               ads_entries['fortney2013'], ads_entries['fortney2012']]
    start  = 0
    index  = 0
    rows   = 2
    nmatch = 4
    am.display(results, start, index, rows, nmatch, short=True)
    captured = capsys.readouterr()
    assert captured.out == f"""
Title: A deeper look at Jupiter
Authors: Fortney, Jonathan
adsurl: https://ui.adsabs.harvard.edu/\\#abs/2018Natur.555..168F
{u.BOLD}bibcode{u.END}: 2018Natur.555..168F

Title: The Hunt for Planet Nine: Atmosphere, Spectra, Evolution, and
    Detectability
Authors: Fortney, Jonathan J.; et al.
adsurl: https://ui.adsabs.harvard.edu/\\#abs/2016ApJ...824L..25F
{u.BOLD}bibcode{u.END}: 2016ApJ...824L..25F

Showing entries 1--2 out of 4 matches.  To show the next set, execute:
bibm ads-search\n"""


def test_display_second_batch(capsys, ads_entries):
    results = [ads_entries['fortney2018'], ads_entries['fortney2016'],
               ads_entries['fortney2013'], ads_entries['fortney2012']]
    start  = 0
    index  = 2
    rows   = 2
    nmatch = 4
    am.display(results, start, index, rows, nmatch, short=True)
    captured = capsys.readouterr()
    assert captured.out == f"""
Title: A Framework for Characterizing the Atmospheres of Low-mass Low-
    density Transiting Planets
Authors: Fortney, Jonathan J.; et al.
adsurl: https://ui.adsabs.harvard.edu/\\#abs/2013ApJ...775...80F
{u.BOLD}bibcode{u.END}: 2013ApJ...775...80F

Title: On the Carbon-to-oxygen Ratio Measurement in nearby Sun-like Stars:
    Implications for Planet Formation and the Determination of Stellar
    Abundances
Authors: Fortney, Jonathan J.
adsurl: https://ui.adsabs.harvard.edu/\\#abs/2012ApJ...747L..27F
{u.BOLD}bibcode{u.END}: 2012ApJ...747L..27F

Showing entries 3--4 out of 4 matches.\n"""


def test_display_over(capsys, ads_entries):
    results = [ads_entries['fortney2018'], ads_entries['fortney2016'],
               ads_entries['fortney2013'], ads_entries['fortney2012']]
    start  = 0
    index  = 3
    rows   = 2
    nmatch = 4
    am.display(results, start, index, rows, nmatch, short=True)
    captured = capsys.readouterr()
    assert captured.out == f"""
Title: On the Carbon-to-oxygen Ratio Measurement in nearby Sun-like Stars:
    Implications for Planet Formation and the Determination of Stellar
    Abundances
Authors: Fortney, Jonathan J.
adsurl: https://ui.adsabs.harvard.edu/\\#abs/2012ApJ...747L..27F
{u.BOLD}bibcode{u.END}: 2012ApJ...747L..27F

Showing entries 4--4 out of 4 matches.\n"""


@pytest.mark.skip(reason="Can I test this without monkeypatching the request?")
def test_add_bibtex_success(capsys, mock_init):
    cm.set("ads_token", os.environ.get("ADS_TOKEN"))
    captured = capsys.readouterr()
    bibcodes = ['1925PhDT.........1P']
    keys = ['Payne1925phdStellarAtmospheres']
    am.add_bibtex(bibcodes, keys)
    captured = capsys.readouterr()
    assert captured.out == "\nMerged 1 new entries.\n" \
                           "(Not counting updated references)\n"
    loaded_bibs = bm.load()
    assert len(loaded_bibs) == 1
    assert loaded_bibs[0].content == \
"""@PHDTHESIS{Payne1925phdStellarAtmospheres,
       author = {{Payne}, Cecilia Helena},
        title = "{Stellar Atmospheres; a Contribution to the Observational Study of High Temperature in the Reversing Layers of Stars.}",
     keywords = {Astronomy},
       school = {RADCLIFFE COLLEGE.},
         year = 1925,
        month = Jan,
       adsurl = {https://ui.adsabs.harvard.edu/\\#abs/1925PhDT.........1P},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}"""


@pytest.mark.skip(reason="Can I test this without monkeypatching the request?")
def test_add_bibtex_fail(capsys, mock_init):
    cm.set("ads_token", os.environ.get("ADS_TOKEN"))
    captured = capsys.readouterr()
    bibcodes = ['1925PhDT.......X.1P']
    keys = ['Payne1925phdStellarAtmospheres']
    am.add_bibtex(bibcodes, keys)
    captured = capsys.readouterr()
    assert captured.out \
           == "\nError: There were no entries found for the input bibcodes.\n"
    loaded_bibs = bm.load()
    assert len(loaded_bibs) == 0


@pytest.mark.skip(reason="Can I test this without monkeypatching the request?")
def test_add_bibtex_warning(capsys, mock_init):
    # A partially failing call will still add those that succeed:
    cm.set("ads_token", os.environ.get("ADS_TOKEN"))
    captured = capsys.readouterr()
    bibcodes = ['1925PhDT.....X...1P', '2018MNRAS.481.5286F']
    keys = ['Payne1925phdStellarAtmospheres', 'FolsomEtal2018mnrasHD219134']
    am.add_bibtex(bibcodes, keys)
    loaded_bibs = bm.load()
    assert len(loaded_bibs) == 1
    captured = capsys.readouterr()
    assert captured.out == """
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
Warning:

There were bibcodes not found:
 - 1925PhDT.....X...1P

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


Merged 1 new entries.
(Not counting updated references)\n"""


@pytest.mark.skip(reason="Can I test this without monkeypatching the request?")
def test_update(capsys, mock_init_sample):
    cm.set("ads_token", os.environ.get("ADS_TOKEN"))
    captured = capsys.readouterr()
    am.update()
    captured = capsys.readouterr()
    assert captured.out == """
Merged 0 new entries.
(Not counting updated references)
There were 1 entries updated from ArXiv to their peer-reviewed version.
These ones changed their key:
BeaulieuEtal2010arxivGJ436b -> BeaulieuEtal2011apjGJ436b\n"""


@pytest.mark.skip(reason="Can I test this without monkeypatching the request?")
def test_manager():
    pass