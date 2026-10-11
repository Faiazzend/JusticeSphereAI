import pytest
import pytest_asyncio
import httpx
from app.main import app
from app.database import init_db


@pytest.mark.asyncio
async def test_full_api_workflow():
    # Initialize DB
    await init_db()

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Health check
        res = await client.get("/health")
        assert res.status_code == 200
        assert res.json()["status"] == "healthy"
        assert res.json()["version"] == "1.5.3"

        # 2. MCP Tools list
        res = await client.get("/mcp/tools")
        assert res.status_code == 200
        tools = res.json()["tools"]
        assert len(tools) == 3

        # 3. MCP Call
        res = await client.post(
            "/mcp/call",
            json={
                "name": "calculate_risk_matrix",
                "arguments": {"flagged_counts": {"critical": 3, "high": 1, "medium": 0}},
            },
        )
        assert res.status_code == 200
        assert res.json()["result"]["governance_verdict"] == "REJECT / REDLINE"

        # 4. Playbooks
        res = await client.get("/api/v1/playbook/")
        assert res.status_code == 200
        assert len(res.json()) >= 3

        # 5. Load and execute benchmark contract (M&A)
        res = await client.post("/api/v1/contracts/demo/ma")
        assert res.status_code == 200
        contract = res.json()
        contract_id = contract["id"]
        assert contract["status"] == "analyzed"
        assert contract["overall_risk_score"] > 0
        assert len(contract["identified_risks"]) > 0
        assert len(contract["debate_transcript"]) >= 4
        assert len(contract["redlines"]) > 0
        assert len(contract["obligations"]) > 0

        # 6. Contract Detail
        res = await client.get(f"/api/v1/contracts/{contract_id}")
        assert res.status_code == 200
        assert res.json()["id"] == contract_id

        # 7. Export DOCX with Track Changes
        res = await client.get(f"/api/v1/analysis/{contract_id}/export/docx")
        assert res.status_code == 200
        assert "application/vnd.openxmlformats-officedocument" in res.headers["content-type"]
        assert len(res.content) > 1000

        # 8. Audit Summary
        res = await client.get("/api/v1/analysis/audit/summary")
        assert res.status_code == 200
        summary = res.json()
        assert summary["total_tokens"] > 0
        assert summary["total_runs"] > 0
        assert "Auditor Agent" in summary["by_agent"]
        assert "Opposing Counsel" in summary["by_agent"]
        assert "Redline Synthesizer" in summary["by_agent"]
        assert "Obligation Extractor" in summary["by_agent"]

        # 9. LLM Config
        res = await client.get("/api/v1/analysis/llm/config")
        assert res.status_code == 200
        assert "active_provider" in res.json()

        # 10. Delete contract
        res = await client.delete(f"/api/v1/contracts/{contract_id}")
        assert res.status_code == 200
        assert res.json()["status"] == "success"

        # Confirm deleted
        res = await client.get(f"/api/v1/contracts/{contract_id}")
        assert res.status_code == 404
