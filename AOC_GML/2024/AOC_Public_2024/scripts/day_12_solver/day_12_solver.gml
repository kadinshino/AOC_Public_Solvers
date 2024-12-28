///// drone surveying 

function in_bounds(_x, _y, _grid) {
    return _x >= 0 && _x < array_length(_grid) && _y >= 0 && _y < array_length(_grid[0]);
}

// Utility function to check if a cell exists in the region.
function region_contains(_region, _x, _y) {
    for (var _i = 0; _i < array_length(_region); _i++) {
        var _cell = _region[_i];
        if (_cell[0] == _x && _cell[1] == _y) {
            return true; // Cell found in the region.
        }
    }
    return false; // Cell not found.
}
// #endregion

// #region Flood Fill
// Flood fill algorithm to identify a region of the same type in the grid.
function flood_fill(_grid, _x, _y, _target, _visited) {
    var _stack = [[_x, _y]];
    var _region = [];

    while (array_length(_stack) > 0) {
        var _cell = array_pop(_stack);
        var _cx = _cell[0];
        var _cy = _cell[1];

        if (_visited[_cx, _cy]) {
            continue;
        }

        _visited[_cx, _cy] = true;
        array_push(_region, [_cx, _cy]);

        // Check neighbors
        var _directions = [[-1, 0], [1, 0], [0, -1], [0, 1]];
        for (var _dir = 0; _dir < array_length(_directions); _dir++) {
            var _nx = _cx + _directions[_dir][0];
            var _ny = _cy + _directions[_dir][1];
            if (in_bounds(_nx, _ny, _grid) && !_visited[_nx, _ny] && _grid[_nx][_ny] == _target) {
                array_push(_stack, [_nx, _ny]);
            }
        }
    }

    return _region;
}
// #endregion

// #region Price Calculation
// Function to calculate the total price of regions based on a specified method.
function calculate_total_price(_grid, _method) {
    if (_method != "corners" && _method != "ides") {
        show_error("Method must be either 'corners' or 'ides'", true);
    }

    var _visited = []; // Create a 2D visited array.
    for (var _i = 0; _i < array_length(_grid); _i++) {
        _visited[_i] = array_create(array_length(_grid[0]), false);
    }

    var _regions = [];

    // Identify regions using flood fill.
    for (var _i = 0; _i < array_length(_grid); _i++) {
        for (var _j = 0; _j < array_length(_grid[0]); _j++) {
            if (!_visited[_i, _j]) {
                var _region = flood_fill(_grid, _i, _j, _grid[_i][_j], _visited);
                array_push(_regions, {region: _region, type: _grid[_i][_j]});
            }
        }
    }

    // Calculate total price based on the method.
    var _total = 0;

    for (var _r = 0; _r < array_length(_regions); _r++) {
        var _region_data = _regions[_r];
        var _region = _region_data.region;
        var _type = _region_data.type;
        var _nregion = array_length(_region);

        if (_method == "corners") {
            var _corners = 0;

            for (var _k = 0; _k < array_length(_region); _k++) {
                var _cell = _region[_k];
                var _cx = _cell[0];
                var _cy = _cell[1];

                // Neighbor checks
                var _west = region_contains(_region, _cx - 1, _cy);
                var _east = region_contains(_region, _cx + 1, _cy);
                var _north = region_contains(_region, _cx, _cy - 1);
                var _south = region_contains(_region, _cx, _cy + 1);

                // Direct corners: Missing horizontal and vertical neighbors
                if (!_north && !_west) _corners++;
                if (!_north && !_east) _corners++;
                if (!_south && !_west) _corners++;
                if (!_south && !_east) _corners++;

                // Diagonal corners: Ensure these aren't double-counted
                if (_north) {
                    if (_west && !region_contains(_region, _cx - 1, _cy - 1)) _corners++;
                    if (_east && !region_contains(_region, _cx + 1, _cy - 1)) _corners++;
                }
                if (_south) {
                    if (_west && !region_contains(_region, _cx - 1, _cy + 1)) _corners++;
                    if (_east && !region_contains(_region, _cx + 1, _cy + 1)) _corners++;
                }
            }

            var _cost = _nregion * _corners;
            show_debug_message("Region " + _type + " cost with discount: Region size = " + string(_nregion) + ", Corners = " + string(_corners) + ", Cost = " + string(_cost));
            _total += _cost;

        } else if (_method == "ides") {
            var _sides = 0;
            for (var _k = 0; _k < array_length(_region); _k++) {
                var _cell = _region[_k];
                var _cx = _cell[0];
                var _cy = _cell[1];

                var _directions = [[-1, 0], [1, 0], [0, -1], [0, 1]];
                for (var _dir = 0; _dir < array_length(_directions); _dir++) {
                    var _nx = _cx + _directions[_dir][0];
                    var _ny = _cy + _directions[_dir][1];

                    if (!in_bounds(_nx, _ny, _grid) || !region_contains(_region, _nx, _ny)) {
                        _sides++;
                    }
                }
            }
            var _cost = _nregion * _sides;
            show_debug_message("Region " + _type + " cost without discount: Region size = " + string(_nregion) + ", Sides = " + string(_sides) + ", Cost = " + string(_cost));
            _total += _cost;
        }
    }

    return _total;
}
// #endregion

// #region Debug
// Debug function to test the grid and price calculations.
function debug() {
    var _grid = [
        ["A", "A", "A", "A"],
        ["B", "B", "C", "D"],
        ["B", "B", "C", "C"],
        ["E", "E", "E", "C"]
    ];

    // Calculate the total price using the provided methods
    show_debug_message("Total price without discount: " + string(calculate_total_price(_grid, "ides")));
    show_debug_message("Total price with discount: " + string(calculate_total_price(_grid, "corners")));
}
// #endregion
