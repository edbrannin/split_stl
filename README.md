Usage:

1. `pip install -r requirements.txt`
2. `python split_stl.py split filename_to_split`
    * Splits up an STL file into groups that don't share vertices.
3. `python split_stl.py join these_were_actually.stl the_same_part.stl -o combined.stl
    * Prints to stdout if you omit the "-o combined.stl" argument
