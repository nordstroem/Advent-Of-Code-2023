
inputs = [(56,499), (97,2210),(77,1097),(93,1440)]
# test_inputs = [(7,9), (15,40), (30, 200)]
max_time = 56977793
record_distance = 499221010971440


lengths = []
for boost_time in range(max_time):
    lengths.append(boost_time * (max_time - boost_time))
print(len([t for t in lengths if t > record_distance]))