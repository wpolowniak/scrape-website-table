import pandas as pd
import argparse

def scrape_data(url: str) -> pd.DataFrame:
    """Extract tables from a given url and combine into one table
    """
    # pull tables from given url
    df_list = pd.read_html(url)

    # instantiate empty dataframe to append to
    df = pd.DataFrame()
    # append each table to df_list to the consolidated dataframe
    for i in df_list:
        df = df.append(i)

    return df

def high_level_data_clean(df: pd.DataFrame) -> pd.DataFrame:
    """Drop duplicates, rename columns and reset index of raw pulled data
    """
    # drop duplicate rows
    df = df.drop_duplicates()
    # rename columns
    df = df.rename(columns={0:'member_raw', 1:'website'})
    # reset index
    df = df.reset_index(drop=True)

    return df

def format_data_for_output(df: pd.DataFrame) -> pd.DataFrame:
    """Split member_raw field and location columns into more granular columns of data
    """
    # drop any rows that only have the state name
    idx_to_drop = (
        df.loc[
            (df['website'].isnull()) & ~(df['member_raw'].str.contains(':'))
        ].sort_values('website').index
    )
    df = df.drop(idx_to_drop).reset_index(drop=True)

    # split member_raw on ' : ' to separate the member name from their location
    df_split = df['member_raw'].str.split(' : ', expand=True).rename(columns={0:'member', 1:'location'})

    # split city & state column
    df_loc = df_split['location'].str.split(', ', expand=True).rename(columns={0:'city', 1:'state'})

    # combine dataframes
    df_combined = pd.concat([df, df_split, df_loc], axis=1)

    # select only relevant columns
    df_final = df_combined[['member', 'city', 'state', 'website']]

    return df_final

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', '-u', help='URL to scrape data from', default='https://www.bluehawk.coop/our-co-op/our-member-locations')
    parser.add_argument('--loc', '-l', help='directory to save output xlsx file')

    # if provided a url use that; otherwise use the default URL
    args = parser.parse_args()

    url = args.url
    loc = args.loc
    
    scraped_df = scrape_data(url)
    cleaned_df = high_level_data_clean(scraped_df)
    final_df = format_data_for_output(cleaned_df)
    final_df.to_excel(loc, index=False)