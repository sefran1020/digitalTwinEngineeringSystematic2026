# -*- coding: utf-8 -*-
"""Convert narrative/parenthetical author-year citations to pandoc citeproc syntax."""
import re, glob, os

JEE = "G:/DESARROLLO2026_SINENTORNO/gemelosAnalisis/JEE-WILEY"
OUT = "G:/DESARROLLO2026_SINENTORNO/gemelosAnalisis/entrega/build"
os.makedirs(OUT, exist_ok=True)

# (author-literal, year, suffix-or-'', key). Order: longest/suffixed first.
M = [
 ("Álvarez Ariza and Hernández Hernández","2026","","alvarez_ariza_investigating_2026"),
 ("Bokhtiar Al Zami et al.","2025","","bokhtiar_al_zami_digital_2025"),
 ("Kumar Karanam and Hartman","2025","","kumar_karanam_systematic_2025"),
 ("Karanam and Hartman","2025","","kumar_karanam_systematic_2025"),
 ("De Larmelina et al.","2026","","de_larmelina_conceptualizing_2026"),
 ("Terkaj et al.","2024","a","terkaj_framework_2024"),
 ("Wang et al.","2025","b","wang_innovative_2025"),
 ("Terkaj et al.","2024","","terkaj_virtual_2024"),
 ("Abdelrahman et al.","2025","","abdelrahman_what_2025"),
 ("Al-Jumeily et al.","2026","","al-jumeily_implementing_2026"),
 ("AlMekkawi et al.","2026","","almekkawi_effectiveness_2026"),
 ("Alkhedher et al.","2021","","alkhedher_interactive_2021"),
 ("Andrieu et al.","2021","","andrieu_remote_2021"),
 ("Azofeifa et al.","2025","","azofeifa_top_2025"),
 ("Bolaños et al.","2026","","bolanos_design_2026"),
 ("Bonavolonta et al.","2026","","bonavolonta_sustainability_2026"),
 ("Chamorro-Atalaya et al.","2024","","chamorro-atalaya_use_2024"),
 ("Chen et al.","2025","","chen_ai-enhanced_2025"),
 ("Chen et al.","2026","","chen_effects_2026"),
 ("Chumchuen and Akatimagool","2023","","chumchuen_remote_2023"),
 ("Cuperman and Raveh","2026","","cuperman_academic_2026"),
 ("Dautaj et al.","2026","","dautaj_importance_2026"),
 ("Dayo et al.","2024","","dayo_evaluating_2024"),
 ("Demir and Uşak","2025","","demir_analyzing_2025"),
 ("Denissova et al.","2026","","denissova_factors_2026"),
 ("Eltaiba et al.","2025","","eltaiba_benefits_2025"),
 ("Espinoza et al.","2025","","espinoza_virtual_2025"),
 ("Fan and Zhang","2025","","fan_impacts_2025"),
 ("Gallego et al.","2025","","gallego_low-cost_2025"),
 ("Giussani et al.","2025","","giussani_study_2025"),
 ("Haase","2022","","haase_teaching_2022"),
 ("Harris et al.","2020","","harris_framework_2020"),
 ("Hunpinyo et al.","2026","","hunpinyo_isa95_2026"),
 ("Jiang et al.","2026","","jiang_state_2026"),
 ("Jin et al.","2026","","jin_extended_2026"),
 ("Kabir and Ray","2025","","kabir_digital_2025"),
 ("Khan et al.","2026","","khan_teaching_2026"),
 ("Kim and Kirollos","2026","","kim_effect_2026"),
 ("Kwateng and Leong","2026","","kwateng_enhancing_2026"),
 ("Kwateng et al.","2026","","kwateng_enhancing_2026"),
 ("Lainidis and Mystakidis","2026","","lainidis_systematic_2026"),
 ("Lampropoulos et al.","2025","","lampropoulos_virtual_2025"),
 ("Lee et al.","2023","","lee_digital_2023"),
 ("Lee et al.","2025","","lee_digital_2025"),
 ("Lei et al.","2022","","lei_teaching_2022"),
 ("Li et al.","2026","","li_effects_2026"),
 ("Liljaniemi and Paavilainen","2020","","liljaniemi_using_2020"),
 ("Liu et al.","2025","","liu_cognitive_2025"),
 ("Llanos-Ruiz et al.","2025","","llanos-ruiz_virtual_2025"),
 ("Lu et al.","2025","","lu_digital_2025"),
 ("Machado et al.","2025","","machado_automatic_2025"),
 ("Maladzhi and Bello","2025","","maladzhi_digital_2025"),
 ("Naukkarinen and Sainio","2018","","naukkarinen_supporting_2018"),
 ("Niţu et al.","2026","","nitu_engineering_2026"),
 ("Omrany et al.","2026","","omrany_digital_2026"),
 ("Panagiotakis et al.","2022","","panagiotakis_remote_2022"),
 ("Prichetnikov et al.","2020","","prichetnikov_investigation_2020"),
 ("Ruppert et al.","2023","","ruppert_demonstration_2023"),
 ("Saini and Garg","2026","","saini_industry_2026"),
 ("Sakkas et al.","2025","","sakkas_multiplayer_2025"),
 ("Sell et al.","2025","","sell_international_2025"),
 ("Sepasgozar","2020","","sepasgozar_digital_2020"),
 ("Tarng et al.","2024","","tarng_application_2024"),
 ("Thelen et al.","2022","","thelen_comprehensive_2022"),
 ("Tokhayeva et al.","2026","","tokhayeva_virtualisation_2026"),
 ("Treffinger et al.","2022","","treffinger_investigations_2022"),
 ("Vergara et al.","2025","","vergara_decade_2025"),
 ("Weichbroth et al.","2024","","weichbroth_toward_2024"),
 ("Widowati et al.","2025","","widowati_meta-analysis_2025"),
 ("Xiang et al.","2025","","xiang_research_2025"),
 ("Yindeemak et al.","2026","","yindeemak_emerging_2026"),
 ("Zare et al.","2026","","zare_engineering_2026"),
 ("Zhang et al.","2024","","zhang_effectiveness_2024"),
 ("Zhong et al.","2026","","zhong_virtual_2026"),
]

