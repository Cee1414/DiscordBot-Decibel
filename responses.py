def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == "hello":
        return "hey there!"
    
    if p_message == "?help":
        return "commands are: "
    

       
    

    
    return "IDK what u said"