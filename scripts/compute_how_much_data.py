def compute_how_much_data(words: list = [0,0,0,0]):
    """order of: es en sl cs"""
    print(f"{int(words[0] / 32.2)} {int(words[1] / 14.6)} {int(words[2] / 18.6)} {int(words[3] / 19.7)}")

compute_how_much_data([50000, 50000, 210000, 30000])



# train es requested: 20000 provided: 2905 0.018364458929222324
# train en requested: 20000 provided: 12962 0.10964371045238533
# train sl requested: 20000 provided: 11170 0.06166527043552782
