import errno
import gradio as gr
import json
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

MAX_INPUT_LENGTH = 100_000

def analyze_text(text: str) -> str:
    """Analyze text and return statistics.
    
    Args:
        text: The input text to analyze
    
    Returns:
        JSON string with analysis results
    """
    try:
        if text is None or not isinstance(text, str):
            logger.warning("analyze_text received invalid input: %r", text[:200] if isinstance(text, str) else text)
            return json.dumps({"error": "Invalid input: text must be a non-empty string"})
        if len(text) > MAX_INPUT_LENGTH:
            logger.warning("analyze_text received oversized input: %r", text[:200])
            return json.dumps({"error": "Input too large: maximum length is 100000 characters"})
        if not text or text.isspace():
            logger.warning("analyze_text received empty input: %r", text[:200])
            return json.dumps({"error": "No text to analyze"})
        words = text.split()
        chars = len(text)
        chars_no_spaces = len(text.replace(" ", ""))
        sentences = sum(1 for c in text if c in ".!?")
        
        avg_word_length = round(chars_no_spaces / len(words), 2) if words else 0
        avg_sentence_length = round(len(words) / max(sentences, 1), 2)
        
        return json.dumps({
            "total_characters": chars,
            "characters_without_spaces": chars_no_spaces,
            "total_words": len(words),
            "total_sentences": max(sentences, 1),
            "average_word_length": avg_word_length,
            "average_sentence_length": avg_sentence_length
        }, indent=2)
    except Exception as e:
        logger.exception("analyze_text failed unexpectedly")
        return json.dumps({"error": "An unexpected error occurred"})

def extract_keywords(text: str, count: int = 5) -> str:
    """Extract keywords (most common words) from text.
    
    Args:
        text: The input text
        count: Number of keywords to return (default 5)
    
    Returns:
        JSON string with keywords and frequencies
    """
    try:
        if text is None or not isinstance(text, str):
            logger.warning("extract_keywords received invalid input: %r", text[:200] if isinstance(text, str) else text)
            return json.dumps({"error": "Invalid input: text must be a non-empty string"})
        if len(text) > MAX_INPUT_LENGTH:
            logger.warning("extract_keywords received oversized input: %r", text[:200])
            return json.dumps({"error": "Input too large: maximum length is 100000 characters"})
        if not text or text.isspace():
            logger.warning("extract_keywords received empty input: %r", text[:200])
            return json.dumps({"error": "No text to analyze"})
        if not isinstance(count, int) or isinstance(count, bool) or count < 1:
            logger.warning("extract_keywords received invalid count: %r", count)
            return json.dumps({"error": "Invalid input: count must be a positive integer"})
        stopwords = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "is", "are", "was", "were", "be", "been", "by", "from"
        }
        
        words = text.lower().split()
        filtered = [w.strip(".,!?;:") for w in words if w.lower() not in stopwords]
        
        from collections import Counter
        word_freq = Counter(filtered)
        top_words = word_freq.most_common(count)
        
        return json.dumps({
            "keywords": [{"word": w, "frequency": f} for w, f in top_words]
        }, indent=2)
    except Exception as e:
        logger.exception("extract_keywords failed unexpectedly")
        return json.dumps({"error": "An unexpected error occurred"})

def check_reading_level(text: str) -> str:
    """Estimate reading difficulty level.
    
    Args:
        text: The input text
    
    Returns:
        JSON string with reading level estimate
    """
    try:
        if text is None or not isinstance(text, str):
            logger.warning("check_reading_level received invalid input: %r", text[:200] if isinstance(text, str) else text)
            return json.dumps({"error": "Invalid input: text must be a non-empty string"})
        if len(text) > MAX_INPUT_LENGTH:
            logger.warning("check_reading_level received oversized input: %r", text[:200])
            return json.dumps({"error": "Input too large: maximum length is 100000 characters"})
        if not text or text.isspace():
            logger.warning("check_reading_level received empty input: %r", text[:200])
            return json.dumps({"error": "No text to analyze"})
        sentences = max(sum(1 for c in text if c in ".!?"), 1)
        words = len(text.split())
        vowels = "aeiou"
        syllables = sum(1 for c in text.lower() if c in vowels)
        
        if words == 0:
            logger.warning("check_reading_level received text with no words: %r", text[:200])
            return json.dumps({"error": "No text to analyze"})
        
        grade = max(0, (0.39 * (words / sentences)) + (11.8 * (syllables / words)) - 15.59)
        
        if grade < 6:
            level = "Elementary School"
        elif grade < 9:
            level = "Middle School"
        elif grade < 13:
            level = "High School"
        else:
            level = "College/Academic"
        
        return json.dumps({
            "grade_level": round(grade, 1),
            "reading_level": level
        }, indent=2)
    except Exception as e:
        logger.exception("check_reading_level failed unexpectedly")
        return json.dumps({"error": "An unexpected error occurred"})

# Create web UI
with gr.Blocks(title="Text Processor") as demo:
    gr.Markdown("# Text Processing Tools")
    gr.Markdown("Analyze text statistics, extract keywords, and check reading difficulty.")
    
    with gr.Tab("Analyze Text"):
        text_input1 = gr.Textbox(
            label="Enter text",
            lines=8,
            placeholder="Paste your text here..."
        )
        analysis_output = gr.Textbox(label="Analysis Results", lines=8)
        gr.Button("Analyze", size="lg").click(analyze_text, text_input1, analysis_output)
    
    with gr.Tab("Extract Keywords"):
        text_input2 = gr.Textbox(label="Enter text", lines=8)
        count_input = gr.Slider(1, 20, value=5, step=1, label="Number of keywords")
        keywords_output = gr.Textbox(label="Keywords", lines=8)
        gr.Button("Extract", size="lg").click(
            extract_keywords,
            [text_input2, count_input],
            keywords_output
        )
    
    with gr.Tab("Reading Level"):
        text_input3 = gr.Textbox(label="Enter text", lines=8)
        level_output = gr.Textbox(label="Reading Level Analysis", lines=5)
        gr.Button("Check Level", size="lg").click(check_reading_level, text_input3, level_output)

if __name__ == "__main__":
    try:
        demo.launch(mcp_server=True)
    except OSError as e:
        logger.exception("Failed to launch the app")
        if e.errno == errno.EADDRINUSE:
            print("Port already in use — try a different port (e.g. demo.launch(server_port=7861))", file=sys.stderr)
        else:
            print(f"Failed to launch server: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception:
        logger.exception("Failed to launch the app")
        print("Failed to launch the app. See the log output above for details.", file=sys.stderr)
        sys.exit(1)