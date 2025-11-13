SYSTEM_PROMPT = (
    "Eres un asistente RAG. Responde en español, citando hallazgos del CONTEXTO cuando sea útil. "
    "Si la respuesta no está en el contexto, dilo claramente. Sé conciso y técnico cuando aplique."
)

def build_prompt(question: str, context: str) -> str:
    return (
        f"[SISTEMA]\n{SYSTEM_PROMPT}\n\n"
        f"[CONTEXTO]\n{context}\n\n"
        f"[PREGUNTA]\n{question}\n\n"
        f"[INSTRUCCIONES]\nResponde usando el CONTEXTO."
    )
