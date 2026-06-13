# Discussion

This review set out to characterise educational digital twins (DTs) across four
objectives and, crucially, to examine how their technical, pedagogical and
evaluative dimensions travel together. The synthesis of 65 studies yields a
consistent but sobering picture: the field reliably demonstrates feasibility and
engagement, is disciplinarily broad, and is shifting toward more capable,
bidirectional and occasionally AI-augmented twins, yet its evidence rests on a
small minority of methodologically strong studies. Interpreting this pattern, not
the headline enthusiasm, is the purpose here.

The most consequential finding is structural rather than aggregate: across the
corpus, the maturity of the twin is largely decoupled from the rigour with which
it is evaluated. The studies that describe how complete a twin is—its
bidirectional synchronisation, its layered architecture—are seldom the studies
that test whether it improves learning, and the capability-by-evidence frontier
is almost empty. Read through constructive alignment [@biggs_enhancing_1996;
@biggs_teaching_2011], this is a systemic misalignment: the field has invested
heavily in one element of the instructional system—the learning activity, the
twin itself—while the intended learning outcomes and the assessment that would
evidence them remain comparatively underspecified. The pattern is, in this sense,
a familiar one in engineering and STEM education, where the adoption of a new
instructional technology routinely outpaces the rigorous evaluation of its effect
[@henderson_facilitating_2011], and it reproduces for digital twins the very
situation that comparative reviews of virtual and remote laboratories have
documented for two decades: enthusiastic deployment, a prevailing "no significant
difference" verdict, and a thin and methodologically weak evidence base beneath it
[@brinson_learning_2015; @heradio_virtual_2016]. This decoupling also mirrors a
tension documented across the wider DT
literature, where academic sophistication consistently outpaces validated
deployment and workforce readiness [@chen_ai-enhanced_2025]. It is compounded by
terminological inflation: the prevalence of self-described "complete" twins,
rarely accompanied by latency or synchronisation measurements, suggests that the
label is applied more loosely than the established physical-to-virtual and
virtual-to-physical data-flow criteria would warrant [@thelen_comprehensive_2022], and
that the field still lacks shared criteria for evaluating what a twin actually
does [@liu_cognitive_2025]. Claims of Industry 4.0/5.0 competence and institutional
benefit similarly outpace demonstrated outcomes, and the asymmetry between
benefit-only and barrier-only studies counsels caution in reading the field's
optimism at face value.

One alternative reading of the decoupling deserves stating, because it tempers a
purely critical interpretation. The separation between capable-but-unevaluated and
evaluated-but-simple twins partly tracks a division of publication labour: in our
corpus, architecture-heavy work appears disproportionately in conference and
engineering venues, whereas the studies that mount controlled evaluations tend to
be journal articles, and conference papers score markedly lower on the
evidence-quality composite than journal articles. Part of what looks like a
within-study failure to evaluate may therefore reflect where each kind of
contribution is published. This does not dissolve the problem—the field as a whole
still lacks studies that are both technically complete and rigorously
evaluated—but it locates it at the level of the field's reporting ecosystem rather
than of individual authors' competence.

Three exploratory analyses sharpen this reading. The thematic co-occurrence
structure (Figure 6) shows a field organised around a pedagogy–competencies–
evidence core—competencies and pedagogy co-occur in 34 studies and pedagogy and
evidence in 31—while the AI dimension stays peripheral, never co-occurring with
another theme in more than eight studies; the DT–AI convergence prominent in the
industrial literature [@chen_ai-enhanced_2025; @liu_cognitive_2025] thus remains marginal
and largely unvalidated in education. The
attribute-association network (Figure 8) resolves the studies into three loosely
connected communities—technical capability, evaluation rigour and curricular
design—bridged between the technical and curricular groups mainly by a *negative*
association, whereby courses labelled "active learning" tend not to employ the
most capable bidirectional twins. The research-frontier gap map (Figure 9)
localises the decoupling: of 35 empirical studies, eighteen fall in the lowest-capability
columns and only one occupies the high-capability, strong-evidence cell, while the
multivariate embedding (Figure 11) recovers a valid topological structure whose
dominant axis separates empirical from non-empirical work. Tellingly, effect-size
reporting is flat across design types even as twin maturity rises over time
(Figure 7), so weak quantification is a field-wide habit, not an artefact
of the weakest designs.

These patterns demand interpretive caution. They derive from 65 studies spread
across many sparsely populated cells; the association estimates carry wide
bootstrap confidence intervals, several compatible with no effect—the apparent
link between immersive laboratories and sustainability quantification, for
instance, rests on only two studies—and the embedding accounts for only a modest
share of inertia. They are therefore best read as a map of hypotheses for
confirmatory study, not as established relationships. That such an exploratory
layer is necessary is itself diagnostic of how little well-reported empirical work
the field has produced.

These observations extend, rather than echo, prior syntheses of DTs in education.
Earlier bibliometric work mapped the field's rapid growth and flagged unresolved
questions around teacher competence and governance, but did not weigh the quality
of the underlying learning evidence [@chamorro-atalaya_use_2024];
domain-specific reviews reached a "strong consensus" on DT effectiveness for
training while themselves noting the fragmented, largely conceptual nature of the
literature [@omrany_digital_2026]; and materials-science mapping documents
exponential output without appraising educational outcomes at all
[@vergara_decade_2025]. By coupling a structured description of architecture and
pedagogy with an explicit, sensitivity-tested quality appraisal and a relational
analysis, the present review adds the dimension these accounts lack: not how much
is published, but how well what is claimed has been shown.

