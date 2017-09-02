import apiclient.discovery
import os
import pickle


class GoogleSearchManager:
    def __init__(self):
        self.api_key = "YOUR_API_KEY"
        self.cse_id1 = "YOUR_CSE_ID"
        self.cse_id_to_use = self.cse_id1
        self.start_num = 1

    def search_file_on_google(self, query, file_type):
        if os.path.exists("./last_search_result.log"):
            print("Last crawled data found! Those data were used.")
            with open("./last_search_result.log", "rb") as file:
                return True, pickle.load(file)

        else:
            service = apiclient.discovery.build("customsearch", "v1", developerKey=self.api_key)
            search_result = service.cse().list(q=query,
                                               cx=self.cse_id_to_use,
                                               fileType=file_type,
                                               num=10,
                                               filter="1",
                                               start=self.start_num).execute()
            self.start_num += 10

            result_links = []
            for item in search_result["items"]:
                link = item["link"]
                if link.endswith(file_type):
                    result_links.append(link)

            return False, result_links
