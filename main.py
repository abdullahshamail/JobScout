import argparse
from agents.planner import plan
from agents.ingest import ingest
from agents.matcher import match_jobs
from agents.explainer import explain
from agents.critic import critique
from rich import print

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd")
    ap.add_argument("resume")
    args = ap.parse_args()

    resume = open(args.resume).read()
    cfg = plan()

    index = ingest()
    matches = match_jobs(index, resume, cfg["top_k"])

    # after matches computed
    for rank, (job, score) in enumerate(matches, start=1):
        print("="*90)
        print(f"{rank}. {job.title} @ {job.company} [{job.source}]")
        print(f"Score: {score:.3f} | Location: {job.location}")
        print(f"Link: {job.url}")


if __name__ == "__main__":
    main()
