def get_id(message):
    message = message.split(' ')
    index_of_id = message.index("id")
    # Get the substring after the word "id"
    return message[index_of_id + 1]