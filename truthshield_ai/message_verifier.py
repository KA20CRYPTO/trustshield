from rag_engine import rag_engine

class MessageVerifier:
    def __init__(self):
        self.rag = rag_engine

    def verify_message(self, message):
        """
        Verifies a message using RAG and returns a structured result.
        Returns:
            dict: {
                "status": "Safe" | "Unsafe" | "Unverified",
                "explanation": str
            }
        """
        try:
            qa_chain = self.rag.get_qa_chain()
            if not qa_chain:
                return {
                    "status": "Unverified",
                    "explanation": "System could not initialize RAG engine."
                }
            
            # The prompt in rag_engine is designed to return the classification + explanation
            # Format expected: "[Status] Explanation..."
            response = qa_chain.run(message)
            
            # Simple parsing of the response
            # Note: LLM output is not always deterministic, so we robustly check for keywords
            response_lower = response.lower()
            
            status = "Unverified"
            if "safe" in response_lower and "unsafe" not in response_lower.replace("safe", ""): # Avoid matching "unsafe" as "safe"
                 # Check if it starts with Safe or is classified as Safe
                 if "safe" in response_lower[:10]:
                     status = "Safe"
            
            if "unsafe" in response_lower:
                if "unsafe" in response_lower[:10]:
                    status = "Unsafe"
            
            if "unverified" in response_lower:
                 if "unverified" in response_lower[:15]:
                    status = "Unverified"

            # Clean up explanation
            # Heuristic: Remove the status word if it appears at the start
            explanation = response
            for s in ["Safe", "Unsafe", "Unverified", "safe", "unsafe", "unverified"]:
                if explanation.lower().startswith(s):
                    explanation = explanation[len(s):].strip(" .:-")
                    break
            
            # Formatting checks
            if not explanation:
                explanation = response # Fallback

            return {
                "status": status,
                "explanation": explanation
            }
            
        except Exception as e:
            return {
                "status": "Unverified",
                "explanation": f"Error during verification: {str(e)}"
            }
