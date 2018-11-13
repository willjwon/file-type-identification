def print_progress(current_level, max_level, num_max_bars=50):
    progress = current_level / max_level
    num_bars_to_print = int(progress * num_max_bars)
    num_spaces_to_print = num_max_bars - num_bars_to_print
    print("|{}>{}| ({}/{}, {:2.2f}%)".format("=" * num_bars_to_print,
                                             " " * num_spaces_to_print,
                                             current_level,
                                             max_level,
                                             progress * 100),
          end="\r")
