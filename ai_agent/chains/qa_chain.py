"""
qa_chain.py  –  General-purpose QA chain with
               • dynamic tool use (blockchain + Tavily search)
               • automatic intent detection
               • robust content extraction (price / definition / how-to / general)
               • full reasoning trace + logging
"""

import re
from typing import Optional, List

from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, AgentType

from ai_agent.tools.tools import blockchain_tool, search_tool
from ai_agent.logger import log_query
from ai_agent.access_control import check_permission


# --------------------------------------------------------------------------- #
#  Utility helpers                                                            #
# --------------------------------------------------------------------------- #

def _extract_lkr_prices(text: str) -> List[int]:
    """Return every LKR price found in text as an int list."""
    matches = re.findall(r"LKR[\s\xa0]*([0-9][0-9,]{2,})", text, flags=re.I)
    prices = []
    for m in matches:
        try:
            price = int(m.replace(",", ""))
            if 100_000 <= price <= 50_000_000:  # sane Sri-Lankan car range
                prices.append(price)
        except ValueError:
            pass
    return prices


def _clean_sentences(blob: str) -> List[str]:
    return [s.strip() for s in blob.split(".") if len(s.strip()) > 20]


# --------------------------------------------------------------------------- #
#  QAChain                                                                    #
# --------------------------------------------------------------------------- #

class QAChain:
    """Single-entry QA chain that can answer both blockchain and open-web queries."""

    def __init__(self, max_iterations: int = 3):
        self.llm = ChatOllama(model="llama3.1")

        # Only single-input tools – compatible with classic LangChain agents
        self.agent = initialize_agent(
            tools=[blockchain_tool, search_tool],
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=max_iterations,
        )

        self.max_iterations = max_iterations
        self.explanation_steps: List[str] = []

    # ------------------------------------------------------------------ #
    #  Intent & extraction helpers                                        #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _intent(query: str) -> str:
        q = query.lower()
        if any(w in q for w in ("price", "cost", "value", "lkr", "$")):
            return "price"
        if any(w in q for w in ("how to", "steps", "guide")):
            return "how_to"
        if any(w in q for w in ("define", "what is", "meaning")):
            return "definition"
        return "general"

    @staticmethod
    def _is_complete(text: str) -> bool:
        return (
            len(text) > 40
            and not any(t in text for t in ("'title':", "Observation:", "Action:"))
            and text.rstrip()[-1] in ".!?"
        )

    # ------------------------------------------------------------------ #
    #  Core extraction                                                    #
    # ------------------------------------------------------------------ #

    def _extract_answer(self, raw: str, query: str) -> Optional[str]:
        """Turn the raw agent output into a clean, final answer."""
        if not raw or "Agent stopped" in raw:
            return None

        # 1) If agent already produced a nice sentence – keep it
        if self._is_complete(raw):
            return raw.strip()

        intent = self._intent(query)

        # 2) Handle PRICE queries
        if intent == "price":
            prices = _extract_lkr_prices(raw)
            if prices:
                prices = sorted(set(prices))
                if len(prices) == 1:
                    return (
                        f"Current market data shows a price of about "
                        f"LKR {prices[0]:,} for {query.strip('?')}"
                    )
                return (
                    f"Current listings show a range of "
                    f"LKR {prices[0]:,} – LKR {prices[-1]:,} "
                    f"for {query.strip('?')} (condition and trim dependent)."
                )

        # 3) Simple “definition / how-to / general” heuristics
        sentences = _clean_sentences(raw)
        if sentences:
            # pick first sentence that contains a keyword from query
            key_words = set(query.lower().split())
            for s in sentences:
                if key_words & set(s.lower().split()):
                    return s + "."
            return sentences[0] + "."

        return None

    # ------------------------------------------------------------------ #
    #  Main .run()                                                       #
    # ------------------------------------------------------------------ #

    def run(self, query: str, user_id: str = "default_user"):
        self.explanation_steps.clear()
        self.explanation_steps.append(f"Received query: {query}")

        # Permission check
        try:
            check_permission(user_id, self._entity_type(query))
            self.explanation_steps.append("Permission check passed.")
        except Exception as exc:
            self.explanation_steps.append(f"Permission denied: {exc}")
            return "Access denied.", "\n".join(self.explanation_steps)

        # Loop through reasoning iterations
        answer = None
        for step in range(1, self.max_iterations + 1):
            self.explanation_steps.append(f"Step {step}: invoking agent")
            raw = self.agent.run(query)
            self.explanation_steps.append(f"Raw agent output captured.")

            answer = self._extract_answer(raw, query)
            if answer:
                self.explanation_steps.append("Answer extracted successfully.")
                break

        if not answer:
            answer = (
                "I found some relevant information but couldn't extract a clear answer. "
                "Please try re-phrasing the question."
            )
            self.explanation_steps.append("Fallback generic response used.")

        # Log & return
        log_query(user_id, query, answer)
        return answer, "\n".join(self.explanation_steps)

    # ------------------------------------------------------------------ #
    #  Helpers                                                           #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _entity_type(query: str) -> str:
        q = query.lower()
        if any(w in q for w in ("vehicle", "car")):
            return "vehicle"
        if any(w in q for w in ("land", "property")):
            return "land"
        return "general"

    # Convenience wrapper for legacy calls
    def handle_query(self, query: str, user_id: str = "default_user"):
        ans, _ = self.run(query, user_id)
        return ans


# --------------------------------------------------------------------------- #
#  CLI test                                                                   #
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    chain = QAChain()
    uid = "test_user_1"
    q = input("Enter your query: ")
    ans, trace = chain.run(q, uid)
    print("\nAnswer:\n", ans)
    print("\n--- Explanation Trace ---")
    print(trace)
