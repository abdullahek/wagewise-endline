import pyodbc



tbl_user_response= "endline_answers" # User_questions_log
tbl_user_qt_response = "endline_question_response" # User_Response_Logs
tbl_question_list = "endline_questions_list" # {tbl_question_list}


def Get_DB_conn():
    tbl_user_qt_response = "endline_answers"
    for retry in range(3):
        try:
            conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                  'Server=tcp:gbot-euro-server.database.windows.net,1433;'
                                  'Database=test;'
                                  # 'Trusted_Connection=yes;'
                                  ';UID=myadmin;'
                                  'PWD=pipQe8-sadjej-covcaf')
            cursor = conn.cursor()
            return conn,cursor
        except Exception as e:
            print('failed')
            continue
    raise  # throw if the retry fails too often

def Send_Survey_Question(User,Type):
    try:

        conn, cursor = Get_DB_conn()

        pending_list = []
        new_questions = []
        responses_list = []

        if Type == 'Pending':
            query = f"select *,datediff(hour,sent_on,getdate()) as HourDiff from {tbl_user_response} where User_Number = '{User}' and Response_Status = 0 and completed = 0;"
            cursor.execute(query)
            for i in cursor:

                if i[5]>48 or i[5]>168:
                    message = f"Sending message to {i[1]} after {i[5]} hours. Since, there isn't any response received against last question."
                    # print(message)
                    query = f"SELECT * FROM {tbl_question_list} where status = 1 and number = '{i[2]}';"
                    cursor.execute(query)
                    question = cursor.fetchone()
                    question = question[2]
                    user_question_list = {
                                            "User"      :   i[1],
                                            "Question"  :   question[2]
                                         }
                    pending_list.append(user_question_list)
                else:
                    print("No pending Responses")
        elif Type == "New":
            query = f"select max(cast(Q_number as int)) as Last_question_id from {tbl_user_response} where User_Number = '{User}'  and completed = 0;"
            cursor.execute(query)
            question = cursor.fetchone()

            message = f"Sending message to {User} for new question after Question ID {question[0]}."
            # print(message)

            if question[0] is None:
                query = f"SELECT * FROM {tbl_question_list} where status = 1 and number in ('-3','-2','-1');"
            else:

                query = f"SELECT  top 1 * FROM {tbl_question_list} where status = 1 and cast(number as integer) > cast('{question[0]}' as integer) and number not in ('Thanks Continue','Invalid');"
                # print(query)
            cursor.execute(query)
            question = cursor.fetchall()
            for i in question:
                question_ = i[2]
                Options = i[3]
                id = i[1]
                json_list = {
                                "Q_Number": id,
                                "Question": question_.replace('$','\n'),
                                'Options': Options.replace('$',"\n")
                }
                new_questions.append(json_list)
        elif Type == "Response":
            query = f"select max(Q_number) as Last_question_id ,(select count(1) from {tbl_user_response} where user_number = '{User}'  and completed = 0) as q_count from {tbl_user_response} where User_Number = '{User}'  and completed = 0 and Response_Status = 0 and datediff(hour,sent_on,getdate())<48;"
            cursor.execute(query)
            question = cursor.fetchone()

            question_options = f"select Options_List,Is_MultiSelect,Allow_Other from {tbl_question_list} where number = '{question[0]}';"
            cursor.execute(question_options)
            Options_question = cursor.fetchone()
            if Options_question:
                # print(Options_question[0])
                # print(Options_question[1])

                output = Options_question[0].split(',')
                # print(output)

                Multi_True = Options_question[1]
                Allow_Other = Options_question[2]
                # print(Multi_True)

                message = f"Message received from {User} agianst Question ID {question[0]} and current question count is {question[1]}."
                # print(message)

                response = {
                    "Question": question[0].replace('$',"\n"),
                    "Options": output,
                    "count": question[1],
                    "Multi": Multi_True,
                    "OtherAllowed": Allow_Other
                }

                responses_list.append(response)

        return new_questions,pending_list,responses_list
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def add_User_response(User, Response):
    try:
        conn, cursor = Get_DB_conn()
        new, pending, responses_list = Send_Survey_Question(User, 'Response')

        if responses_list:

            query = f"insert into {tbl_user_qt_response} select * from ( select '{User}' as user_,'{responses_list[0]['Question']}' as response_q,'{Response}' as response_,getdate() as received_on, 0 as completed ) as e where not exists (select 1 from {tbl_user_qt_response} l where l.user_number = e.user_ and l.response = e.response_ and l.q_number = e.response_q  and l.completed = 0);"

            cursor.execute(query)

            cursor.commit()

            update_status = f"Update {tbl_user_response} set response_status = 1 where user_number = '{User}' and Q_Number = '{responses_list[0]['Question']}' and response_status = 0  and completed = 0;"

            cursor.execute(update_status)

            cursor.commit()

            # print("Response saved successfully!!")
        else:
            print("No pending questions!!")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def add_Question_Sent_Log(Q_List,User):
    try:
        conn, cursor = Get_DB_conn()

        for i in Q_List:
        # Q_List
        #     print(i['Q_Number'])
            if i['Q_Number']=='21':
                query = f"insert into {tbl_user_response} select * from (select '{User}' as user_,'{i['Q_Number']}' as q_number,1 as status_,getdate() as date_, 0 as completed ) as r where not exists (select 1 from {tbl_user_response} L where L.User_Number = R.user_ and L.Q_Number = R.Q_Number and L.Response_Status = 0  and L.completed = 0);"
            else:
                query = f"insert into {tbl_user_response} select * from (select '{User}' as user_,'{i['Q_Number']}' as q_number,0 as status_,getdate() as date_, 0 as completed ) as r where not exists (select 1 from {tbl_user_response} L where L.User_Number = R.user_ and L.Q_Number = R.Q_Number and L.Response_Status = 0  and L.completed = 0);"
        cursor.execute(query)
        cursor.commit()
        # print("Question has been logged succeddfully!!")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def Validate_Options(Options, Response):
    try:
        if Response in Options:
            return "valid"
        else:
            return "invalid"
    except Exception as e:
        print(e)
    # finally:

def Vipe_clean_user_question_logs(User):
    try:
        conn, cursor = Get_DB_conn()

        query = f"update {tbl_user_response} set completed = 1 where User_Number = '{User}' and completed != 1; update {tbl_user_qt_response} set completed = 1 where User_Number = '{User}' and completed != 1;"
        cursor.execute(query)
        cursor.commit()
        # print("Question history has been Removed successfully!!")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def check_survey_status(num):
    try:
        conn, cursor = Get_DB_conn()

        query = f"select count(1) as cnt_ from {tbl_user_response} where User_Number = '{num}' and completed = 1;"
        cursor.execute(query)
        Survey_Status = cursor.fetchone()

        status = Survey_Status[0]
        return status
        # print("Question history has been Removed successfully!!")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def registered(num):
    """
    Returns 0 if user is not registered, 1 if registered
    """
    conn, cursor = Get_DB_conn()
    query = f"select count(1) as r from users where number = '{num}' and registered = 1;"
    cursor.execute(query)
    question = cursor.fetchone()
    print("Printing user")
    print(question)
    if question[0] is not None:
        print(question[0])
        if question[0] >= 1:
            return 1
        else:
            return 0
    else:
        return 0
