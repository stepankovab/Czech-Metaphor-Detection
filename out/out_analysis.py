import json

# with open("out/841ec20e-ec1b-4fee-b96c-c3c4384bec9c.json", 'r', encoding='utf-8') as f: # all 4 to cs f1 0.69 
with open("out/db3ae9fa-f430-4b70-ba85-483d92d719ab.json", 'r', encoding='utf-8') as f:  # cs poetry
# with open("out/b4039236-b58a-4161-ada2-e1cf7f2d0466.json", 'r', encoding='utf-8') as f:  # cs
# with open("out/6176f0a0-0add-491d-9c0e-8a7cf122cc12.json", 'r', encoding='utf-8') as f:  # sl
# with open("out/5e117058-8bde-4b20-9574-04c011d7195e.json", 'r', encoding='utf-8') as f:  # en
    results = dict(json.load(f))

# dict_keys(['words', 'poss', 'preds', 'labels'])


# with open("out_xlmr_100k_SLENCS.txt", 'w', encoding='utf-8') as f:

for i in range(len(results["words"])):
    note = ""
    if results["preds"][str(i)] == 1:
        if results['labels'][str(i)] == 1:
            note = "   ---   poznal"

        if  results['labels'][str(i)] == 0:
            note = "   ---   navic"

    if results["preds"][str(i)] == 0:
        if results['labels'][str(i)] == 1:
            note = "   ---   miss"
    
    # f.write(results["words"][str(i)] + " " + note + "\n")
    print(results["words"][str(i)], note)