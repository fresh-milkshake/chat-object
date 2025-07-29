import doctest
import sys
from typing import List

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn


console = Console()


def run_doctests() -> int:
    modules: List[str] = [
        "chat_object.consts",
        "chat_object.message",
        "chat_object.chat",
    ]

    total_failures: int = 0
    total_tests: int = 0

    console.print(Panel.fit("[bold cyan]Running doctests for package...[/bold cyan]", style="bold blue"))
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Module", style="bold")
    table.add_column("Tests", justify="right")
    table.add_column("Failures", justify="right")
    table.add_column("Status", style="bold")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        transient=True,
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Testing modules...", total=len(modules))
        for module_name in modules:
            module_tests = 0
            module_failures = 0
            status = ""
            try:
                module = __import__(module_name, fromlist=["*"])
                finder = doctest.DocTestFinder()
                tests = finder.find(module)

                if not tests:
                    status = "[yellow]No doctests[/yellow]"
                else:
                    for test in tests:
                        runner = doctest.DocTestRunner(verbose=False)
                        result = runner.run(test)
                        module_failures += result.failed
                        module_tests += result.attempted
                    if module_tests == 0:
                        status = "[yellow]No doctests[/yellow]"
                    elif module_failures == 0:
                        status = "[green]✅ Passed[/green]"
                    else:
                        status = f"[red]❌ {module_failures} failed[/red]"
                total_failures += module_failures
                total_tests += module_tests
            except ImportError:
                status = "[red]❌ Import error[/red]"
                module_failures = 1
                total_failures += 1
            except Exception:
                status = "[red]❌ Error[/red]"
                module_failures = 1
                total_failures += 1
            table.add_row(
                f"[cyan]{module_name}[/cyan]",
                str(module_tests),
                str(module_failures),
                status,
            )
            progress.update(task, advance=1)

    console.print(table)

    passed_tests = total_tests - total_failures
    summary_text = Text()
    summary_text.append("Summary: ", style="bold")
    summary_text.append(f"{passed_tests}/{total_tests} tests passed", style="bold green" if total_failures == 0 else "bold yellow")
    console.print(summary_text)

    if total_failures > 0:
        console.print(f"[bold red]❌ Failed: {total_failures} tests[/bold red]")
        return 1
    else:
        console.print("[bold green]✅ All tests passed![/bold green]")
        return 0


def main() -> None:
    """Main entry point."""
    try:
        exit_code = run_doctests()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Test execution interrupted by user[/bold yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Unexpected error: {e}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
