import numpy as np
import math


def beam_search_decoder(predictions, top_k=3):
    # start with an empty sequence with zero score
    output_sequences = [([], 0)]

    # looping through all the predictions
    for token_probs in predictions:
        new_sequences = []

        # append new tokens to old sequences and re-score
        for old_seq, old_score in output_sequences:
            for char_index in range(len(token_probs)):
                new_seq = old_seq + [char_index]
                # considering log-likelihood for scoring
                new_score = old_score + math.log(token_probs[char_index])
                new_sequences.append((new_seq, new_score))

        # sort all new sequences in the de-creasing order of their score
        output_sequences = sorted(new_sequences, key=lambda val: val[1], reverse=True)

        # select top-k based on score
        # *Note- best sequence is with the highest score
        output_sequences = output_sequences[:top_k]

    return output_sequences


model_prediction = [[0.1, 0.7, 0.1, 0.1],
                    [0.7, 0.1, 0.1, 0.1],
                    [0.1, 0.1, 0.6, 0.2],
                    [0.1, 0.1, 0.1, 0.7],
                    [0.4, 0.3, 0.2, 0.1]]

decoded_predictions = beam_search_decoder(model_prediction, top_k=5)
print(decoded_predictions)

# [Out]: [([1, 0, 2, 3, 0], -2.497141187456343),
#         ([1, 0, 2, 3, 1], -2.784823259908124),
#         ([1, 0, 2, 3, 2], -3.1902883680162883),
#         ([1, 0, 3, 3, 0], -3.595753476124453),
#         ([1, 0, 2, 3, 3], -3.8834355485762337)]