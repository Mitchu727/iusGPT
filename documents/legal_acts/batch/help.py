import os
from pathlib import Path

current_path = Path(__file__).parent

for name in [
    "ustawa_prawo_wekslowe",
    "ustawa_prawo_o_adwokaturze",
    "ustawa_ksiegach_wieczystych_i_hipotece",
    "ustawa_o_radcach_prawnych",
    "ustawa_prawo_spoldzielcze",
    "ustawa_o_rzeczniku_praw_obywatelskich",
    "ustawa_prawo_o_stowarzyszeniach",
    "ustawa_o_samorządzie_gminnym",
    "ustawa_o_prawie_autorskim_i_prawach_pokrewnych",
    "ustawa_o_własności_lokali",
    "ustawa_o_zastawie_rejestrowym_i_rejestrze_zastawów",
    "konstytucja_rzeczpospolitej_polskiej"
]:
    os.mkdir(current_path/name)