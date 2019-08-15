import markovify

def build_message(text, max_length):
    text_model = markovify.Text(text)
    message = text_model.make_short_sentence(max_length)
    while message is None:
        message = text_model.make_short_sentence(max_length)
    return message

def generate_message(name):
    with open("dataset/" + name + ".txt") as f:
        text = f.read()
    return build_message(text, 80)

def generate_from_iterable(iterable):
    return build_message('\n'.join(iterable), 280)