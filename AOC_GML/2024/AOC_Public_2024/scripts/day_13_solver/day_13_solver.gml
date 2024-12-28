function solve_claw_machine(_a_x, _a_y, _b_x, _b_y, _p_x, _p_y) {
    // Arrays to represent possible values of _x and _y
    var _solutions = [];
    var _min_cost = 999999999;
    var _best_solution = undefined;

    // Brute force approach to find solutions
    for (var _x = 0; _x <= 100; _x++) { // Adjust the upper limit as needed
        for (var _y = 0; _y <= 100; _y++) {
            if (_x * _a_x + _y * _b_x == _p_x && _x * _a_y + _y * _b_y == _p_y) {
                var _cost = 3 * _x + _y;
                if (_cost < _min_cost) {
                    _min_cost = _cost;
                    _best_solution = [_x, _y];
                }
            }
        }
    }

    return [_min_cost, _best_solution];
}

function claw_machine(){

// Main execution
var _input_file = "machines.txt";
var _offset = 10000000000000;
var _machines = parse_input(_input_file, _offset);

var _results = [];
var _total_cost = 0;

for (var i = 0; i < array_length(_machines); i++) {
    var _machine = _machines[i];
    var _a_x = _machine[0];
    var _a_y = _machine[1];
    var _b_x = _machine[2];
    var _b_y = _machine[3];
    var _p_x = _machine[4];
    var _p_y = _machine[5];

    var _result = solve_claw_machine(_a_x, _a_y, _b_x, _b_y, _p_x, _p_y);
    array_push(_results, _result);

    if (_result[0] < 999999999) {
        _total_cost += _result[0];
    }
}

// Display results
for (var i = 0; i < array_length(_results); i++) {
    show_debug_message("Minimum Cost: " + string(_results[i][0]) + ", Solution: " + string(_results[i][1]));
}

show_debug_message("Total machines processed: " + string(array_length(_machines)));
show_debug_message("Total cost of all solutions: " + string(_total_cost));

}

// Function to parse input data from a text file
function parse_input(_file_path, _offset) {
    var _machines = [];
    var _file = file_text_open_read(_file_path);

    if (_file < 0) {
        show_error("Failed to open file: " + _file_path, true);
        return _machines;
    }

    while (!file_text_eof(_file)) {
        var _a_line = "";
        var _b_line = "";
        var _prize_line = "";

        // Read three lines for each machine
        if (!file_text_eof(_file)) _a_line = file_text_readln(_file);
        if (!file_text_eof(_file)) _b_line = file_text_readln(_file);
        if (!file_text_eof(_file)) _prize_line = file_text_readln(_file);

        // Parse the lines
        try {
            var _a_x = string_digits(string_copy(_a_line, string_pos("+", _a_line) + 1, 10));
            var _a_y = string_digits(string_copy(_a_line, string_pos(",", _a_line) + 1, 10));
            var _b_x = string_digits(string_copy(_b_line, string_pos("+", _b_line) + 1, 10));
            var _b_y = string_digits(string_copy(_b_line, string_pos(",", _b_line) + 1, 10));
            var _p_x = string_digits(string_copy(_prize_line, string_pos("=", _prize_line) + 1, 10)) + _offset;
            var _p_y = string_digits(string_copy(_prize_line, string_pos(",", _prize_line) + 1, 10)) + _offset;

            array_push(_machines, [real(_a_x), real(_a_y), real(_b_x), real(_b_y), real(_p_x), real(_p_y)]);
        } catch (e) {
            show_debug_message("Skipping invalid block: " + _a_line + ", " + _b_line + ", " + _prize_line);
        }
    }

    file_text_close(_file);
    return _machines;
}
