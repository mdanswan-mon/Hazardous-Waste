def remove_stop_words(content, sw_path):
    
    stop_words = [word.strip() for word in open(sw_path, 'r').readlines()]