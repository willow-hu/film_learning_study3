import pandas as pd
import numpy as np
import os

# Participants: 1~11, 16
participants = list(range(1, 16)) 

# Map seq to topic (0 or 1)
seq_df = pd.read_csv('questionnaire/seq.csv', index_col=0)

# Load answers
ans = pd.read_csv('questionnaire/long_term/answers.csv')

# Participant to seq
def par2seq(par_id):
    return par_id % 4 if par_id % 4 != 0 else 4

# Parse participant id
def get_par_id(par_field):
    if isinstance(par_field, str):
        par_field = par_field.replace('P', '')
    return int(par_field)

def get_answer_seq(row):
    """
    The answers are the second chars '(A)' of the column 3 to 6. 
    """
    return [row[i][1] for i in range(3, 7)]


res_all = pd.DataFrame(columns=['strategy', 'topic', 'corpus', 'method', 'participant', 'score'])

# Load the responses
response_folder = 'questionnaire\\long_term\\responses'

for file in os.listdir(response_folder):
    topic = file.split('.')[0][:-2]
    strategy = topic.split('_')[0]
    corpus = topic.split('_')[1]
    correct_ans = ans[topic].tolist()

    response = pd.read_csv(os.path.join(response_folder, file))

    for _, row in response.iterrows():
        # Get participant id
        par_id = get_par_id(row['Participant number:'])
        if par_id not in participants:
            continue

        # Whether this material use our method
        seq = 'seq' + str(par2seq(par_id))

        # Get the topic for the current participant
        method = seq_df[topic][seq]

        # Count correct answers
        answers = get_answer_seq(row)
        score = sum([1 for i, j in zip(answers, correct_ans) if i == j])

        # Create a row of the summary
        personal_response = [strategy, topic, corpus, method, par_id, score]

        # Add this row to the dataframe
        res_all = pd.concat([res_all, pd.DataFrame([personal_response], columns=res_all.columns)])

res_all.to_csv('questionnaire\\long_term\\response_summary_long.csv', index=False)