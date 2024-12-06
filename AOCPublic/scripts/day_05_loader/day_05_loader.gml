#region /// load_page_data

function load_page_data(_file_path) {
    // Load the buffer from the file
    var _buffer = buffer_load(_file_path);
    
    // Read the buffer data
    buffer_seek(_buffer, buffer_seek_start, 0);
    var _data = buffer_read(_buffer, buffer_string);
    
    // Split data into lines
    var _lines = string_split(_data, "\n");
    
    // Initialize global variables
    global.pages = [];
    global.page_order = [];
    
    // Parse lines into pages and page orders
    var _parsing_pages = true;
    for (var _i = 0; _i < array_length(_lines); _i++) {
        var _line = string_trim(_lines[_i]);
        if (_line == "") {
            _parsing_pages = false;
            continue;
        }
        
        if (_parsing_pages) {
            // Parse pages
            array_push(global.pages, _line);
        } else {
            // Parse page orders
            var _page_order = string_split(_line, ",");
            for (var _j = 0; _j < array_length(_page_order); _j++) {
                _page_order[_j] = real(_page_order[_j]);
            }
            array_push(global.page_order, _page_order);
        }
    }
    
    // Clean up the buffer
    buffer_delete(_buffer);
}
#endregion
