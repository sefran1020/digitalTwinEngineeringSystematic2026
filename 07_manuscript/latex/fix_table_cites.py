#!/usr/bin/env python3
# Convert the author-year text in the Table 1 / Table 2 "Study" cells into
# IEEE numeric citations: "Surname et al. (year)" -> "Surname et al. [@citekey]"
# (pandoc renders [@key] as the numeric [x]). Operates on the source markdown.
import io
p = '../sources_md/03_results.md'
s = open(p, encoding='utf-8').read()
repl = {
    'Kwateng et al. (2026)': 'Kwateng et al. [@kwateng_enhancing_2026]',
    'Lu et al. (2025)': 'Lu et al. [@lu_digital_2025]',
    'Lin et al. (2025)': 'Lin et al. [@lin_visfactory_2025]',
    'Tarng et al. (2024)': 'Tarng et al. [@tarng_application_2024]',
    'Wang et al. (2025)': 'Wang et al. [@wang_innovative_2025]',
    'Khan et al. (2026)': 'Khan et al. [@khan_teaching_2026]',
    'Li (2025)': 'Li [@li_exploration_2025]',
    'Liljaniemi et al. (2025)': 'Liljaniemi et al. [@liljaniemi_enhancing_2025]',
    'Ning et al. (2024)': 'Ning et al. [@ning_exploration_2024]',
    'Ortiz et al. (2025)': 'Ortiz et al. [@ortiz_digital_2025]',
    'Park et al. (2026)': 'Park et al. [@park_ar_2026]',
    'Álvarez Ariza et al. (2026)': 'Álvarez Ariza et al. [@alvarez_ariza_investigating_2026]',
    'García et al. (2026)': 'García et al. [@garcia_digital_2026]',
    'Speicher et al. (2026)': 'Speicher et al. [@speicher_digital_2026]',
    'de Melo Freires et al. (2025)': 'de Melo Freires et al. [@federal_university_of_amazonas_development_2025]',
    'Sakkas et al. (2025)': 'Sakkas et al. [@sakkas_multiplayer_2025]',
    'Terkaj et al. (2024)': 'Terkaj et al. [@terkaj_framework_2024]',
    'Machado et al. (2025)': 'Machado et al. [@machado_automatic_2025]',
}
# replace longest keys first to avoid partial overlaps (e.g. 'Li (2025)')
n = 0
for k in sorted(repl, key=len, reverse=True):
    c = s.count(k)
    s = s.replace(k, repl[k])
    n += c
open(p, 'w', encoding='utf-8').write(s)
print(f'replaced {n} author-year cells with @cite (rendered as [x])')
EOF_CHECK = None
