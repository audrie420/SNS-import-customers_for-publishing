# group 2 - past import db handlers


def flag_update(p_df, AVID, header_name, flag_up):
    update_field = header_name + "_UPD"
    if flag_up == True:
        p_df.loc[p_df["AVID"] == AVID, update_field] = True
    else:
        p_df.loc[p_df["AVID"] == AVID, update_field] = False


def flag_inspect(p_df, AVID, header_name, flag_up):
    inspect_field = header_name + "_INS"
    if flag_up == True:
        p_df.loc[p_df["AVID"] == AVID, inspect_field] = True
    else:
        p_df.loc[p_df["AVID"] == AVID, inspect_field] = False


def update_timestamp(
    incoming_timestamp,
    p_df,
    AVID,
    header_name,
):
    timestamp_field = header_name + "_TS"
    p_df.loc[p_df["AVID"] == AVID, timestamp_field] = incoming_timestamp


def flag_update_all_fields(dataframe, AVID, flag_up, all_df_headers: list):
    for field in all_df_headers:
        flag_update(dataframe, AVID, field, flag_up)
    # for each field name, flag_update()


def flag_inspect_all_fields(dataframe, AVID, flag_up, all_df_headers: list):
    for field in all_df_headers:
        flag_inspect(dataframe, AVID, field, flag_up)
    # for each field name, flag_update()


def update_timestamp_all_fields(
    incoming_timestamp, dataframe, AVID, all_df_headers: list
):
    for field in all_df_headers:
        update_timestamp(incoming_timestamp, dataframe, AVID, field)
    # for each field name, update_timestamp()
