import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import pandas as pd


class LogAnalyzer:
    log_library_path = None
    log_library = None
    log_parser = None

    def __init__(self, log_library_path, log_parser):
        self.log_library_path = log_library_path
        self.log_library = pd.read_csv(log_library_path)
        self.log_parser = log_parser
        self.scaler = MinMaxScaler()
        self.scaler.fit(self.log_library)

    # This function adds an issue to the library. The production version is not expected to include it
    def add_issue(self, issue_file, reason):
        issue = self.log_parser.parse_logs(issue_file)
        self.log_library = self.log_library.append(issue, ignore_index=True)
        self.log_library.to_csv(self.log_library_path, index=False)

    def check_issue(self, issue, threshold=0.5):
        issue_embedding = self.get_embedding(issue)
        sims = []
        skipped = False
        for index, detected_issue in self.log_library.iterrows():
            print("Issue vector: ")
            print(issue_embedding)
            print("Library issue vector: ")
            print(detected_issue.values)
            issue_embedding = self.scaler.transform([issue_embedding]).reshape(-1)
            is_skip = detected_issue[-1]
            detected_issue = detected_issue
            detected_issue_embedding = self.scaler.transform(
                [list(detected_issue.values)]
            ).reshape(-1)
            sim = self.compare_issues(issue_embedding, detected_issue_embedding)
            if len(sims) > 0:
                if sim[0][0] >= np.max(sims):
                    if is_skip:
                        skipped = True
                    else:
                        skipped = False
            print("SIM: ")
            print(sim)
            sims.append(sim[0][0])
        return np.max(sims) if not skipped else 0.0

    def compare_issues(self, issue1, issue2, comparator=cosine_similarity):
        return comparator([issue1], [issue2])

    def get_embedding(self, issue):
        return self.log_parser.parse_logs(issue)
