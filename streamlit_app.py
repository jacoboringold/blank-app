import re
from datetime import datetime
from typing import Any, Dict, List

import streamlit as st

st.set_page_config(page_title="Hyatt Comfort Concierge", page_icon="🛏️", layout="wide")

# Demo inventory. In production these would come from hotel systems.
INVENTORY = {
    "bath_towel": {"label": "Bath towels", "stock": 40, "limit": 8, "price": None},
    "hand_towel": {"label": "Hand towels", "stock": 35, "limit": 8, "price": None},
    "washcloth": {"label": "Washcloths", "stock": 30, "limit": 8, "price": None},
    "pool_towel": {"label": "Pool towels", "stock": 28, "limit": 10, "price": None},
    "sheet_set": {"label": "Fresh sheet sets", "stock": 18, "limit": 3, "price": None},
    "blanket": {"label": "Cozy blankets", "stock": 14, "limit": 3, "price": 79},
    "pillow_soft": {"label": "Soft pillows", "stock": 10, "limit": 4, "price": 59},
    "pillow_firm": {"label": "Firm pillows", "stock": 12, "limit": 4, "price": 59},
    "pillow_hypoallergenic": {"label": "Hypoallergenic pillows", "stock": 8, "limit": 4, "price": 69},
}

SERVICE_CATALOG = [
    "Extra towels and pool towels",
    "Fresh sheets and cozy blankets",
    "Soft, firm, and hypoallergenic pillows",
    "Cribs and family amenities",
    "Dining and room-service recommendations",
    "Comfort products available for purchase",
]

SUGGESTIONS = {
    "pool": ["pool towels", "family-friendly dining", "children's amenities"],
    "blanket": ["soft or firm pillows", "comfort-product purchase", "late-night dining"],
    "pillow": ["another pillow type", "cozy blanket", "purchase this pillow for home"],
}

if "messages" not in st.session_state:
    st.session_state.messages = []
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "preferences" not in st.session_state:
    st.session_state.preferences = {}
if "guest_room" not in st.session_state:
    st.session_state.guest_room = ""


def check_inventory(item: str, quantity: int) -> Dict[str, Any]:
    record = INVENTORY[item]
    if quantity > record["limit"]:
        return {"ok": False, "reason": "limit", "available": record["stock"], "limit": record["limit"]}
    if quantity > record["stock"]:
        return {"ok": False, "reason": "inventory", "available": record["stock"], "limit": record["limit"]}
    return {"ok": True, "available": record["stock"], "limit": record["limit"]}


def create_housekeeping_task(item: str, quantity: int, room: str, special: str = "") -> Dict[str, Any]:
    result = check_inventory(item, quantity)
    if not result["ok"]:
        return {"ok": False, **result}
    INVENTORY[item]["stock"] -= quantity
    task_id = f"HK-{len(st.session_state.tasks) + 1001}"
    task = {
        "id": task_id,
        "room": room,
        "item": item,
        "label": INVENTORY[item]["label"],
        "quantity": quantity,
        "special": special.strip(),
        "status": "accepted",
        "created_at": datetime.now().strftime("%H:%M:%S"),
    }
    st.session_state.tasks.append(task)
    return {"ok": True, **task}


def record_preference(category: str, value: str) -> None:
    st.session_state.preferences[category] = value


def retail_price(item: str):
    return INVENTORY[item]["price"]


def parse_quantity(text: str, default: int = 1) -> int:
    words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
    for word, value in words.items():
        if re.search(rf"\b{word}\b", text):
            return value
    match = re.search(r"\b(\d+)\b", text)
    return int(match.group(1)) if match else default


