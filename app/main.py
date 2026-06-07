from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt

from services.document_saver import save_document
from graph.workflows.research_router import research_router

import os
import traceback

console = Console()


def show_banner():
    console.print(
        Panel.fit(
            "[bold cyan]Research Assistant[/bold cyan]\n"
            "[green]Powered by LangGraph + Gemini[/green]",
            border_style="blue",
        )
    )


def process_query(query: str, pdf_path: str = None):

    # Debug Information
    print("\n========== DEBUG ==========")
    print("QUERY:", query)
    print("QUERY TYPE:", type(query))
    print("PDF PATH:", pdf_path)
    print("PDF PATH TYPE:", type(pdf_path))
    print("===========================\n")

    with console.status(
        "[bold green]Researching...[/bold green]",
        spinner="dots",
    ):

        response = research_router.invoke(
            {
                "query": query,
                "file_path": pdf_path
            }
        )

    return response


def display_answer(answer: str):

    console.print()
    console.rule("[bold blue]Research Result[/bold blue]")

    md = Markdown(answer)

    console.print(md)

    console.rule()


def get_pdf_path():

    pdf_path = Prompt.ask(
        "\n[bold yellow]PDF Path (Optional)[/bold yellow]",
        default=""
    )

    if pdf_path is None:
        return None

    pdf_path = str(pdf_path).strip()

    if not pdf_path:
        return None

    if not os.path.exists(pdf_path):

        console.print(
            f"[red]PDF not found:[/red] {pdf_path}"
        )

        return None

    if not pdf_path.lower().endswith(".pdf"):

        console.print(
            "[red]Only PDF files are supported[/red]"
        )

        return None

    return pdf_path


def main():

    show_banner()

    while True:

        query = Prompt.ask(
            "\n[bold cyan]Ask Question[/bold cyan]"
        )

        if query.lower() in ["exit", "quit", "bye"]:

            console.print(
                "\n[yellow]Goodbye![/yellow]"
            )

            break

        pdf_path = get_pdf_path()

        try:

            response = process_query(
                query=query,
                pdf_path=pdf_path
            )

            print("\n========== RESPONSE ==========")
            print(type(response))
            print(response)
            print("==============================\n")

            answer = response.get(
            "final_answer",
            "No answer generated."
        )

            if isinstance(answer, list):
                answer = str(answer)

            path = save_document(answer)

            display_answer(answer)

            console.print()

            console.print(
                f"[bold cyan]Verification:[/bold cyan] "
                f"{response.get('verification_status', 'UNKNOWN')}"
            )

            console.print(
                f"[bold cyan]Confidence:[/bold cyan] "
                f"{response.get('confidence_score', 0)}%"
            )

            console.print(
                f"[bold cyan]Reviewer Notes:[/bold cyan] "
                f"{response.get('critic_feedback', '')}"
            )

            console.print(
                f"\n[green]✓ Saved:[/green] {path}"
            )

            if pdf_path:

                console.print(
                    "[cyan]PDF Mode Used (No Web Search)[/cyan]"
                )

        except KeyboardInterrupt:

            console.print(
                "\n[red]Interrupted by user[/red]"
            )

            break

        except Exception as error:

            console.print(
                "\n[bold red]FULL ERROR TRACEBACK[/bold red]\n"
            )

            traceback.print_exc()

            console.print(
                Panel(
                    str(error),
                    title="ERROR",
                    border_style="red",
                )
            )


if __name__ == "__main__":
    main()