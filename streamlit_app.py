import re
from datetime import datetime
from typing import Any, Dict, List

import streamlit as st

st.set_page_config(page_title="Hyatt Comfort Concierge", page_icon="🛏️", layout="centered", initial_sidebar_state="collapsed")

# Mobile-first styling for iPhone Safari / small screens.
st.markdown("""
<style>
.block-container { max-width: 760px; padding: .7rem .65rem 5rem; }
header { visibility: hidden; height: 0; }
.stButton > button { min-height: 46px; border-radius: 12px; font-size: 16px; }
.stTextInput input, .stNumberInput input, textarea { font-size: 16px !important; border-radius: 10px; }
.stSelectbox [data-baseweb="select"] { min-height: 46px; }
[data-testid="stChatInput"] { bottom: .4rem; }
@media (max-width: 700px) {
  .block-container { padding: .55rem .5rem 5rem; }
  h1 { font-size: 1.55rem !important; }
  h2 { font-size: 1.25rem !important; }
  h3 { font-size: 1.08rem !important; }
}
</style>
""", unsafe_allow_html=True)

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

if "messages" not in st.session_state: st.session_state.messages = []
if "tasks" not in st.session_state: st.session_state.tasks = []
if "preferences" not in st.session_state: st.session_state.preferences = {}
if "guest_room" not in st.session_state: st.session_state.guest_room = ""


def check_inventory(item: str, quantity: int) -> Dict[str, Any]:
    record = INVENTORY[item]
    if quantity > record["limit"]:
        return {"ok": False, "reason": "limit", "available": record["stock"], "limit": record["limit"]}
    if quantity > record["stock"]:
        return {"ok": False, "reason": "inventory", "available": record["stock"], "limit": record["limit"]}
    return {"ok": True, "available": record["stock"], "limit": record["limit"]}


def create_housekeeping_task(item: str, quantity: int, room: str, special: str = "") -> Dict[str, Any]:
    result = check_inventory(item, quantity)
    if not result["ok"]: return {"ok": False, **result}
    INVENTORY[item]["stock"] -= quantity
    task_id = f"HK-{len(st.session_state.tasks) + 1001}"
    task = {"id": task_id, "room": room, "item": item, "label": INVENTORY[item]["label"], "quantity": quantity,
            "special": special.strip(), "status": "accepted", "created_at": datetime.now().strftime("%H:%M:%S")}
    st.session_state.tasks.append(task)
    return {"ok": True, **task}


