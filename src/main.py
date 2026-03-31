from src.guardrails.input_guard import check_input
from src.guardrails.output_guard import check_output
from src.agents.planner import create_plan
from src.agents.executor import execute_plan
from src.agents.critic import generate_response

def run_agent(user_query: str) -> str:
    print(f"\n{'='*60}")
    print(f"User: {user_query}")
    print('='*60)

    # Step 1: Input guardrail
    input_check = check_input(user_query)
    if not input_check["allowed"]:
        print(f"[BLOCKED - {input_check['reason']}]")
        return input_check["message"]

    # Step 2: Planner agent
    print("[Planner] Creating execution plan...")
    plan = create_plan(user_query)
    print(f"[Planner] Plan: {plan}")

    # Step 3: Executor agent
    print("[Executor] Running tools...")
    tool_results = execute_plan(plan)
    print(f"[Executor] Results:\n{tool_results}")

    # Step 4: Critic agent generates final response
    print("[Critic] Generating response...")
    response = generate_response(user_query, tool_results)

    # Step 5: Output guardrail
    output_check = check_output(response)
    if not output_check["safe"]:
        print(f"[OUTPUT BLOCKED - {output_check['reason']}]")
        return output_check["message"]

    return f"\n{response}"

if __name__ == "__main__":
    print("Financial Assistant (type 'quit' to exit)\n")
    while True:
        query = input("You: ").strip()
        if query.lower() in ["quit", "exit"]:
            break
        if query:
            result = run_agent(query)
            print(f"\nAssistant: {result}\n")