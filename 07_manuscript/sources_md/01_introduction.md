# Introduction

Laboratory and hands-on instruction occupy a privileged place in engineering
education. The instructional laboratory is not an adjunct to the lecture but a
setting with its own learning objectives—instrumentation, experimentation,
modelling, design, and the disciplined translation of theory into practice—that
the field has articulated explicitly and treated as constitutive of professional
competence [@feisel_role_2005; @lei_teaching_2022; @naukkarinen_supporting_2018].
Yet the physical laboratory is a constrained resource. Time, space, equipment
cost, maintenance, and safety place hard limits on how many students can practise,
how often, and on how current the available apparatus remains relative to the
industrial state of the art [@lei_teaching_2022; @prichetnikov_investigation_2020].
The COVID-19 pandemic sharpened these long-standing constraints, forcing the rapid
migration of practical courses online and exposing how poorly procedural skill
formation tolerates the loss of physical access [@haase_teaching_2022;
@alkhedher_interactive_2021]. In response, virtual, remote and simulation-based
laboratories have proliferated across engineering disciplines—from electrical
measurement, transmission lines and microcontroller programming to chemical
reaction engineering and control systems [@chumchuen_remote_2023;
@andrieu_remote_2021; @panagiotakis_remote_2022; @naukkarinen_supporting_2018;
@lei_teaching_2022].

The displacement of practical work from physical apparatus to its digital
surrogates raises a question that has organised engineering-education research for
two decades: do non-traditional laboratories achieve the same learning outcomes as
hands-on work? Comparative reviews have repeatedly found that virtual and remote
laboratories can match hands-on settings on many measured outcomes, with the
relative advantage depending on the outcome and the instructional design rather
than on the medium alone [@ma_handson_2006; @corter_constructing_2007;
@lindsay_effects_2005; @brinson_learning_2015]. That literature is equally
notable, however, for what it says about evidence: Brinson's review of the
empirical research reports that the great majority of studies find "no significant
difference" yet are dominated by weak designs and self-report, and bibliometric
syntheses document rapid growth in publication without commensurate growth in
methodological rigour [@brinson_learning_2015; @heradio_virtual_2016;
@potkonjak_virtual_2016]. A recent review of digital technologies for practical
teaching reaches the same double conclusion: these tools improve access,
flexibility and engagement, but the evidence that they replace the tacit,
procedural learning of the physical workshop remains limited
[@maladzhi_digital_2025]. The digital twin enters engineering education as the
most recent and most technically ambitious member of this lineage, and it inherits
the lineage's unresolved question.

Among these digital approaches, the digital twin (DT) has emerged as a distinct
and more demanding proposition. First articulated by Grieves in the
context of product-lifecycle management [as reported in @liljaniemi_using_2020], a DT is a virtual representation of a physical asset
maintained in correspondence with it through a data connection, such that the
state of one is reflected in the other across the asset's lifecycle
[@de_larmelina_conceptualizing_2026;
@weichbroth_toward_2024]. This definitional core is widely shared, but the term
remains contested. Analysing more than 15,000 publications, @abdelrahman_what_2025 show that no consensus definition exists and that several features often
assumed to be intrinsic—real-time bidirectional data flow, simulation, and
embedded artificial intelligence (AI)—are not yet mature even in industrial
practice. The literature therefore distinguishes degrees of integration, from a
static digital model, through a digital shadow with one-way physical-to-virtual
updating, to a fully bidirectional digital twin capable of closed-loop control
[Kritzinger et al., 2018, as cited in @liljaniemi_using_2020;
@abdelrahman_what_2025; @bokhtiar_al_zami_digital_2025]. This gradation matters pedagogically, because it
separates a DT from a conventional simulation or an immersive scene: what is
labelled a "twin" may range from a high-fidelity but disconnected model to an
instrumented, synchronised cyber-physical system [@kabir_digital_2025;
@lee_digital_2025]. Establishing this maturity—rather than assuming it from the
label—is consequently a prerequisite for any serious account of what educational
DTs are and what they can teach.

The motivation to bring DTs into the classroom is inseparable from the competence
demands of Industry 4.0 and the emerging, human-centred Industry 5.0
[@saini_industry_2026; @kabir_digital_2025]. Employers and accreditation bodies
increasingly expect graduates to be fluent in the industrial Internet of Things,
automation and data analytics and, with the Industry 5.0 turn, in human–machine
collaboration and sustainability-oriented practice [@sell_international_2025;
@azofeifa_top_2025; @dautaj_importance_2026]. Several studies document a
persistent mismatch between graduate competencies and labour-market expectations
[@denissova_factors_2026], while survey evidence shows that engineering faculty
themselves often feel insufficiently prepared, and insufficiently equipped, to
teach these technologies [@cuperman_academic_2026]. DTs are proposed in this
context precisely because they can expose students to the same
cyber-physical systems they will meet in industry, and align that exposure
with competence frameworks articulated for Industry 5.0 work and learning
factories [@zare_engineering_2026; @nitu_engineering_2026; @al-jumeily_implementing_2026].

