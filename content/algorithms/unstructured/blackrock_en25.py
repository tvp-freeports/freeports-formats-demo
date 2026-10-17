"""The two readings of BLACKROCK-EN25 that configuration cannot do.

Four of this format's six data are configuration: the holdings, the management company and the
statement of net assets are rows of the ``structured`` tables, and the SFDR annex is a
``semistructured`` block. This module exists for the other two, and the reasons are worth stating,
because "it needed Python" is the sentence a format author should always be able to replace with
one that says *what* needed it.

Why the table of sub-delegations is not a row
---------------------------------------------
Note 16 of the financial statements (p92) is the only page of the report that ties a delegate to a
sub-fund. It writes it as a table — ``Fund name`` beside ``Sub-Investment Managers`` — and the
``table`` reader of the engine's ``inv_managers`` filter reads exactly that shape, asking only for
its blocks on a grid: ``table-row`` and ``table-col`` in the metadata, which are the keys it
defaults to.

Of the two levels above, only the ``structured`` ``investments`` row produces such a grid, and it
cannot be borrowed here. That row always builds **three** pipes — the grid, the sub-fund's name and
the currency statement — and the last two have nothing to read on a page of notes: their cells are
empty, an empty selection takes every line, and the pipe keeps the first. Note 16 would therefore
publish ``FUND_NAME: "90"`` and ``CURRENCY_STATEMENT: "90"``, the printed page number, as results of
this pipeline. A grid of its own costs fifteen lines and claims nothing it has not read.

The join, which ``Collapse`` would have done
--------------------------------------------
One of the six names is too long for its column and wraps, so ``iShares Emerging Markets Government
Bond Advanced Index Fund `` and ``(IE)`` arrive as two rows of the first column. They are joined
with **nothing** between them, because the generator leaves the space at the end of the first
piece — the same rule, and the same reason, as the engine's own collapse.

A row carrying only a manager is not joined but **continued**: two of the six sub-funds have two
delegates each, and the second sits on a row of its own with the fund column left empty, the way
a table writes a cell spanning two rows. Repeating the fund there is reading the layout, which is
where `R23` puts it — and without it those two sub-funds keep their first delegate and lose their
second, silently: measured, `BlackRock (Singapore) Limited` disappeared from the output of
`iShares Global Aggregate 1-5 Year Bond Index Fund (IE)` altogether.
"""

from freeports.core import PdfBlock, Pipeline
from freeports.utils.pdf_extract import (
    PdfLineSelection,
    get_table_coordinates,
    pdflines_from_pagedict,
)
from freeports.output import FundAssets
from freeports.standard_funcs.deserialize import DeserializerInvestmentStandard, DeserializerFundStandard, DeserializerAssetsStandard
from freeports.utils.deserialize import to_int, to_date_with_en_month
#: The table's body: the ordinary face, between its own header and the sentence that closes it.
#:
#: Both bounds are lines of the page and neither is an ordinate, because the page carries the same
#: face above the table (the list of related parties) and below it (two paragraphs of prose). The
#: left bound is a number and it is measured: the table's columns begin at ``x=32.8`` and the prose
#: at ``x=28.8``, so ``30`` separates them — the only abscissa in this format, and it is here
#: because the sentence that closes the table is the second paragraph, not the first.
_BODY = PdfLineSelection(font="arialmt", font_size=(8.4, 8.6)) & PdfLineSelection.area_from_bounds(
    x0=30.0,
    y0=PdfLineSelection(font="arial-boldmt", font_size=(8.4, 8.6), text="^Fund name$"),
    x1=1e6,
    y1=PdfLineSelection(text="^The Investment Manager will arrange"),
)

#: The block type the ``inv_managers`` filter is pointed at, in ``args/text_filter.yaml``.
BLOCK_TYPE = "DELEGATION_ROW"


