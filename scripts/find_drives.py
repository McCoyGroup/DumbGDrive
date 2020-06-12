
params = CLI.get_parse_dict(
    (
        '--pageSize',
        dict(
            default=25, type=int, dest='pageSize',
            help="The maximum number of files to return per page. Partial or empty result pages are possible even before the end of the files list has been reached. Acceptable values are 1 to 1000, inclusive. (Default: 100"
        )
    ),
    (
        '--pageToken',
        dict(
            default="", type=str, dest='pageToken',
            help="The token for continuing a previous list request on the next page. This should be set to the value of 'nextPageToken' from the previous response"
        )
    ),
    (
        '--q',
        dict(
            default="", type=str, dest='q',
            help="A query for filtering the file results. 'See the Search for files' guide for the supported syntax."
        )
    )
)

drives_api = Drive() #

listing = drives_api.list(**params)['drives']

print("\n".join(str(f) for f in listing))