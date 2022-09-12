from subtitle_dataframes_io import *
from collections import Counter
from datetime import datetime, date, timedelta


def character_subtitle_mentions(sentences, nlp, num_chars=10):
    """
    searches for potential character names mentioned in dialogue
    uses blacklist to avoid false positives
    """
    people_blacklist = ['Jesus', 'Jesus Christ', 'Whoo', 'God', 'Mm', 'Dude', 'Mm-hmm', 'Huh']

    doc = nlp(' '.join(sentences))
    people = []

    for ent in doc.ents:
        if ent.label_ == 'PERSON' and ent.text not in people_blacklist:
            people.append(ent.text)
    count = Counter(people)
    char_count = count.most_common(num_chars)

    characters = []
    for character in char_count:
        characters.append(character[0])
    return characters


def character_offscreen_speakers(subtitle_df, num_chars=10):
    """
    searches for potential character names labeled as offscreen speakers
    uses blacklist to avoid false positives
    """
    speaker_blacklist = ['MAN', 'WOMAN', 'BOY', 'GIRL', 'BOTH', 'ALL']

    speaker_counts = subtitle_df.speaker.value_counts()
    speakers = []

    x = 0
    y = 0
    if len(speaker_counts) == 0:
        return None
    else:
        while y < num_chars:
            if speaker_counts.index[x] not in speaker_blacklist:
                speakers.append(speaker_counts.index[x])
                y += 1
            x += 1

        return speakers


def dialogue_breaks(subtitle_df, threshold=10):
    """
    searches for potential scene boundaries by identifying breaks in dialogue over a certain threshold (in seconds)
    """
    x = 1
    delay_threshold = timedelta(seconds=threshold)
    breaks = []

    while x < len(subtitle_df):
        if subtitle_df.iloc[x].cleaned_text or subtitle_df.iloc[x].laugh == 1:
            y = 1

            while not subtitle_df.iloc[x - y].cleaned_text:
                y += 1
            delay = datetime.combine(date.today(), subtitle_df.iloc[x].start_time) - datetime.combine(date.today(),
                                                                                                      subtitle_df.iloc[
                                                                                                          x - y].end_time)

            if delay > delay_threshold:
                breaks.append(x)
        x += 1

    return breaks
