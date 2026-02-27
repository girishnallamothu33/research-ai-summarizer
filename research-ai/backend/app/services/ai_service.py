import openai
from app.config import settings
import json

openai.api_key = settings.OPENAI_API_KEY

def generate_summary(text: str, discipline: str) -> dict:
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_openai_api_key_here":
        # Mock response if no API key
        return {
            "short_summary": f"[{discipline} Context] A mock 5-line summary of the document. It highlights the main thesis, methodology, results, implications, and future work. Provide a valid OpenAI key in .env for real results.",
            "detailed_summary": f"This is a detailed mock summary focusing on {discipline}. The paper presents an innovative approach to solving existing problems in the field. It introduces new metrics and validates them against standard benchmarks, showing a 15% improvement.",
            "keywords": ["mock data", "api missing", discipline, "placeholder", "demo analysis"],
            "key_insights": [
                "The primary insight is testing the system architecture successfully.",
                "Real AI text generation requires an active OpenAI API key.",
                "The methodology successfully parses and routes PDFs.",
                f"From a {discipline} perspective, this is a simulated response."
            ],
            "discipline_interpretation": f"This indicates that the software structure is ready for actual {discipline} researchers once the API key is configured."
        }
        
    prompt = f"""
    Analyze the following research text and provide a JSON response customized for the '{discipline}' discipline.
    Ensure the JSON structure exactly matches:
    {{
      "short_summary": "A 5-line summary",
      "detailed_summary": "In-depth summary",
      "keywords": ["keyword1", "keyword2"],
      "key_insights": ["insight1", "insight2"],
      "discipline_interpretation": "Interpretation specific to {discipline}"
    }}
    
    Text:
    {text[:8000]} # Limit to avoid context token issues for standard models
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a specialized academic researcher. Respond only with valid JSON matching the exact schema provided."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        return {
            "short_summary": "Error generating summary",
            "detailed_summary": f"Exception occurred: {str(e)}",
            "keywords": ["error"],
            "key_insights": [],
            "discipline_interpretation": ""
        }

def get_cross_domain_ideas(text: str):
    return {
        "ideas": [
            "Apply AI architectures to molecular biology data.",
            "Utilize statistical physics models in economic forecasting."
        ]
    }
