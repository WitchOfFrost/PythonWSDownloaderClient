def print_progress_bar(bytes_so_far, total_bytes):
    progress = bytes_so_far / total_bytes
    bar_length = 60 
    block = int(round(bar_length * progress))
    text = "\rPercent: [{0}] {1:.2f}%".format("#" * block + "-" * (bar_length - block), progress * 100)
    print(text, end="")