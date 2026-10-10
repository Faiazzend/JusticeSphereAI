import asyncio
from app.agents.nodes.auditor_agent import auditor_node
from app.agents.nodes.opposing_agent import opposing_node
from app.agents.nodes.redline_agent import redline_node
from app.agents.nodes.obligation_agent import obligation_node
from app.agents.state import ContractReviewState

async def run_pipeline():
    test_state: ContractReviewState = {
        "contract_id": "test-gemini-pipeline",
        "contract_title": "Enterprise Cloud & AI Licensing Agreement",
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

    print("[*] 1. Running Auditor Agent with Gemini...")
    auditor_res = await auditor_node(test_state)
    test_state.update(auditor_res)
    print(f"    - Flagged {len(test_state['identified_risks'])} risks")

    print("[*] 2. Running Opposing Counsel Agent with Gemini...")
    opposing_res = await opposing_node(test_state)
    test_state.update(opposing_res)
    print(f"    - Debate transcript turns: {len(test_state['debate_transcript'])}")

    print("[*] 3. Running Redline Synthesizer Agent with Gemini...")
    redline_res = await redline_node(test_state)
    test_state.update(redline_res)
    print(f"    - Redlines synthesized: {len(test_state['redlines'])}")
    print(f"    - Composite Risk Score: {test_state['overall_score']}")

    print("\n" + "=" * 65)
    print("LIVE AGENT DEBATE OUTPUT (POWERED BY GOOGLE GEMINI 3.5 FLASH LITE):")
    print("=" * 65)
    for turn in test_state.get("debate_transcript", []):
        print(f"\n[{turn['agent_name']}] -> Target: {turn.get('target_clause')}")
        print(f"{turn['content']}")
    print("=" * 65)

if __name__ == "__main__":
    asyncio.run(run_pipeline())
