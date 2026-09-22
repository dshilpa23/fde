"""
seed_data.py — UHG Claims Intelligence Service (L3)

Fixed, deterministic seed data used throughout Session 1 and Session 2.
20 eval cases in eval/cases.json are written against these exact values —
do not change counts or amounts here without updating eval/cases.json.

Dataset shape:
  5 members
  5 providers (2 out-of-network)
  10 claims (3 in_review, 2 approved, 2 denied, 2 pending_info, 1 submitted)
"""

from decimal import Decimal

MEMBERS = [
    {"member_id": "MBR-001", "name": "Alice Johnson",  "plan": "PPO-Gold"},
    {"member_id": "MBR-002", "name": "Brian Lee",       "plan": "HMO-Silver"},
    {"member_id": "MBR-003", "name": "Carla Mendes",    "plan": "PPO-Gold"},
    {"member_id": "MBR-004", "name": "David Okafor",    "plan": "PPO-Bronze"},
    {"member_id": "MBR-005", "name": "Elena Petrova",   "plan": "HMO-Silver"},
]

PROVIDERS = [
    {"provider_id": "NPI-100001", "name": "Lakeside Medical Group",      "in_network": True},
    {"provider_id": "NPI-100002", "name": "Riverside Family Clinic",     "in_network": True},
    {"provider_id": "NPI-100003", "name": "Summit Orthopedics",          "in_network": True},
    {"provider_id": "NPI-100004", "name": "Pinegrove Urgent Care",       "in_network": False},
    {"provider_id": "NPI-100005", "name": "Harborview Specialty Center", "in_network": False},
]

# Status lifecycle: submitted -> in_review -> approved / denied / pending_info
# Out-of-network providers (NPI-100004, NPI-100005) always trigger pending_info.
CLAIMS = [
    {"claim_id": "CLM-001", "member_id": "MBR-001", "provider_id": "NPI-100001",
     "status": "approved",     "billed_amount": Decimal("450.00")},
    {"claim_id": "CLM-002", "member_id": "MBR-002", "provider_id": "NPI-100002",
     "status": "in_review",    "billed_amount": Decimal("1200.00")},
    {"claim_id": "CLM-003", "member_id": "MBR-001", "provider_id": "NPI-100004",
     "status": "pending_info", "billed_amount": Decimal("2750.50")},
    {"claim_id": "CLM-004", "member_id": "MBR-003", "provider_id": "NPI-100003",
     "status": "denied",       "billed_amount": Decimal("875.25")},
    {"claim_id": "CLM-005", "member_id": "MBR-004", "provider_id": "NPI-100002",
     "status": "approved",     "billed_amount": Decimal("320.00")},
    {"claim_id": "CLM-006", "member_id": "MBR-002", "provider_id": "NPI-100001",
     "status": "in_review",    "billed_amount": Decimal("610.75")},
    {"claim_id": "CLM-007", "member_id": "MBR-005", "provider_id": "NPI-100005",
     "status": "pending_info", "billed_amount": Decimal("3400.00")},
    {"claim_id": "CLM-008", "member_id": "MBR-003", "provider_id": "NPI-100003",
     "status": "denied",       "billed_amount": Decimal("9574.75")},
    {"claim_id": "CLM-009", "member_id": "MBR-004", "provider_id": "NPI-100001",
     "status": "in_review",    "billed_amount": Decimal("540.00")},
    {"claim_id": "CLM-010", "member_id": "MBR-005", "provider_id": "NPI-100002",
     "status": "submitted",    "billed_amount": Decimal("210.00")},
]

# Reference values for eval/cases.json and lab exercises:
#   in_review count        = 3   (CLM-002, CLM-006, CLM-009)
#   approved count         = 2   (CLM-001, CLM-005)
#   denied count            = 2   (CLM-004, CLM-008)
#   pending_info count     = 2   (CLM-003, CLM-007)
#   submitted count        = 1   (CLM-010)
#   denied total billed    = 875.25 + 9574.75 = 10450.00
#   approved total billed  = 450.00 + 320.00  = 770.00
#   MBR-001 claim count    = 2   (CLM-001, CLM-003)
#   out-of-network claims  = 2   (CLM-003, CLM-007) — both correctly pending_info
