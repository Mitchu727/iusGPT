import os
from pathlib import Path

current_path = Path(__file__).parent

for name in [
    # "ustawa_prawo_wekslowe",
    # "ustawa_prawo_o_adwokaturze",
    # "ustawa_ksiegach_wieczystych_i_hipotece",
    # "ustawa_o_radcach_prawnych",
    # "ustawa_prawo_spoldzielcze",
    # "ustawa_o_rzeczniku_praw_obywatelskich",
    # "ustawa_prawo_o_stowarzyszeniach",
    # "ustawa_o_samorządzie_gminnym",
    # "ustawa_o_prawie_autorskim_i_prawach_pokrewnych",
    # "ustawa_o_własności_lokali",
    # "ustawa_o_zastawie_rejestrowym_i_rejestrze_zastawów",
    # "konstytucja_rzeczpospolitej_polskiej",
    "ustawa_o_krajowym_rejestrze_sadowym",
    "ustawa_o_gospodarce_nieruchomosciami",
    "ustawa_o_samorzadzie_powiatowym",
    "ustawa_o_samorzadzie_wojewodztwa",
    "ustawa_o_systemie_ubezpieczeń_spolecznych",
    "ustawa_o_swiadczeniach_pienieznych_z_ubezpieczenia_spolecznego_w_razie_choroby_i_macierzyństwa",
    "ustawa_o_spoldzielniach_mieszkaniowych",
    "ustawa_o_ochronie_praw_lokatorow,_mieszkaniowym_zasobie_gminy_i_o_zmianie_kodeksu_cywilnego",
    "ustawa_prawo_o_ustroju_sadow_powszechnych",
    "ustawa_prawo_o_postepowaniu_przed_sadami_administracyjnymi",
    "ustawa_prawo_upadlosciowe",
    "ustawa_o_szczegolnych_zasadach_rozwiazywania_z_pracownikami_stosunkow_pracy_z_przyczyn_niedotyczacych_pracownikow",
    "ustawa_o_ubezpieczeniach_obowiazkowych_ubezpieczeniowym_funduszu_gwarancyjnym_i_polskim_biurze_ubezpieczycieli_komunikacyjnych",
    "ustawa_o_kosztach_sadowych_w_sprawach_cywilnych",
    "ustawa_o_ochronie_konkurencji_i_konsumentow",
    "ustawa_o_wojewodzie_i_administracji_rzadowej_w_wojewodztwie",
    "ustawa_o_przeciwdzialaniu_nadmiernym_opoznieniom_w_transakcjach_handlowych",
    "ustawa_o_prawach_konsumenta",
    "ustawa_prawo_restrukturyzacyjne",
    "ustawa_prawo_o_prokuraturze",
    "ustawa_o_prokuratorii_generalnej_rzeczypospolitej_polskiej",
    "ustawa_o_sadzie_najwyzszym",
    "ustawa_prawo_przedsiebiorcow",
    "ustawa_o_centralnej_ewidencji_i_informacji_o_dzialalnosci_gospodarczej_i_punkcie_informacji_dla_przedsiebiorcy",
]:
    os.mkdir(current_path/name)