"""Scan main.tex for em dashes and phrasing that reads as machine-generated."""
import re, sys
from pathlib import Path
tex = Path(sys.argv[1]).read_text(encoding="utf-8")
# strip comments
body = "\n".join(l for l in tex.splitlines() if not l.lstrip().startswith("%"))
lines = body.splitlines()

def report(label, pattern, flags=re.I):
    hits = [(i + 1, l.strip()[:140]) for i, l in enumerate(lines) if re.search(pattern, l, flags)]
    print(f"\n== {label}: {sum(len(re.findall(pattern, l, flags)) for l in lines)} hit(s)")
    for n, l in hits[:40]:
        print(f"  L{n}: {l}")

report("em dashes (--- or unicode)", r"---|\u2014")
report("spaced en dash used as punctuation", r"\s--\s|\u2013")
report("rhetorical question marks outside the title", r"\?(?!.*\\title)")
words = ["delve", "leverage", "robust", "crucial", "notably", "furthermore", "moreover", "additionally", "overall",
         "in summary", "it is worth", "it is important", "landscape", "underscore", "highlight", "showcase", "seamless",
         "harness", "paradigm", "holistic", "nuanced", "intricate", "pivotal", "testament", "realm", "embark", "foster",
         "comprehensive", "cutting-edge", "game-chang", "unlock", "empower", "elevate", "in conclusion", "in this paper",
         "it should be noted", "serves as", "plays a (crucial|key|vital) role", "not only", "a wide range", "in today",
         "ever-evolving", "navigate", "dive", "unpack", "importantly", "crucially", "essentially", "arguably", "ultimately",
         "key takeaway", "transformative", "myriad", "plethora", "utilize", "facilitate", "enhance", "in order to",
         "it is clear that", "clearly", "obviously", "of course", "remarkabl", "strikingly", "interestingly", "compelling",
         "powerful", "exciting", "promising", "best practice", "actionable", "insightful", "valuable insight"]
report("AI-flavoured words/phrases", r"\b(" + "|".join(words) + r")\w*")
report("emphasis via \\emph (count)", r"\\emph\{")
report("bold inline labels", r"\\textbf\{")
report("colon-led lists in prose (': (1)')", r":\s*\(1\)")
report("exclamation marks", r"!")
report("'this is expected' / 'as expected'", r"as expected|this is expected|unsurprising")
report("sentence starting with 'This' + verb (vague referent)", r"(?:^|\. )This (is|means|shows|pattern|suggests|indicates)")
