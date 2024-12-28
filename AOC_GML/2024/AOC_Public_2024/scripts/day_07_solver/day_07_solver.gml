#region Define the operators
var _operators = ["+", "*", "||"];
#endregion

#region /// Evaluation Dynamic

// Function to evaluate an expression dynamically based on operator combinations
function eval_expression_dynamic(_numbers, _operators, _comb_index) {
    var _result = _numbers[0];
    var _num_ops = array_length(_numbers) - 1;
    var _num_operators = array_length(_operators); // Pre-calculate operator length
    var _temp = _comb_index;

    for (var _i = 0; _i < _num_ops; _i++) {
        var _op = _operators[_temp mod _num_operators]; // Use pre-calculated length
        _temp = _temp div _num_operators;

        switch (_op) {
            case "+":
                _result += _numbers[_i + 1];
                break;
            case "*":
                _result *= _numbers[_i + 1];
                break;
            case "||":
                _result = real(string(_result) + string(_numbers[_i + 1])); // Can be optimized further depending on data types
                break;
        }
    }

    return _result;
}

#endregion
#region /// Pars And Evaluate Data Part 1.

// Function to parse and evaluate data from a file and identify invalid results
function parse_and_evaluate(_data, _operators) {
    show_debug_message("Parsing and evaluating data with operators: " + string(_operators));
    var _total_sum = 0;

    var _equations = array_map(_data, function(_line) {
        var _parts = string_split_ext(_line, [":", " "], true);  // Split the line by ":" and spaces
        var _operands = []; // Initialize an empty array for operands

        // Add operands from index 1 onward (everything after the result)
        for (var i = 1; i < array_length(_parts); i++) {
            array_push(_operands, real(_parts[i]));
        }

        return {
            result: real(_parts[0]), // The result is the first element
            operands: _operands       // The rest are operands
        };
    });

    var _num_operators = array_length(_operators); // Pre-calculate operator length

    for (var _i = 0; _i < array_length(_equations); _i++) {
        var _eq = _equations[_i];
        var _target = real(_eq.result);  // Ensure _target is a real number
        var _numbers = _eq.operands;

        var _num_ops = array_length(_numbers) - 1;
        var _max_combinations = power(_num_operators, _num_ops);
        var _is_valid = false;

        for (var _j = 0; _j < _max_combinations; _j++) {
            var _calc_result = eval_expression_dynamic(_numbers, _operators, _j);
            
            // Allow small floating point differences with a tolerance
            if (abs(_calc_result - _target) < 0.0001) {  // Adjust tolerance as needed
                _is_valid = true;
                break; // Early exit for valid results
            }
        }

        if (_is_valid) {
            _total_sum += _target;
        } else {
            // Store invalid equations for Part 2 re-evaluation
            array_push(global.invalid_equations, _eq);
            show_debug_message("Invalid equation found: " + string(_eq));  // Debugging output
        }
    }

    show_debug_message("Total sum from Part 1: " + string(_total_sum));
	
	global._pass_reval += string(_total_sum)
	
    return _total_sum;
}

#endregion
#region /// Pars And Evaluate Data Part 2

// Function to parse and evaluate the file, including the re-evaluation of invalid results
function parse_and_evaluate_file(_file_path, _operators) {
    var _data = load_data_from_file(_file_path);
    var part_1_sum = parse_and_evaluate(_data, _operators);

    // Debugging: Check invalid results before passing to part 2
    show_debug_message("Invalid Results from Part 1: " + string(global.invalid_equations));

    // Pass invalid results to part 2 for re-validation
    var part_2_sum = 0;

    if (array_length(global.invalid_equations) > 0) {
        show_debug_message("Using invalid results for re-evaluation...");

        // Re-evaluate only the invalid results from Part 1 using the same operators
        part_2_sum = parse_and_evaluate_invalid_results(global.invalid_equations, _operators);
    }

	global._pass_reval += string(part_2_sum)

    // Combine the results from part 1 and part 2
    return part_1_sum + part_2_sum;
	
}

#endregion
#region /// Pars And Re-Evaluate Part 2
// New function for re-evaluating invalid equations passed from Part 1
function parse_and_evaluate_invalid_results(invalid_equations, _operators) {
    var _total_sum = 0;

    // Iterate over the invalid equations
    for (var _i = 0; _i < array_length(invalid_equations); _i++) {
        var _eq = invalid_equations[_i];
        var _target = _eq.result;
        var _numbers = _eq.operands;

        var _num_ops = array_length(_numbers) - 1;
        var _max_combinations = power(array_length(_operators), _num_ops);
        var _is_valid = false;

        // Try all operator combinations to re-evaluate invalid equations
        for (var _j = 0; _j < _max_combinations; _j++) {
            var _calc_result = eval_expression_dynamic(_numbers, _operators, _j);
            
            // Allow small floating point differences with a tolerance
            if (abs(_calc_result - _target) < 0.0001) {  // Adjust tolerance as needed
                _is_valid = true;
                break; // Early exit for valid results
            }
        }

        // If the equation is valid after re-evaluation, add to the total sum
        if (_is_valid) {
            _total_sum += _target;
        }
    }

    return _total_sum;
}
#endregion
