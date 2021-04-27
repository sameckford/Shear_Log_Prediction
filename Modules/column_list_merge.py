def column_list_merge(df, log_dictionary):
    for i in log_dictionary:
        original_count = df[log_dictionary[i][0]].count()
        for j in log_dictionary[i][1:]:
            try:
                df[log_dictionary[i][0]].fillna(df[j], inplace=True)
                df.drop([j], axis=1, inplace=True)
                print("Number of values added to " +log_dictionary[i][0]+ " column = " + str(abs(original_count - df[log_dictionary[i][0]].count())))
            except:
                print(str(j)+' column does not exist')
                pass