def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == "hello":
        return "hey there!"
    
    if p_message == "?help":
        return "commands are: ?dc, ?join, ?play? ?stop, ?pause, ?resume, hello "
    
    if p_message.startswith("?play"):
        return f"Now playing: {p_message.split()[1]}"

    
   
