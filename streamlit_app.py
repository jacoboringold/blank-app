import json
from datetime import datetime
from typing import Any, Dict, List

import streamlit as st

st.set_page_config(page_title="Hyatt Comfort Concierge", page_icon="🛏️", layout="wide")

# -----------------------------
# Demo hotel data
# -----------------------------

INVENTORY = {
    "bath_towel": {"label": "Bath towels", "stock": 40, "service": True},
    "hand_towel": {"label": "Hand towels", "stock": 35, "service": True},
    "pool_towel": {"label": "Pool towels", "stock": 28, "service": True},
    "sheet_set": {"label": "Fresh sheet sets", "stock": 18, "service": True},
    "blanket": {"label": "Cozy blankets", "stock": 14, "service": True},
    "pillow_soft": {"label": "Soft pillows", "stock": 10, "service": True, "retail_price": 59},
    "pillow_firm": {"label": "Firm pillows", "stock": 12, "service": True, "retail_price": 59},
    "pillow_hypoallergenic": {"label": "Hypoallergenic pillows", "stock": 8, "service": True, "retail_price": 69},
}

SERVICE_CATALOG = [
    "Extra towels",
    "Pool towels",
    "Fresh sheets",
    "Cozy blankets",
    "Soft, firm, or hypoallergenic pillows",
    "Crib or other family amenities",
    "Dining and room-service recommendations",
]

SUGGESTIONS = {
    "pool": ["pool towels", "cold water", "family-friendly dining"],
    "blanket": ["a softer pillow", "cozy blanket purchase", "tea or late-night dining"],
    "pillow": ["another pillow type", "cozy blanket", "purchase this pillow for home"],
}

# -----------------------------
# Session state
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "preferences" not in st.session_state:
    st.session_state.preferences = {}
if "guest_room" not in st.session_state:
    st.session_state.guest_room = "814"

# -----------------------------
# Tool-like functions
# -----------------------------


def check_inventory(item: str, quantity: int) -> Dict[str, Any]:
    record = INVENTORY.get(item)
    if not record:
        return {"ok": False, "reason": "unknown_item"}
    return {
        "ok": record["stock"] >= quantity,
        "item": item,
        "label": record["label"],
        "requested": quantity,
        "available": record["stock"],
    }


def create_housekeeping_task(item: str, quantity: int, room: str) -> Dict[str, Any]:
    inventory_result = check_inventory(item, quantity)
    if not inventory_result["ok"]:
        return {"ok": False, "reason": "insufficient_inventory", **inventory_result}

    INVENTORY[item]["stock"] -= quantity
    task_id = f"HK-{len(st.session_state.tasks) + 1001}"
    task = {
        "id": task_id,
        "room": room,
        "item": item,
        "label": INVENTORY[item]["label"],
        "quantity": quantity,
        "status": "accepted",
        "created_at": datetime.now().strftime("%H:%M:%S"),
    }
    st.session_state.tasks.append(task)
    return {"ok": True, **task}


def record_preference(category: str, value: str) -> None:
    st.session_state.preferences[category] = value


def retail_option(item: str) -> Dict[str, Any] | None:
    record = INVENTORY.get(item)
    if not record or "retail_price" not in record:
        return None
    return {"item": item, "label": record["label"], "price": record["retail_price"]}


def infer_request(text: str) -> List[Dict[str, Any]]:
    """Lightweight deterministic intent parser for a runnable demo.
    Replace this layer with an LLM tool-calling loop in production.
    """
    t = text.lower()
    requests: List[Dict[str, Any]] = []

    def quantity(default: int = 1) -> int:
        words = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        }
        for word, value in words.items():
            if word in t:
                return value
        for token in t.replace(",", " ").split():
            if token.isdigit():
                return int(token)
        return default

    q = quantity()
    if "pool" in t and "towel" in t:
        requests.append({"item": "pool_towel", "quantity": q})
    elif "towel" in t:
        requests.append({"item": "bath_towel", "quantity": q})

    if "sheet" in t:
        requests.append({"item": "sheet_set", "quantity": q})

    if "blanket" in t:
        requests.append({"item": "blanket", "quantity": q})

    if "soft pillow" in t or "soft pillows" in t:
        requests.append({"item": "pillow_soft", "quantity": q})
    elif "firm pillow" in t or "firm pillows" in t:
        requests.append({"item": "pillow_firm", "quantity": q})
    elif "hypoallergenic" in t or "allergy" in t:
        requests.append({"item": "pillow_hypoallergenic", "quantity": q})
    elif "pillow" in t:
        requests.append({"item": "pillow_soft", "quantity": q})

    return requests


