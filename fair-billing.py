import argparse
from datetime import datetime

class Bill:
    def __init__(self,log_file_path) -> None:
        self.log_file_path = log_file_path
  
    def read_logs(self):
        try:
            log_list = list()
            with open(self.log_file_path, 'r') as f:
                for line in f:
                    log = line.strip().split()
                    try:
                        timestamp = datetime.strptime(log[0], "%H:%M:%S")
                        username = str(log[1]).strip()
                        event = str(log[2]).strip().lower()
                        if event in ['start','end']:
                            log_list.append((timestamp,username,event))
                    except:
                        pass
                    
            return log_list

        except FileNotFoundError:
            print(f"Error: Log file not found at {self.log_file_path}")
  
    def calculate_session_duration(self,log_list):
        session_data = dict()
        if len(log_list)==0:
            print("There is no session log available.")
        
        default_start_time = log_list[0][0]
        default_end_time = log_list[-1][0]
        current_user = None
        
        skip_entries = []
        for i in range(len(log_list)):
            if i not in skip_entries:
                curent_user = log_list[i][1]
                event = log_list[i][2]
                start_time = None
                end_time = None
                if event == 'start':
                    start_time = log_list[i][0]
                    for j in range(i,len(log_list)):
                        if curent_user == log_list[j][1] and log_list[j][2] == 'end' and j not in skip_entries:
                            end_time = log_list[j][0]
                            skip_entries.append(j)
                            break

                    if end_time == None:
                        end_time = default_end_time
                
                
                else:
                    start_time = default_start_time
                    end_time = log_list[i][0]



                if curent_user not in session_data:
                    session_data[curent_user] = dict()
                    session_data[curent_user]['count'] = 1
                    session_data[curent_user]['duration'] = (end_time - start_time).seconds
                    
                else:
                    session_data[curent_user]['count'] += 1
                    session_data[curent_user]['duration'] += (end_time - start_time).seconds

        return session_data
    
    def print_session_data(self,session_data):
        for user_name, detail in session_data.items():
            print(user_name, detail['count'], detail['duration']) 
            


def main():
    parser = argparse.ArgumentParser(description="Calculate billing")
    parser.add_argument("logfile", type=str, help="session data")
    args = parser.parse_args()

    bill_obj = Bill(log_file_path=args.logfile)
    log_list = bill_obj.read_logs()
    session_data = bill_obj.calculate_session_duration(log_list)
    bill_obj.print_session_data(session_data)


if __name__ == "__main__":
    main()