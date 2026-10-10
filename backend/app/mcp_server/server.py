import json
from typing import Dict, Any, List

# Rule dictionaries for MCP evaluation
STANDARD_PLAYBOOK = {
    "indemnification": {
        "rule": "Must be mutual, capped at 12 months fees, excludes indirect damages.",
        "risk_threshold": "Unilateral indemnification is prohibited."
    },
    "liability": {
        "rule": "Aggregate cap must equal 1x annual contract value, disclaimer of consequential damages mandatory.",
        "risk_threshold": "Uncapped liability is unacceptable."
    },
    "ip": {
        "rule": "Customer owns custom deliverables; Vendor retains background IP with license.",
        "risk_threshold": "Assignment of vendor background tools is prohibited."
    },
    "termination": {
        "rule": "Requires 30 days written notice and opportunity to cure.",
        "risk_threshold": "Immediate termination without cause or cure is high risk."
    }
}


class FastContractMCPServer:
    """
    Lightweight, self-contained Model Context Protocol server exposing
    ContractMind legal tools for local or SSE MCP hosts.
    """

    def __init__(self):
        self.name = "contractmind-mcp-server"
        self.version = "1.0.0"

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "evaluate_clause",
                "description": "Evaluates a contract clause against corporate playbook standards.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "clause_text": {"type": "string", "description": "The text of the clause to evaluate"},
                        "clause_type": {"type": "string", "description": "indemnification, liability, ip, or termination"}
                    },
                    "required": ["clause_text", "clause_type"]
                }
            },
            {
                "name": "get_playbook_rules",
                "description": "Fetches standard playbook rules for liability, indemnification, IP, and termination.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "playbook_id": {"type": "string", "description": "Identifier for the playbook"}
                    }
                }
            },
            {
                "name": "calculate_risk_matrix",
                "description": "Calculates composite legal risk score based on high-risk flags.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "flagged_counts": {"type": "object", "description": "Dictionary of critical, high, medium counts"}
                    },
                    "required": ["flagged_counts"]
                }
            }
        ]

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name == "evaluate_clause":
            clause_text = arguments.get("clause_text", "")
            clause_type = arguments.get("clause_type", "liability").lower()
            standard = STANDARD_PLAYBOOK.get(clause_type, STANDARD_PLAYBOOK["liability"])
            
            clause_lower = clause_text.lower()
            risk_signals = {
                "liability": ["unlimited", "uncapped", "sole discretion", "no aggregate cap", "exceeding contract value"],
                "indemnification": ["solely indemnify", "hold harmless and defend", "tipping basket", "unilateral", "first dollar"],
                "ip": ["irrevocably assign", "sole property of customer", "grant-back", "without accounting", "all foreground and background"],
                "termination": ["immediately without notice", "without cause", "no cure", "waives right to cure"]
            }

            matched_risks = [sig for sig in risk_signals.get(clause_type, ["unlimited", "solely"]) if sig in clause_lower]
            is_risky = len(matched_risks) > 0
            severity = "CRITICAL" if len(matched_risks) >= 2 else ("HIGH" if is_risky else "LOW")

            return {
                "clause_type": clause_type,
                "is_compliant": not is_risky,
                "risk_level": severity,
                "flagged_signals": matched_risks,
                "standard_policy": standard["rule"],
                "risk_threshold": standard.get("risk_threshold", ""),
                "recommended_action": f"Redline clause to eliminate [{', '.join(matched_risks)}]" if is_risky else "Accept as drafted conforming to standard playbook."
            }

        elif tool_name == "get_playbook_rules":
            return {
                "playbook_name": "Standard Corporate Playbook",
                "rules": STANDARD_PLAYBOOK
            }

        elif tool_name == "calculate_risk_matrix":
            flags = arguments.get("flagged_counts", {})
            critical = flags.get("critical", 0)
            high = flags.get("high", 0)
            medium = flags.get("medium", 0)
            score = min(100.0, (critical * 35.0) + (high * 20.0) + (medium * 10.0))
            return {
                "composite_risk_score": score,
                "verdict": "REJECT / REDLINE" if score > 50 else "APPROVED WITH CAUTION"
            }

        return {"error": f"Unknown tool: {tool_name}"}


mcp_server = FastContractMCPServer()
