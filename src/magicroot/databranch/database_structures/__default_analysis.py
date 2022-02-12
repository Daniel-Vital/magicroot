
class DefaultAnalysis:

    @staticmethod
    def nulls(df):
        """
        Creates Dataframe with all lines with any null value
        :param df: Dataframe to check the nulls on
        :return: DataFrame with all lines with any null value
        """
        return df[df.isnull().any(axis=1)]

    @staticmethod
    def duplicated_columns(df, columns=None):
        """
        Creates Dataframe with all lines which are repeated in all rows for the given columns,
        if no columns are given evaluates repeated lines for all columns
        :param df: Dataframe to be evaluated
        :param columns: Columns to be evaluated
        :return: DataFrame with all lines with all repeated rows
        """
        df_filter = df if columns is None else df[columns]
        return df[df_filter.duplicated(keep=False)]

    @staticmethod
    def duplicated_index(df):
        """
        Creates Dataframe with all lines which are repeated in index
        :return: DataFrame with all lines with all repeated rows
        """
        return df[df.index.duplicated(keep=False)]

    @staticmethod
    def advanced_describe(df, by, compute_map):
        """
        This function creates a Dataframe with aggregator functions grouped by the given columns
        Similarly to the method pandas.DataFrame.describe()
        :param by: list of columns to group the dataframe
        :param compute_map: Two dimensional list with the columns and respective functions
        Each element of the list should have exactly two elements, the first being a list of columns and the
        second being a list of functions.
        The columns should appear only once in the compute_map
        Example:
        [
            [[column_1, column_2], [function_1]],
            [[column_1], [function_1, function_2]
        ]
        :return: a Dataframe with the results
        """
        return df.loc[
               :, [column for n in compute_map for column in n[0]] + by
               ].groupby(by).agg({column: n[1] for n in compute_map for column in n[0]})

    @staticmethod
    def smaller_than_reference_columns(df, columns=None, reference=None):
        """
        Creates Dataframe with all lines which have values less than the given reference in the given columns
        :param df: Dataframe to be evaluated
        :param columns: Columns to be evaluated
        :param reference: Value to compare to columns
        :return: DataFrame with all the flagged lines
        """
        df_filter = df if columns is None else df[columns]
        return df.loc[(df_filter < reference).any(axis=1)]

    @staticmethod
    def negative_columns(df, columns=None):
        """
        Creates Dataframe with all lines which are negative in the given columns
        :param df: Dataframe to be evaluated
        :param columns: Columns to be evaluated
        :return: DataFrame with all the flagged lines
        """
        return DefaultAnalysis().smaller_than_reference_columns(df=df, columns=columns, reference=0)