def auth_re(a):
    # escape, then make whitespace flexible (handle line breaks)
    return re.escape(a).replace(r'\ ', r'\s+')

PLACE = {}      # marker -> ('narr'|'atom', key)
ctr = [0]
def mark(kind, key):
    ctr[0]+=1
    m = f"\x00{ctr[0]}\x00"
    PLACE[m] = (kind, key)
    return m

def convert(text):
    # Phase 1: narrative  Author (YYYY[suf])
    for a,y,s,k in M:
        pat = re.compile(auth_re(a)+r'\s*\('+y+(s if s else r'[ab]?')+r'\)')
        text = pat.sub(lambda mo, k=k: mark('narr',k), text)
    # Phase 1b: atoms  Author, YYYY[suf]
    for a,y,s,k in M:
        pat = re.compile(auth_re(a)+r',\s*'+y+(s if s else r'[ab]?')+r'(?![0-9])')
        text = pat.sub(lambda mo, k=k: mark('atom',k), text)
    # Phase 2: convert parenthetical groups that contain atom markers to [ ... ]
    def fix_paren(mo):
        inner = mo.group(1)
        if not any(PLACE.get(m,('',''))[0]=='atom' for m in re.findall(r'\x00\d+\x00', inner)):
            return mo.group(0)
        # replace atom markers with @key, narr markers (shouldn't be here) too
        def rep(m2):
            kind,key = PLACE[m2.group(0)]
            return '@'+key
        inner2 = re.sub(r'\x00\d+\x00', rep, inner)
        return '['+inner2+']'
    text = re.sub(r'\(([^()]*\x00\d+\x00[^()]*)\)', fix_paren, text)
    # Phase 3: any remaining markers -> narrative @key (or @key for stray atoms)
    def rep_rest(m2):
        kind,key = PLACE[m2.group(0)]
        return '@'+key
    text = re.sub(r'\x00\d+\x00', rep_rest, text)
    return text

report = []
for fp in sorted(glob.glob(JEE+"/0*.md")):
    PLACE.clear(); ctr[0]=0
    raw = open(fp,encoding='utf-8').read()
    out = convert(raw)
    fn = os.path.basename(fp)
    open(OUT+"/"+fn,'w',encoding='utf-8').write(out)
    report.append((fn, raw.count('\x00')==0, out.count('@')))
    # leftover author-year not converted?
    leftovers = re.findall(r'[A-ZÁ-Ú][\wÀ-ÿ.\'’-]+(?: et al\.| and [A-ZÁ-Ú][\wÀ-ÿ-]+)?,?\s*\(?(?:19|20)\d{2}[ab]?\)?', out)
    # filter obvious non-cites
    print(f"== {fn}: {out.count('@')} citations ==")

# show any residual author-year tokens (potential misses) excluding pure numeric stats
import sys
print("\n--- scanning for residual author-year citation tokens ---")
for fp in sorted(glob.glob(OUT+"/0*.md")):
    txt = open(fp,encoding='utf-8').read()
    for mo in re.finditer(r'[A-ZÁ-Ú][\wÀ-ÿ.\'’-]+(?:\s+et al\.|\s+and\s+[A-ZÁ-Ú][\wÀ-ÿ-]+)?\s*[,(]\s*(?:19|20)\d{2}[ab]?\)?', txt):
        frag = mo.group(0)
        if 'Kritzinger' in frag: continue
        print(f"  {os.path.basename(fp)}: {frag!r}")
