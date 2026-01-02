import argparse
from rich import print
from agents.graph import job_graph


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("resume", help="Path to resume text file")
    ap.add_argument(
        "--intent",
        default="machine learning and data science roles",
        help="Job search intent"
    )
    args = ap.parse_args()

    # Load resume
    with open(args.resume, "r") as f:
        resume_text = f.read()

    # Initial state passed into LangGraph
    initial_state = {
        "resume_text": resume_text,
        "user_intent": args.intent,
    }

    # 🔥 THIS is the agentic execution
    final_state = job_graph.invoke(initial_state)

    matches = final_state.get("matches", [])

    print("\n[bold cyan]Top Matches[/bold cyan]\n")

    for rank, (job, score) in enumerate(matches, start=1):
        print("=" * 90)
        print(f"[bold]{rank}. {job.title} @ {job.company}[/bold]")
        print(f"Score: {score:.3f}")
        print(f"Location: {job.location}")
        print(f"Source: {getattr(job, 'source', 'Unknown')}")
        print(f"Link: {job.url}")

    if final_state.get("explanation"):
        print("\n[bold green]Explanation[/bold green]")
        print(final_state["explanation"])

    if final_state.get("critique"):
        print("\n[bold yellow]Critique[/bold yellow]")
        print(final_state["critique"])


if __name__ == "__main__":
    main()