def infer_requests(text: str) -> List[Dict[str, Any]]:
    t = text.lower()
    q = parse_quantity(t)
    found = []
    if "pool towel" in t or ("pool" in t and "towel" in t):
        found.append({"item": "pool_towel", "quantity": q})
    elif "towel" in t:
        found.append({"item": "bath_towel", "quantity": q})
    if "hand towel" in t:
        found.append({"item": "hand_towel", "quantity": q})
    if "washcloth" in t:
        found.append({"item": "washcloth", "quantity": q})
    if "sheet" in t:
        found.append({"item": "sheet_set", "quantity": q})
    if "blanket" in t:
        found.append({"item": "blanket", "quantity": q})
    if "soft pillow" in t:
        found.append({"item": "pillow_soft", "quantity": q})
    elif "firm pillow" in t:
        found.append({"item": "pillow_firm", "quantity": q})
    elif "hypoallergenic" in t or "allergy pillow" in t:
        found.append({"item": "pillow_hypoallergenic", "quantity": q})
    elif "pillow" in t:
        found.append({"item": "pillow_soft", "quantity": q})
    return found


def agent_response(user_text: str) -> str:
    text = user_text.strip()
    lower = text.lower()
    if not text:
        return "Tell me what would make your room more comfortable."
    if not st.session_state.guest_room:
        return "First, enter your room number in the Order Up panel. Then I can place requests for you."
    if "usual" in lower or "same as" in lower:
        if st.session_state.preferences:
            prefs = ", ".join(st.session_state.preferences.values())
            return f"I remember these explicit preferences from this stay: {prefs}. Tell me what you'd like me to arrange."
        return "I don't have a comfort preference recorded yet. Tell me which pillow, blanket, or linen setup you want me to remember."
    if any(x in lower for x in ["services", "what else", "what can you do", "don't know", "dont know"]):
        return "I can arrange towels, pool towels, sheets, blankets, several pillow types, and family amenities. I can also surface relevant hotel services you may not know about, without adding anything to your order unless you ask."

    requests = infer_requests(text)
    if not requests:
        return "I can help with towels, sheets, blankets, and soft, firm, or hypoallergenic pillows. You can also use the Order Up panel to place a precise request."

    confirmations = []
    for req in requests:
        result = create_housekeeping_task(req["item"], req["quantity"], st.session_state.guest_room)
        label = INVENTORY[req["item"]]["label"]
        if result["ok"]:
            confirmations.append(f"{req['quantity']} {label.lower()} via {result['id']}")
            if req["item"].startswith("pillow"):
                record_preference("pillow", label)
            if req["item"] == "blanket":
                record_preference("blanket", label)
        elif result["reason"] == "limit":
            confirmations.append(f"I can only send up to {result['limit']} {label.lower()} in one request")
        else:
            confirmations.append(f"only {result['available']} {label.lower()} remain in this demo inventory")

    response = "Done: " + "; ".join(confirmations) + "."
    if "pool" in lower:
        response += " Since you're using the pool, I can also surface family-friendly services available during your stay."
    if "pillow" in lower or "blanket" in lower:
        response += " If you love the setup, those comfort products can also be purchased for home."
    return response


st.title("🛏️ Hyatt Comfort Concierge")
st.caption("Guest service agent prototype • fulfillment + context + discovery + optional commerce")

# Top room identity bar
room_col, status_col = st.columns([1, 2])
with room_col:
    room = st.text_input("Room number", value=st.session_state.guest_room, placeholder="e.g. 814")
    if room != st.session_state.guest_room:
        st.session_state.guest_room = room.strip()
with status_col:
    if st.session_state.guest_room:
        st.success(f"Requests will be routed to room {st.session_state.guest_room}.")
    else:
        st.info("Enter your room number before placing an order.")

left, right = st.columns([1.25, 1], gap="large")

# ---------------- CHAT ----------------
with left:
    st.subheader("💬 Concierge chat")
    st.caption("Ask naturally. The agent can also explain what other services are available.")

    if not st.session_state.messages:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Welcome. Tell me what would make your room more comfortable. I can arrange towels, sheets, blankets, pillows, and more."
        })
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("Try: 'We have four kids at the pool. Can we get six towels?'")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": agent_response(prompt)})
        st.rerun()

