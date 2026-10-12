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
> database or a complete set of grants: see **[Why these four](#why-these-four)** and
> **[What is not here](#what-is-not-here)**.

## Why these four

A format is the recipe for one report layout, and it is written at one of three **levels** — a row
of a spreadsheet, a block of YAML, or Python — that sum rather than exclude one another. These four
were chosen because between them they use all three, and because they cover every one of the seven
data the output schema carries.

| Format | Document | Why it is here |
|---|---|---|
| `AMUNDI-IT24` | an Italian annual report | the format with **no Python at all**: twenty-six sub-funds, and every one of its five page classes is configuration |
| `AMUNDI-EN24` | a Luxembourg annual report | the largest: eighty-seven sub-funds, a statement of net assets printed **across two facing pages**, and an author's module for what configuration could not reach |
| `DANSKEINVEST-EN24` | a Danish annual report | mergers and renamings read out of prose, and the dash-for-zero convention |
| `BLACKROCK-EN25` | 1 261 pages, Irish, **not supported before this repository** | the worked example: six of the seven data, four of them pure configuration |

## The data, measured

Not a tick per column: the **rows each format's reference output actually carries**, which is what
`make test-slow` compares against. One run per document, four documents.

| Format | holdings | sub-funds | mgmt companies | manager→fund | net assets | SFDR article | ESG indicators | merges/renames |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `AMUNDI-EN24` | 608 | 87 | 15 | 1 218 | 87 | 82 | — | 21 |
| `AMUNDI-IT24` | 111 | 26 | 1 | 26 | 26 | 22 | — | — |
| `BLACKROCK-EN25` | **1 394** | 15 | 1 | 17 | **15** | 4 | **15** | — |
| `DANSKEINVEST-EN24` | 215 | 29 | 10 | 261 | — | 28 | — | 1 |
| **total** | **2 328** | **157** | **27** | **1 522** | **128** | **136** | **15** | **22** |

A dash is **not** a gap in the engine. It is one of three things, and which one is written down:

- the document does not carry the datum — `DANSKEINVEST-EN24` has no statement of net assets to
  read, and `BLACKROCK-EN25` states its mergers in a shape no reader covers yet (below);
  `BLACKROCK-EN25` reads **15** statements where it has 15 sub-funds in `funds.csv` and 23 in the
  report: the eight missing are sub-funds no holding of interest touches;
- the datum is there and concerns no sub-fund the input database points at. Every table here is
  filtered against a **target list** of companies, and the figures above are the list in
  `tests/input_db/` — seventy-six companies. A different list gives different figures from the same
  documents, which is the point of the separation;
- four of `BLACKROCK-EN25`'s sub-funds have an SFDR annex and nineteen do not, because only an
  Article 8 or 9 product has one. Four is the right answer, not a shortfall.

### What `BLACKROCK-EN25` left out, and why

Both are written down rather than left to be noticed:

- **the mergers and renamings.** Page 5 states three renamings, measured, in the shape *a dated
  lead-in sentence, then one bullet per event with the verb inside the bullet*. Of the engine's two
  readers one wants the date inside each event's own sentence and the other wants the kind of event
  in the heading, so neither fits; covering it is a change to a reader, for one format and three
  rows, and it was not made;
- **four holdings of a company on the target list**, held as *cash equivalents* in the per-sub-fund
  summary rather than in the schedule of investments, where the amount does not sit beside the
  name. The engine skips those four rows and says so in `out/.log.csv` — which is the only place
  the fact is recorded, and the reason the warning was left in place rather than configured away.

### The amounts are as the document prints them

`BLACKROCK-EN25` prints its figures in thousands (`Fair value EUR '000`), and the engine publishes
the number it read: `investments.csv` carries `2863.0` where the page says `2,863`. The unit stays
in the document. This is true of the collection generally and not of this format in particular, and
it is a deliberate limit rather than an oversight — scaling a figure means writing the scale
somewhere, and a written scale is a value nobody re-reads against the page.

```sh
make init                             # first time: point git at .githooks/
make test                             # the per-page suite — the development loop
make ci-fast                          # what the commit hook runs: lint, tests, report, verdict
make help                             # every target, with a line each
```

**Two command surfaces, one vocabulary.** `make` changes *this* repository — it writes the
measurements, refreshes the committed reports, and rewrites the manifest when it is entitled to.
`freeports-dev` and `freeports-validate` answer questions *about* a repository, including one that
is not yours, and write only where you point them:

```sh
freeports-dev make-tests <FORMAT>              # write a format's reference output
freeports-dev inspect-page -f <FORMAT> -p <N>  # look at a page while writing a format
freeports-dev test --repo <path> --all         # somebody else's repository, both suites
freeports-dev ci-report --repo <path> -f json  # their figures, as a model to query
freeports-validate check-grants                # verify every claim made in validation/
```

Every target is one of those commands with `--repo` pointed here, so the two never disagree:
`make test-fast` is `freeports-dev test --fast`, `make ci-check` is `freeports-dev ci-check`, and
`make check-grants` is `freeports-validate check-grants`. On Windows the targets are typed
`make.bat <target>` from `cmd` or PowerShell — a shim that starts a POSIX shell and calls the same
`Makefile`.

## What this repository has been vouched for

**142 files, by one contributor, under one methodology.** A grant is a signed statement that a
named contributor checked a named file under a named methodology, and the hash it records is of
that file's bytes: if a granted file changes, `check-grants` says so until somebody re-grants it
deliberately.

What is covered here is what the *basic check* methodology declares it covers — the reference
outputs of the four test suites (`tests/formats/**/out/*.csv` and `*.yaml`) and their per-page
fixtures (`tests/formats/**/pages/**`) — and vouching for one of those means the run that produced
it completed, its columns are the expected ones, and **a person read the values looking for obvious
nonsense**. It is deliberately a *weak* certification: it says the program works on this data and
the output looks reasonable, not that the data is right.

The three commands that produced it, and the one that checks it:

```sh
freeports-validate create-document        # once per contributor
freeports-validate grant <files...> with "basic check"
freeports-validate sign-document          # the only step that needs the key
freeports-validate check-grants           # needs no key at all
```

A page that cannot be reached is reported as **inconclusive**, never as a match or a mismatch:
`check-grants` ends such a run with exit status **3**, *not checked*, because unmeasured is not a
pass.

<!-- freeports-validate:begin -->
<!-- Written by `freeports-validate report`. Anything between the markers is replaced. -->

142 grants by 1 contributor under 1 methodology; coverage 136/136 (100%); check-grants: failing

*Generated by `freeports-validate report`, and demonstrative: it shows what this repository's validation documents claim as of one run, not that the data is correct. To be sure of any line, run `freeports-validate check-grants` yourself.* [What these claims are worth: the general methodology](https://docs.freeports.org/en/stable/validation/general_methodology.html).

| Methodology | Grants | Coverage | Adopted by |
| --- | ---: | ---: | --- |
| [basic check](https://docs.freeports.org/en/stable/_sources/validation/methodologies/basic_check.rst.txt) | 142 | 136/136 (100%) | Oreste Sciacqualegni |

<!-- freeports-validate:end -->

### The same claims, six other ways

Each page below is one of the three lookup subcommands written down for the whole repository at
once, rather than for the one file, contributor or methodology you would name on the command line.

| Page | The same view as |
|---|---|
| [By file — who vouched for it](validation/report/file-contributor.md) | `freeports-validate who-grants <file>` |
| [By file — under which methodology](validation/report/file-methodology.md) | `freeports-validate who-grants -m <file>` |
| [By contributor — the methodologies they used](validation/report/contributor-methodology.md) | `freeports-validate granted-by <contributor>` |
| [By contributor — the files they vouched for](validation/report/contributor-file.md) | `freeports-validate granted-by -f <contributor>` |
| [By methodology — the files it covers](validation/report/methodology-file.md) | `freeports-validate granted-with <methodology>` |
| [By methodology — who adopted it](validation/report/methodology-contributor.md) | `freeports-validate granted-with -c <methodology>` |

## How `BLACKROCK-EN25` was written

A 1 261-page report that nothing in the project could read, to six data and a passing suite. The
order is the one the project recommends and it is not arbitrary: **start from the holdings**,
because they are the datum every later step is filtered against, and widen the scope one step at a
time — one page, then the whole document, freezing the result as a test at each widening.

```sh
freeports-dev find-text -f BLACKROCK-EN25 --regex 'SCHEDULE OF INVESTMENTS' --pages-only
freeports-dev inspect-page -f BLACKROCK-EN25 -p 106 -m lines --order x --columns 2
freeports-dev inspect-page -f BLACKROCK-EN25 -p 106 -t investments -m pdf_blks
freeports-dev inspect-document -f BLACKROCK-EN25
freeports-dev make-tests -f BLACKROCK-EN25 -t investments -p 106
```

What it took, datum by datum:

| Datum | Level | What it came to |
|---|---|---|
| holdings | `structured` | **two rows of CSV**: one of nine cells, one of five |
| management company | `structured` | one row, **two** cells filled of eleven |
| statement of net assets | `structured` | one row, sixteen cells of twenty-two |
| SFDR article | `semistructured` | a YAML block of eight lines, because one of the four annexes words a template heading with its own capitals and the structured level deliberately does not let a row override an anchor |
| investment managers | `semistructured` + Python | the table of sub-delegations needs its cells on a grid, and nothing above produces one without also claiming a sub-fund name the page has not got |
| ESG indicators | `semistructured` + Python | the reader pairs a figure with the name of its own row, and pairing is the one thing no level above does |

Three measurements decided the shape of all of it, and each is written beside the configuration it
produced:

1. **the classification anchor read on one page covered 870 of 983.** `Currency Holdings` is one
   text object on most pages and **two** on a hundred and thirteen of them, same table and same
   columns. `Investment` as a column heading covers all 983;
2. **ordinate bands read on one page of the balance sheet gave three sub-funds of twenty-three.**
   A sub-fund's title takes one to four lines according to its length and drags the whole block of
   column headings down with it. Replaced by anchors on the lines themselves — *as far down as the
   row that says `'000`, minus the two rows of years* — the same configuration reads 23 of 23, and
   the accounting equation closes on every one;
3. **the SFDR article is read from the tick in the box, not from the title of the annex.** Three
   of the four say Article 8 and one says Article 9, and all four were read from the box — which is
   also how a missing tick became a one-character addition to the engine rather than a guess.

The reasoning behind each step, and the traps it avoids, is the format author's section of the
engine's own documentation: `analysis_finance_reports/docs/source/guides/formats/`.

## What is not here

- **twenty-two of the twenty-six formats**, and the documents that go with them. The repository
  that maintains them is `analysis_finance_reports_formats`;
- **a production input database.** `tests/input_db/` is the seventy-six-company `TEST` list that
  `freeports-dev setup-input-db` installs, which is what makes the figures above reproducible and
  also what makes them a demonstration rather than a finding;
- **the engine.** Formats are plugins; the extraction code, the three levels and every algorithm
  named in `content/` live in `analysis_finance_reports`;
- **a lint-clean `content/`.** One `ruff` finding survives, in a template copied verbatim from the
  repository that maintains it. The copy is kept byte-identical on purpose — the guarantee this
  repository offers for its three inherited formats is that they behave *exactly* as they do at
  home, and that is checkable with `diff` where a tidied import is not.

## What a commit here has to clear

`ci.yaml` at the root says how this repository is gated, and it is the only file to open to answer
that. `freeports-dev branch-class` says which class the branch you are on is in and the rule that
put it there — run it first whenever the hook does something you did not expect.

| Branch class | What happens |
|---|---|
| `prod` — `main`, `release/*` | a missed threshold, a failing suite, or a `validation_sha256` that moved without `info.version` **refuses the commit** |
| `dev` — the default | everything is measured and reported; nothing is refused |
| `off` — `experimental`, `wip/*` | the hook does nothing at all |

The hook runs one thing — `make pre-commit` on a `dev` branch, `make ci-full` on a `prod` one — so
what the gate consists of is decided in the `Makefile` and can grow without the hook being touched.
On a dev branch that is the linter, the per-page suite, three measurements, both report renderings
and the verdict; on a prod branch it is both suites and the grants re-resolved over the network as
well. Each is a target you can run on its own:

```sh
make test-fast        # the per-page suite, recorded as formats.single_page
make test-slow        # the whole-document suite, recorded as formats.integration
make coverage         # how many documents are tested, and how
make lint             # ruff's findings on content/, and the score out of ten
make doc-coverage     # public objects carrying a docstring
make ci-check         # the verdict table, and the exit status
```

**Only `make ci-check` and `make fingerprint` can refuse a commit.** Everything else measures and
records; the verdict reads what they wrote, together with `ci.yaml` and the class of the branch,
and is the one step that knows whether this branch enforces or reports.

`freeports-dev coverage` counts **documents**, not formats: a format with one `report.pdf` is one
document, and a format with several subdirectories is one document each. A document counts for
*integration* when it has an `out/` — that is, when a whole-document test exists at all — and for
*single page* when at least one of its pages carries all three of `<n>-pdf_blks.json`,
`<n>-txt_blks.json` and `<n>-results.json`. The two are kept apart because a repository can be
strong in one and weak in the other, and one number would hide it.

Seed a threshold in `ci.yaml` only at a figure you have measured. One set above the baseline
refuses the first commit made under it, and then it is the gate somebody switches off rather than
the code somebody fixes.

### What the last run found

<!-- freeports-dev:begin -->
<!-- Written by `freeports-dev ci-report`. Anything between the markers is replaced. -->

6 metrics, 6 gated: 6 pass; branch main → prod (thresholds are enforced); ci-check: failing

*Generated by `freeports-dev ci-report`, and demonstrative: it shows what one run measured on one machine, not that the software is correct. To be sure of any line, re-run the command that measures it and `freeports-dev ci-check` yourself.* [What is gated here, and what refuses: the commit gate](https://docs.freeports.org/en/latest/guides/devops/the-gate.html).

| Metric | Measured | Minimum | Verdict |
| --- | ---: | ---: | --- |
| `tests.formats.integration` | 100.0 % | 100.0 % | pass |
| `tests.formats.single_page` | 100.0 % | 100.0 % | pass |
| `docs.python` | 91.2 % | 91.0 % | pass |
| `lint.python` | 9.992 | 9.900 | pass |
| `grants.coverage` | 100.0 % | 100.0 % | pass |
| `grants.keys_online` | 100.0 % | 100.0 % | pass |

formats.integration — did not pass. Run `make test-slow`.

*pass* — measured, current, and at or above the minimum this repository asks for.

<!-- freeports-dev:end -->

The same figures are written out two more ways beside it: [what each threshold is a threshold
*of*](ci/report/thresholds.md), and [where each figure comes from](ci/report/breakdown.md). There is
an [HTML page](ci/report/index.html) carrying all three as tabs, and `freeports-dev ci-report
--format json` is the model every one of them is drawn from.

### The fingerprint, and the version

`info.validation_sha256` in `package.yaml` is the hash of the hashes of **every file a grant
covers**, in `LC_ALL=C` order, with the path inside each hashed line — so moving a file counts as
much as editing it. You can check it by hand:

```sh
printf '%s\n' <the granted paths> | LC_ALL=C sort | xargs sha256sum | sha256sum
```

When it moves, `info.version` must move too. Which component is your choice: the change may be a
correction or a whole new format, and only you know which. On a `dev` branch the hook warns and
does **not** write the new fingerprint — writing it would leave the manifest claiming that version
X covers content Y, which is a false statement, and the point of the field is that it is not one.

### Keeping all of it current

The commit hook refreshes both reports and adds what it rewrote to the commit being made, so the
published figures and the change that moved them arrive together. Two targets do the same by hand:

```sh
make ci-report          # the badges, the block above, the two pages and the HTML
make validation-report  # the grant badges, its block, and the six lookup pages
make validation         # that, plus check-grants and check-keys — the whole grant picture
```

Each is **one walk of the repository rendered many times**, never one walk per artefact: the grant
report resolves every methodology page from the configured sources, and doing that once per page
would fetch each of them nine times over for an answer that cannot have changed in between.

Neither report can refuse a commit, on any branch. A methodology page that could not be resolved
leaves the figures as they were and says so — a repository whose documentation server is down still
has to be committable, and a report rewritten to say "coverage --, check-grants failing" would be a
claim about somebody's web server written into tracked files. What may refuse is a *threshold*, and
that is `make ci-check`'s decision on a `prod` branch.
