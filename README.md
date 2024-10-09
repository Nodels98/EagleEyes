# EagleEyes
Cloud word monitoring was extracted from Goftino chat platform

# Goftino WordCloud Generator

This Python project generates word clouds based on chat logs collected from the Goftino platform. The word clouds include both single-word and double-word (bi-gram) frequency visualizations. It also filters out common stop words.

## Features
- Generates word clouds from Persian and Arabic text.
- Processes both single-word and double-word occurrences.
- Filters out specified stop words.
- Updates every 20 minutes and creates new word cloud images.

## Requirements
- Python 3.x
- Required libraries:
  - `wordcloud`
  - `matplotlib`
  - `arabic_reshaper`
  - `bidi.algorithm`
  - `codecs`
  - `re`
  
You can install them with the following command:

```bash
pip install wordcloud matplotlib arabic_reshaper bidi
