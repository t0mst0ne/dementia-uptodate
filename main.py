#!/usr/bin/env python3
"""Dementia and Alzheimer's Disease weekly source report generator."""

import sys
from pathlib import Path
from rich.console import Console

sys.path.insert(0, str(Path(__file__).parent))
from src import webscraper, crossref_fetcher

console = Console()


def cmd_scrape(days: int = 7):
    import asyncio, json
    console.print("\n[bold]Scraping configured dementia sources...[/bold]")
    results = asyncio.run(webscraper.fetch_all(days=days))
    for source, articles in results.items():
        console.print(f"  [cyan]{source}[/cyan]: {len(articles)} dementia articles found")
        for a in articles[:5]:
            console.print(f"    • {a.title[:80]}")
            if a.url:
                console.print(f"      {a.url}")

    # Save to JSON for reference and report integration
    out = Path(__file__).parent / "data" / "webscrape_cache.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(
        {src: [{"title": a.title, "url": a.url, "source": a.source,
                "published": a.published, "summary": a.summary, "tags": a.tags}
               for a in arts]
         for src, arts in results.items()},
        ensure_ascii=False, indent=2
    ))
    console.print(f"[green]✓ Cached → {out}[/green]")
    return results


def cmd_journals():
    import asyncio, json
    console.print("\n[bold]Fetching journal articles via CrossRef...[/bold]")
    results = asyncio.run(crossref_fetcher.fetch_all())
    for journal, articles in results.items():
        console.print(f"  [cyan]{journal}[/cyan]: {len(articles)} dementia articles")
        for a in articles[:4]:
            has_abs = "✓" if a.abstract_digest else "—"
            console.print(f"    [{has_abs}] {a.title[:75]}")
            console.print(f"        https://doi.org/{a.doi}")

    out = Path(__file__).parent / "data" / "journals_cache.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(
        {j: [{"title": a.title, "doi": a.doi, "journal": a.journal,
              "authors": a.authors, "published": a.published,
              "abstract": a.abstract, "abstract_digest": a.abstract_digest,
              "tags": a.tags, "url": a.url}
             for a in arts]
         for j, arts in results.items()},
        ensure_ascii=False, indent=2
    ))
    console.print(f"[green]✓ Cached → {out}[/green]")
    return results


def cmd_run():
    """Run the weekly public-source collection pipeline."""
    web_results = cmd_scrape()
    journal_results = cmd_journals()

    from datetime import date, datetime
    week = date.today().isocalendar()
    report_path = Path(__file__).parent / "reports" / f"{week[0]}-W{week[1]:02d}.md"
    report_path.parent.mkdir(exist_ok=True)
    report = [
        f"# Dementia & Alzheimer's Disease — Weekly Trend Report {week[0]}-W{week[1]:02d}",
        f"\n> Generated {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} from configured web and journal sources.\n",
        webscraper.format_articles_md(web_results),
        crossref_fetcher.format_articles_md(journal_results),
    ]
    report_path.write_text("\n".join(report))
    console.print(f"[green]✓ Source report written → {report_path}[/green]")


COMMANDS = {
    "scrape": cmd_scrape,
    "journals": cmd_journals,
    "run": cmd_run,
}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "run"
    if cmd not in COMMANDS:
        console.print(__doc__)
        sys.exit(1)
    COMMANDS[cmd]()
