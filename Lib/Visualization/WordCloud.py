from wordcloud import WordCloud
from matplotlib import pyplot as plt

def draw_word_cloud(frequencies, mask):
    wordcloud = WordCloud(width=1000, height=666, random_state=1, background_color='white', colormap='inferno', collocations=False, mask=mask).generate_from_frequencies(frequencies)
    plt.figure(figsize=(10, 15))
    plt.imshow(wordcloud)
    plt.axis("off")
    
def save_word_cloud(frequencies, mask, path, dpi=300):
    wordcloud = WordCloud(width=1000, height=666, random_state=1, background_color='white', colormap='inferno', collocations=False, mask=mask).generate_from_frequencies(frequencies)
    print(f"Saving word cloud to {path}")
    plt.figure(figsize=(10, 15))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig(path, dpi=dpi)
    plt.close(plt.gcf())