def parse_quantity(text: str, default: int = 1) -> int:
    words = {"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10}
    for word, value in words.items():
        if re.search(rf"\b{word}\b", text): return value
    match = re.search(r"\b(\d+)\b", text)
    return int(match.group(1)) if match else default


def infer_requests(text: str) -> List[Dict[str, Any]]:
    t = text.lower(); q = parse_quantity(t); found = []
    if "pool towel" in t or ("pool" in t and "towel" in t): found.append({"item":"pool_towel","quantity":q})
    elif "towel" in t: found.append({"item":"bath_towel","quantity":q})
    if "hand towel" in t: found.append({"item":"hand_towel","quantity":q})
    if "washcloth" in t: found.append({"item":"washcloth","quantity":q})
    if "sheet" in t: found.append({"item":"sheet_set","quantity":q})
    if "blanket" in t: found.append({"item":"blanket","quantity":q})
    if "soft pillow" in t: found.append({"item":"pillow_soft","quantity":q})
    elif "firm pillow" in t: found.append({"item":"pillow_firm","quantity":q})
    elif "hypoallergenic" in t or "allergy pillow" in t: found.append({"item":"pillow_hypoallergenic","quantity":q})
    elif "pillow" in t: found.append({"item":"pillow_soft","quantity":q})
    return found


def agent_response(text: str) -> str:
    lower = text.lower().strip()
    if not st.session_state.guest_room: return "Please enter your room number above first, then I can place a request."
    if "usual" in lower or "same as" in lower:
        if st.session_state.preferences: return "I remember: " + ", ".join(st.session_state.preferences.values()) + ". What should I arrange?"
        return "I don't have a comfort preference recorded yet. Tell me which setup you want me to remember."
    if any(x in lower for x in ["services", "what else", "what can you do", "don't know", "dont know"]):
        return "I can arrange towels, pool towels, fresh sheets, cozy blankets, several pillow types, family amenities, and dining help. I can also surface relevant services without adding anything to your order unless you ask."
    requests = infer_requests(text)
    if not requests: return "I can help with towels, sheets, blankets, and soft, firm, or hypoallergenic pillows. Or use Order Up below for a precise request."
    confirmations = []
    for req in requests:
        result = create_housekeeping_task(req["item"], req["quantity"], st.session_state.guest_room)
        label = INVENTORY[req["item"]]["label"]
        if result["ok"]:
            confirmations.append(f"{req['quantity']} {label.lower()} · {result['id']}")
            if req["item"].startswith("pillow"): st.session_state.preferences["pillow"] = label
            if req["item"] == "blanket": st.session_state.preferences["blanket"] = label
        elif result["reason"] == "limit": confirmations.append(f"maximum {result['limit']} {label.lower()} per request")
        else: confirmations.append(f"only {result['available']} {label.lower()} remain")
    response = "Done: " + "; ".join(confirmations) + "."
    if "pool" in lower: response += " Since you're using the pool, I can also tell you about family-friendly services."
    if "pillow" in lower or "blanket" in lower: response += " If you love the setup, I can show you comfort products available for home."
    return response


st.title("🛏️ Hyatt Comfort Concierge")
st.caption("A mobile-first guest service agent")

room = st.text_input("ROOM NUMBER", value=st.session_state.guest_room, placeholder="814")
st.session_state.guest_room = room.strip()
if st.session_state.guest_room: st.success(f"Ready for room {st.session_state.guest_room}")
else: st.info("Enter your room number to begin.")

st.subheader("💬 Concierge")
if not st.session_state.messages:
    st.session_state.messages.append({"role":"assistant","content":"Hi! What would make your room more comfortable? I can arrange towels, sheets, blankets, pillows, and more."})
for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.write(message["content"])
prompt = st.chat_input("Ask for towels, pillows, blankets…")
if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    st.session_state.messages.append({"role":"assistant","content":agent_response(prompt)})
    st.rerun()

st.divider()
st.subheader("🧺 Order Up")
st.caption("Fast controls for guests who already know what they need.")

categories = {
    "Towels": [("bath_towel","Bath towels"),("hand_towel","Hand towels"),("washcloth","Washcloths"),("pool_towel","Pool towels")],
    "Bedding": [("sheet_set","Fresh sheets"),("blanket","Cozy blankets")],
    "Pillows": [("pillow_soft","Soft"),("pillow_firm","Firm"),("pillow_hypoallergenic","Hypoallergenic")],
}
selected = st.session_state.get("selected_item", "bath_towel")
for category, choices in categories.items():
    st.markdown(f"**{category}**")
    labels = [x[1] for x in choices]
    current_label = next((label for key,label in choices if key == selected), labels[0])
    picked_label = st.radio(category, labels, index=labels.index(current_label), horizontal=True, label_visibility="collapsed")
    selected = next(key for key,label in choices if label == picked_label)

record = INVENTORY[selected]
quantity = st.number_input("QUANTITY", min_value=1, max_value=record["limit"], value=1, step=1)
st.caption(f"Maximum {record['limit']} per request · {record['stock']} currently available")
special = st.text_area("SPECIAL REQUESTS", placeholder="Please leave outside the door • Two pillows firm • Before 8 PM", height=82)

if st.button("🛎️ REQUEST IT", type="primary", use_container_width=True):
    if not st.session_state.guest_room:
        st.error("Enter your room number first.")
    else:
        result = create_housekeeping_task(selected, int(quantity), st.session_state.guest_room, special)
        if result["ok"]:
            if selected.startswith("pillow"): st.session_state.preferences["pillow"] = record["label"]
            if selected == "blanket": st.session_state.preferences["blanket"] = record["label"]
            st.success(f"Requested {quantity} × {record['label']}. Request {result['id']} accepted.")
            if record["price"]: st.info(f"Love it? The {record['label'].lower()} is available for home purchase at ${record['price']}.")
        elif result["reason"] == "limit": st.error(f"Maximum {result['limit']} per request.")
        else: st.error(f"Only {result['available']} are available right now.")

st.divider()
st.subheader("🛍️ Comfort Shop")
st.caption("Loved something during your stay? Take the comfort home.")
merch = [("blanket","Cozy blanket",79),("pillow_soft","Soft pillow",59),("pillow_firm","Firm pillow",59),("pillow_hypoallergenic","Hypoallergenic pillow",69)]
for key, label, price in merch:
    c1, c2 = st.columns([2,1])
    with c1: st.write(f"**{label}**\n\n${price}")
    with c2:
        if st.button("ADD", key=f"add_{key}", use_container_width=True): st.success(f"Added {label.lower()} to demo cart.")

st.divider()
st.subheader("✨ Discover more")
if st.button("What else can you help me with?", use_container_width=True):
    if not st.session_state.guest_room: st.info("Enter your room number first.")
    else:
        st.session_state.messages.append({"role":"user","content":"What else can you help me with?"})
        st.session_state.messages.append({"role":"assistant","content":agent_response("What else can you help me with?")})
        st.rerun()

with st.expander("Housekeeping status"):
    if st.session_state.tasks:
        for task in reversed(st.session_state.tasks[-8:]):
            note = f" · {task['special']}" if task["special"] else ""
            st.write(f"🟡 **{task['id']}** · Room {task['room']} · {task['quantity']} × {task['label']}{note}")
    else: st.write("No requests yet.")

with st.expander("Explicit comfort preferences"):
    if st.session_state.preferences:
        for k,v in st.session_state.preferences.items(): st.write(f"**{k.title()}:** {v}")
    else: st.write("None recorded yet.")

with st.expander("🎯 Interview story"):
    st.write("Chat handles ambiguity. Order Up handles precise fulfillment. Both use the same hotel tools and state. The agent checks limits and inventory, routes the request to a room, records explicit preferences, surfaces services, and connects a successful comfort interaction to optional commerce.")
