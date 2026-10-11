import pytest
import io
import json
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_llm_health_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/analysis/llm/health")
        assert resp.status_code == 200
        data = resp.json()
        assert "status" in data
        assert "active_provider" in data
        assert "providers" in data
        assert "fallback-simulator" in data["providers"]
        assert data["providers"]["fallback-simulator"]["available"] is True


@pytest.mark.asyncio
async def test_calendar_ics_and_json_csv_exports():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Load demo contract
        demo_resp = await client.post("/api/v1/contracts/demo/nda")
        assert demo_resp.status_code == 200
        contract_id = demo_resp.json()["id"]

        # 1. Test iCalendar (.ics) export
        ics_resp = await client.get(f"/api/v1/analysis/{contract_id}/export/ics")
        assert ics_resp.status_code == 200
        assert "text/calendar" in ics_resp.headers.get("content-type", "")
        ics_text = ics_resp.text
        assert "BEGIN:VCALENDAR" in ics_text
        assert "END:VCALENDAR" in ics_text
        assert "PRODID:-//ContractMind" in ics_text

        # 2. Test JSON export
        json_resp = await client.get(f"/api/v1/analysis/{contract_id}/export/json")
        assert json_resp.status_code == 200
        assert "application/json" in json_resp.headers.get("content-type", "")
        json_data = json_resp.json()
        assert json_data["contract_id"] == contract_id
        assert "redlines" in json_data
        assert "obligations" in json_data

        # 3. Test CSV export
        csv_resp = await client.get(f"/api/v1/analysis/{contract_id}/export/csv")
        assert csv_resp.status_code == 200
        assert "text/csv" in csv_resp.headers.get("content-type", "")
        csv_text = csv_resp.text
        assert "REDLINES & NEGOTIATION RECOMMENDATIONS" in csv_text
        assert "EXTRACTED OBLIGATIONS & COVENANTS" in csv_text


@pytest.mark.asyncio
async def test_contract_compare_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Load two contracts
        c1 = (await client.post("/api/v1/contracts/demo/nda")).json()
        c2 = (await client.post("/api/v1/contracts/demo/saas")).json()

        compare_resp = await client.post(
            "/api/v1/contracts/compare",
            json={
                "base_contract_id": c1["id"],
                "target_contract_id": c2["id"],
            },
        )
        assert compare_resp.status_code == 200
        data = compare_resp.json()
        assert data["base_id"] == c1["id"]
        assert data["target_id"] == c2["id"]
        assert "risk_score_delta" in data
        assert "sections" in data
        assert len(data["sections"]) > 0


@pytest.mark.asyncio
async def test_custom_playbook_crud():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create custom playbook
        new_pb = {
            "id": "fintech_compliance",
            "name": "Fintech Compliance Playbook",
            "description": "Rules for banking and PCI-DSS compliance.",
            "rules": [
                {
                    "category": "Data Security",
                    "severity": "CRITICAL",
                    "preferred_position": "SOC 2 Type II and ISO 27001 mandated.",
                    "fallback_position": "Annual SOC 2 bridge letter accepted.",
                    "hard_stop": "No self-attestation only.",
                }
            ],
        }
        create_resp = await client.post("/api/v1/playbook/custom", json=new_pb)
        assert create_resp.status_code == 200
        assert create_resp.json()["id"] == "fintech_compliance"

        # List custom playbooks
        list_resp = await client.get("/api/v1/playbook/custom")
        assert list_resp.status_code == 200
        custom_pbs = list_resp.json()
        assert any(pb["id"] == "fintech_compliance" for pb in custom_pbs)

        # Delete custom playbook
        del_resp = await client.delete("/api/v1/playbook/custom/fintech_compliance")
        assert del_resp.status_code == 200
        assert del_resp.json()["status"] == "success"


@pytest.mark.asyncio
async def test_stream_and_pagination():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Test pagination
        list_resp = await client.get("/api/v1/contracts/?skip=0&limit=2")
        assert list_resp.status_code == 200
        assert len(list_resp.json()) <= 2

        # 2. Test invalid upload extension
        bad_file = {"file": ("malicious.exe", b"not safe", "application/octet-stream")}
        bad_upload = await client.post("/api/v1/contracts/upload", files=bad_file)
        assert bad_upload.status_code == 400


@pytest.mark.asyncio
async def test_user_auth_registration_and_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register user
        reg_payload = {
            "email": "counsel@enterprise.ai",
            "password": "SecurePassword123!",
            "full_name": "General Counsel",
            "role": "reviewer",
        }
        reg_resp = await client.post("/api/v1/auth/register", json=reg_payload)
        assert reg_resp.status_code in (200, 400)  # 200 on new, 400 if already exists

        # Login user
        login_payload = {
            "email": "counsel@enterprise.ai",
            "password": "SecurePassword123!",
        }
        login_resp = await client.post("/api/v1/auth/login", json=login_payload)
        assert login_resp.status_code == 200
        token_data = login_resp.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
        assert token_data["email"] == "counsel@enterprise.ai"
