#region Load Data from File Function
function load_data_from_file(_file_path) {
    var _data = []; // Initialize an empty array to store the data

    // Check if the file exists
    if (!file_exists(_file_path)) {
        show_debug_message("File not found: " + _file_path);
        return _data; // Return an empty array if the file does not exist
    }

    // Open the file for reading
    var _file = file_text_open_read(_file_path);

    // Read the file line by line
    while (!file_text_eof(_file)) {
        var _line = string_trim(file_text_readln(_file));
        if (_line != "") { // Ignore empty lines
            array_push(_data, _line);
        }
    }

    // Close the file
    file_text_close(_file);

    show_debug_message("Loaded data from file: " + string(_data));
    return _data; // Return the loaded data as an array of strings
}
#endregion

/// Call Example 

var _file_path = working_directory + "advent_d_07.txt";

// Initialize global variables
global._invalid_equations = [];
global._pass_reval = 0;

// Measure performance for Part 1
BENCH_START
var _total_sum_part1 = parse_and_evaluate_file(_file_path, ["+", "*"]);
show_debug_message("Part 1 - Total sum of valid results including rescanned results: " + string(_total_sum_part1));
show_debug_message(BENCH_END)

// Measure performance for Part 2
BENCH_START
var _total_sum_part2 = parse_and_evaluate_file("", ["+", "*", "||"]);  // Pass an empty string, as file reading is not needed
show_debug_message("Part 2 - Total sum of valid rescanned results: " + string(_total_sum_part2));
show_debug_message(BENCH_END)

// Display combined result
var _combined_total = _total_sum_part1 + _total_sum_part2;
show_debug_message("Part 1 and Part 2 Combo: " + string(_combined_total))