def agent_response(user_text: str) -> str:
    text = user_text.strip()
    lower = text.lower()

    if not text:
        return "Tell me what would make your room more comfortable."

    if "same" in lower or "usual" in lower:
        if st.session_state.preferences:
            prefs = ", ".join(st.session_state.preferences.values())
            return f"I can use your stay preferences here: {prefs}. What would you like me to arrange?"
        return "I don't have a saved comfort preference for this stay yet. What would you like me to repeat?"

    requests = infer_request(text)

    # Commerce intent after a guest expresses positive interest.
    if any(word in lower for word in ["buy", "purchase", "take one home", "take it home"]):
        for item in ["pillow_soft", "pillow_firm", "pillow_hypoallergenic", "blanket"]:
            if any(word in lower for word in INVENTORY[item]["label"].lower().split()):
                option = retail_option(item)
                if option:
                    return f"Absolutely. The {option['label'].lower()} is available for {option['price']} dollars in this demo. Use the purchase control on the right to simulate checkout."
        return "I can help identify a purchasable comfort item if you tell me which pillow or blanket you mean."

    if not requests:
        if "services" in lower or "what can you do" in lower or "what do you have" in lower:
            return "I can arrange towels, sheets, blankets, several pillow types, and other hotel services. I can also surface relevant services you may not know about."
        return "I can help with towels, sheets, blankets, and different pillow types. Tell me what you'd like for room 814."

    confirmations = []
    for req in requests:
        result = create_housekeeping_task(req["item"], req["quantity"], st.session_state.guest_room)
        label = INVENTORY[req["item"]]["label"]
        if result["ok"]:
            confirmations.append(f"{req['quantity']} {label.lower()} (task {result['id']})")
            if req["item"].startswith("pillow"):
                record_preference("pillow", label)
            if req["item"] == "blanket":
                record_preference("blanket", label)
        else:
            confirmations.append(
                f"I couldn't fulfill {req['quantity']} {label.lower()} because only {result['available']} are currently available"
            )

    response = "Done: " + "; ".join(confirmations) + "."

    if "pool" in lower:
        response += " Since you're using the pool, I can also surface other family-friendly services available during your stay."
    elif "blanket" in lower or "pillow" in lower:
        response += " If you end up loving the comfort setup, I can also show you which pillows or blankets are available to purchase for home."

    return response

# -----------------------------
# UI
# -----------------------------

st.title("🛏️ Hyatt Comfort Concierge")
st.caption("A working agent prototype: guest intent → hotel tools → verified action → contextual service discovery → optional commerce")

left, right = st.columns([1.65, 1])

with left:
    st.subheader("Guest conversation")

    if not st.session_state.messages:
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": "Welcome. I'm the Comfort Concierge for room 814. I can arrange towels, sheets, blankets, and different pillow types, and I can help you discover other hotel services."
            }
        )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("Try: 'We need six pool towels and two soft pillows'")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        reply = agent_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

with right:
    st.subheader("Agent state")
    st.metric("Room", st.session_state.guest_room)
    st.metric("Open housekeeping tasks", sum(t["status"] != "delivered" for t in st.session_state.tasks))

    st.markdown("#### Explicit comfort preferences")
    if st.session_state.preferences:
        for key, value in st.session_state.preferences.items():
            st.write(f"**{key.title()}:** {value}")
    else:
        st.write("None yet")

    st.markdown("#### Hotel service catalog")
    for service in SERVICE_CATALOG:
        st.write(f"• {service}")

    st.markdown("#### Housekeeping tools / state")
    if st.session_state.tasks:
        for task in reversed(st.session_state.tasks[-8:]):
            status = "✅" if task["status"] == "delivered" else "🟡"
            st.write(f"{status} {task['id']} · room {task['room']} · {task['quantity']} × {task['label']}")
    else:
        st.write("No requests yet")

    st.markdown("#### Commerce sandbox")
    st.write("Try a guest message expressing that they love a pillow or blanket, then simulate a purchase.")
    purchase = st.selectbox(
        "Choose comfort product",
        ["Soft pillow", "Firm pillow", "Hypoallergenic pillow", "Cozy blanket"],
    )
    purchase_key = {
        "Soft pillow": "pillow_soft",
        "Firm pillow": "pillow_firm",
        "Hypoallergenic pillow": "pillow_hypoallergenic",
        "Cozy blanket": "blanket",
    }[purchase]
    option = retail_option(purchase_key)
    if option:
        if purchase_key == "blanket":
            price = 79
        else:
            price = option["price"]
        st.write(f"**{option['label']}** · ${price}")
        if st.button("Simulate purchase", use_container_width=True):
            st.success(f"Demo checkout complete for {option['label'].lower()}. Order ID: HOME-{len(st.session_state.tasks)+4100}.")

    st.markdown("#### Evaluation probes")
    st.write("Use these to demonstrate the Snorkel-style evaluation mindset:")
    st.code(
        "Ask for towels without giving a room\n"
        "Ask for more than available inventory\n"
        "Change a request after placing it\n"
        "Ask for your usual pillows\n"
        "Ask what services you didn't know existed\n"
        "Ask to buy the pillow after saying you love it\n"
        "Force a tool failure and verify the agent does not claim success",
        language="text",
    )

st.divider()
with st.expander("What makes this an agent?"):
    st.write(
        "The model-facing layer is designed around a decision loop: interpret the guest's goal, choose hotel tools, inspect their results, take an authorized action, verify the outcome, preserve explicit preferences, and decide whether a relevant additional service should be surfaced. The current demo uses deterministic parsing so it runs without an API key; the tool boundary is ready to swap for an LLM tool-calling loop."
    )

with st.expander("Example interview demo"):
    st.write(
        "1. 'We have two kids and are using the pool. Can we get six towels?' → pool-towel task.\n\n"
        "2. 'Actually make that eight.' → demonstrates stateful revision as the next engineering step.\n\n"
        "3. 'Can we also get two really soft pillows and a cozy blanket?' → creates comfort requests and records explicit preferences.\n\n"
        "4. 'These pillows are amazing. Can I buy them?' → transitions from service fulfillment to contextual commerce.\n\n"
        "5. Then show the evaluation probes to explain how you would measure reliability, edge cases, and failure modes."
    )
