import asyncio
from app.agents.graph import contract_review_graph
from app.agents.state import ContractReviewState

async def run_pipeline():
    test_state: ContractReviewState = {
        "contract_id": "test-gemini-pipeline",
        "raw_text": "Provider reserves the right to ingest, de-identify, and use Customer Data and Prompts to train foundational AI models. Seller liability capped under first-dollar tipping basket of $1.5M.",
        "sections": [
            {
                "section_number": "4.1",
                "title": "AI Training and Data Usage",
                "content": "Provider reserves the right to ingest, de-identify, and use Customer Data and Prompts to train foundational AI models."
            },
            {
                "section_number": "5.2",
                "title": "Indemnification Basket",
                "content": "Seller liability capped under first-dollar tipping basket of $1.5M."
            }
        ],
        "playbook_rules": [],
        "identified_risks": [],
        "redlines": [],
        "debate_transcript": [],
        "obligations": [],
        "compliance_matrix": {},
        "overall_score": 0.0,
        "risk_summary": {},
        "current_status": "initialized",
        "use_local_llm": False,
        "llm_provider": "gemini",
        "model_name": "gemini-3.5-flash-lite"
    }
    print("[*] Executing multi-agent review graph with live Gemini...")
    result = await contract_review_graph.ainvoke(test_state)
    print("\n[SUCCESS] Finished Multi-Agent Pipeline!")
    print(f"Identified Risks: {len(result.get('identified_risks', []))}")
    print(f"Redlines Synthesized: {len(result.get('redlines', []))}")
    print(f"Overall Risk Score: {result.get('overall_score')}")
    print("\n--- Live Multi-Agent Debate Transcript ---")
    for turn in result.get("debate_transcript", []):
        agent = turn.get("agent_name")
        content = turn.get("content")
        print(f"[{agent}]: {content}\n")

if __name__ == "__main__":
    asyncio.run(run_pipeline())
