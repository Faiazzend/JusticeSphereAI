import pytest
from app.agents.nodes.auditor_agent import auditor_node
from app.agents.nodes.opposing_agent import opposing_node
from app.agents.nodes.redline_agent import redline_node
from app.agents.nodes.obligation_agent import obligation_node


@pytest.mark.asyncio
async def test_agent_pipeline_execution():
    state = {
        "contract_id": "test_001",
        "contract_title": "Test MSA",
        "raw_text": "Vendor shall indemnify Client. Aggregate liability is uncapped.",
        "sections": [
            {
                "section_number": "1.0",
                "title": "Indemnification & Liability",
                "content": "Vendor shall solely defend and hold harmless Client. Liability is unlimited.",
                "page_number": 1
            }
        ],
        "playbook_rules": [],
        "debate_cycle": 1,
        "max_debate_cycles": 2,
        "use_local_llm": False,
        "identified_risks": [],
        "debate_transcript": [],
        "redlines": [],
        "obligations": [],
        "risk_summary": {},
        "overall_score": 0.0,
        "current_status": "init",
        "error": None
    }

    # 1. Auditor Node
    res1 = await auditor_node(state)
    state.update(res1)
    assert len(state["identified_risks"]) > 0
    assert len(state["debate_transcript"]) == 1

    # 2. Opposing Node
    res2 = await opposing_node(state)
    state.update(res2)
    assert len(state["debate_transcript"]) > 1

    # 3. Redline Node
    res3 = await redline_node(state)
    state.update(res3)
    assert len(state["redlines"]) > 0
    assert state["overall_score"] > 0.0

    # 4. Obligation Node
    res4 = await obligation_node(state)
    state.update(res4)
    assert isinstance(state["obligations"], list)
