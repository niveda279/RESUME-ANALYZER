"""
careercast.cli — Command-line interface for CareerCast.

Entry point: ``careercast`` (configured in pyproject.toml)

Subcommands
-----------
  analyze      Parse a resume file and print extracted entities
  predict      Predict the career role for a resume file or text
  skill-gap    Analyze skill gaps between a resume and a target role
  models       Show performance metrics for all trained models
  version      Print the package version and exit
"""

import os
import sys
import json

import click

# Ensure the backend directory is importable
_PKG_DIR    = os.path.dirname(os.path.abspath(__file__))
_BACKEND    = os.path.abspath(os.path.join(_PKG_DIR, "..", "backend"))
if _BACKEND not in sys.path:
    sys.path.insert(0, _BACKEND)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _print_json(data: dict) -> None:
    click.echo(json.dumps(data, indent=2, ensure_ascii=False, default=str))


def _load_text_from_arg(file_path: str | None, text: str | None) -> str:
    """Return plain text from either a file path or a --text flag."""
    if file_path:
        if not os.path.isfile(file_path):
            raise click.ClickException(f"File not found: {file_path}")
        from utils.parser import extract_text_from_file
        raw = extract_text_from_file(file_path)
        if not raw or raw.startswith("Error"):
            raise click.ClickException(f"Failed to read file: {raw}")
        return raw
    if text:
        return text
    raise click.ClickException("Provide either a FILE or --text argument.")


# ── CLI root ──────────────────────────────────────────────────────────────────

@click.group()
@click.version_option(package_name="careercast", prog_name="careercast")
def main():
    """CareerCast — AI-powered resume analysis toolkit."""
    pass


# ── version ───────────────────────────────────────────────────────────────────

@main.command("version")
def version_cmd():
    """Print the CareerCast package version."""
    from careercast import __version__
    click.echo(f"CareerCast v{__version__}")


# ── analyze ───────────────────────────────────────────────────────────────────

@main.command("analyze")
@click.argument("file", required=False, type=click.Path(exists=True))
@click.option("--text", "-t", default=None, help="Raw resume text instead of a file.")
@click.option("--json-output", is_flag=True, default=False, help="Output as JSON.")
def analyze_cmd(file, text, json_output):
    """Parse a resume FILE and print extracted entities.

    Examples:\n
      careercast analyze resume.pdf\n
      careercast analyze --text "John Doe | Python, SQL" --json-output
    """
    from utils.parser import extract_text_from_file, parse_resume_text

    raw = _load_text_from_arg(file, text)
    result = parse_resume_text(raw)

    if json_output:
        result.pop("raw_text", None)        # omit verbose field in JSON mode
        _print_json(result)
        return

    click.echo(click.style("\n── Parsed Resume Entities ──────────────────", bold=True))
    click.echo(f"  Name           : {result.get('name', 'N/A')}")
    click.echo(f"  Email          : {result.get('email', 'N/A')}")
    click.echo(f"  Phone          : {result.get('phone', 'N/A')}")
    click.echo(f"  Education      : {result.get('education', 'N/A')}")
    click.echo(f"  Experience     : {result.get('experience', 'N/A')}")
    click.echo(f"  Certifications : {result.get('certifications', 'N/A')}")
    skills = result.get("skills", [])
    click.echo(f"  Skills ({len(skills)})    : {', '.join(skills) if skills else 'None detected'}")
    click.echo("")


# ── predict ───────────────────────────────────────────────────────────────────

@main.command("predict")
@click.argument("file", required=False, type=click.Path(exists=True))
@click.option("--text", "-t", default=None, help="Raw resume text instead of a file.")
@click.option(
    "--model", "-m",
    default="best",
    show_default=True,
    type=click.Choice(["best", "logistic_regression", "random_forest", "xgboost"],
                      case_sensitive=False),
    help="Model to use for prediction.",
)
@click.option("--all-models", is_flag=True, default=False,
              help="Show predictions from all three models.")
@click.option("--json-output", is_flag=True, default=False, help="Output as JSON.")
def predict_cmd(file, text, model, all_models, json_output):
    """Predict the career role for a resume FILE.

    Examples:\n
      careercast predict resume.pdf\n
      careercast predict resume.pdf --model random_forest\n
      careercast predict resume.pdf --all-models --json-output
    """
    from utils.ml_service import predict_all_models, get_best_model_prediction

    raw = _load_text_from_arg(file, text)

    if all_models:
        result = predict_all_models(raw)
        if json_output:
            _print_json(result)
            return
        _print_model_table(result)
        return

    if model == "best":
        pred = get_best_model_prediction(raw)
    else:
        all_preds = predict_all_models(raw)
        key = model.lower().replace(" ", "_")
        pred = all_preds.get(key, all_preds.get("logistic_regression", {}))

    if json_output:
        _print_json(pred)
        return

    click.echo(click.style("\n── Career Prediction ───────────────────────", bold=True))
    click.echo(f"  Predicted Role : {click.style(pred.get('predicted_role','?'), fg='green', bold=True)}")
    click.echo(f"  Confidence     : {pred.get('confidence', 0):.1f}%")
    breakdown = pred.get("breakdown", [])
    if breakdown:
        click.echo(click.style("\n  Top Role Probabilities:", bold=True))
        for item in breakdown[:5]:
            bar = "█" * int(item["probability"] / 5)
            click.echo(f"    {item['role']:<28} {item['probability']:5.1f}% {bar}")
    click.echo("")


