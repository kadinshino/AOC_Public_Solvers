// Function to split a stone into two stones based on its digits
function _split_stone(_number) {
    var _digits = string(_number);
    var _mid = floor(string_length(_digits) / 2);
    var _left = real(string_copy(_digits, 1, _mid));
    var _right = real(string_copy(_digits, _mid + 1, string_length(_digits) - _mid));
    
    return [(_left == "" ? 0 : _left), (_right == "" ? 0 : _right)];
}

// Function to transform a single stone based on the rules
function _transform_stone(_number) {
    if (_number == 0) {
        return [1];
    } else if (string_length(string(_number)) % 2 == 0) {
        return _split_stone(_number);
    } else {
        return [_number * 2024];
    }
}

// Function to process stones recursively with memoization
function _process_stones(_stones, _blinks, _memo) {
    if (array_length(_stones) == 0 || _blinks <= 0) {
        return array_length(_stones); // Base case: no more splits
    }

    var _key = string(_stones) + ":" + string(_blinks);
    if (ds_map_exists(_memo, _key)) {
        return ds_map_find_value(_memo, _key);
    }

    var _total_stones = 0;
    for (var i = 0; i < array_length(_stones); i++) {
        var _new_stones = _transform_stone(array_get(_stones, i));
        
        // Debug: Print transformed stones
 //       show_debug_message("Transformed stone " + string(array_get(_stones, i)) + " to " + string(_new_stones));
        
        // Recursive processing
        var _result = _process_stones(_new_stones, _blinks - 1, _memo);
        _total_stones += _result;
    }

    ds_map_add(_memo, _key, _total_stones);
    return _total_stones;
}

// Main function to simulate the process
function call_11() {
    // Example input
    var _initial_stones = [6, 11, 33023, 4134, 564, 0, 8922422, 688775];
    
    // Initialize memoization map
    var _memo = ds_map_create();
    
    var _total_stone_count = 0;
    
    for (var i = 0; i < array_length(_initial_stones); i++) {
        var _stone = array_get(_initial_stones, i);
        _total_stone_count += _process_stones([_stone], 75, _memo); // Each stone is processed with 6 blinks
        
        // Debug message showing the number of stones after processing each initial stone
    //    show_debug_message("Finished processing stone " + string(_stone) + ". Total Stones: " + string(_total_stone_count));
    }
    
    ds_map_destroy(_memo);
    
    // Output the results
    show_debug_message("After processing all stones with 6 blinks, there are " + string(_total_stone_count) + " stones.");
}