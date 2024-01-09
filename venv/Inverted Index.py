class InvertedIndex:
    def __init__(self, word_to_docs_mapping):
        self.mapped_words_to_docs = word_to_docs_mapping

    """Query accepts either a words as str or a tuple of strs"""
    def query(self, words):
        list_of_ids = set()
        list_of_ids_intersection = set()
        if isinstance(words, str):
            list_of_ids = set(doc_id for doc_id, term in self.mapped_words_to_docs if term == words)
            print(list_of_ids)
            return list_of_ids
        else:
            for word in words:
                if not list_of_ids_intersection:
                    list_of_ids = set(doc_id for doc_id, term in self.mapped_words_to_docs if term == word)
                    list_of_ids_intersection = list_of_ids
                else:
                    list_of_ids = set(doc_id for doc_id, term in self.mapped_words_to_docs if term == word)
                    list_of_ids_intersection.intersection_update(list_of_ids)
            print(list_of_ids_intersection)
            return list_of_ids

    def dump(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            for item in self.mapped_words_to_docs:
                f.write(str(item)+'///&')

    @classmethod
    def load(cls, filepath):
        mapped_words_to_docs = set()
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                split_list = line.strip().split('///&')
                for item in split_list:
                    if item != '':
                        mapped_words_to_docs.add(ast.literal_eval((item)))
        return cls(mapped_words_to_docs)


def load_document(filepath):
    with open(filepath, 'r', encoding='utf8') as f:
        enumerated_dict = dict(enumerate(f))
    cleaned_dict = {key: value.rstrip('\n') for key, value in enumerated_dict.items()}
    return cleaned_dict
    # {article_id: article_content}


def build_inverted_index(articles):
    words_to_docs_mapped = set()
    for id, content in articles.items():
        content = content.split()
        for term in content:
            words_to_docs_mapped.add((id, term))
    return InvertedIndex(words_to_docs_mapped)
    # InvertedIndex object

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="option")

build_parser = subparsers.add_parser("build")
build_parser.add_argument("--dataset", required=True)
build_parser.add_argument("--index", required=True)

query_parser = subparsers.add_parser("query")
query_parser.add_argument("--index", required=True)
query_parser.add_argument("--query_words", required=True)

args = parser.parse_args()

if args.option == "build":
    articles = load_document(args.dataset)
    inverted_index = build_inverted_index(articles)
    inverted_index.dump(args.index)
    print("Inverted index built and saved to", args.index)
elif args.option == "query":
    loaded_index = InvertedIndex.load(args.index)
    try:
        parsed_words = ast.literal_eval(args.query_words)
        loaded_index.query(parsed_words)
    except ValueError:
        loaded_index.query(args.query_words)



#py 6pr.py build --dataset tests/wikipedia_sample.txt --index index.txt
#py 6pr.py query --index index.txt --query_words "('the', 'Anarchism')"