def _print_model_table(result: dict) -> None:
    headers = ["Model", "Predicted Role", "Confidence"]
    rows = [
        ["Logistic Regression",
         result.get("logistic_regression", {}).get("predicted_role", "?"),
         f"{result.get('logistic_regression', {}).get('confidence', 0):.1f}%"],
        ["Random Forest",
         result.get("random_forest", {}).get("predicted_role", "?"),
         f"{result.get('random_forest', {}).get('confidence', 0):.1f}%"],
        ["XGBoost",
         result.get("xgboost", {}).get("predicted_role", "?"),
         f"{result.get('xgboost', {}).get('confidence', 0):.1f}%"],
    ]
    click.echo(click.style("\n── All Model Predictions ───────────────────", bold=True))
    click.echo(f"  {'Model':<22} {'Predicted Role':<30} {'Confidence'}")
    click.echo(f"  {'─'*22} {'─'*30} {'─'*10}")
    for row in rows:
        click.echo(f"  {row[0]:<22} {row[1]:<30} {row[2]}")
    best = result.get("best_model", "N/A")
    click.echo(f"\n  Best model (by CV accuracy): {click.style(best, fg='cyan', bold=True)}\n")


# ── skill-gap ─────────────────────────────────────────────────────────────────

@main.command("skill-gap")
@click.argument("file", required=False, type=click.Path(exists=True))
@click.option("--text", "-t", default=None, help="Raw resume text instead of a file.")
@click.option("--role", "-r", default=None,
              help="Target role (auto-detected from resume if omitted).")
@click.option("--json-output", is_flag=True, default=False, help="Output as JSON.")
def skill_gap_cmd(file, text, role, json_output):
    """Analyze skill gaps for a resume FILE against a target role.

    Examples:\n
      careercast skill-gap resume.pdf --role "Data Scientist"\n
      careercast skill-gap resume.pdf --json-output
    """
    from utils.parser import parse_resume_text
    from utils.ml_service import get_best_model_prediction
    from services.skill_gap import analyze_skill_gap

    raw = _load_text_from_arg(file, text)
    parsed = parse_resume_text(raw)
    candidate_skills = parsed.get("skills", [])

    if not role:
        pred = get_best_model_prediction(raw)
        role = pred.get("predicted_role", "Software Engineer")

    gap = analyze_skill_gap(candidate_skills, role)

    if json_output:
        _print_json(gap)
        return

    match_pct = gap.get("match_percentage", 0)
    matched   = gap.get("matched_skills", [])
    missing   = gap.get("missing_skills", [])
    priority  = gap.get("priority_gaps", [])

    color = "green" if match_pct >= 70 else ("yellow" if match_pct >= 40 else "red")

    click.echo(click.style(f"\n── Skill Gap Analysis — {role} ──────────────", bold=True))
    click.echo(f"  Match Score  : {click.style(f'{match_pct}%', fg=color, bold=True)}")
    click.echo(f"  Matched ({len(matched)}) : {', '.join(s['skill'] for s in matched) or 'None'}")
    click.echo(f"  Missing ({len(missing)}) : {', '.join(s['skill'] for s in missing) or 'None'}")

    if priority:
        click.echo(click.style("\n  🚨 Priority Gaps (Critical/High):", bold=True))
        for gap_item in priority:
            click.echo(f"\n  [{gap_item['priority']}] {click.style(gap_item['skill'], fg='red')}")
            click.echo(f"    → {gap_item['suggestion']}")
    else:
        click.echo(click.style("\n  ✅ No critical skill gaps! Great profile for this role.", fg="green"))
    click.echo("")


# ── models ────────────────────────────────────────────────────────────────────

@main.command("models")
@click.option("--json-output", is_flag=True, default=False, help="Output as JSON.")
def models_cmd(json_output):
    """Display performance metrics for all trained models."""
    from utils.ml_model import get_all_metrics

    metrics = get_all_metrics()

    if json_output:
        _print_json(metrics)
        return

    click.echo(click.style("\n── Trained Model Performance ───────────────", bold=True))

    models_data = {
        "Logistic Regression": metrics.get("logistic_regression", {}),
        "Random Forest":       metrics.get("random_forest", {}),
        "XGBoost":             metrics.get("xgboost", {}),
    }

    for name, m in models_data.items():
        if not m:
            click.echo(f"  {name:<22}: Not available")
            continue
        acc = m.get("accuracy", m.get("cv_accuracy_mean", 0))
        f1  = m.get("f1_weighted", m.get("f1", 0))
        click.echo(
            f"  {name:<22}: Accuracy={acc*100:.1f}%  F1={f1*100:.1f}%"
            if isinstance(acc, float) and acc <= 1
            else f"  {name:<22}: Accuracy={acc:.1f}%  F1={f1:.1f}%"
        )

    best = metrics.get("best_model", "N/A")
    click.echo(f"\n  Best model: {click.style(best, fg='cyan', bold=True)}\n")


# ── entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
