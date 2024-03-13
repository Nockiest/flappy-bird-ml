     print(pipe_height,last_pipe_added)
        pipes.append({'x': WINDOW_WIDTH, 'y': 0, 'height': pipe_height})
        pipes.append({'x': WINDOW_WIDTH, 'y': pipe_height + pipe_gap, 'height': WINDOW_HEIGHT - pipe_height - pipe_gap})
    