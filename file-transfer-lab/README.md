# File Transfer Lab
The program handles the next command:
- ./framedClient put (name of a file)

The Client verifies if the file is a valid input to send, and reads it it in parts of 100 bytes.

The Server verifies that it does not own that file already, and if does not, it allocates it.
