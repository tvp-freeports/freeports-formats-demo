# freeports-formats-demo

![grants](validation/report/badges/grants-total.svg)
![coverage](validation/report/badges/grants-coverage.svg)
![check-grants](validation/report/badges/check-grants.svg)

![ci](ci/report/badges/ci-status.svg)
![tests.formats.integration](ci/report/badges/tests-formats-integration.svg)
![tests.formats.single_page](ci/report/badges/tests-formats-single_page.svg)
![docs.python](ci/report/badges/docs-python.svg)
![lint.python](ci/report/badges/lint-python.svg)

A **freeports formats repository**: the format definitions under `content/`, the reference outputs
their test suites are checked against under `tests/formats/`, and the signed statements about both
under `validation/`.

> ## This is a demonstration repository
>
> It holds **four** of the twenty-six formats the project maintains, and it exists to be read
> rather than to be run in production. Three of the four were copied, unchanged, from the
> repository that maintains them; the fourth, `BLACKROCK-EN25`, was written here, from an
> unsupported PDF, as the worked example. Nothing here is a complete corpus, a complete input
> database or a complete set of grants: see **[Why these four](#why-these-four)**

## Why these four

A format is the recipe for one report layout, and it is written at one of three **levels** — a row
of a spreadsheet, a block of YAML, or Python — that sum rather than exclude one another. These four
were chosen because between them they use all three, and because they cover every one of the seven
data the output schema carries.
