from pathlib import Path
from bs4 import BeautifulSoup

HTML_PATH = Path(__file__).resolve().parents[1] / "index.html"

def load_soup():
    html = HTML_PATH.read_text(encoding="utf-8")
    return BeautifulSoup(html, "html.parser")

def test_at_least_one_project_link_exists():
    soup = load_soup()
    heading = soup.find('h2', string=lambda x: x and 'Projects' in x)
    assert heading, "Projects section heading not found"
    section = heading.find_parent('section')
    assert section, "Projects section not found"
    links = section.find_all('a')
    assert len(links) >= 1, "No project links found"

def test_target_blank_has_noopener_noreferrer():
    soup = load_soup()
    for anchor in soup.find_all('a', target='_blank'):
        rel = anchor.get('rel', [])
        if isinstance(rel, str):
            rel = rel.split()
        assert 'noopener' in rel and 'noreferrer' in rel, f"Anchor {anchor} missing rel=\"noopener noreferrer\""