def _cells(page):
    """The table's cells, keyed by ``(row, column)``, with every wrapped name reunited."""
    lines = _BODY.select(pdflines_from_pagedict(page))
    cells = {}
    for (row, col), line in zip(get_table_coordinates(lines), lines):
        cells[(row, col)] = cells.get((row, col), "") + line.text

    joined, previous, fund = {}, None, None
    for row in sorted({row for row, _ in cells}):
        columns = sorted(col for r, col in cells if r == row)
        # A row holding nothing but the first column is the tail of the name above it.
        if columns == [0] and previous is not None:
            joined[(previous, 0)] += cells[(row, 0)]
            fund = joined[(previous, 0)]
            continue
        for col in columns:
            joined[(row, col)] = cells[(row, col)]
        # A row holding no name continues the sub-fund of the row above: a cell spanning two rows.
        if 0 in columns:
            fund = cells[(row, 0)]
        elif fund is not None:
            joined[(row, 0)] = fund
        previous = row
    return joined


def delegations(page):
    """One block per cell of note 16's table, on the grid the ``table`` reader walks."""
    return [
        PdfBlock(BLOCK_TYPE, {"table-row": row, "table-col": col}, text)
        for (row, col), text in sorted(_cells(page).items())
    ]


# ----------------------------------------------------------------------------------------------
# The ESG indicators
# ----------------------------------------------------------------------------------------------
# Why the indicators are not a `dated_rows` row either
# ----------------------------------------------------
# The reader is general enough -- it keeps the blocks whose `series` and `column` are the ones
# asked for, takes the block's text as the value and its `indicator` metadata as the name -- but
# nothing in the two levels above produces blocks carrying those three keys. They pair a value
# with the name of its **own row**, and pairing is what this pipe does; the reader then only has
# to say which column it wants, which is `R5`: the most recent, and not last year's.
#
# The table, measured on p1227 and identical on the other three disclosures:
#
#     Sustainability Indicator          Metric              2025     2024     2023
#     Exclusion of issuers with a       % market value      0.00%    0.00%    0.00%
#     JP Morgan ESG ("JESG") Rating     exposure to ...
#     Band of 5
#
# The indicator's name wraps over one to four lines and its **first** line is level with its
# values, so a value's row is the band from its own ordinate to the next value's.

#: The header of the most recent column, which is also what tells this page apart from the other
#: thirty-two of the disclosure section.
_YEAR = PdfLineSelection(font="arial-boldmt", font_size=(8.4, 8.6), text="^2025") & (
    PdfLineSelection.area(395.0, 1.0, 440.0, 1e6)
)

#: The three columns of figures, by the abscissa of each year's own header. Measured: 2025 at
#: 402.4, 2024 at 456.4, 2023 at 510.4, every value of every one of the four disclosures.
_COLUMNS = [(395.0, 440.0), (450.0, 495.0), (504.0, 549.0)]

#: The column of names, which ends where the column of metrics begins — ``x=316.8`` on all four
#: disclosures, and the longest line of a name measured is ``314.8``, so the bound is ``316``.
#: Set at ``312`` it cut two names in the middle (``Exclusion of issuers with an MSCI ESG``), and
#: a truncated name matches nothing later (`R24`): the bound is worth measuring, not guessing.
_NAMES = PdfLineSelection(font="arialmt", font_size=(8.4, 8.6)) & PdfLineSelection.area(
    150.0, 1.0, 316.0, 1e6
)

#: The distance at or above which the column of names has stopped being one name. The lines of a
#: name are 10.2 points apart on every page measured, and what follows the table is further than
#: that; one and a half lines sits between the two with margin on either side.
_NAME_GAP = 15.0

#: What closes the table: the next question of the European template, which is set in the heading
#: face. Without a floor the **last** indicator's name runs on into the prose below and comes out
#: as `Exposure to bonds classed as green bondsportfolio.portfolio. ... portfolio.` -- a name no
#: later phase can match, which is `R24` in its quietest form.
_NEXT_QUESTION = PdfLineSelection(font="arial-boldmt", font_size=(8.4, 8.6))


