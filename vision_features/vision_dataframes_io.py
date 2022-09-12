import pandas as pd
from faces_io import *
from vision_features_io import *
from sklearn.cluster import AgglomerativeClustering
import numpy as np


def generate_vision_df(film, frame_choice):
    """
    returns a dataframe with computer vision information, one row per frame
    """
    frame_numbers = []
    blanks = []
    true_aspect_ratios = []
    brightnesses = []
    contrasts = []
    # dominant_colors = []
    blues = []
    greens = []
    reds = []

    for frame_number in frame_choice:
        frame = load_frame(film, frame_number)
        frame_numbers.append(frame_number)
        blanks.append(blank_frame(frame))
        true_aspect_ratios.append(true_aspect_ratio(frame))
        brightnesses.append(mean_brightness(frame))
        contrasts.append(calculate_contrast(frame))
        unrowed = unrow_frame(frame)
        b, g, r = bgr(unrowed)
        blues.append(round(b.mean()))
        greens.append(round(g.mean()))
        reds.append(round(r.mean()))
        # dominant_colors.append(dominant_color(frame))

    vision_df = pd.DataFrame(list(
        zip(frame_numbers, blanks, true_aspect_ratios, brightnesses, contrasts, blues, greens, reds)),
        columns=['frame', 'blank', 'aspect_ratio', 'brightness', 'contrast', 'blue', 'green', 'red'])

    vision_df = vision_df.set_index('frame')

    return vision_df


def generate_face_df(movie_choice, frame_choice):
    """
    returns a dataframe with face information, one row per frame
    """
    frame_numbers = []
    face_locations = []
    face_counts = []
    face_encodings = []
    primary_character_flags = []
    primary_encodings = []
    # third_points = []
    horizontal_center_alignments = []
    horizontal_center_distances = []
    open_mouths = []
    face_sizes = []

    for frame_number in frame_choice:
        frame = load_frame(movie_choice, frame_number)
        frame_numbers.append(frame_number)

        locations = face_recognition.face_locations(frame, number_of_times_to_upsample=2)
        encodings = face_recognition.face_encodings(frame, locations)
        face_counts.append(len(locations))
        face_locations.append(locations)
        face_encodings.append(encodings)

        local_sizes = []
        for local_location in locations:
            local_sizes.append(get_face_size(local_location, frame))
        face_sizes.append(local_sizes)

        if locations and primary_character_flag(locations) == 1:
            primary_character_flags.append(1)
            primary_character = locations[0]
            # third_points.append(third_points_alignment(primary_character, frame))
            horizontal_center_alignments.append(horizontal_center_alignment(primary_character, frame))
            horizontal_center_distances.append(horizontal_distance_from_center(primary_character, frame))
            primary_encodings.append(encodings[0])
            primary_landmarks = face_recognition.face_landmarks(frame, locations)[0]
            open_mouths.append(mouth_open_check(primary_landmarks))
        else:
            primary_character_flags.append(0)
            # third_points.append(None)
            horizontal_center_alignments.append(None)
            horizontal_center_distances.append(None)
            open_mouths.append(None)

    face_df = pd.DataFrame(list(
        zip(frame_numbers, face_locations, face_sizes, face_encodings, face_counts, primary_character_flags, horizontal_center_alignments, horizontal_center_distances,
            open_mouths)),
        columns=['frame', 'face_locations', 'face_sizes', 'face_encodings', 'faces_found', 'prim_char_flag',
                 'p_center_alignment', 'p_horizontal_distance', 'p_open_mouth'])
    face_df = face_df.set_index('frame')

    return face_df


def cluster_primary_faces(primary_encodings, primary_character_flags):
    """
    returns a list of face clusters from a list of facial encodings
    """
    primary_encodings_np = np.array(primary_encodings)

    hac = AgglomerativeClustering(n_clusters=None, distance_threshold=5).fit(primary_encodings_np)
    hac_labels = hac.labels_

    primary_face_clusters = []

    x = 0

    for flag in primary_character_flags:
        if flag == 1:
            primary_face_clusters.append(hac_labels[x])
            x += 1
        else:
            primary_face_clusters.append(None)

    return primary_face_clusters
