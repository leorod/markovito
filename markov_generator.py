import markovify

def generate_message(name):
    with open("dataset/" + name + ".txt") as f:
        text = f.read()
    text_model = markovify.Text(text)
    message = text_model.make_short_sentence(80)
    while message is None:
        message = text_model.make_short_sentence(80)
    return message