# ---------------- ORDER-UP KIOSK ----------------
with right:
    st.subheader("🧺 Order Up")
    st.caption("A simple, precise kiosk for guests who already know what they need.")

    items = [
        ("bath_towel", "Bath towels"),
        ("hand_towel", "Hand towels"),
        ("washcloth", "Washcloths"),
        ("pool_towel", "Pool towels"),
        ("sheet_set", "Fresh sheet sets"),
        ("blanket", "Cozy blankets"),
        ("pillow_soft", "Soft pillows"),
        ("pillow_firm", "Firm pillows"),
        ("pillow_hypoallergenic", "Hypoallergenic pillows"),
    ]
    selected = st.selectbox("What do you need?", items, format_func=lambda x: x[1])
    key, label = selected
    record = INVENTORY[key]
    quantity = st.number_input(
        "Quantity",
        min_value=1,
        max_value=record["limit"],
        value=1,
        step=1,
        help=f"Maximum {record['limit']} per request.",
    )
    st.caption(f"Request limit: {record['limit']} • Currently available: {record['stock']}")

    special = st.text_area(
        "Special instructions",
        placeholder="Examples: Please leave outside the door. Two pillows should be firm. Please deliver before 8 PM.",
        height=90,
    )

    if st.button("Request it →", type="primary", use_container_width=True):
        if not st.session_state.guest_room:
            st.error("Please enter your room number first.")
        else:
            result = create_housekeeping_task(key, int(quantity), st.session_state.guest_room, special)
            if result["ok"]:
                if key.startswith("pillow"):
                    record_preference("pillow", label)
                if key == "blanket":
                    record_preference("blanket", label)
                st.success(f"Requested {quantity} × {label}. Task {result['id']} is accepted.")
                if record["price"]:
                    st.info(f"Like it? This {label.lower()} is also available for home purchase at ${record['price']}.")
            elif result["reason"] == "limit":
                st.error(f"That's above the request limit. Please request no more than {result['limit']} at a time.")
            else:
                st.error(f"Only {result['available']} are available in this demo inventory.")

    st.markdown("#### Discover services")
    st.write("You don't need to know everything the hotel offers. Ask the concierge:")
    if st.button("What else can you help me with?", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "What else can you help me with?"})
        st.session_state.messages.append({"role": "assistant", "content": agent_response("What else can you help me with?")})
        st.rerun()

# ---------------- BOTTOM STATE / DEMO ----------------
st.divider()
state_left, state_mid, state_right = st.columns(3)
with state_left:
    st.markdown("#### 🧹 Housekeeping queue")
    if st.session_state.tasks:
        for task in reversed(st.session_state.tasks[-6:]):
            note = f" • {task['special']}" if task["special"] else ""
            st.write(f"🟡 **{task['id']}** · Room {task['room']} · {task['quantity']} × {task['label']}{note}")
    else:
        st.write("No requests yet.")
with state_mid:
    st.markdown("#### 🛏️ Explicit preferences")
    if st.session_state.preferences:
        for k, v in st.session_state.preferences.items():
            st.write(f"**{k.title()}:** {v}")
    else:
        st.write("None recorded yet.")
with state_right:
    st.markdown("#### 🛍️ Comfort shop")
    for key in ["blanket", "pillow_soft", "pillow_firm", "pillow_hypoallergenic"]:
        price = retail_price(key)
        if price:
            st.write(f"{INVENTORY[key]['label']} · **${price}**")

with st.expander("🎯 Interview demo: why this is an agent"):
    st.write(
        "The chat interface handles ambiguous natural language. The Order Up kiosk handles structured requests with visible limits, room routing, and special instructions. Both feed the same operational tools and state. The agent can interpret intent, check inventory and request limits, create a verified housekeeping task, remember explicit comfort preferences, and surface relevant services or comfort products."
    )
    st.code(
        "1. Enter room 814.\n"
        "2. Chat: 'We're taking the kids to the pool. Can we get six towels?'\n"
        "3. Use Order Up: two soft pillows + special instruction.\n"
        "4. Ask: 'What else do you offer?'\n"
        "5. Say: 'These pillows are amazing. Can I buy them?'\n"
        "6. Try to exceed a request limit and watch the agent refuse safely."
    )
