"""Smoke test for an installed snips_nlu_parsers wheel (run outside the source tree)."""
import sys

import snips_nlu_parsers
from snips_nlu_parsers import BuiltinEntityParser, get_all_languages

print("python", sys.version.split()[0], "| snips_nlu_parsers from", snips_nlu_parsers.__file__)
print("languages:", get_all_languages())

res = BuiltinEntityParser.build("en").parse("Raise to sixty two degrees celsius")
assert res[0]["entity_kind"] == "snips/temperature" and res[0]["entity"]["value"] == 62.0, res
print("en:", res[0]["value"], "->", res[0]["entity"])

res = BuiltinEntityParser.build("fr").parse("réveille-moi demain à huit heures")
assert any(r["entity_kind"] == "snips/datetime" for r in res), res
print("fr:", [(r["value"], r["entity_kind"]) for r in res])
print("OK")