def _value_cells(lines, year_bottom):
    """The figures of the three year columns, by column index counted from the most recent."""
    cells = []
    for index, (x0, x1) in enumerate(_COLUMNS):
        band = PdfLineSelection(font="arialmt", font_size=(8.4, 8.6)) & PdfLineSelection.area(
            x0, year_bottom, x1, 1e6
        )
        cells.extend((index, line) for line in band.select(lines))
    return cells


def indicators(page):
    """One block per figure, carrying the name of its own row, its column and its series.

    ``series`` is always ``0``: this table has one series, the sub-fund's, where AMUNDI-EN24's has
    the sub-fund's and its benchmark's. Writing the key all the same is what lets the reader stay
    one reader.
    """
    lines = pdflines_from_pagedict(page)
    year = _YEAR.select(lines)
    if not year:
        return []
    bottom = year[0].bbox[3]
    names = sorted(_NAMES.select(lines), key=lambda line: line.bbox[1])
    names = [line for line in names if line.bbox[1] >= bottom]
    # Every line of an indicator's name begins at the column's left edge -- measured 153.7 on all
    # four disclosures -- while the prose that follows the table is indented differently (170.4)
    # and the bullet that opens the next question differently again (155.2). Taking the edge from
    # the page rather than writing it down keeps this a rule and not a coordinate.
    if names:
        edge = min(line.bbox[0] for line in names)
        names = [line for line in names if abs(line.bbox[0] - edge) <= 1.0]

    cells = _value_cells(lines, bottom)
    if not cells:
        return []
    firsts = sorted({round(line.bbox[1], 1) for _, line in cells})
    closing = [
        line.bbox[1] for line in _NEXT_QUESTION.select(lines) if line.bbox[1] > firsts[-1]
    ]
    table_bottom = min(closing) if closing else 1e6

    blocks = []
    for index, line in cells:
        top = round(line.bbox[1], 1)
        following = [y for y in firsts if y > top]
        floor = following[0] if following else table_bottom
        pieces, previous = [], None
        for candidate in names:
            y0 = candidate.bbox[1]
            if y0 < top - 0.5 or y0 >= floor - 0.5:
                continue
            # A gap wider than a line and a half is not a wrap: it is the prose under the table.
            if previous is not None and y0 - previous >= _NAME_GAP:
                break
            pieces.append(candidate.text)
            previous = y0
        name = "".join(pieces)
        if not name.strip():
            continue
        blocks.append(
            PdfBlock(
                "ESG_FIGURE",
                {"indicator": name.strip(), "series": 0, "column": index},
                line.text,
            )
        )
    return blocks


#: The filters and the deserializers are configuration: see ``args/text_filter.yaml``, and the
#: ``labelled_value`` and ``fund`` pipes of the same pipelines. The three levels sum by pipeline
#: name, so this module supplies a ``pdf_extract`` alone for each of its two.
d=DeserializerInvestmentStandard()
def deserialize(txt_blk):
    i=d(txt_blk)
    if i is not None:
        i.market_value = i.market_value * 1000
    return i


da=DeserializerAssetsStandard(to_int,date_converter=to_date_with_en_month)
def deserialize_assets(txt_blk):
    a=da(txt_blk)
    if a is not None:
        tot_assets = a.tot_assets * 1000
        net_assets = a.net_assets * 1000
        liabilities = a.liabilities * 1000
        return FundAssets(
            fund=a.fund,
            date=a.date,
            tot_assets=tot_assets,
            liabilities=liabilities,
            net_assets=net_assets,
            currency=a.currency
        )


pipelines = {
    "investments": Pipeline(deserialize=(deserialize,DeserializerFundStandard())),
    # The statement's extraction and filter are the structured row in `fund_assets/args.csv`; its
    # partial-pipes row leaves the deserializer to this module, which reads the '000 amounts.
    "fund_assets": Pipeline(deserialize=deserialize_assets),
    # "inv_managers": Pipeline(pdf_extract=delegations),
    "esg_indicators": Pipeline(pdf_extract=indicators),
}