DTs rarely arrive alone. They are typically embedded within, or compared against,
a broader wave of immersive and virtual technologies—virtual, augmented and mixed
reality, the metaverse, and serious games—whose use in engineering and higher
education has expanded rapidly and been mapped by numerous reviews
[@lampropoulos_virtual_2025; @jin_extended_2026; @fan_impacts_2025;
@espinoza_virtual_2025; @llanos-ruiz_virtual_2025]. The evidence on these
technologies is, however, mixed. Many studies report gains in motivation,
engagement and the understanding of complex concepts, but controlled comparisons
sometimes find no significant difference in measured learning outcomes relative
to traditional methods, underscoring that pedagogical design, not technology
alone, drives the effect [@giussani_study_2025; @yindeemak_emerging_2026;
@lainidis_systematic_2026]. Within this landscape, DT-based education has
grown from early demonstrations in construction and mechanical engineering
[@sepasgozar_digital_2020; @liljaniemi_using_2020; @treffinger_investigations_2022]
into a varied corpus spanning manufacturing, robotics, electrical and chemical
engineering, aviation maintenance and even university mathematics
[@khan_teaching_2026; @kwateng_enhancing_2026; @hunpinyo_isa95_2026;
@xiang_research_2025; @bolanos_design_2026; @lee_digital_2023], often coupled with
project-based and experiential pedagogies and framed as preparation for
Industry 4.0/5.0 practice [@zhang_effectiveness_2024; @ruppert_demonstration_2023;
@terkaj_virtual_2024; @alvarez_ariza_investigating_2026].

This momentum has produced several reviews, but they leave the lineage's
central question—whether the technology achieves the learning outcomes of
hands-on work, and on what quality of evidence—largely unanswered for DTs.
Existing syntheses tend either to survey immersive technologies broadly,
with DTs as one instance among many [@lampropoulos_virtual_2025;
@tokhayeva_virtualisation_2026; @jiang_state_2026], or to concentrate on a single
application niche, such as DT-coupled virtual learning environments for smart
manufacturing [@kumar_karanam_systematic_2025]. Across this body of work three
gaps recur. First, the techno-pedagogical architecture of educational DTs—their
deployment environment, communication protocols and synchronisation, and degree
of bidirectional integration—is seldom characterised jointly with the pedagogy it
is meant to serve, so that technical and instructional accounts run in parallel
rather than being read together. Second, and continuing the evidence-quality
concern that comparative laboratory reviews have raised since Brinson
[@brinson_learning_2015; @heradio_virtual_2016], reviews rarely appraise the
methodological quality of the underlying learning evidence; effectiveness claims
are aggregated without weighting how rigorously each was established, even though
the immersive-technology literature itself warns that headline gains often rest
on small, uncontrolled designs [@fan_impacts_2025; @giussani_study_2025].
Third, no synthesis has examined how technical, pedagogical and evaluative
choices co-vary across the field—whether, for example, the most technically
capable twins are also the most rigorously evaluated, or whether ambitious
competence claims are matched by demonstrated outcomes. Addressing these gaps
calls for a synthesis that treats architecture, pedagogy, evidence quality and
institutional context as linked dimensions rather than as separate narratives,
and that reads them through an explicit instructional lens rather than as a
technical inventory.

Accordingly, this systematic review synthesises 65 primary studies on the use of
digital twins in engineering and higher education, published between 2018 and
2026. The corpus was coded through an inductive thematic analysis organised into
eight themes, and the synthesis is then read through the alignment lens set out in
the next section. On that basis the review pursues four objectives, each posed as
a question about the instructional system rather than the artefact: (O1) to
characterise the technological architectures and deployment environments of
educational DTs—their enabling components, synchronisation and convergence with
AI—and the instructional affordances these provide; (O2) to describe the
pedagogical designs adopted and the Industry 4.0/5.0 competencies they target, and
to ask whether that pedagogy engages students constructively and aligns
competencies to the twin; (O3) to appraise the empirical evidence for learning
outcomes—at what level of evaluation, and with what methodological rigour, it
rests; and (O4) to assess the institutional benefits claimed for DTs and the
barriers to their adoption, and whether those claims are aligned with demonstrated
outcomes. Beyond profiling each dimension separately, the review analyses how
these dimensions co-occur and relate, so that the maturity of the technology can
be read against the rigour of its evaluation and the breadth of competence claims
against the weight of demonstrated learning. By coupling a structured description
of what is being built with a critical appraisal of what has actually been shown,
the review aims to give engineering educators, researchers and institutions an
evidence-weighted map of the field and a foundation for the research agenda
developed in the sections that follow.

The significance of this work for engineering education research and practice lies
in its appraisal stance. Rather than cataloguing digital-twin applications, the
review weighs the *quality* of the evidence behind them and asks how technical,
pedagogical and evaluative choices co-vary, reading the field as an instructional
system through the alignment lens developed in the next section rather than as a
catalogue of technology. The intent is to give researchers an evidence-weighted
basis for identifying where confirmatory, transfer-oriented work is most needed,
and to give educators and institutions a more cautious basis for adopting digital
twins—pairing them with explicit pedagogy, aligned assessment, and instrumented
cost, sustainability and accessibility claims—than a technology-led reading would
support. What the synthesis shows about the balance between technical maturity and
evaluative rigour, and what follows from it, is developed in the Results and
Discussion.