The few strong studies in our corpus report substantial gains, of the order of
Cohen's d ≈ 0.9–1.25. These sit at, or above, the upper bound of
meta-analytic estimates for comparable immersive interventions—knowledge-
acquisition effects around a standardised mean difference of 0.33–0.48 in
virtual- and augmented-reality simulation [@li_effects_2026;
@almekkawi_effectiveness_2026], and collaborative- or mobile-VR effects near Hedges'
g 0.47–0.50 [@chen_effects_2026; @widowati_meta-analysis_2025]. This positioning warrants
restraint. Such meta-analyses report high heterogeneity and inconsistent effects
across domains; more pointedly, effect sizes in this literature have declined
over time as designs have become
more rigorous—from very large early estimates to small recent ones
[@widowati_meta-analysis_2025]—a trajectory consistent with novelty effects and weak
controls. Our predominantly recent, single-institution, non-randomised studies
are precisely those most exposed to this inflation, reinforcing that the reported
gains are promising but not yet robustly generalisable.

A second under-examined frontier concerns whether learning on a twin persists and
transfers to physical practice—the upper, more consequential levels of
Kirkpatrick's evaluation hierarchy [@kirkpatrick_kirkpatricks_2016]. The corpus
sits overwhelmingly at the lower levels: reactions and immediate post-tests
dominate, whereas to our reading only one study measured learning retention at a
specified multi-month follow-up (three and six months) [@lin_visfactory_2025], and
none measured transfer to subsequent physical-laboratory or workplace performance.
The broader evidence offers little reassurance: in a review of 64 VR studies, only
two examined transfer at all [@zhong_virtual_2026]. Transfer cannot be assumed from immersion or visual
fidelity; it depends on functional rather than merely perceptual correspondence
[@harris_framework_2020], and inadequate technical fidelity can even produce
negative transfer [@kim_effect_2026]. The corpus's habit of asserting twin
"completeness" without synchronisation or fidelity metrics is therefore not a
minor reporting gap but a direct threat to the ecological-validity claims on which
much of the pedagogical case rests.

Several implications follow. For curriculum design, DTs should be paired with an
intentional, named pedagogy and aligned assessment rather than deployed as
active-learning settings whose instructional model is left implicit. Concretely,
future implementations should move beyond generic "active experimentation" and
anchor their designs in explicit learning theory: constructivist and
social-constructivist principles for knowledge building, Biggs' constructive
alignment to lock intended competencies, twin-based activities and assessment into
a single coherent system [@biggs_enhancing_1996], and—where the goal is learner
self-direction in open-ended, capability-oriented tasks—student-agency models such
as heutagogy [@blaschke_heutagogy_2012]. One design in particular is conspicuously
under-exploited: having students *construct* the twin rather than merely operate a
ready-made one. In ICAP terms this is the apex of cognitive engagement
[@chi_icap_2014], and in constructionist terms it makes the learner the builder of
the model they are meant to understand; yet our corpus documents it only once,
even though the learning-factory tradition it most naturally belongs to is already
present in the field. The negative technical–curricular bridge
in the attribute network suggests engineering ambition and pedagogical design are
currently advancing on parallel tracks; naming and theorising the pedagogy is what
would allow the instructional design to keep pace with the sophistication of the
twin. For
researchers, the priority is methodological, and it is the one the
engineering-education research community has urged for two decades: holding studies
of instructional innovation to the standards of rigorous educational research
[@streveler_conducting_2006]. Concretely, this means
pre-registered comparators, reported effect sizes, and explicit measurement of
retention and transfer, supported by designs—including rigorous single-case and
quasi-experimental approaches—suited to authentic laboratory settings
[@dayo_evaluating_2024], with the reporting transparency that educational-technology
research is repeatedly found to lack [@demir_analyzing_2025]. For institutions,
accessibility and sustainability claims need instrumentation rather than
assertion, particularly where digital-divide constraints shape who benefits
[@eltaiba_benefits_2025]. For tool builders,
interoperability, synchronisation metrics and the validation of AI components
remain prerequisites for credible educational deployment [@chen_ai-enhanced_2025].

Several limitations qualify this synthesis. The corpus is recent and skewed
toward manufacturing and automation and undergraduate cohorts; the
relational analyses rest on small cell counts and are hypothesis-generating rather
than confirmatory; and the evidence-quality composite is necessarily ad hoc,
though its banding proved robust under threshold-sensitivity analysis. Full-text
attrition was substantial: 61 of 126 eligible records could not be retrieved, and
this loss was differential by document type—82% of the unretrieved reports were
conference papers, against 40% of the included corpus. Because conference papers in
our corpus score markedly lower on evidence quality than journal articles, the
missing reports would, if anything, be expected to reinforce rather than soften the
weak-dominated profile we report, so the corpus median is best read as a
conservative bound; nonetheless the gap limits coverage of conference-reported
architectures, and of 2024 in particular. Relatedly, we did not formally assess
publication or reporting bias—no meta-analytic funnel test is meaningful here—but
the asymmetry between benefit-only and barrier-only studies is consistent with
selective reporting and should be read in that light. Finally, coverage of 2026 is
necessarily partial, since the search was run mid-year and early-access records
continue to appear. We
deliberately refrained from meta-analysis, a decision the marked clinical and
methodological heterogeneity of the broader literature retrospectively supports
[@widowati_meta-analysis_2025]. The agenda these gaps define is concrete: populate the
empty capability-by-evidence frontier with pre-registered, multi-institution
quasi-experiments on high-maturity twins; measure transfer and retention rather
than immediate satisfaction; validate AI-augmented and cognitive twins against
declared performance criteria; and standardise the reporting of synchronisation,
cost and sustainability, so that the field's momentum can mature into cumulative,
trustworthy evidence.
