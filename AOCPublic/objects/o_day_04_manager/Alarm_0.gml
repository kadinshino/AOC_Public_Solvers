/// @description Insert description here

var _word = "XMAS";

// Call the function
var _positions = search_word(global.test_data_04, _word);

// Output the found positions
for (var _i = 0; _i < array_length(_positions); _i++) {
    var _pos = _positions[_i];
//    show_debug_message("Found " + _word + " at row " + string(_pos[0] + 1) + ", col " + string(_pos[1] + 1));
}

var _results = string(global.count_results);
show_debug_message("sum of XMAS results " + _results);

// Call the function
var _positions = search_xmas_pattern(global.test_data_04);

// Output the found positions
for (var _i = 0; _i < array_length(_positions); _i++) {
    var _pos = _positions[_i];
//    show_debug_message("Found X-MAS pattern at row " + string(_pos[0] + 1) + ", col " + string(_pos[1] + 1));
}

// Display the count of found positions
show_debug_message("Total occurrences of the X-MAS pattern: " + string(array_length(_positions)));
