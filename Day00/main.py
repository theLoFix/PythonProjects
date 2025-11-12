import base64

def encode_to_base64(input_string):
    """Encodes a given string to Base64 format."""
    encoded_bytes = base64.b64encode(input_string.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def decode_from_base64(encoded_string):
    """Decodes a Base64 encoded string back to its original format."""
    decoded_bytes = base64.b64decode(encoded_string.encode('utf-8'))
    return decoded_bytes.decode('utf-8')    

print("Please provide a Base64 string to encode:")
user_input = input()
encoded_str = decode_from_base64(user_input)
print(f"Decoded string: {encoded_str}")
