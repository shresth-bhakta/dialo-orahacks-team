from faiss_check import SemanticSearch
semantic_search = SemanticSearch('Orders.csv')
semantic_search.run_search('What is the details of order id 90196?')