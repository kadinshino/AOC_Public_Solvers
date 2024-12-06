/// @description Insert description here

function search_word(_grid, _word) {
    var _rows = array_length(_grid);
    var _cols = array_length(_grid[0]);
    var _word_len = string_length(_word);
    var _word_chars = [];
    for (var _i = 0; _i < _word_len; _i++) {
        _word_chars[_i] = string_char_at(_word, _i + 1);
    }

    global.count_results = 0;

    var _directions = [
        0, 1, 0, -1, 
        1, 0, -1, 0, 
        1, 1, -1, -1, 
        -1, 1, 1, -1
    ];
    var _directions_count = array_length(_directions);

    for (var _r = 0; _r < _rows; _r++) {
        for (var _c = 0; _c < _cols; _c++) {
            if (_grid[_r][_c] == _word_chars[0]) {
                for (var _d = 0; _d < _directions_count; _d += 2) {
                    var _dr = _directions[_d];
                    var _dc = _directions[_d + 1];
                    var _match = true;

                    if (_r + (_word_len - 1) * _dr < 0 || _r + (_word_len - 1) * _dr >= _rows ||
                        _c + (_word_len - 1) * _dc < 0 || _c + (_word_len - 1) * _dc >= _cols) {
                        continue;
                    }

                    for (var _k = 1; _k < _word_len; _k++) {
                        var _nr = _r + _dr * _k;
                        var _nc = _c + _dc * _k;

                        if (_grid[_nr][_nc] != _word_chars[_k]) {
                            _match = false;
                            break;
                        }
                    }

                    if (_match) {
                        global.count_results++;
                    }
                }
            }
        }
    }
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function search_xmas_pattern(_grid) {
    var _found_positions = [];
    var _unique_positions = ds_map_create(); // Map to track unique positions

    var _rows = array_length(_grid);
    var _cols = array_length(_grid[0]);

    for (var _r = 1; _r < _rows - 1; _r++) {
        for (var _c = 1; _c < _cols - 1; _c++) {
            // Ensure we're not out of bounds for a 3x3 region
            if (_r - 1 < 0 || _r + 1 >= _rows || _c - 1 < 0 || _c + 1 >= _cols) {
                continue;
            }

            // Extract the diagonals and center
            var _top_left = _grid[_r - 1][_c - 1];
            var _top_right = _grid[_r - 1][_c + 1];
            var _center = _grid[_r][_c];
            var _bottom_left = _grid[_r + 1][_c - 1];
            var _bottom_right = _grid[_r + 1][_c + 1];

            // Ensure the center is 'A'
            if (_center != "A") continue;

            // Check the diagonals for MAS patterns (forward or reverse)
            var _is_mas_pattern = function(_diagonal) {
                return (_diagonal[0] == "M" && _diagonal[1] == "A" && _diagonal[2] == "S") ||
                       (_diagonal[0] == "S" && _diagonal[1] == "A" && _diagonal[2] == "M");
            };

            if (_is_mas_pattern([_top_left, _center, _bottom_right]) && _is_mas_pattern([_top_right, _center, _bottom_left])) {
                var _key = string(_r) + "_" + string(_c);
                if (!ds_map_exists(_unique_positions, _key)) {
                    ds_map_add(_unique_positions, _key, true);
                    array_push(_found_positions, [_r, _c]);
                }
            }
        }
    }

    ds_map_destroy(_unique_positions);
    return _found_positions;
}

function search_and_display_positions(_data, _word, _pattern) {
    var _positions_word = search_word(_data, _word);
    var _positions_pattern = search_xmas_pattern(_data);
    
    // Output results for the word search
    if (array_length(_positions_word) > 0) {
        for (var _i = 0; _i < array_length(_positions_word); _i++) {
            var _pos = _positions_word[_i];
            show_debug_message("Found " + _word + " at row " + string(_pos[0] + 1) + ", col " + string(_pos[1] + 1));
        }
    } else {
        show_debug_message("No occurrences of " + _word + " found.");
    }

    // Output results for the pattern search
    if (array_length(_positions_pattern) > 0) {
        for (var _i = 0; _i < array_length(_positions_pattern); _i++) {
            var _pos = _positions_pattern[_i];
            show_debug_message("Found " + _pattern + " pattern at row " + string(_pos[0] + 1) + ", col " + string(_pos[1] + 1));
        }
    } else {
        show_debug_message("No occurrences of the " + _pattern + " pattern found.");
    }

    // Display the count of found positions for both
    show_debug_message("Total occurrences of the word '" + _word + "': " + string(array_length(_positions_word)));
    show_debug_message("Total occurrences of the " + _pattern + " pattern: " + string(array_length(_positions_pattern)));
}
