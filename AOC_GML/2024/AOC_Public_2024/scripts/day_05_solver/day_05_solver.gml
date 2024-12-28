 #region Helper Functions

function array_swap(_array, _index1, _index2) {
    var _temp = _array[_index1];
    _array[_index1] = _array[_index2];
    _array[_index2] = _temp;
}

// Custom quicksort with pair swapping
function quick_sort_with_pairs(_array, _low, _high, _pair_map) {
    if (_low < _high) {
        var _pi = partition_with_pairs(_array, _low, _high, _pair_map);
        quick_sort_with_pairs(_array, _low, _pi - 1, _pair_map);
        quick_sort_with_pairs(_array, _pi + 1, _high, _pair_map);
    }
}

#endregion

function partition_with_pairs(_array, _low, _high, _pair_map) {
    var _pivot = _array[_high], _i = _low - 1;
    var _pivot_pair_list = ds_map_find_value(_pair_map, _pivot);
    if (_pivot_pair_list == undefined) return _high;
    var _pivot_pair_list_size = ds_list_size(_pivot_pair_list);

    for (var _j = _low; _j < _high; _j++) {
        var _current_pair_list = ds_map_find_value(_pair_map, _array[_j]);
        if (_current_pair_list != undefined && ds_list_find_index(_current_pair_list, _pivot) != -1) {
            array_swap(_array, ++_i, _j);
        }
    }
    array_swap(_array, _i + 1, _high);
    return _i + 1;
}

function process_page_orders() {
    var _pages = global.pages;
    var _page_order = global.page_order;
    var _pages_dict = ds_map_create();

    // Function to parse pages into dictionary
    var parse_pages = function(_pages, _pages_dict) {
        for (var _i = 0; _i < array_length(_pages); _i++) {
            var _page = string_split(_pages[_i], "|");
            var _left = real(_page[0]);
            var _right = real(_page[1]);

            if (!ds_map_exists(_pages_dict, _left)) {
                _pages_dict[? _left] = ds_list_create();
            }
            ds_list_add(_pages_dict[? _left], _right);
        }
    };

    // Function to validate a single order
    var validate_order = function(_order, _pages_dict) {
        var _seen_pages = ds_map_create();
        var _is_correct = true;

        for (var _i = 0; _i < array_length(_order); _i++) {
            var _page = _order[_i];

            if (ds_map_exists(_pages_dict, _page)) {
                var _pair_list = ds_map_find_value(_pages_dict, _page);
                for (var _j = 0; _j < ds_list_size(_pair_list); _j++) {
                    var _right_page = ds_list_find_value(_pair_list, _j);
                    if (ds_map_exists(_seen_pages, _right_page)) {
                        _is_correct = false;
                        break;
                    }
                }
            }

            ds_map_add(_seen_pages, _page, true);
            if (!_is_correct) break;
        }

        ds_map_destroy(_seen_pages);
        return _is_correct;
    };

    // Function to calculate the sum of middle numbers in orders
    var calculate_middle_sum = function(_orders) {
        var _sum = 0;
        for (var _i = 0; _i < array_length(_orders); _i++) {
            var _order = _orders[_i];
            if (array_length(_order) > 0) {
                _sum += _order[floor(array_length(_order) / 2)];
            }
        }
        return _sum;
    };

    // Function to clean up resources
    var clean_up_resources = function(_pages_dict) {
        ds_map_clear(_pages_dict);
        ds_map_destroy(_pages_dict);
        show_debug_message("Cleanup completed.");
    };

    // Step 1: Parse pages into dictionary
    parse_pages(_pages, _pages_dict);

    // Step 2: Validate page orders
    var _correct_page_orders = [];
    var _incorrect_orders = [];
    for (var _i = 0; _i < array_length(_page_order); _i++) {
        if (validate_order(_page_order[_i], _pages_dict)) {
            array_push(_correct_page_orders, _page_order[_i]);
        } else {
            array_push(_incorrect_orders, _page_order[_i]);
        }
    }

    // Step 3: Calculate sum of middle numbers for correct orders
    var _sum_of_correct_middles = calculate_middle_sum(_correct_page_orders);
    show_debug_message("Sum of middle numbers (correct): " + string(_sum_of_correct_middles));

    // Step 4: Correct and sort incorrect orders
    var _corrected_orders = [];
    for (var _i = 0; _i < array_length(_incorrect_orders); _i++) {
        quick_sort_with_pairs(_incorrect_orders[_i], 0, array_length(_incorrect_orders[_i]) - 1, _pages_dict);
        array_push(_corrected_orders, _incorrect_orders[_i]);
    }

    // Step 5: Calculate sum of middle numbers for corrected orders
    var _sum_of_corrected_middles = calculate_middle_sum(_corrected_orders);
    show_debug_message("Sum of middle numbers (corrected): " + string(_sum_of_corrected_middles));

    // Step 6: Clean up resources
    clean_up_resources(_pages_dict);
}
