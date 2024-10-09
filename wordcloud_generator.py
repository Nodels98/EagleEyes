import os
import time
from datetime import datetime
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import defaultdict
import arabic_reshaper
from bidi.algorithm import get_display
import codecs
import re

# Function to find the latest modified .txt file starting with 'cleen_input'
def find_latest_file(directory, prefix):
    txt_files = [f for f in os.listdir(directory) if f.startswith(prefix) and f.endswith('.txt')]
    if not txt_files:
        return None
    latest_file = max(txt_files, key=lambda f: os.path.getmtime(os.path.join(directory, f)))
    return os.path.join(directory, latest_file)

# Function to process message and count single and double word occurrences
def wordcloud_logic(message):
    wordsArr = message.split(' ')
    singleWordcloud = defaultdict(int)
    doubleWordcloud = defaultdict(int)
    
    maxWeightSingle = 0
    maxWeightDouble = 0
    singleMaxWeight = ''
    doubleMaxWeight = ''
    
    # Single and Double Word Processing
    for i in range(len(wordsArr)):
        if len(wordsArr[i]) == 0:
            continue
        
        # Single word count
        singleWordcloud[wordsArr[i]] += 1
        
        # Update max weight for single word
        if singleWordcloud[wordsArr[i]] > maxWeightSingle:
            maxWeightSingle = singleWordcloud[wordsArr[i]]
            singleMaxWeight = wordsArr[i]
        
        # Double word (bi-gram) count
        if i + 1 < len(wordsArr) and len(wordsArr[i + 1]) > 0:
            wc2dKey = wordsArr[i] + ' ' + wordsArr[i + 1]
            doubleWordcloud[wc2dKey] += 1
            
            # Update max weight for double word
            if doubleWordcloud[wc2dKey] > maxWeightDouble:
                maxWeightDouble = doubleWordcloud[wc2dKey]
                doubleMaxWeight = wc2dKey
    
    # Filter words by weight threshold (one-third of max weight)
    single_filtered = {word: weight for word, weight in singleWordcloud.items() if weight > maxWeightSingle // 3}
    double_filtered = {word: weight for word, weight in doubleWordcloud.items() if weight > maxWeightDouble // 3}
    
    return single_filtered, double_filtered

# Function to reshape Arabic text for proper rendering
def reshape_arabic_text(text):
    reshaped_text = ""
    lines = text.splitlines()
    for line in lines:
        reshaped_line = arabic_reshaper.reshape(line.strip())
        reshaped_text += get_display(reshaped_line) + " "
    return reshaped_text

# Function to generate and save word cloud as PNG
def generate_wordcloud(word_counts, filename, font_path):
    wc = WordCloud(
        width=1920, height=1080, background_color='white', font_path=font_path
    )
    
    wordcloud_img = wc.generate_from_frequencies(word_counts)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud_img, interpolation="bilinear")
    plt.axis('off')
    plt.savefig(filename, format='png')
    plt.close()

# Function to filter input text based on a source text file and remove non-Persian/Arabic characters
def filter_input(input_file_path, source_file_path, output_file_path):
    # Define a regex pattern for Persian, Arabic characters, and 3-digit numbers
    persian_arabic_char_pattern = re.compile(r'[آ-یء-ي]+|\b\d{3}\b')
    
    # Function to keep only Persian, Arabic characters, and 3-digit numbers
    def filter_persian_arabic_text(text):
        # Replace non-Persian/Arabic characters and non-3-digit numbers
        return ' '.join(persian_arabic_char_pattern.findall(text))
    
    # Read the source words
    with codecs.open(source_file_path, 'r', encoding='utf-8') as file:
        source_words = {line.strip() for line in file if line.strip()}
    
    print(f"Source words (count: {len(source_words)}): {source_words}")  # Debugging

    # Read the input file and filter out words found in source_words
    cleaned_lines = []
    with codecs.open(input_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Remove non-Persian/Arabic characters and filter out words from source_words
            cleaned_line = filter_persian_arabic_text(line)
            filtered_line = ' '.join(word for word in cleaned_line.split() if word not in source_words)
            cleaned_lines.append(filtered_line)
    
    # Save the cleaned lines to the output file
    with codecs.open(output_file_path, 'w', encoding='utf-8') as file:
        for line in cleaned_lines:
            file.write(line + '\n')

# Main loop to run the word cloud generation every 20 minutes
def main_loop():
    directory = 'Goftino_Monitoring/'
    prefix1 = 'cleen_input'
    prefix2 = 'chat_log'
    font_path = 'Goftino_Monitoring/NotoNaskhArabic-Regular.ttf'
    path_stop_words = 'Goftino_Monitoring/short.txt'
# short.txt contains several words in each line that should not appears in wordcloud png

    while True:
        # Get current time
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        chat_log = find_latest_file(directory, prefix2)
        print("1:",chat_log)
        outputpath = f'Goftino_Monitoring/cleen_input_goftino{current_time}.txt'
        filter_input(chat_log, path_stop_words,outputpath )
        # Find the latest modified file starting with 'cleen_input'
        latest_file = find_latest_file(directory, prefix1)
        if latest_file:
            print(f"Processing file: {latest_file}")

            # Read the filtered input and reshape the text
            with codecs.open(latest_file, 'r', encoding='utf-8') as file:
                message = file.read()

            reshaped_message = reshape_arabic_text(message)
            single_wordcloud, double_wordcloud = wordcloud_logic(reshaped_message)

            # Generate single-word and double-word word clouds
            generate_wordcloud(single_wordcloud, f'Goftino_Monitoring/static/single_wordcloud5_{current_time}.png', font_path)
            generate_wordcloud(double_wordcloud, f'Goftino_Monitoring/static/double_wordcloud5_{current_time}.png', font_path)

            print(f"Word clouds generated at {current_time}")
        else:
            print("No valid file found.")

        # Wait for 20 minutes (1200 seconds) before generating the next word clouds
        time.sleep(1000)




# Run the main loop
if __name__ == "__main__":
    main_loop()
