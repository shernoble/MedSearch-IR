from flask import Flask, jsonify, render_template, request
from whoosh.index import open_dir,Index
from whoosh.fields import Schema, TEXT, KEYWORD, ID
from whoosh.qparser import QueryParser
from whoosh.qparser.plugins import FuzzyTermPlugin

app = Flask(__name__)

# Load the Whoosh index
index_path = "output_files_whoosh_main"
# Define the schema
schema = Schema(
    url=ID(unique=True, stored=True),
    content=TEXT(stored=True),
    tags=KEYWORD,
    path=ID(unique=True, stored=True)
)
myindex = open_dir(index_path,schema=schema)
searcher = myindex.searcher()
# w=myindex.writer()



if not isinstance(myindex, Index):
    raise ValueError("The 'index' object is not a valid Whoosh Index.")


def perform_search(query_string):
    query_parser = QueryParser("content", schema=schema)
    query_parser.add_plugin(FuzzyTermPlugin())
    fuzzy_query = query_string + "~1"
    query = query_parser.parse(fuzzy_query)
    results = searcher.search(query, limit=10)
    # print(results[0]['content'])
    # print("content printed")
    return [{'url': result['url'], 'path': result['path'], 'score': result.score,'content':result['content'][:120]} for result in results]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the user query from the form
        user_query = request.form['query']

        # Perform the fuzzy search
        results = perform_search(user_query)

        # Display the results on the web page
        return render_template('index.html', user_query=user_query, results=results)

    # Render the initial form
    return render_template('index.html')

# def update_scores(feedback_data):
#     with myindex.writer() as writer:
#         for feedback in feedback_data:
#             url = feedback['url']
#             # Fetch the document by URL
#             query = searcher.document(url=url)
#             if query:
#                 # Update the score based on feedback type
#                 if feedback['feedbackType'] == 'rel':
#                     # Increment the score by 0.1
#                     new_score = query.score + 0.1  # Adjust the increment based on your criteria
#                 elif feedback['feedbackType'] == 'nrel':
#                     # Decrement the score by 0.1
#                     new_score = query.score - 0.1  # Adjust the decrement based on your criteria
#                 else:
#                     # For other cases, maintain the existing score
#                     new_score = query.score  # Set a default score if it doesn't exist
#                 # Update the document in the index
#                 writer.update_document(url=url, score=new_score)
#     # No need to explicitly commit; the "with" statement will take care of it

def calculate_map(predictions, total_relevant):
    # total_relevant = rel_data
    precision_at_k_values = []
    relevant_count = 0
    precision_sum = 0.0

    for i, prediction in enumerate(predictions, 1):
        if prediction['feedbackType'] == 'rel':
            relevant_count += 1
            precision_at_k = relevant_count / i
            precision_sum += precision_at_k

    if total_relevant > 0:
        map_value = precision_sum / total_relevant
        return map_value
    else:
        return 0.0


def precision_at_k(predictions, k):
    # Ensure that k is not greater than the total number of items
    k = min(k, len(predictions))
    
    # Count the number of relevant items among the top k items
    relevant_at_k = sum(1 for item in predictions[:k] if item['feedbackType'] == 'rel')
    
    # Calculate Precision at k
    precision = relevant_at_k / k if k > 0 else 0.0
    
    return precision


@app.route('/submit_feedback',methods=['POST'])
def submit_feedback():
    data = request.json
    feedbackData = data.get('feedbackData', [])
    # rel_data = data.get('relData', [])
    # nrel_data = data.get('nrelData', [])
    user_query = data.get('userQuery', '')
    resLen = data.get('reslen')
    # p @k, k=5
    # ndcg
    #map-p at each rel, avg it
    # print(rel_data);
    # find number of rel data
    rel_count = sum(1 for feedback in feedbackData if feedback['feedbackType'] == 'rel')
    print("total_rel:",rel_count)
    print("**************************MEAN AVG PRECISION*****************************")
    map_value=calculate_map(feedbackData,rel_count);
    print("MAP:",map_value)
    print("**************************PRECISION AT k=3*****************************")
    p_k=precision_at_k(feedbackData,3);
    print("precision @ k=3 : ",p_k)


    # update_scores(feedback_data)
    # print(feedback_data)
    # After updating scores, re-evaluate the user's query
    updated_results = perform_search(user_query)

    return jsonify({'status': 'success', 'results': updated_results})
    # Render the template with the updated results
    # return render_template('index.html', user_query=user_query, results=updated_results)

if __name__ == '__main__':
    app.run(debug=True)
