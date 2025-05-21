from transformers import pipeline

# Initialize the summarization pipeline
# using model "t5-small" for our process
try:
    summarizer = pipeline('summarization', model='t5-small')
except OSError:
    print("Downloading t5-small model...") # Fallback for first time download
    summarizer = pipeline('summarization', model='t5-small')

# Example long text (you can replace this with any text you want to summarize)
long_text = """
Artificial intelligence (AI) is rapidly transforming various industries, from healthcare to finance and entertainment.
Machine learning, a subset of AI, involves training algorithms on vast amounts of data to enable them to make predictions
or decisions without being explicitly programmed. Deep learning, a further specialization, utilizes neural networks
with multiple layers to analyze complex patterns in data. This has led to breakthroughs in areas like natural
language processing, computer vision, and speech recognition. While AI offers immense potential for innovation
and efficiency, it also raises ethical concerns regarding job displacement, bias in algorithms, and the potential
for misuse. Researchers and policymakers are actively working on frameworks to ensure responsible AI development
and deployment, aiming to harness its benefits while mitigating its risks for a better future. The economic impact
is also significant, with companies investing heavily in AI research and development to gain a competitive edge.
The ongoing evolution of AI promises even more sophisticated applications in the coming years.
"""

# Generate summary
# min_length and max_length control the length of the output summary
summary = summarizer(long_text, max_length=80, min_length=25, do_sample=False)

print("--- Original Text ---")
print(long_text)
print("\n--- Generated Summary ---")
print(summary[0]['summary_text'])