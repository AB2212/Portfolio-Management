import pickle


def save_object(obj, filepath):
    with open(filepath, "wb") as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_object(filepath):
    with open(filepath, "rb") as input:
        return pickle.load(input)
