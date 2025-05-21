import streamlit as st
from transformers import pipeline, set_seed
from transformers.utils.logging import set_verbosity_error

# Suppress Hugging Face pipeline logging noise unless it's an error
set_verbosity_error()

# --- MODEL LOADING (Cached for performance) ---
@st.cache_resource # Updated caching decorator
def load_generator():
    """Loads the text generation pipeline."""
    try:
        return pipeline('text-generation', model='gpt2')
    except Exception as e:
        st.error(f"Error loading text generation model: {e}")
        st.error("This might be due to a network issue or the model files not being found.")
        st.error("Try checking your internet connection or the Hugging Face model hub status.")
        return None

@st.cache_resource # Updated caching decorator
def load_summarizer():
    """Loads the summarization pipeline."""
    try:
        return pipeline('summarization', model='t5-small')
    except Exception as e:
        st.error(f"Error loading summarization model: {e}")
        st.error("This might be due to a network issue or the model files not being found.")
        st.error("Try checking your internet connection or the Hugging Face model hub status.")
        return None

# --- APPLICATION LAYOUT ---
st.set_page_config(page_title="LLM Content Studio", layout="wide")
st.title("📝 LLM Content Studio: Create & Summarize")
st.markdown("""
Welcome to the LLM Content Studio! Use the tabs below to switch between **Content Creation** and **Text Summarization**.
""")

# Load models
generator = load_generator()
summarizer = load_summarizer()

if generator is None or summarizer is None:
    st.warning("One or more models could not be loaded. Please check the error messages above.")
    st.stop()


tab1, tab2 = st.tabs(["✨ Content Creation", "📚 Text Summarization"])

# --- TAB 1: CONTENT CREATION ---
with tab1:
    st.header("✨ Content Creation Engine")
    st.markdown("Provide a prompt and let the AI generate text for you.")

    user_prompt = st.text_area("Enter your prompt here:", height=150, placeholder="e.g., Write a short story about a robot who discovers music...")

    col1, col2, col3 = st.columns(3)
    with col1:
        max_length = st.slider("Max Length (tokens):", min_value=50, max_value=1000, value=200, step=10)
    with col2:
        temperature = st.slider("Temperature (randomness):", min_value=0.1, max_value=1.5, value=0.8, step=0.05)
    with col3:
        num_sequences = st.slider("Number of Sequences:", min_value=1, max_value=5, value=1, step=1)

    # Advanced options
    with st.expander("Advanced Generation Settings"):
        top_k = st.slider("Top-K Sampling:", min_value=0, max_value=100, value=50, step=1, help="If set to > 0, only the top k most likely tokens are considered for generation.")
        top_p = st.slider("Top-P (Nucleus) Sampling:", min_value=0.0, max_value=1.0, value=0.95, step=0.01, help="If set to < 1.0, only the most probable tokens with probabilities that add up to top_p or higher are considered.")
        no_repeat_ngram_size = st.slider("No Repeat N-gram Size:", min_value=0, max_value=5, value=2, step=1, help="If set to int > 0, all ngrams of that size can only occur once.")
        seed = st.number_input("Seed (for reproducibility, 0 for random):", min_value=0, value=42, step=1)


    if st.button("🚀 Generate Content", type="primary", use_container_width=True):
        if not user_prompt:
            st.warning("Please enter a prompt to generate content.")
        elif not generator:
            st.error("Text generation model is not available.")
        else:
            with st.spinner("AI is thinking... 🧠"):
                try:
                    if seed > 0:
                        set_seed(seed)

                    # Ensure pad_token_id is set if the model requires it (like gpt2)
                    # Some models might not have it by default or it might be eos_token_id
                    pad_token_id_val = generator.tokenizer.eos_token_id if generator.tokenizer.pad_token_id is None else generator.tokenizer.pad_token_id

                    generated_outputs = generator(
                        user_prompt,
                        max_length=max_length,
                        num_return_sequences=num_sequences,
                        temperature=temperature,
                        top_k=top_k if top_k > 0 else None, # pipeline expects None if 0
                        top_p=top_p if top_p < 1.0 else None, # pipeline expects None if 1.0
                        no_repeat_ngram_size=no_repeat_ngram_size if no_repeat_ngram_size > 0 else None,
                        pad_token_id=pad_token_id_val
                    )
                    st.subheader("Generated Content:")
                    for i, output in enumerate(generated_outputs):
                        st.markdown(f"--- **Result {i+1}** ---")
                        st.text_area(label=f"Output {i+1}", value=output['generated_text'], height=250, key=f"gen_output_{i}")
                        st.markdown("---")
                except Exception as e:
                    st.error(f"An error occurred during content generation: {e}")
                    st.error("Details: This could be due to invalid parameter combinations or an issue with the model.")

# --- TAB 2: TEXT SUMMARIZATION ---
with tab2:
    st.header("📚 Text Summarization Engine")
    st.markdown("Paste your long text below and the AI will generate a concise summary.")

    text_to_summarize = st.text_area("Enter the text you want to summarize:", height=300, placeholder="Paste your article, notes, or any long text here...")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        summary_min_length = st.slider("Min Summary Length (tokens):", min_value=10, max_value=200, value=30, step=5)
    with col_s2:
        summary_max_length = st.slider("Max Summary Length (tokens):", min_value=30, max_value=500, value=150, step=10)

    if st.button("✍️ Generate Summary", type="primary", use_container_width=True):
        if not text_to_summarize:
            st.warning("Please enter text to summarize.")
        elif not summarizer:
            st.error("Summarization model is not available.")
        elif summary_min_length >= summary_max_length:
            st.warning("Min summary length must be less than Max summary length.")
        else:
            with st.spinner("AI is condensing... 🤏"):
                try:
                    summary_output = summarizer(
                        text_to_summarize,
                        min_length=summary_min_length,
                        max_length=summary_max_length,
                        do_sample=False # Typically False for summarization for more factual output
                    )
                    st.subheader("Generated Summary:")
                    st.text_area(label="Summary", value=summary_output[0]['summary_text'], height=200, key="summary_output")
                except Exception as e:
                    st.error(f"An error occurred during summarization: {e}")
                    st.error("Details: Ensure the input text is not too short or too long for the model's capacity.")


