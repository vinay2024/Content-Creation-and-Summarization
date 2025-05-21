from transformers import pipeline

# Initialize the text generation pipeline
# using model "gpt2" for our process

try:
    generator = pipeline('text-generation', model='gpt2')
except OSError:
    print("Downloading gpt2 model...") # Fallback for first time download if interrupted
    generator = pipeline('text-generation', model='gpt2')


# Define a prompt
prompt = "The quick brown fox jumps over the lazy dog. "

# Generate text
# max_length: The maximum length of the sequence to be generated.
# num_return_sequences: The number of independently computed returned sequences.
# no_repeat_ngram_size: If set to int > 0, all ngrams of that size can only occur once.
# temperature: Controls randomness. Lower is more deterministic, higher is more random.
# top_k, top_p: Control nucleus sampling.
generated_texts = generator(
    prompt,
    max_length=150,
    num_return_sequences=1,
    no_repeat_ngram_size=2,
    temperature=0.8,
    top_k=50,
    top_p=0.95,
    pad_token_id=generator.tokenizer.eos_token_id # Suppress warning
)

for i, text in enumerate(generated_texts):
    print(f"--- Generated Text {i+1} ---")
    print(text['generated_text'])
    print("-" * 30)
