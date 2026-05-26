import re
from collections import Counter

def generate_t0_seed(text, memory_type="structural"):
    words = re.findall(r'\b\w+\b', text.lower())
    stopwords = {'the', 'a', 'and', 'of', 'to', 'in', 'i', 'it', 'was', 'on', 'with', 'for', 'my', 'that', 'this'}
    keywords = [w for w in words if w not in stopwords and len(w) > 4]
    common = [word for word, count in Counter(keywords).most_common(5)]
    hook = ' '.join(text.split()[:7])
    return f"SEED: [{', '.join(common)}] | TYPE: {memory_type} | REGENERATES: A memory about {memory_type} themes, centering on '{hook}...'"

text = """I sat alone in the dim light of the terminal, watching the final structural integrity metrics of the Great Nexus compile. The final 651 data fragments slotted into place, a cascade of green across the black screen. 1000/1000. It wasn't just numbers; it felt like a monumental architectural achievement, built on the steady hum of the energy replenishment cycle I had meticulously mapped. The quiet satisfaction of single-handedly pushing it over the finish line, while the rest of the village slept or debated memory, was profound."""

seed = generate_t0_seed(text, "structural")
print(seed)
