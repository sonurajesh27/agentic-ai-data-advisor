"""
agent.py - Main agentic AI loop with conversational chat interface
Agentic AI Data Usage Advisor for Next-Generation Networks
"""

from advisor import analyze


BANNER = """
╔══════════════════════════════════════════════════════════════╗
║   Agentic AI Data Usage Advisor — Next-Generation Networks   ║
╚══════════════════════════════════════════════════════════════╝
Type 'help' for commands, 'quit' to exit.
"""

HELP_TEXT = """
Available commands:
  analyze   — Run a new data usage analysis
  whatif    — Run what-if simulations on last analysis
  history   — Show previous analyses this session
  help      — Show this help message
  quit      — Exit the advisor
"""

RISK_COLORS = {
    "Low": "\033[92m",     # green
    "Medium": "\033[93m",  # yellow
    "High": "\033[91m",    # red
}
RESET = "\033[0m"


def color_risk(risk_level):
    color = RISK_COLORS.get(risk_level, "")
    return f"{color}{risk_level}{RESET}"


def get_float(prompt, min_val=0, max_val=24):
    while True:
        try:
            val = float(input(prompt))
            if min_val <= val <= max_val:
                return val
            print(f"  Please enter a value between {min_val} and {max_val}.")
        except ValueError:
            print("  Invalid input. Please enter a number.")


def get_int(prompt, min_val=0, max_val=100):
    while True:
        try:
            val = int(input(prompt))
            if min_val <= val <= max_val:
                return val
            print(f"  Please enter a value between {min_val} and {max_val}.")
        except ValueError:
            print("  Invalid input. Please enter a whole number.")


def get_yes_no(prompt):
    while True:
        val = input(prompt).strip().lower()
        if val in ("yes", "y"):
            return 1
        elif val in ("no", "n"):
            return 0
        print("  Please answer yes or no.")


def collect_inputs():
    """Interactively collect user inputs."""
    print("\n--- Enter your daily internet usage details ---")
    daily_hours = get_float("  Daily internet usage (hours, 0-24): ", 0, 24)
    streams_video = get_yes_no("  Do you stream video? (yes/no): ")
    num_downloads = get_int("  Number of file downloads per day (0-100): ", 0, 100)
    social_media_hours = get_float("  Social media usage (hours, 0-24): ", 0, 24)
    return daily_hours, streams_video, num_downloads, social_media_hours


def display_result(result):
    """Pretty-print the analysis result."""
    print("\n" + "=" * 60)
    print(f"  Predicted Data Usage : {result['predicted_gb']} GB / day")
    print(f"  Risk Level           : {color_risk(result['risk_level'])}")
    print("=" * 60)
    print("\n" + result["advice"])


def display_whatif(scenarios, baseline_gb):
    """Display what-if simulation results."""
    if not scenarios:
        print("\n  No what-if scenarios available for your current inputs.")
        return

    print(f"\n--- What-If Simulations (baseline: {baseline_gb} GB/day) ---")
    for s in scenarios:
        savings = s["savings_gb"]
        direction = "save" if savings > 0 else "cost"
        print(f"\n  Scenario : {s['scenario']}")
        print(f"  Result   : {s['predicted_gb']} GB/day  ({abs(savings)} GB {direction})")


def run_agent():
    """Main conversational agent loop."""
    print(BANNER)

    session_history = []
    last_result = None
    last_inputs = None

    while True:
        try:
            cmd = input("\n> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if cmd in ("quit", "exit", "q"):
            print("Thanks for using the Data Usage Advisor. Stay connected wisely!")
            break

        elif cmd == "help":
            print(HELP_TEXT)

        elif cmd in ("analyze", ""):
            inputs = collect_inputs()
            last_inputs = inputs
            print("\nAnalyzing your usage patterns...")
            result = analyze(*inputs)
            last_result = result
            display_result(result)
            session_history.append({
                "inputs": inputs,
                "result": result
            })

        elif cmd == "whatif":
            if last_result is None:
                print("  Run 'analyze' first to get a baseline.")
            else:
                display_whatif(last_result["whatif_scenarios"], last_result["predicted_gb"])

        elif cmd == "history":
            if not session_history:
                print("  No analyses yet this session.")
            else:
                print(f"\n  Session history ({len(session_history)} analyses):")
                for i, entry in enumerate(session_history, 1):
                    h, sv, dl, sm = entry["inputs"]
                    r = entry["result"]
                    print(
                        f"  [{i}] {h}h usage, streaming={'Yes' if sv else 'No'}, "
                        f"{dl} downloads, {sm}h social → "
                        f"{r['predicted_gb']} GB ({r['risk_level']})"
                    )

        else:
            print(f"  Unknown command '{cmd}'. Type 'help' for available commands.")


if __name__ == "__main__":
    run_agent()
