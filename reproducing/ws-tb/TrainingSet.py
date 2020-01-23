import gzip
import random
import sys
import argparse

def read_corpus(path):
	with gzip.open(path + "corpus.tsv.gz") as file:
		lines = file.readlines()
		ids = []
		
		for line in lines:
			parts = line.decode().split('\t')
			id = parts[0]
			ids.append(id)
			
	return ids
		
		
def training_set(path, targetpath):
	ids = read_corpus(path)
	pos_training = random.sample(ids, 9106)
	
	set = []
	for pos_id in pos_training:
		neg_training = random.sample(ids, 100)
		set.append((pos_id, neg_training))

	with open(targetpath + "/train.pos.txt", 'w', encoding='utf-8') as pos:
		with open(targetpath + "/train.neg.txt", 'w', encoding='utf-8') as neg:
			for s in set:
				pos.write(s[0] + '\t' + 'x' + '\n')
				for nid in s[1]:
					neg.write(s[0] + '\t' + nid + '\n')
					
	
def main(args):
	training_set(args.path, args.targetpath)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(sys.argv[0])
    argparser.add_argument("--path",
            type = str
        )
    argparser.add_argument("--targetpath",
	        type = str
	    )
    args = argparser.parse_args()
    print(args)
    print("")
    main(args)
