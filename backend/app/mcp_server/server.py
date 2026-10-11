import re
from typing import Dict, Any, List, Optional


class FastContractMCPServer:
    """
    Model Context Protocol (MCP) Server for ContractMind v1.5.
    Provides standard JSON-RPC tool schemas and handlers.
    """

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "evaluate_clause",
                "description": "Evaluates contract clause against corporate playbook for compliance and risk exposure.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "clause_text": {
                            "type": "string",
                            "description": "The exact wording of the contractual clause to evaluate.",
                        },
                        "clause_type": {
                            "type": "string",
                            "description": "Type of clause, e.g. 'indemnity', 'ai_training', 'liability', 'termination'.",
                        },
                    },
                    "required": ["clause_text", "clause_type"],
                },
            },
            {
                "name": "get_playbook_rules",
                "description": "Retrieves institutional negotiation rules and hard stops for a given playbook.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "playbook_id": {
                            "type": "string",
                            "description": "Identifier of the corporate playbook (e.g. 'standard', 'strict', 'founder').",
                        }
                    },
                },
            },
            {
                "name": "calculate_risk_matrix",
                "description": "Calculates composite weighted risk score and formal governance verdict.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "flagged_counts": {
                            "type": "object",
                            "properties": {
                                "critical": {"type": "integer"},
                                "high": {"type": "integer"},
                                "medium": {"type": "integer"},
                                "low": {"type": "integer"},
                            },
                            "required": ["critical", "high", "medium"],
                        }
                    },
                    "required": ["flagged_counts"],
                },
            },
        ]

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name == "evaluate_clause":
            clause_text = arguments.get("clause_text", "")
            clause_type = arguments.get("clause_type", "general")

            signals = []
            risk_level = "LOW"
            is_compliant = True

            lower_text = clause_text.lower()
            if "unlimited" in lower_text or "tipping basket" in lower_text:
                signals.append("Uncapped financial exposure")
                risk_level = "CRITICAL"
                is_compliant = False
            if "without accounting" in lower_text or "grant-back" in lower_text:
                signals.append("Uncompensated IP transfer")
                risk_level = "HIGH"
                is_compliant = False
            if "immediate termination" in lower_text or "sole discretion" in lower_text:
                signals.append("Unilateral termination trigger")
                risk_level = "MEDIUM"
                is_compliant = False
            if "train" in lower_text or "ingest" in lower_text or "model checkpoint" in lower_text:
                signals.append("Unauthorized AI model training on customer telemetry")
                risk_level = "CRITICAL"
                is_compliant = False

            return {
                "clause_type": clause_type,
                "is_compliant": is_compliant,
                "risk_level": risk_level,
                "flagged_signals": signals,
                "standard_policy": "All high-risk triggers require mutual consent and liability caps.",
                "recommended_action": "REPLACE_WITH_CONSENSUS_REDLINE" if not is_compliant else "ACCEPT",
            }

        elif tool_name == "get_playbook_rules":
            playbook_id = arguments.get("playbook_id", "standard")
            return {
                "playbook_id": playbook_id,
                "rules": [
                    {
                        "category": "AI Training",
                        "hard_stop": "Strict prohibition on customer data retention for model weights.",
                        "preferred": "Zero data retention with transient inference only.",
                    },
                    {
                        "category": "Indemnification",
                        "hard_stop": "No first-dollar tipping baskets.",
                        "preferred": "True deductible basket capped at 1.0x annual fees.",
                    },
                    {
                        "category": "Limitation of Liability",
                        "hard_stop": "No unlimited liability without mutual carve-outs.",
                        "preferred": "12-month trailing fees cap with 2x super-cap.",
                    },
                ],
            }

        elif tool_name == "calculate_risk_matrix":
            counts = arguments.get("flagged_counts", {})
            critical = counts.get("critical", 0)
            high = counts.get("high", 0)
            medium = counts.get("medium", 0)

            score = min(100.0, 35 * critical + 20 * high + 10 * medium)
            verdict = "REJECT / REDLINE" if score >= 60.0 else "APPROVED WITH CAUTION"

            return {
                "composite_score": round(score, 1),
                "risk_tier": "SEVERE" if score >= 75 else ("ELEVATED" if score >= 50 else "NOMINAL"),
                "governance_verdict": verdict,
                "breakdown": {"critical": critical, "high": high, "medium": medium},
            }

        raise ValueError(f"Unknown MCP tool: {tool_name}")


mcp_server = FastContractMCPServer()
