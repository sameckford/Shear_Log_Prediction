def rolling_imputer_old(df, log='DTS', filter_length=100, cut_harshness=0.001):
    """ Interpolate over smaller distances and filter outside of that.
        Default window length is 100 samples and filtered at cut_harshness of filter_length (above 50 by default). """
    
    ### Flag all the null rows then do a rolling sum to highlight areas with large gaps
    print(str(round(df[log].isna().sum()/len(df), 3)) + " " + log + " proportion of nulls")
    df['test_flag'] = df[log].isna()
    df['test_flag'] = df.groupby('Wellname')['test_flag'].transform(lambda s: s.rolling(filter_length, center=True, min_periods=1).sum())
    ### filter the values that are a large way away from real values
    df.drop(df[df['test_flag'] >(filter_length*cut_harshness)].index, inplace = True)
    df['test_rolling_mean'] = df.groupby('Wellname')[log].transform(lambda s: s.rolling(window=filter_length, center=True, min_periods=1, win_type='gaussian').mean(std=filter_length*0.2))
    ### Fill nulls with rolling mean values
    df[log].fillna(df.test_rolling_mean)
    df.dropna(subset=[log], axis=0, how='any', inplace=True)
    ### Drop extra columns
    df.drop(['test_flag'], axis=1, inplace=True)
    return df

def rolling_imputer(df, log='DTS', filter_length=100):
    """ Interpolate over smaller distances and filter outside of that."""
    ### Flag all the null rows then do a rolling sum to highlight areas with large gaps
    df['test_rolling_mean'] = df.groupby('Wellname')[log].transform(lambda s: s.rolling(window=int(filter_length), center=True, min_periods=int(filter_length*0.1)).mean())
    ### Fill nulls with rolling mean values
    df[log].fillna(df.test_rolling_mean, inplace=True)
    df.dropna(subset=[log], axis=0, how='any', inplace=True)
    ### Drop extra columns
    df.drop(['test_rolling_mean'], axis=1, inplace=True)
    return df